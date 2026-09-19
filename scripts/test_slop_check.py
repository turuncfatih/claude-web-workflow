#!/usr/bin/env python3
"""Self-test for slop_check.py.

A checker nobody tests is a checker that quietly stops catching things. These
assert both directions: slop is caught, and clean copy is not falsely accused.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from slop_check import audit  # noqa: E402

SLOP = """<html><head>
<title>Elevate Your Business With Our Cutting-Edge Robust Solution Today</title>
<meta name="description" content="In today's fast-paced world, look no further than our state-of-the-art services designed to take your business to the next level with seamless integration and total peace of mind."></head>
<body><h1>Welcome</h1><h1>Also Welcome</h1>
<p>In today's fast-paced world, whether you're a small business or a large enterprise, we've got you covered.</p>
<p>Our services are fast, reliable and affordable, built by an expert team.</p>
<p>We are trusted by thousands of satisfied customers with a 99% satisfaction rate.</p>
<p>Our approach may help your business grow, and is designed to deliver real value.</p>
<p>We offer a wide range of options, tailored to your needs, for total peace of mind.</p>
</body></html>"""

CLEAN = """<html><head>
<title>Lock repair in Kadikoy - Acme Locks</title>
<meta name="description" content="Cylinder replacement from 850 TL including the cylinder. We stock the four most common brands, so most jobs finish on the first visit."></head>
<body><h1>Lock repair in Kadikoy</h1>
<p>A standard cylinder replacement takes 20 to 30 minutes on site.</p>
<p>Price depends on three things: cylinder type, lock brand, and whether the door itself is damaged. We quote before starting, and the quote does not change unless you approve it.</p>
<p>We stock cylinders for Kale, Yale, Mottura and Cisa. If your lock is something else, we usually need a second visit, and we will say so on the phone rather than after arriving.</p>
<p>We do not work on safes.</p>
<p>Open 08:00 to 20:00, seven days.</p>
</body></html>"""


def run(html: str) -> list:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        return audit([page])


def main() -> int:
    failures = []

    slop = run(SLOP)
    rules = {f.rule for f in slop}
    for expected in ("slop-phrase", "unsourced-number", "structure"):
        if expected not in rules:
            failures.append(f"slop page: expected a '{expected}' finding, got {sorted(rules)}")
    if not [f for f in slop if f.severity == "high"]:
        failures.append("slop page: expected at least one HIGH finding")

    clean = run(CLEAN)
    high = [f for f in clean if f.severity == "high"]
    if high:
        failures.append(
            "clean page: false positives — " + "; ".join(f"{f.rule}: {f.detail}" for f in high))

    print(f"slop page:  {len(slop)} findings, rules {sorted(rules)}")
    print(f"clean page: {len(clean)} findings, {len(high)} high")

    if failures:
        print("\nFAILED:")
        for f in failures:
            print(f"  {f}")
        return 1

    print("\nSelf-test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
