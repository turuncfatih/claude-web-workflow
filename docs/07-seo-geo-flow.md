# 7. SEO and GEO

Two audiences now. Classic search ranks **pages**; AI answers cite **passages**.
The work overlaps but is not the same, and most sites have done none of the
second.

| | Classic SEO | GEO |
|---|---|---|
| Unit | The page | The passage |
| Goal | Rank in a list | Be quoted in an answer |
| Rewards | Authority, links, relevance | Clear, self-contained, attributable statements |
| Measured by | Position, clicks | Mentions, citations, share of answer |

The good news: the same writing serves both. A passage that can be quoted
without surrounding context is also a passage that reads well.

## The order of operations

Order matters more than any individual step. Doing these out of sequence is the
most common reason SEO work produces no result.

```
1  seo-plan        what this site is for, and who it competes with
2  seo-cluster     keywords grouped by real SERP overlap → the page inventory
3  seo-content-brief  per page, before a word is written
4  write           content-writer, from the brief
5  seo-schema      JSON-LD from the content that now exists
6  seo-technical   crawl, index, headers, CWV, rendering
7  seo-geo         citability, crawler access, brand signals
8  seo-audit       the whole site, with a score
9  seo-drift       baseline, so the next deploy can be diffed
```

**Steps 1 and 2 decide the site's architecture.** Running them after the pages
exist turns strategy into a retrofit. `seo-cluster` groups by actual SERP
overlap rather than by how similar words look, which is why its output is a page
inventory and an internal link map rather than a keyword list.

## What GEO actually asks for

### 1. Passage-level citability

An AI answer quotes a passage and attributes it. That works when a passage is
**self-contained** — it makes sense lifted out of the page.

| Not citable | Citable |
|---|---|
| "As mentioned above, this usually takes a while." | "A standard cylinder replacement takes 20–30 minutes on site." |
| "Our prices are competitive." | "Cylinder replacement starts at ₺X, including the cylinder." |
| "It depends on several factors." | "Price depends on three things: cylinder type, lock brand, and whether the door is damaged." |

The pattern: **a specific claim, stated completely, in one or two sentences.**
Notice that all three "citable" examples also pass the opposite test from
[chapter 5](05-not-looking-ai-made.md) — a competitor might genuinely say
something different. That is not a coincidence. Copy that is worth quoting and
copy that does not read as machine-written are the same copy.

### 2. Crawler accessibility

An AI crawler that cannot render your JavaScript sees nothing. This is where a
static site has a structural advantage — the content is in the HTML, with no
execution required. Check what is actually reachable, not what renders in your
browser.

### 3. Structured data that matches the visible text

Schema tells a machine what a page is about. The rule that matters: **JSON-LD
must describe what is actually on the page.** Schema that claims a price the
page does not show is a mismatch, and mismatches are penalised harder than
missing schema.

`seo-schema` generates and validates it.

### 4. Brand mention signals

AI answers draw on how often and in what context a name appears across the web,
not only on the site itself. This is the slowest part of the work and the part a
site cannot do alone — consistent NAP data, real directory listings, genuine
citations.

For a local business, `seo-local` and `seo-maps` cover the mechanics.

### 5. A note on `llms.txt`

Optional, cheap, and widely misrepresented. Google has stated it does not use
it. Add it if you like; do not count it as work done.

## Local, when the business is local

For a business with a physical presence or a service area, the local layer
outranks almost everything else:

| Skill | Covers |
|---|---|
| `seo-local` | GBP, NAP consistency, citations, reviews, local schema, location pages |
| `seo-maps` | Geo-grid rank tracking, GBP audit, review intelligence, competitor radius |

**NAP consistency is the highest-value, lowest-effort item in local SEO.** Name,
address and phone identical everywhere — site, GBP, directories, social. This is
also why `site.ts` exists as a single source of truth in
[chapter 0](00-setup.md): one place to change, no drift.

## Multi-language

If the site has more than one language, `seo-hreflang` is not optional. The
failure mode is silent — nothing breaks, nothing errors, the international
footprint simply does not work. Every language version references every other,
including itself, with correct region codes.

## Measuring

Everything above works offline against your own files. These need credentials
and turn guesses into measurements:

| Skill | Gives you |
|---|---|
| `seo-google` | Search Console positions, indexation, CrUX field data, GA4 organic |
| `seo-dataforseo` | Live SERPs, volumes, backlinks, and AI-visibility checks |
| `seo-backlinks` | Referring domains, anchors, toxic links, competitor gaps |

On a site that launched last week these return nothing useful. Connect them when
there is traffic to reason about.

## The habit that keeps it working

```
/seo-drift baseline      # before a significant change
   ... do the work ...
/seo-drift               # after: what changed, and was it intended?
```

Regressions are silent. A title that got longer, a heading level that got
skipped, a canonical that moved — none of these fail a build, and all of them
cost traffic. A baseline turns "I think it's fine" into a diff.
