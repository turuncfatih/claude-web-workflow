# 11. Shipping on Cloudflare Pages

A static site, deployed by `git push`, on a global CDN, with TLS and DDoS
mitigation included. There is no server to run, and the parts that would
otherwise be server configuration live in two files in the repository — which
means they are reviewable in a diff like everything else.

## Connecting the repository

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**
2. Pick the repository, pick the production branch (`main`)
3. Build settings:

| Setting | Astro |
|---|---|
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node version | `NODE_VERSION` env var, e.g. `22` |

Every push to `main` deploys to production. **Every other branch gets its own
preview URL**, which is the single most useful property of this setup: a real
URL, on real infrastructure, before anything is merged.

## Custom domain

Pages → your project → **Custom domains** → add the apex and `www`.

If the domain's DNS is already on Cloudflare, the records are created for you.
If not, move nameservers first — half-configured DNS is a bad afternoon.

Keep one canonical host and redirect the other. Both answering is a duplicate
content problem and a cookie-scope problem at once.

## `public/_headers`

Anything in `public/` is copied to the output root, so this file ships with the
site and is reviewed in the diff:

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'

# Fingerprinted assets never change under the same name.
/_astro/*
  Cache-Control: public, max-age=31536000, immutable

/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=2592000
```

The caching rule that matters: **fingerprinted assets immutable, HTML not.** An
HTML file cached for a year is a site you cannot fix. Astro fingerprints
`/_astro/*`, so those are safe to pin forever; leave HTML on the default so a
deploy is visible immediately.

## `public/_redirects`

```
# Old URLs keep their equity. 301, not 302.
/eski-sayfa            /yeni-sayfa            301
/blog/*                /rehberler/:splat      301

# One canonical host.
https://www.example.com/*  https://example.com/:splat  301

/404                   /404.html              404
```

Rules are evaluated top to bottom; the first match wins. Redirect chains cost
both crawl budget and time, so redirect to the final destination rather than
through two hops.

## Security settings worth turning on

| Setting | Why |
|---|---|
| **Always Use HTTPS** | Redirects http → https at the edge |
| **Automatic HTTPS Rewrites** | Fixes mixed content without touching the source |
| **Bot Fight Mode** | Free, and enough for a marketing site |
| **Minimum TLS 1.2** | Drops obsolete clients |
| **Access on preview deployments** | Otherwise every branch is publicly readable — including work in progress |

That last row is the one people miss. Preview URLs are public by default and
they are indexable; a staging page ranking for your brand is an unpleasant way
to find that out.

## Analytics without a cookie banner

Cloudflare **Web Analytics** is server-side, cookieless, and needs no consent
banner in most jurisdictions. It replaces the single heaviest third-party script
on a typical marketing site and removes the banner that hurts LCP on every first
visit.

Enable it in Pages → your project → Analytics.

## Performance that comes for free

Already handled by the platform, so do not rebuild it:

- Global CDN — assets served near the visitor
- Brotli compression
- HTTP/3
- TLS termination at the edge, certificates renewed automatically

What is still yours: [chapter 8](08-performance.md). The CDN makes a slow page
arrive quickly; it does not make it fast.

## After the deploy

The build passing is not the same as the site working.

```bash
# Headers as actually served
curl -sI https://example.com | grep -iE "content-security|strict-transport|x-frame|cf-cache-status"

# The canonical redirect really redirects
curl -sI https://www.example.com | head -3

# Sitemap and robots are reachable
curl -s https://example.com/sitemap-index.xml | head
curl -s https://example.com/robots.txt
```

Then a browser pass over the **live** URL — render at three breakpoints, console
clean, the primary action works, the form submits. See
[chapter 10](10-verification.md).

Finally, once:

- Submit the sitemap in Search Console
- Request indexing for the handful of pages that matter
- Capture an `seo-drift` baseline, so the next deploy is a diff

## The whole shipping loop

```
git push origin main
      ▼
Cloudflare builds and deploys        (~1 min)
      ▼
curl checks: headers, redirects, sitemap
      ▼
browser pass on the live URL
      ▼
/seo-drift          did anything change that was not meant to?
```

Four steps, and only the first is automatic. The other three are why the site
stays correct after the tenth deploy rather than only after the first.
