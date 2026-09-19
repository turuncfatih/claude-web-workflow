# Skills catalogue

Every skill this workflow uses, one line each, with the phase it belongs to.
The narrative version is [docs/02](../docs/02-skills-map.md).

Skills marked **⚡** need credentials or an extension; everything else works
offline against your own files.

## Strategy — before any file exists

| Skill | Reach for it when |
|---|---|
| `seo-plan` | Starting a new site and you need architecture, keyword strategy and a content roadmap |
| `seo-cluster` | You need the page inventory — groups keywords by real SERP overlap and outputs a hub-and-spoke structure with an internal link matrix |
| `seo-competitor-pages` | The business needs "X vs Y" or "alternatives to X" pages |
| `seo-programmatic` | Pages will be generated at scale from a data source, and you need thin-content and index-bloat safeguards |
| `seo-sxo` | A page is well-optimised and still does not rank — reads the SERP backwards to find the page-type mismatch |

## Design

| Skill | Reach for it when |
|---|---|
| `frontend-design` | Giving a new interface an aesthetic direction that does not read as templated |
| `design-craft` | Setting or checking the quality bar — typography, colour, animation discipline, state coverage, accessibility floor |
| `brand-guidelines` | A defined brand's colours and type must be applied |
| `theme-factory` | You want a coherent theme fast, for a landing page or an artifact |
| `canvas-design` | Original visual art is needed as PNG or PDF |

## Content

| Skill | Reach for it when |
|---|---|
| `seo-content-brief` | **Before writing** — competitive brief with per-section word counts and keyword guidance |
| `seo-content` | After writing — E-E-A-T, depth, readability, thin-content risk, AI citation readiness |

## Technical SEO

| Skill | Reach for it when |
|---|---|
| `seo-technical` | Crawlability, indexability, security headers, URL structure, mobile, CWV, JS rendering |
| `seo-schema` | Detecting, validating or generating JSON-LD |
| `seo-sitemap` | Validating or generating an XML sitemap |
| `seo-hreflang` | The site has more than one language or region — non-optional then |
| `seo-images` | Alt text, formats, sizes, responsive images, lazy loading, CLS |
| `seo-image-gen` | Auditing OG/social images and planning what needs generating |

## GEO — being cited by AI answers

| Skill | Reach for it when |
|---|---|
| `seo-geo` | AI Overviews, ChatGPT search, Perplexity — crawler access, passage citability, brand signals |
| `seo-flow` | You want the evidence-led Find → Leverage → Optimize → Win prompts for a stage |

## Local

| Skill | Reach for it when |
|---|---|
| `seo-local` | Physical premises or a service area — GBP, NAP, citations, reviews, local schema |
| `seo-maps` | Geo-grid rank tracking, GBP audit, review intelligence, competitor radius |

## E-commerce

| Skill | Reach for it when |
|---|---|
| `seo-ecommerce` | Product schema, Shopping visibility, marketplace gaps, pricing comparison |

## Audit and regression

| Skill | Reach for it when |
|---|---|
| `seo-audit` | Whole-site audit with a health score, delegating to specialists |
| `seo-page` | Deep analysis of one page |
| `seo-drift` | **Baseline before a change, diff after** — catches the regressions nobody would look for |

## Live data ⚡

| Skill | Reach for it when |
|---|---|
| `seo-google` ⚡ | Search Console positions and indexation, PageSpeed, CrUX field data, GA4 organic |
| `seo-dataforseo` ⚡ | Live SERPs, keyword volume, backlinks, AI-visibility checks |
| `seo-backlinks` ⚡ | Referring domains, anchor distribution, toxic links, competitor gaps |

On a site that launched last week these return nothing useful. Connect them when
there is traffic to reason about.

## Build and verify

| Skill | Reach for it when |
|---|---|
| `webapp-testing` | Driving the local app with Playwright — verify behaviour, screenshot, read browser logs |

## Three rules

1. **Invoke before the work, not after.** A skill loaded after the page is
   written becomes a review; loaded before, it becomes a method.
2. **One skill per question.** Four at once produces an answer that hedges across
   all four.
3. **A skill is not a subagent.** A skill loads a procedure into the current turn;
   a subagent runs elsewhere with its own context. Skill for *how*, subagent for
   *who*.
