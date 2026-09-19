#!/usr/bin/env python3
"""Mechanical detection of machine-written web copy.

Judgment does not belong here. This script finds only what a regular expression
can prove, and it finds it instantly, for free, on every build. What survives it
goes to the `slop-auditor` agent, which applies the tests a script cannot:
whether a claim is specific, and whether a competitor could dispute it.

    python3 scripts/slop_check.py dist/
    python3 scripts/slop_check.py dist/ --max-medium 5
    python3 scripts/slop_check.py page.html --quiet

Exit code is 1 if anything at or above the failure threshold is found, so this
drops straight into CI. Edit the lists below — they are meant to grow every time
a new tell gets past you.

No third-party dependencies, by design: a check that needs an install is a check
that stops being run.
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------- #
# The lists. Grow these.
# --------------------------------------------------------------------------- #

# Phrases that appear in machine-written marketing copy and almost nowhere else.
SLOP_PHRASES_EN = [
    "in today's fast-paced world", "in today's digital age", "look no further",
    "we've got you covered", "take your", "to the next level", "elevate your",
    "unlock the power", "seamless", "robust solution", "cutting-edge",
    "state-of-the-art", "game-changer", "game changing", "revolutionize",
    "revolutionise", "delve into", "dive into", "a testament to",
    "rich tapestry", "at the end of the day", "it's not just", "whether you're",
    "when it comes to", "in the realm of", "navigate the complexities",
    "unlock your potential", "tailored to your needs", "wide range of",
    "one-stop shop", "peace of mind", "rest assured", "the perfect blend",
]

SLOP_PHRASES_TR = [
    "günümüzün hızla değişen", "günümüz dünyasında", "başka yere bakmanıza gerek yok",
    "bir adım öteye taşıyın", "bir üst seviyeye", "yanınızdayız",
    "ihtiyaçlarınıza özel", "geniş yelpazede", "kusursuz bir deneyim",
    "yenilikçi çözümler", "sektörde öncü", "müşteri memnuniyeti odaklı",
    "kaliteden ödün vermeden", "en son teknoloji", "uzman kadromuzla",
    "yılların tecrübesi", "gönül rahatlığıyla", "tek adresi",
    "hayatınızı kolaylaştır", "fark yaratan",
]

# Non-committal constructions. A few are fine; a page full of them says nothing.
HEDGES_EN = [
    r"\bmay help\b", r"\bcan help\b", r"\bis designed to\b", r"\baims to\b",
    r"\bstrives to\b", r"\bcan often\b", r"\bmight be\b", r"\btends to\b",
    r"\bhelps to\b", r"\bcan be a great\b",
]

HEDGES_TR = [
    r"\bolabilir\b", r"\bsağlayabilir\b", r"\byardımcı olabilir\b",
    r"\bamaçlamaktadır\b", r"\bhedeflemektedir\b", r"\bsunmayı amaçl",
]

# Numbers presented as fact with no source anywhere near them.
UNSOURCED_NUMBER = re.compile(
    r"(?:\b\d{1,3}\s?%|\b%\s?\d{1,3}\b)"
    r"|\b(?:thousands|millions|hundreds) of (?:satisfied |happy )?\w+"
    r"|\b(?:binlerce|milyonlarca|yüzlerce) (?:mutlu |memnun )?\w+"
    r"|\b\d+(?:[.,]\d+)?\s?(?:/\s?5|out of 5|üzerinden \d)\b",
    re.IGNORECASE,
)

# Cues that a source is present, which downgrades an unsourced-number finding.
SOURCE_CUE = re.compile(
    r"(kaynak|source|according to|göre|\bref\b|https?://|\bsurvey\b|\banket\b)",
    re.IGNORECASE,
)

# "fast, reliable and affordable" — the three-adjective reflex.
TRIAD_EN = re.compile(r"\b(\w+),\s+(\w+),?\s+and\s+(\w+)\b")
TRIAD_TR = re.compile(r"\b(\w+),\s+(\w+)\s+ve\s+(\w+)\b")

SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}


# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Finding:
    severity: str
    file: str
    rule: str
    detail: str


class VisibleText(HTMLParser):
    """Extracts what a reader actually sees, plus the head metadata we check."""

    SKIP = {"script", "style", "noscript", "template", "svg"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "blockquote", "td", "figcaption"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._current: list[str] = []
        self.blocks: list[str] = []
        self.title = ""
        self.meta_description = ""
        self.h1_count = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            a = dict(attrs)
            if (a.get("name") or "").lower() == "description":
                self.meta_description = a.get("content") or ""

        if tag in self.BLOCK:
            self._flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "title":
            self._in_title = False
        if tag in self.BLOCK:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data.strip()
            return
        if data.strip():
            self._current.append(data.strip())

    def _flush(self) -> None:
        if self._current:
            self.blocks.append(" ".join(self._current))
            self._current = []

    def close(self) -> None:  # noqa: D102
        super().close()
        self._flush()


def extract(path: Path) -> VisibleText:
    parser = VisibleText()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    return parser


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def check_phrases(page: VisibleText, name: str) -> list[Finding]:
    text = " ".join(page.blocks).lower()
    return [
        Finding("high", name, "slop-phrase", f'"{phrase}"')
        for phrase in SLOP_PHRASES_EN + SLOP_PHRASES_TR
        if phrase in text
    ]


def check_hedges(page: VisibleText, name: str) -> list[Finding]:
    text = " ".join(page.blocks)
    hits = [
        m.group(0)
        for pattern in HEDGES_EN + HEDGES_TR
        for m in re.finditer(pattern, text, re.IGNORECASE)
    ]
    words = max(len(text.split()), 1)
    # Roughly one hedge per 150 words before it reads as evasive.
    if len(hits) > max(2, words // 150):
        return [Finding("medium", name, "hedging",
                        f"{len(hits)} hedged constructions in {words} words: "
                        + ", ".join(sorted(set(hits))[:5]))]
    return []


def check_triads(page: VisibleText, name: str) -> list[Finding]:
    hits = [
        m.group(0)
        for block in page.blocks
        for pattern in (TRIAD_EN, TRIAD_TR)
        for m in pattern.finditer(block)
    ]
    if len(hits) >= 3:
        return [Finding("medium", name, "triad-reflex",
                        f"{len(hits)} three-item lists: " + " | ".join(hits[:3]))]
    return []


def check_unsourced_numbers(page: VisibleText, name: str) -> list[Finding]:
    findings = []
    for block in page.blocks:
        for match in UNSOURCED_NUMBER.finditer(block):
            if not SOURCE_CUE.search(block):
                findings.append(Finding(
                    "high", name, "unsourced-number",
                    f'"{match.group(0).strip()}" in: {block[:90]}…'))
    return findings


def check_uniformity(page: VisibleText, name: str) -> list[Finding]:
    """Human writing varies in paragraph length. Generated writing does not."""
    lengths = [len(b.split()) for b in page.blocks if len(b.split()) >= 12]
    if len(lengths) < 5:
        return []
    spread = statistics.pstdev(lengths) / statistics.mean(lengths)
    if spread < 0.25:
        return [Finding("low", name, "uniform-rhythm",
                        f"{len(lengths)} paragraphs, length spread {spread:.2f} "
                        f"(mean {statistics.mean(lengths):.0f} words) — too even")]
    return []


def check_structure(page: VisibleText, name: str) -> list[Finding]:
    findings = []
    if not page.title:
        findings.append(Finding("high", name, "structure", "no <title>"))
    elif len(page.title) > 60:
        findings.append(Finding("medium", name, "structure",
                                f"title is {len(page.title)} chars (max 60)"))

    if not page.meta_description:
        findings.append(Finding("medium", name, "structure", "no meta description"))
    elif len(page.meta_description) > 160:
        findings.append(Finding("medium", name, "structure",
                                f"meta description is {len(page.meta_description)} chars (max 160)"))

    if page.h1_count != 1:
        findings.append(Finding("high", name, "structure",
                                f"{page.h1_count} <h1> elements, expected exactly 1"))
    return findings


CHECKS = [check_phrases, check_hedges, check_triads,
          check_unsourced_numbers, check_uniformity, check_structure]


# --------------------------------------------------------------------------- #

def audit(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        page = extract(path)
        name = str(path)
        for check in CHECKS:
            findings.extend(check(page, name))
    return findings


def collect(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(p for p in target.rglob("*.html") if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect machine-written web copy.")
    ap.add_argument("target", type=Path, help="an HTML file, or a directory to walk")
    ap.add_argument("--fail-on", choices=["high", "medium", "low"], default="high",
                    help="minimum severity that fails the run (default: high)")
    ap.add_argument("--quiet", action="store_true", help="only print findings")
    args = ap.parse_args()

    if not args.target.exists():
        print(f"not found: {args.target}", file=sys.stderr)
        return 2

    pages = collect(args.target)
    if not pages:
        print(f"no HTML found under {args.target}", file=sys.stderr)
        return 2

    findings = audit(pages)
    threshold = SEVERITY_ORDER[args.fail_on]
    failing = [f for f in findings if SEVERITY_ORDER[f.severity] >= threshold]

    if not args.quiet:
        print(f"slop check: {len(pages)} page(s), {len(findings)} finding(s)\n")

    for severity in ("high", "medium", "low"):
        group = [f for f in findings if f.severity == severity]
        if not group:
            continue
        print(f"{severity.upper()}  ({len(group)})")
        for f in group:
            print(f"  {f.file}  [{f.rule}]  {f.detail}")
        print()

    if failing:
        print(f"FAILED: {len(failing)} finding(s) at or above '{args.fail_on}'.")
        return 1

    if not args.quiet:
        print("Mechanical check passed. Judgment still required — "
              "hand this to the slop-auditor agent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
