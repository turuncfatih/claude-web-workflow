# 2. The skills map

A skill is a packaged procedure — a checklist, a method, a set of thresholds —
that loads into the turn when you invoke it. Invoking the right one is usually
the difference between a generic answer and a specific one.

The catalogue below is the set this workflow actually leans on. The full
one-line-each list is in [reference/skills-catalogue.md](../reference/skills-catalogue.md).

## By phase

### Plan — before any file exists

| Skill | What it gives you |
|---|---|
| `seo-plan` | Site architecture, keyword strategy, content roadmap for a new site |
| `seo-cluster` | Groups keywords by **actual SERP overlap**, not text similarity, and turns them into a hub-and-spoke page structure |
| `seo-competitor-pages` | Comparison and alternatives page structures, if the business needs them |

`seo-cluster` is the one that changes the site rather than decorating it: its
output *is* your page inventory and internal link map. Run it before you decide
what pages exist, not after.

### Design

| Skill | What it gives you |
|---|---|
| `frontend-design` | Aesthetic direction for new UI — how to make choices that do not read as templated |
| `design-craft` | Quality bar: typography hierarchy, colour system, animation discipline, state coverage, accessibility floor |
| `brand-guidelines` | Applies a defined brand's colours and type |
| `theme-factory` | Pre-set themes, or generates one, for artifacts and landing pages |

`design-craft` is the one to invoke when reviewing, not only when creating. Its
"does not look machine-made" rules are the basis of
[chapter 5](05-not-looking-ai-made.md).

### Build

| Skill | What it gives you |
|---|---|
| `webapp-testing` | Drives the local app with Playwright — verify behaviour, capture screenshots, read browser logs |

### Content

| Skill | What it gives you |
|---|---|
| `seo-content-brief` | Competitive brief with per-section word counts and keyword guidance, before writing |
| `seo-content` | Reviews finished content for E-E-A-T, depth, readability, thin-content risk |

Brief first, write second, review third. Writing without a brief produces text
that has to be rewritten once the brief exists anyway.

### Technical SEO

| Skill | What it gives you |
|---|---|
| `seo-technical` | Crawlability, indexability, security headers, URL structure, mobile, CWV, JS rendering |
| `seo-schema` | Detects, validates and generates JSON-LD |
| `seo-sitemap` | Validates or generates XML sitemaps |
| `seo-hreflang` | Multi-language and multi-region tags, and the mistakes that break them |
| `seo-images` | Alt text, formats, sizes, responsive images, lazy loading, CLS |

`seo-hreflang` earns its place the moment a site has more than one language —
the failure mode is silent, and it costs the whole international footprint.

### GEO — being found by AI answers

| Skill | What it gives you |
|---|---|
| `seo-geo` | AI Overviews, ChatGPT search, Perplexity: crawler accessibility, passage-level citability, brand mention signals |
| `seo-sxo` | Reads SERPs backwards to find page-type mismatches — why a well-optimised page still does not rank |

See [chapter 7](07-seo-geo-flow.md). These two are the newest part of the
workflow and the part most sites have not done at all.

### Local

| Skill | What it gives you |
|---|---|
| `seo-local` | Google Business Profile, NAP consistency, citations, reviews, local schema, location pages |
| `seo-maps` | Geo-grid rank tracking, GBP audit, review intelligence, competitor radius |

### Audit and drift

| Skill | What it gives you |
|---|---|
| `seo-audit` | Full-site audit, delegating to specialists, with a health score |
| `seo-page` | Deep single-page analysis |
| `seo-drift` | **Baseline and diff** — did this deploy break something that was fine? |

`seo-drift` is git for your on-page SEO. Capture a baseline before a large
change and diff after; it catches the regressions nobody would have looked for.

### Live data

| Skill | What it gives you |
|---|---|
| `seo-google` | Search Console, PageSpeed, CrUX field data, GA4 organic |
| `seo-dataforseo` | Live SERPs, keyword volume, backlinks, AI visibility — needs the DataForSEO extension |
| `seo-backlinks` | Referring domains, anchor distribution, toxic links, competitor gaps |

Everything above this section works offline against your own files. These three
need credentials, and they are where guesses become measurements.

### Images

| Skill | What it gives you |
|---|---|
| `seo-image-gen` | Audits OG/social images, plans what needs generating |
| `canvas-design` | Original visual art as PNG/PDF |

See [chapter 6](06-visual-assets.md) for where these fit against an external
image tool.

## How to actually invoke them

```
/seo-cluster "emergency plumber istanbul"
/frontend-design
/design-craft
/seo-technical https://example.com
/seo-drift baseline
```

Three rules that save time:

1. **Invoke the skill before the work, not after.** A skill loaded after the
   page is written becomes a review; loaded before, it becomes a method.
2. **One skill per question.** Loading four at once produces an answer that
   hedges across all four.
3. **A skill is not a subagent.** The skill loads a procedure into the current
   turn; a subagent runs somewhere else with its own context. Use a skill for
   *how*, a subagent for *who*. See [chapter 1](01-model-division-of-labour.md).
