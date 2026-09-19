#!/usr/bin/env python3
"""Repository hygiene checks.

A guide that teaches a spec and then ships examples violating it has no
authority. Both of these run in CI.
"""

from __future__ import annotations

import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_SECTIONS = [
    "## Role",
    "## Invoke / do not invoke",
    "## Inputs",
    "## Output contract",
    "## Tools",
    "## Model tier",
    "## Definition of done",
    "## Veto",
    "## Failure & escalation",
    "## Anti-goals",
]


def check_links() -> list[str]:
    problems, checked = [], 0

    for md in sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts):
        for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", md.read_text()):
            target = match.group(2).split("#")[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            if not (md.parent / urllib.parse.unquote(target)).resolve().exists():
                problems.append(f"{md.relative_to(ROOT)} -> {target}")

    print(f"links:  {checked} relative links checked, {len(problems)} broken")
    return problems


def check_agent_specs() -> list[str]:
    problems = []
    files = sorted(p for p in (ROOT / "agents").glob("*.md") if p.stem != "README")

    for agent in files:
        text = agent.read_text()
        where = agent.relative_to(ROOT)

        if not text.startswith("---\n"):
            problems.append(f"{where}: no frontmatter")
            continue

        frontmatter = text.split("---\n")[1]

        name = re.search(r"^name:\s*(\S+)", frontmatter, re.M)
        if name is None:
            problems.append(f"{where}: frontmatter has no 'name'")
        elif name.group(1) != agent.stem:
            problems.append(f"{where}: name '{name.group(1)}' does not match the filename")

        if not re.search(r"^description:\s*\S", frontmatter, re.M):
            problems.append(f"{where}: frontmatter has no 'description'")

        # This repository's whole argument is that tier is a stated decision.
        if not re.search(r"^model:\s*\S", frontmatter, re.M):
            problems.append(f"{where}: frontmatter has no 'model' — the tier must be explicit")

        for section in REQUIRED_SECTIONS:
            if section not in text:
                problems.append(f"{where}: missing '{section}'")

    print(f"agents: {len(files)} agent specs checked, {len(problems)} problems")
    return problems


def check_one_writer() -> list[str]:
    """Exactly one agent may hold Write/Edit. The team's core claim."""
    writers = []
    for agent in sorted((ROOT / "agents").glob("*.md")):
        if agent.stem == "README":
            continue
        frontmatter = agent.read_text().split("---\n")[1]
        tools = re.search(r"^tools:\s*(.+)$", frontmatter, re.M)
        if tools and re.search(r"\b(Write|Edit)\b", tools.group(1)):
            writers.append(agent.stem)

    print(f"writers: {len(writers)} agent(s) with write access: {', '.join(writers) or 'none'}")
    if len(writers) != 1:
        return [f"expected exactly one writer, found {len(writers)}: {', '.join(writers)}"]
    return []


def main() -> int:
    problems = check_links() + check_agent_specs() + check_one_writer()

    if problems:
        print("\nFAILED:")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
