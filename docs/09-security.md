# 9. Security

A static marketing site has a small attack surface, and that is exactly why the
failures are embarrassing when they happen: they are all avoidable, and they are
all in the same five places.

This is a role, not a checklist someone remembers. `security-reviewer` is the
only agent in this workflow with a **judgment veto** — it can stop a release,
with evidence. Its definition is in [agents/](../agents/).

## The five places

### 1. Secrets in the bundle

A static site is shipped to the visitor in full. Anything in the build output is
public — there is no server to hide behind.

```bash
# What the reviewer actually runs
grep -rEn "(api[_-]?key|secret|token|password|bearer|AIza|sk-|ghp_)" dist/ \
  --include='*.js' --include='*.html' --include='*.json'

# Source maps leak your source. Ship them only if you mean to.
find dist -name '*.map'
```

The rule: if a key must stay secret, it cannot be in a static site at all. It
belongs behind a function or a form endpoint.

### 2. Forms

The one place a marketing site takes input.

| Check | Why |
|---|---|
| Where does it POST? | A third-party endpoint is a data processor — know which, and say so |
| Spam protection | A honeypot field beats a CAPTCHA for a small site: no third-party JS, no accessibility cost |
| What is collected | Collect the minimum. A phone number you do not need is a liability you do |
| Is it announced? | A privacy notice on the page that collects, not only in a footer link |
| `autocomplete` | Correct tokens on name, email, tel — an accessibility and usability requirement |

### 3. Headers

On Cloudflare Pages, `public/_headers` — deployed with the site, reviewable in
the diff:

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

Two notes worth having:

- **`Content-Security-Policy` is the one that matters**, and the one people skip
  because it breaks things. On a zero-JS static site it is nearly free — there
  are no inline scripts to allow. Add it early, while the site is small.
- **`Strict-Transport-Security` with `preload`** is effectively irreversible.
  Add `preload` only when you are sure every subdomain will be HTTPS forever.

Verify what is actually served, not what you think you configured:

```bash
curl -sI https://example.com | grep -iE "content-security|strict-transport|x-frame|referrer|permissions"
```

### 4. Third-party scripts

Every embedded script runs with the full privileges of your page. It can read
the DOM, read forms as they are typed, and change independently of your deploy.

For each one the reviewer asks: **what does it do, who owns it, what does it
receive, and what breaks if it disappears?** A script that cannot answer all four
should not ship. This is a security question and a performance question and a
privacy question at once, which is why [chapter 8](08-performance.md) reaches the
same conclusion from the other direction.

### 5. Exposure

```bash
# Anything that should not be in the output
find dist -name '.env*' -o -name '*.bak' -o -name '.git*' -o -name '*.sql'

# Is the admin/staging/preview path indexable?
grep -r "noindex" dist/ | head
```

Also: an email address in plain text in the markup gets scraped. A form or an
obfuscated `mailto` is not security, but it is hygiene.

## What the reviewer may and may not block on

Because a veto that fires on everything gets ignored:

| May block | May not block |
|---|---|
| A secret in the build output | A missing header that is nice to have |
| A form posting somewhere undeclared | Dependency versions that are merely not latest |
| No HTTPS, or a broken certificate | Code style or file layout |
| An unannounced third-party script receiving user input | A theoretical risk with no reachable path |
| Personal data collected with no notice | Preferences about framework choice |

Everything in the right column is a **finding** — recorded, scheduled, not a
release blocker. The distinction is what keeps the veto credible.

## Cloudflare's share of this

Some of it is not your code's job at all — see
[chapter 11](11-shipping-cloudflare.md):

- TLS, HSTS and automatic certificate renewal
- DDoS mitigation, on by default
- Bot Fight Mode
- WAF rules, if the site has any dynamic surface at all
- Access control on preview deployments, so staging is not public

## The habit

```
/security-review        # before any release that touches forms, headers or scripts
```

And once, after the first deploy, against the **live URL** rather than the
build. What is configured and what is served are different things, and only one
of them matters.
