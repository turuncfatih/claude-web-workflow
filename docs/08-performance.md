# 8. Performance

For a static marketing site, performance is mostly a matter of not doing things.
The wins are structural and they are decided early — by the time you are
profiling, the expensive mistakes are already in the build.

## The target

| Metric | What it measures | Good | Usual cause when bad |
|---|---|---|---|
| **LCP** | When the largest visible element finishes painting | < 2.5 s | An unoptimised hero image, or a render-blocking font |
| **INP** | How fast the page responds to interaction | < 200 ms | JavaScript that did not need to exist |
| **CLS** | How much the layout jumps while loading | < 0.1 | Images without dimensions; fonts swapping metrics |

These are field metrics. Lighthouse in your browser is a lab number on a fast
machine on a fast connection — useful for catching regressions, useless as a
verdict. Real data comes from CrUX via `seo-google`.

## The structural decisions

### 1. Zero runtime JavaScript, as a target

A marketing site is documents. Documents do not need a framework at runtime.

```js
// astro.config.mjs
export default defineConfig({
  output: 'static',
  build: { format: 'file' },
});
```

Ship a small inline script for the one thing that genuinely needs it — a mobile
menu toggle, a form handler — and nothing else. INP is free when there is no
JavaScript to block the main thread.

This single decision does more for performance than every optimisation below
combined, and it can only be made at the start.

### 2. Self-host fonts, subset, preload one

Third-party font hosting costs a DNS lookup, a connection and a round trip
before any text can paint.

```html
<link rel="preload" href="/fonts/inter-var-latin.woff2" as="font"
      type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var-latin.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;   /* text is visible immediately, in the fallback */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC;
}
```

Three rules:

- **Subset to the characters you use.** A Latin subset is a fraction of the full
  file. If the site is Turkish, include `U+011E-011F, U+0130-0131, U+015E-015F`
  — missing those is a visible bug, not an optimisation.
- **`font-display: swap`**, always. Invisible text is worse than fallback text.
- **Preload only the one file used above the fold.** Preloading four weights
  makes the first paint slower, not faster.

Pick a fallback whose metrics are close to the webfont, or the swap causes CLS.

### 3. Images: the LCP element is different from the rest

```html
<!-- Hero: the LCP element. Eager, prioritised, never lazy. -->
<img src="/hero.avif" width="1200" height="630" alt="…"
     loading="eager" fetchpriority="high">

<!-- Everything below the fold -->
<img src="/thing.avif" width="600" height="400" alt="…"
     loading="lazy" decoding="async">
```

| Rule | Why |
|---|---|
| **Always set `width` and `height`** | Missing dimensions is the single most common cause of CLS |
| **Never lazy-load the LCP image** | `loading="lazy"` on the hero delays the exact thing being measured |
| **AVIF or WebP, with a fallback** | Typically a fraction of the JPEG weight |
| **Export at the largest rendered size** | A 4000px image in a 600px slot is wasted bytes |
| **`srcset` for anything that reflows** | Phones should not download desktop images |

`seo-images` audits all of this.

### 4. CSS that does not block

Inline the critical CSS for above-the-fold content; load the rest normally. On a
small static site the whole stylesheet is often small enough to inline, which
removes a round trip entirely.

Never `@import` in CSS — it serialises requests that could have been parallel.

### 5. Third-party scripts: each one is a decision

Every embedded script is a DNS lookup, a connection, execution time, a privacy
question and a thing that can break independently of your deploy. Analytics, a
chat widget, a map, a font host, a tag manager: that is five, and five is a slow
site.

| Instead of | Use |
|---|---|
| Google Analytics | Cloudflare Web Analytics — no cookies, no banner, no client JS |
| An embedded map | A static map image linking to the map |
| A chat widget | A phone number and a form |
| Google Fonts | Self-hosted, subset |

Each removal is worth more than any amount of tuning.

## Measuring

```
/seo-technical https://example.com     # CWV, rendering, headers, crawlability
/seo-google                            # CrUX field data — real users, 28-day window
/seo-performance                        # lab measurement for regression checking
```

The order matters: field data tells you whether there is a problem; lab data
tells you what changed.

## What not to bother with

- **Micro-optimising a site that ships no JavaScript.** The budget is already spent well.
- **Chasing a Lighthouse 100.** The last few points usually cost readability or accessibility.
- **A CDN in front of a CDN.** Cloudflare Pages is already the CDN — see [chapter 11](11-shipping-cloudflare.md).
