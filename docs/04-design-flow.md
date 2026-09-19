# 4. The design flow

From "we need a page" to a spec a developer agent can build without inventing
anything.

```
brief ──► Stitch screens ──► pick & react ──► extract tokens
                                                   │
                                                   ▼
                                           design spec ──► web-dev
                                                   │
                                                   ▼
                                           design-critic  ◄── rendered page
```

The important property: **the developer never receives prose.** It receives a
spec with token names, breakpoints and states. Prose in a handoff is where a
page starts inventing itself.

## Step 1 — Brief, before any pixels

Three lines, and they come from `CLAUDE.md` plus the request:

```
Goal        The one thing this page must achieve
Audience    Who reads it, and what they already know
Constraint  What is fixed: brand tokens, required sections, legal text
```

A page with two goals gets a hedged design. If the brief has an "and", split
the page or drop one goal.

## Step 2 — Generate screens with Stitch

Ask for **three distinct directions**, not one:

```
Three directions for a <page type> for <business>.
Goal: <the one goal>.
Make them genuinely different in structure — not the same layout recoloured.
Direction A: information-dense, closer to a documentation page than a landing page.
Direction B: editorial, long-form, one column, strong typographic hierarchy.
Direction C: conventional marketing layout — as the control to react against.
```

Asking for three and naming them differently is the whole trick. One request
returns the median layout — and the median layout is what every generated site
looks like. Three contrasting ones give you something to have an opinion about.

## Step 3 — React, do not accept

The output is a starting point. Write down, in plain language:

- What is **right** about each direction, specifically
- What is **generic** about each — the parts any template would have produced
- What is **missing** — the thing this business has that none of them show

That third bullet is where the page stops being interchangeable. A locksmith
whose real differentiator is 24-hour response has a page that leads with
response time, not with a hero image of a door.

## Step 4 — Extract the spec

Turn the chosen direction into something checkable. This is mechanical work — a
Sonnet subagent does it well:

```
Layout        3 breakpoints: 360 / 768 / 1200, with the grid at each
Type          scale in use, which level each block takes
Colour        token names only — never hex. A hex value means a missing token.
Spacing       base rhythm, section padding per breakpoint
States        empty / loading / error / too-long / too-many / partial
Motion        what animates, on what trigger, for how long
Signature     the one element on this page no template would have produced
```

The last line is a requirement, not a flourish. See
[chapter 5](05-not-looking-ai-made.md).

## Step 5 — Hand to the developer

The full handoff contract — Fixed, Open, Forbidden, Acceptance — is in
[agents/](../agents/) and, in its general form, in the
[Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook).

The three rules that matter most at this seam:

1. **No colour that is not a token.** If a state has no token, stop and report
   it. A near-miss colour is invisible in review and wrong forever.
2. **Never shrink the type scale to make copy fit.** Either the copy is too long
   or the layout is wrong. Shrinking hides which.
3. **Never ship only the happy path.** All six states, every time.

## Step 6 — Critique the rendered page

Not the spec — the **rendered page**, screenshotted at real breakpoints. This is
a separate role with a separate prompt, and it is the step most workflows skip.

What it checks, and why it cannot be the same agent that built the page, is
[chapter 5](05-not-looking-ai-made.md).
