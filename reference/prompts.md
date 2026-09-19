# Prompts that earn their place

Not a prompt library. These are the handful where the wording genuinely changes
the output, phase by phase. Everything else is better handled by a
[skill](skills-catalogue.md) or an [agent](../agents/).

The pattern behind all of them: **name the alternative you are rejecting.** A
prompt that says what good looks like gets the median answer. A prompt that says
what to avoid, and what to do instead, gets a decision.

---

## Planning

```
Before we build anything: what pages should this site have, and what is each
page's single goal?

Business: <what it does, where, for whom>
The one thing a visitor should do: <action>
What competitors all say, that we should not repeat: <...>

Do not propose a standard five-page brochure structure unless you can argue for
each page. If two pages would have the same goal, say so and merge them.
```

The last paragraph is what stops you getting Home / About / Services / Blog /
Contact by reflex.

---

## Design direction

```
Three directions for a <page type>. Goal: <the one goal>.
Genuinely different in structure — not the same layout recoloured.

A: information-dense, closer to a documentation page than a landing page
B: editorial, long-form, single column, strong typographic hierarchy
C: conventional marketing layout — the control, to react against

Tokens: <paste token set>. No gradients unless the brand defines one.
Real copy, not lorem ipsum.
```

Then, on what comes back:

```
For each direction, tell me three things:
1. What is specifically right about it
2. What is generic — what any template would have produced
3. What is missing that this business actually has
```

Item 3 is where the page stops being interchangeable.

---

## Copy

```
Write the copy for <page>, following the brief.

Hard rules:
- Every claim must pass the opposite test: would a competitor claim the opposite?
  If no, cut the sentence.
- No number without a source. No invented statistics, ratings or customer counts.
- Say one specific, true, slightly uncomfortable thing — a limit, a case we do not
  serve, a price that is higher than a competitor's and why.
- Vary paragraph length deliberately.
- Forbidden: <paste the phrase list from CLAUDE.md>
```

---

## Review — the sharp version

The single highest-value prompt in this file, and it works on any model,
including one that did not write the page:

```
Here is a page for <business>. Answer three questions, bluntly:

1. Would this page still work if you swapped in a different business's name?
2. Which sentences say nothing a competitor would not also say?
3. What reads as machine-written?

Do not be encouraging. I want the findings, not a summary of what is good.
```

"Do not be encouraging" is doing real work there. Without it you get a paragraph
of praise and two soft suggestions.

---

## Verification

```
Build the site, then verify it.

Report, in this order:
1. Every command you ran, with its exit status
2. Every failure, quoted in full — not summarised
3. Everything you could NOT check, and why

Do not report pass for anything you did not actually verify.
Unverified is not passed.
```

---

## A second opinion, from a different model

Paste the page into a model that did not write it, with no brief and no context:

```
This is a live page for a <business type>. I did not write it and I have no
stake in it.

Which parts are generic? Which claims are empty? What would make you distrust
this business?
```

Withholding the brief is the point. A reviewer who knows why each choice was made
will defend it. See [docs/13](../docs/13-which-ai-for-what.md).
