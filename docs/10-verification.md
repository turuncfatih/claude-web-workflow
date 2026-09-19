# 10. Verification

The step that decides whether any of the rest was real. A workflow without it
reports success while the page is broken — and that is not a rare failure, it is
the default one.

## Scripts first, agents second

The division that keeps this fast and honest:

| Deterministic | Judgment |
|---|---|
| Does it build? | Is this design decided, or templated? |
| Is the title ≤ 60 characters? | Does this claim say anything? |
| Is there exactly one `<h1>`? | Is this failure output actually a failure? |
| Does the page contain a forbidden phrase? | Is this risk reachable? |
| Is the JSON-LD valid? | Is the fix proportionate? |

**Everything in the left column is a script.** Wrapping it in an agent makes it
slower, more expensive and occasionally inconsistent with itself. Everything in
the right column needs a model, and needs one that did not write the thing being
judged.

## The pipeline

```
web-dev finishes
      │
      ▼
  [ scripts ]     build · slop_check.py · structural checks
      │           deterministic, seconds, free
      ▼
release-verifier  builds, renders, clicks, reads console     ── FACT VETO
      │
      ├─────────────┬──────────────┐        (parallel — different inputs,
      ▼             ▼              ▼         never each other's output)
design-critic   slop-auditor   security-reviewer
  findings        findings      JUDGMENT VETO
      │             │              │
      └─────────────┴──────────────┘
                    ▼
        main session (Opus) decides: ship · revise · escalate
```

`release-verifier` runs first, alone. Critiquing the design of a page that does
not render is wasted work.

## The mechanical pass

```bash
npx astro build                          # zero errors, and note the page count
python3 scripts/slop_check.py dist/      # forbidden phrases, structure, rhythm
```

[`scripts/slop_check.py`](../scripts/slop_check.py) is in this repository and
runs with no dependencies. On a deliberately bad page it produces:

```
HIGH  (10)
  bad.html  [slop-phrase]        "in today's fast-paced world"
  bad.html  [slop-phrase]        "we've got you covered"
  bad.html  [unsourced-number]   "99%" in: We are trusted by thousands…
  bad.html  [structure]          2 <h1> elements, expected exactly 1
MEDIUM (2)
  bad.html  [structure]          title is 65 chars (max 60)
LOW   (1)
  bad.html  [uniform-rhythm]     5 paragraphs, length spread 0.22 — too even
```

It exits non-zero, so it belongs in CI as well as in the workflow. Its lists are
meant to grow: **every tell that gets past you becomes a line in the script**,
and then it never gets past you again.

## The three judgment roles

None of them may be the agent that produced the work. An author reviewing their
own output finds nothing — this is structural, not a matter of prompting.

### `release-verifier` — the fact veto

Establishes that the thing runs. No taste, no opinions.

- [ ] Build passes, exit status recorded
- [ ] Every changed page renders at 360 / 768 / 1200
- [ ] Console errors captured, or explicitly confirmed absent
- [ ] Every state from the spec reached and observed
- [ ] Keyboard focus visible on every interactive element
- [ ] Anything unverifiable listed under **Not checked**

That last line is the one that matters most. *Unverified is not passed* — a
verifier that reports success for things it could not check is worse than no
verifier, because it is trusted.

**Blocks on:** a red build, a page that does not render, a console error, an
unmet acceptance criterion.
**Never blocks on:** style, naming, architecture, preferences.

A fact veto needs no severity calibration. It either worked or it did not, and
the output is the evidence.

### `design-critic` — findings

The rendered page, screenshotted. Its checklist and its single decisive question
— *would this page work for a different business with the text swapped?* — are in
[chapter 5](05-not-looking-ai-made.md).

Findings, not a veto. Taste blocking a release is how a veto stops being
respected.

### `security-reviewer` — the judgment veto

[Chapter 9](09-security.md). Evidence mandatory; blocks only on the left column
of that chapter's table.

### Why two vetoes and not three

Two work because they are **different in kind** and cannot deadlock:

| | `security-reviewer` | `release-verifier` |
|---|---|---|
| Basis | Expertise | Tool output |
| Needs evidence | Yes, mandatory | It *is* evidence |
| Overridable | By a human, on the record | No — fix it |

A third veto — a design veto, an architecture veto — deadlocks the team within a
week. `design-critic` and `slop-auditor` produce findings precisely so that this
does not happen. The general argument is in the
[Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook).

## After shipping

Verification does not end at the build. What is configured and what is served
are different things:

```bash
curl -sI https://example.com | grep -iE "content-security|strict-transport|x-frame"
curl -s https://example.com/sitemap.xml | head
```

Plus a browser pass over the **live** URL: render, console, the primary action,
the form. See [chapter 11](11-shipping-cloudflare.md).

## Drift, so the next deploy is a diff

```
/seo-drift baseline      # before a significant change
   ... work ...
/seo-drift               # after: what changed, and was any of it intended?
```

Regressions are silent. A title that grew, a heading level that got skipped, a
canonical that moved — none fail a build, all cost traffic. A baseline turns "I
think it's fine" into something you can read.
