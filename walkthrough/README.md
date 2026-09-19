# Walkthrough: empty folder to live site

One pass through the whole workflow, in order, with the actual commands. The
example is a small local service business, because that is the case where every
part of this matters — design, copy, local SEO, speed and trust all move the
same needle.

Each step links to the chapter that explains *why*.

---

## Day 0 — Setup ([chapter 0](../docs/00-setup.md))

```bash
mkdir acme-locks && cd acme-locks
npm create astro@latest . -- --template minimal --typescript strict --no-install
npm install
git init && git add -A && git commit -m "Astro skeleton"
```

Connect Stitch ([chapter 3](../docs/03-mcp-servers.md)):

```bash
claude mcp add --transport http stitch https://stitch.googleapis.com/mcp
```

Install the team ([agents/](../agents/)):

```bash
mkdir -p .claude/agents && cp <this-repo>/agents/*.md .claude/agents/
cp <this-repo>/scripts/slop_check.py scripts/
```

Write `CLAUDE.md` before anything else. Stack, single sources of truth,
invariants, commands — the template is in [chapter 0](../docs/00-setup.md).

The four invariants worth copying verbatim:

```
1. Check site.ts before adding any constant.
2. Title ≤ 60, meta description ≤ 160, exactly one <h1> per page.
3. No delivery-time promises. Written scope and fixed-price language.
4. No invented metrics. Any number needs a source.
```

---

## Step 1 — Decide what the site is ([chapter 1](../docs/01-model-division-of-labour.md))

Main session, Opus, no code yet.

```
/seo-cluster "çilingir istanbul"
```

`seo-cluster` groups keywords by real SERP overlap, and its output *is* your page
inventory and internal link map. Run it before deciding what pages exist — not
after.

Then the planning prompt from [reference/prompts.md](../reference/prompts.md).
You want a page list where every page has one goal you can state in a sentence.

**Output of this step:** a page inventory in `CLAUDE.md`. No files yet.

---

## Step 2 — Design directions ([chapter 4](../docs/04-design-flow.md))

Ask Stitch for three genuinely different directions. Then build them as one
Artifact with a switcher ([chapter 12](../docs/12-artifacts-for-design-review.md)),
with **real copy, not lorem ipsum**.

Open it. Flip between them. Send the link to the business owner.

React with the three questions:

1. What is specifically right about each?
2. What is generic — what any template would produce?
3. What is missing that this business actually has?

**Output:** a design spec with a named signature element
([chapter 5](../docs/05-not-looking-ai-made.md)).

---

## Step 3 — Design spec and copy, in parallel

Two agents, neither reading the other:

```
> Use the designer agent to turn the chosen direction into a spec.
> Use the content-writer agent to write the home page copy from the brief.
```

`designer` runs on Opus — taste is the deliverable.
`content-writer` runs on Sonnet — copy is cheap to correct.

Before writing, get the brief:

```
/seo-content-brief "çilingir istanbul"
```

---

## Step 4 — Build ([chapter 8](../docs/08-performance.md))

```
> Use the web-dev agent to build the home page from the spec and the copy file.
```

One writer, the only one. The performance decisions are made here and are hard to
undo later:

- `output: 'static'`, zero runtime JavaScript as the target
- Fonts self-hosted, subset, one preloaded, `font-display: swap`
- LCP image eager with `fetchpriority="high"`; everything below the fold lazy
- `width` and `height` on every image

---

## Step 5 — Verify ([chapter 10](../docs/10-verification.md))

Scripts first, always:

```bash
npx astro build
python3 scripts/slop_check.py dist/
```

Then the roles, in order:

```
> Use the release-verifier agent.                          # fact veto — first, alone
> Use the design-critic and slop-auditor agents.           # in parallel
> Use the seo-auditor agent.
```

`release-verifier` runs alone and first. Critiquing a page that does not render is
wasted work.

The question that decides whether step 2 succeeded:

> **Would this page still work if you swapped in a different business's name?**

If yes, go back to step 2. Nothing has been decided yet.

---

## Step 6 — Schema, sitemap, hreflang ([chapter 7](../docs/07-seo-geo-flow.md))

Now that content exists, and not before:

```
/seo-schema
/seo-sitemap
/seo-hreflang      # only if the site has more than one language
/seo-geo           # citability, crawler access, brand signals
```

The schema rule that matters: **JSON-LD must describe what is actually visible on
the page.** Schema claiming a price the page does not show is a mismatch, and
mismatches are penalised harder than missing schema.

---

## Step 7 — Security ([chapter 9](../docs/09-security.md))

```
> Use the security-reviewer agent.
```

Write `public/_headers` before the first deploy, while the site is small enough
that a strict CSP is nearly free.

```bash
grep -rEn "(api[_-]?key|secret|token|password|AIza|sk-)" dist/
find dist -name '*.map' -o -name '.env*'
```

---

## Step 8 — Ship ([chapter 11](../docs/11-shipping-cloudflare.md))

```bash
git add -A && git commit -m "Home page" && git push origin main
```

Cloudflare Pages → Connect to Git → build `npm run build`, output `dist`.

Add the custom domain. Turn on: Always Use HTTPS, Bot Fight Mode, Web Analytics,
and **access control on preview deployments** — that last one is the row people
miss, and public preview URLs get indexed.

---

## Step 9 — Verify the live site

The build passing is not the same as the site working.

```bash
curl -sI https://acme-locks.com | grep -iE "content-security|strict-transport|x-frame|cf-cache-status"
curl -sI https://www.acme-locks.com | head -3      # canonical redirect
curl -s  https://acme-locks.com/sitemap-index.xml | head
```

Then a browser pass on the live URL: three breakpoints, console clean, the phone
link works, the form submits.

---

## Step 10 — Baseline, so the next deploy is a diff

```
/seo-drift baseline
```

Submit the sitemap in Search Console. Request indexing for the pages that matter.

---

## Every deploy after this one

```
plan ─► build ─► scripts ─► verifier ─► critics ─► ship ─► live checks ─► drift
```

Ten steps the first time. Four every time after — and it is those four that keep
the site correct at the tenth deploy rather than only at the first.

## What this costs

For one page, end to end, roughly:

| Work | Model | Share |
|---|---|---|
| Planning and routing | Opus | ~20% |
| Design direction and review | Opus | ~25% |
| Implementation | Sonnet | ~30% |
| Copy | Sonnet | ~15% |
| Audits and verification | Sonnet / Haiku | ~10% |

Running all of it on Opus costs four to six times as much and is better in two of
those five rows. But the number that dominates both is **rework** — which is why
the spending belongs on the plan and the review, the two steps that prevent it.
