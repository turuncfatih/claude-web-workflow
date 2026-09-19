# 12. Artifacts for design review

A design argued about in chat is a design nobody agreed on. An Artifact is a real
web page at a real URL, private by default, that you can open, click and send to
someone. For this workflow it does three jobs no other tool does as cheaply.

## Job 1 — Three directions, side by side, interactive

The single most useful thing you can build here. Not three screenshots — **one
page with a switcher**, so the same content renders in three different design
directions and you can flip between them.

```
Build one HTML artifact with a switcher at the top: Direction A / B / C.
Same content in all three, genuinely different structure — not one layout
recoloured.

A: information-dense, closer to a documentation page than a landing page
B: editorial, long-form, single column, strong typographic hierarchy
C: conventional marketing layout — the control, so we have something to react against

Use these tokens for all three: <paste your token set>.
No lorem ipsum — use the real copy, even if it is rough.
```

Two rules that make this work:

- **Real copy, never lorem ipsum.** Placeholder text makes every layout look fine.
  Real copy is too long in one direction and too short in another, and that is
  exactly the information you are after.
- **The same content in all three.** Otherwise you are comparing copy, not design.

Flipping between three directions in one second tells you more than staring at
one for ten minutes. It is also the fastest cure for the problem in
[chapter 5](05-not-looking-ai-made.md): put the generic direction next to two
opinionated ones and it stops looking acceptable.

## Job 2 — A review surface someone else can open

A client, a colleague, or the business owner does not have your repo, does not
run `npm`, and will not read a Figma comment thread. They will open a link on
their phone.

Useful artifacts for this:

| Artifact | What it replaces |
|---|---|
| Three design directions with a switcher | A meeting |
| A page-inventory table, with each page's goal and status | A spreadsheet nobody updates |
| An audit dashboard — findings by severity, page, owner | Pasting a wall of text into chat |
| A live style guide — tokens, type scale, components, states | A design file the developer never opens |

The style guide is the one that keeps paying. A page that renders your actual
tokens at their actual sizes is the reference `web-dev` and `design-critic` both
work from, and it is always current because it renders the real values.

## Job 3 — Prototyping an interaction before it is built

Some questions cannot be answered by looking: does this form feel long? Is this
accordion better than six sections? Does this table work on a phone?

Build the interaction as an artifact, use it for two minutes, decide, then hand
the decision — not the artifact — to `web-dev`.

## The workflow

```
brief
  ▼
Stitch screens ─────► react, pick two or three worth exploring
  ▼
Artifact: the directions side by side, real copy, real tokens
  ▼
open it · flip between them · send the link · collect reactions
  ▼
extract the spec from the direction that won        ← chapter 4
  ▼
web-dev builds it properly
```

## What an Artifact is not

**It is not the site.** It is a fast, throwaway surface for deciding. It does not
have your build pipeline, your content collections, your schema, your headers or
your performance budget.

Shipping an artifact as a website is the mistake to avoid here. The artifact
answers "which direction?"; `web-dev` answers "how does this actually work?".

Two consequences worth holding on to:

- **Do not let an artifact accumulate features.** The moment it needs real data,
  real routing or real content, it has stopped being a decision tool.
- **Extract the decision, discard the code.** What crosses the boundary is the
  spec — tokens, scale, layout, states — not the artifact's HTML.

## A note on what goes in one

An artifact is a page at a shareable URL. Treat it as publishing:

- Real client data, prices that are not public yet, anything under NDA — keep it out
- No credentials, no keys, no internal URLs
- Nothing that imitates a real company's branding to see how it would look — build
  it with your own tokens

The same rule as any other outward-facing surface: if you would not want it
forwarded, do not put it there.
