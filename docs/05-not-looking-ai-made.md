# 5. Not looking machine-made

The most valuable chapter here, and the one with the least written about it.

A generated site is usually *correct*. It builds, it is responsive, it has
headings. And a visitor can tell within two seconds that nobody decided
anything. That recognition is a trust problem, and no amount of correctness
fixes it.

This chapter is the catalogue of tells, the countermeasures, and the roles that
enforce them.

---

## Part 1 — The visual tells

### What generated design looks like

| Tell | Why it happens |
|---|---|
| **Everything is a card** | A card is the safe container. Nothing is ever wrong inside a card, so everything becomes one |
| **Three-column feature grid** | The median layout for "features". Present on a million pages |
| **Purple-to-indigo gradient** | The default accent when no brand was specified |
| **Glassmorphism, blurred blobs** | Decoration that requires no decision about content |
| **Everything centered** | Centering avoids the question of where the eye should go |
| **Uniform section rhythm** | Every section the same height and padding, so nothing is emphasised |
| **Emoji as icons** | An icon set requires a decision; emoji do not |
| **One weight, one size** | Type at 16–20px throughout, no scale contrast |
| **Perfect symmetry everywhere** | Asymmetry requires a reason, and the safe default has none |
| **Generic stock hero** | An abstract image that could belong to any business |
| **Buttons all equal** | Every action the same size, so no action is primary |

None of these is wrong on its own. All of them together is the signature.

### Countermeasures

**1. One signature element per page.** Something no template would produce,
required in the spec. A price table with real prices. A process with real step
names and real durations. A photo of the actual premises. A map. A comparison
that admits a weakness. If you cannot name the signature element, the page is
interchangeable.

**2. Real type contrast.** A scale where the largest and smallest are far apart
— 40px against 14px, not 20px against 16px. Hierarchy you can see with the page
squinted at.

**3. Deliberate asymmetry, at least once.** One section that breaks the grid on
purpose. It costs one decision and removes the template feeling from the whole
page.

**4. Tokens only, gradients by exception.** No colour that is not a named token.
No gradient unless the brand defines one. This single rule kills the purple
default.

**5. Vary section rhythm.** Sections are not all equally important, so they
should not all be equally tall. Give the important one more room and the
supporting ones less.

**6. A real icon set, consistently.** One family, one weight, one metaphor
style. Mixed icon styles read as assembled rather than designed. See
[chapter 6](06-visual-assets.md).

**7. Reference-driven direction, not adjective-driven.** "Modern and clean"
describes every generated page ever made. "Information density closer to a
documentation site than a landing page" describes one.

---

## Part 2 — The copy tells

Worse than the visual ones, because they survive redesigns.

### The phrase list

Text that appears in machine-written marketing copy and almost nowhere else:

```
In today's fast-paced world          Look no further
Whether you're X or Y                We've got you covered
It's not just X — it's Y             Take your X to the next level
Elevate your                         Unlock the power of
Seamless                             Robust
Cutting-edge                         State-of-the-art
Game-changer                         Revolutionise
Dive into / delve into               A testament to
Rich tapestry                        At the end of the day
```

### The structural tells

Harder to see, and more damaging:

| Tell | What it looks like |
|---|---|
| **Triads everywhere** | "fast, reliable and affordable" — three adjectives, every time, because three sounds complete |
| **Uniform paragraph length** | Every paragraph three sentences. Human writing varies |
| **Claims nobody would dispute** | "Quality matters to us." A competitor would never claim the opposite, so the sentence says nothing |
| **Unsourced numbers** | "99% customer satisfaction", "trusted by thousands" — invented because the shape of the sentence wanted a number |
| **Hedged everything** | "may help", "can often", "is designed to" — the model avoiding commitment |
| **Symmetrical sentences** | Every sentence the same rhythm and length |
| **Sections that restate** | Three sections saying the same thing in different words |

### Countermeasures

**1. A forbidden phrase list in `CLAUDE.md`.** Not a suggestion in a prompt — a
project rule, checked mechanically. The list above is a starting point; add to it
every time you catch one.

**2. The opposite test.** For every claim: *would a competitor claim the
opposite?* If no, delete the sentence. "We use quality parts" fails. "We stock
the four most common lock cylinders, so most jobs finish on the first visit"
passes — a competitor might genuinely not.

**3. Specificity is mandatory.** Every claim carries a concrete detail: a
number with a source, a named process step, a real constraint, a real limit.

**4. No invented metrics, ever.** This belongs in `CLAUDE.md` as an invariant.
A fabricated statistic is the one copy failure that cannot be fixed by an edit —
it is a lie on a business's website.

**5. Vary length on purpose.** A one-sentence paragraph after a long one is a
decision. Uniformity is the absence of one.

**6. Say one uncomfortable true thing.** A limitation, a case you do not serve,
a price that is higher than a competitor's and the reason. Nothing signals a
human author faster, and nothing is less likely to be generated by default.

---

## Part 3 — The roles that enforce it

Rules that nobody checks are decoration. Two roles exist for this, and **neither
may be the agent that produced the work** — an author reviewing their own output
finds nothing.

### `design-critic`

Reviews the **rendered page**, screenshotted at 360 / 768 / 1200 — not the spec,
not the code. Its whole job is the list in Part 1.

```markdown
---
name: design-critic
description: Reviews a rendered page for signs of templated, machine-made design. Runs after the page is built, on screenshots. Never edits.
model: sonnet
tools: Read, Bash, Glob, Grep
---
```

Its checklist:

- [ ] Name the signature element. If you cannot, that is the finding.
- [ ] Is the type scale contrast real, or is everything 16–20px?
- [ ] Is every section the same height and padding?
- [ ] Is every container a card?
- [ ] Any colour outside the token set? Any unspecified gradient?
- [ ] Is there one primary action, visually distinct from the rest?
- [ ] Does any section break the grid on purpose?
- [ ] Would this page work for a different business with the text swapped?

**That last question is the whole test.** If the answer is yes, the page is a
template with content in it.

Findings, not a veto — otherwise taste blocks releases and the veto stops being
respected. See the veto discussion in the
[Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook).

### `slop-auditor`

Two passes, and the order matters.

**Pass 1 — mechanical.** [`scripts/slop_check.py`](../scripts/slop_check.py)
runs over the rendered HTML: forbidden phrases, triad density, paragraph-length
uniformity, unsourced numbers. Deterministic, instant, free. A script, not an
agent — see [chapter 10](10-verification.md).

**Pass 2 — judgment.** The model reads what survived and applies the tests a
script cannot: the opposite test, the specificity requirement, whether any
sentence says something a competitor could dispute.

```markdown
---
name: slop-auditor
description: Audits page copy for machine-written tells — forbidden phrases, empty claims, invented metrics, uniform structure. Runs the mechanical check first, then judges what is left. Never edits.
model: sonnet
tools: Read, Bash, Glob, Grep
---
```

### `release-verifier`

The fact veto. Build, render, console, states. It does not judge taste — it
establishes that the thing runs. Nothing ships without it.

Full definitions for all three are in [agents/](../agents/).

---

## The order these run in

```
web-dev builds
     ▼
release-verifier   does it build and render?        ── VETO
     ▼
design-critic      does it look decided?            ── findings
slop-auditor       does it read like a person?      ── findings
     ▼
main session (Opus) reads all three and decides: ship, revise, or escalate
```

Verifier first, because critiquing the design of a page that does not render is
wasted work. The two critics run in parallel — they read different things and
never each other's output.

## The one question

If you keep nothing else from this chapter:

> **Would this page still work if you swapped in a different business's name?**

If yes, nothing has been decided yet — and that is what "looks AI-made" actually
means.
