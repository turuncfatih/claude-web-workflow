# Claude Web Workflow

**Building a website with Claude, end to end: which model does what, which skills to invoke when, which MCP servers to connect — and the measures that stop the result looking machine-made.**

[![check](https://github.com/turuncfatih/claude-web-workflow/actions/workflows/check.yml/badge.svg)](https://github.com/turuncfatih/claude-web-workflow/actions/workflows/check.yml)
[![licence](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)

🇬🇧 English · [🇹🇷 Türkçe](README.tr.md)

Not "here is a prompt that makes a landing page". This is the whole pipeline from
an empty folder to a live, fast, secure, findable site — the division of labour
between Opus, Sonnet and Haiku, the skills at each phase, Stitch for design,
Artifacts for deciding, a second model for cold review, and the roles that check
the result before anyone sees it.

```
14 chapters · 8 agent definitions · 1 working script · 1 end-to-end walkthrough
```

> **Companion repositories.**
> [Claude Mobile Workflow](https://github.com/turuncfatih/claude-mobile-workflow) — the same workflow for a React Native app.
> [Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook) — the general method for designing agent teams.
> [AgentForge](https://github.com/turuncfatih/agentforge) — the orchestration machinery, implemented in .NET.

---

## Why this exists

### The problem is not that building a website is hard

It stopped being hard. Anyone can now describe a landing page and have working
HTML in ten minutes. That is genuinely new, and it is also the problem: **the
bottleneck moved from producing to judging.**

What comes out of that ten minutes is usually *correct*. It builds. It is
responsive. It has headings and alt text. And it is worth very little, because:

| What you get by default | Why it costs you |
|---|---|
| A page that looks like every other generated page | A visitor decides in two seconds whether anyone cared. Generic design reads as a business that does not |
| Copy that could belong to any company | "Quality service, tailored to your needs" says nothing a competitor would not also say |
| Invented numbers and testimonials | A fabricated statistic on a business's website is not a style problem |
| Nobody checked whether it renders | The build passed. That is not the same as the page working |
| No structured data, no crawl path | Correct and invisible |
| A 6 MB hero image and three tracking scripts | Slow on the connection your customers actually have |

None of these are capability failures. A model can write good copy, design a
considered page and produce valid schema. **They are process failures** — there
was no step that caught anything, because one agent produced the work and the
same agent declared it finished.

### Why a process, and not just a better prompt

A better prompt improves the first draft. It does not create a feedback loop.

The three things that actually change the result are structural, not textual:

1. **Someone other than the author reviews it.** An agent reviewing its own
   output carries the blind spot that produced the problem. This is the same
   reason you do not merge your own pull request.
2. **Something can say no.** A review that cannot stop a release is a comment.
   One role holds a veto, on facts — it built, or it did not.
3. **The deterministic parts are scripts, not judgment.** Counting characters,
   validating JSON-LD, finding a forbidden phrase — a regular expression does
   that instantly, for free, identically every time. Asking a model to do it is
   slower, costs money, and occasionally disagrees with itself.

That is the whole shape of this repository. Everything else is detail.

### Why these tools, specifically

Each choice here is defended in its chapter, but the short version:

| Choice | Reason |
|---|---|
| **A static site** | A marketing site is documents. Documents do not need a framework at runtime, and zero JavaScript makes the performance problem disappear rather than get tuned. Nothing here depends on Astro specifically |
| **Cloudflare Pages** | CDN, TLS, DDoS mitigation and preview URLs are solved problems. `_headers` and `_redirects` live in the repo, so what would otherwise be server configuration is reviewable in a diff |
| **Opus in the main session** | A wrong plan wastes every step after it. That is the most irreversible decision in the project and the cheapest to get right |
| **Sonnet in the subagents** | With a precise spec, implementation is execution. Paying frontier prices for it buys nothing |
| **An image model for illustration, an icon library for icons** | Generated icon sets drift in stroke weight and style, and mixed icons are the loudest sign nobody designed the page |
| **Stitch for layout** | Describing a layout in prose gets you the layout prose describes most easily — which is why generated pages look alike. Reacting to three options breaks that |

### What this actually gives you

Not faster output. You can already get fast output.

- A page a visitor cannot swap another business's name into
- Copy where every claim is one a competitor might genuinely dispute
- A site that was **verified to render** before anyone called it done
- Structured data and a crawl path, so the work is findable
- Security headers and a CSP, added while the site was small enough for it to be free
- A cost you can explain, because the spending follows the irreversibility of the decision rather than the prestige of the task

If you already have a review step, a verifier and a cost model, you will find
little here. If your current process is "generate, look at it, ship", this is the
missing half.

---

## The one thing to take away

A generated site is usually *correct*. It builds, it is responsive, it has
headings — and a visitor can tell in two seconds that nobody decided anything.
That recognition is a trust problem, and correctness does not fix it.

So the whole workflow is built around one question:

> **Would this page still work if you swapped in a different business's name?**

If yes, nothing has been decided yet. [Chapter 5](docs/05-not-looking-ai-made.md)
is the catalogue of tells, the countermeasures, and the roles that enforce them.

---

## Which model does what

| Where | Model | What belongs there |
|---|---|---|
| **Main session** | Opus, high effort | Planning, routing, design direction, final judgment |
| **Subagents** | Sonnet | Implementation, copy, verification — execution against a spec |
| **Narrow, mechanical** | Haiku | Classification, extraction, narrating tool output |
| **Fully deterministic** | *a script* | Counting, validating, diffing — not a model at all |

The rule underneath:

> **Reasoning scales with the irreversibility of the decision, not with the
> prestige of the task.**

The developer agent is **not** your top tier. With a precise spec, implementation
is execution — the irreversible thinking already happened upstream. If your
developer needs Opus, the usual cause is a thin spec, and upgrading the model
hides it. [Chapter 1](docs/01-model-division-of-labour.md).

---

## Which tool for what

| Task | Where | Why |
|---|---|---|
| Repo work, agents, builds | **Claude Code** | It has your files, roles and tools |
| UI layout directions | **Stitch** (MCP) | Something to react against, so you skip the median layout |
| Deciding between directions | **An Artifact** | Three directions, one switcher, a link you can send |
| Illustration, avatars, OG art | **An image model** | Claude does not generate images |
| UI icons | **An icon library** | Generated icon sets drift — and mixed icons are a loud tell |
| Reading a very large corpus | **A long-context model** | Bring back a summary, not decisions |
| Bulk classification | **A low-cost model, or a script** | Volume is a cost problem, not a capability one |
| Cold review of finished copy | **Any model that did not write it** | No shared blind spot |

That last row is the one people skip. A model reviewing its own output has the
same blind spot that produced the problem — structurally identical to an agent
approving its own work. [Chapter 13](docs/13-which-ai-for-what.md).

---

## The team

Eight roles, plus the main session. **One writer. Two vetoes, different in kind.**

| Role | Artifact | Writes? | Model | Veto |
|---|---|:---:|---|:---:|
| *main session* | The plan, the final call | ✗ | **Opus** | — |
| `designer` | Design spec | ✗ | **Opus** | ✗ |
| `content-writer` | Page copy | ✗ | Sonnet | ✗ |
| `web-dev` | Working pages | ✅ | Sonnet | ✗ |
| `design-critic` | "This looks like a template" | ✗ | Sonnet | ✗ |
| `slop-auditor` | "This reads like a machine wrote it" | ✗ | Sonnet | ✗ |
| `seo-auditor` | "Nobody will find this" | ✗ | Haiku | ✗ |
| `security-reviewer` | "This is unsafe to ship" | ✗ | **Opus** | ✅ judgment |
| `release-verifier` | "This does not run" | ✗ | Sonnet | ✅ fact |

```
main session plans
   ├─ designer ───────┐   (parallel)
   └─ content-writer ─┤
                      ▼
                 web-dev  ← the only role that touches the repo
                      ▼
       [ scripts: build · slop_check.py ]
                      ▼
            release-verifier   ── FACT VETO, alone and first
                      ▼
   ┌──────────┬──────────────┬─────────────────┐   (parallel)
   ▼          ▼              ▼                 ▼
design-critic  slop-auditor  seo-auditor  security-reviewer
                                          ── JUDGMENT VETO
                      ▼
      main session: ship · revise · escalate
```

Eight exceeds the playbook's own guideline of three to six, so
[agents/README.md](agents/README.md) argues it explicitly — including the seven
roles that were merged away and why these four critics stayed separate.

---

## The slop check

A real script, no dependencies, in this repository:
[`scripts/slop_check.py`](scripts/slop_check.py)

```bash
python3 scripts/slop_check.py dist/
```

```
HIGH  (10)
  bad.html  [slop-phrase]        "in today's fast-paced world"
  bad.html  [slop-phrase]        "we've got you covered"
  bad.html  [unsourced-number]   "99%" in: We are trusted by thousands…
  bad.html  [structure]          2 <h1> elements, expected exactly 1
MEDIUM (2)
  bad.html  [structure]          title is 65 chars (max 60)
LOW   (1)
  bad.html  [uniform-rhythm]     5 paragraphs, length spread 0.22 — too even
```

It exits non-zero, so it belongs in CI. It checks forbidden phrases (English and
Turkish), hedging density, the three-adjective reflex, unsourced numbers,
paragraph-length uniformity and structural SEO.

**Its lists are meant to grow.** Every tell that gets past you becomes a line in
the script, and then it never gets past you again. What survives the script goes
to `slop-auditor`, which applies the tests a regex cannot: whether a claim is
specific, and whether a competitor could dispute it.

---

## Chapters

| # | Chapter | |
|---|---|---|
| 0 | [Setup](docs/00-setup.md) | From an empty folder. `CLAUDE.md`, the file that does the most work |
| 1 | [Which model does what](docs/01-model-division-of-labour.md) | Opus / Sonnet / Haiku, by phase, with the cost shape |
| 2 | [The skills map](docs/02-skills-map.md) | Which skill at which phase |
| 3 | [MCP servers](docs/03-mcp-servers.md) | Stitch, browser automation, hosting — and what not to connect |
| 4 | [The design flow](docs/04-design-flow.md) | Brief → three directions → react → spec |
| 5 | [**Not looking machine-made**](docs/05-not-looking-ai-made.md) | ★ The tells, the countermeasures, the roles that enforce them |
| 6 | [Visual assets](docs/06-visual-assets.md) | Icons, avatars, the locked style anchor, the revision loop |
| 7 | [SEO and GEO](docs/07-seo-geo-flow.md) | Ranking pages and being cited in answers |
| 8 | [Performance](docs/08-performance.md) | LCP / INP / CLS, and the decisions made at the start |
| 9 | [Security](docs/09-security.md) | Secrets, forms, headers, third-party scripts |
| 10 | [Verification](docs/10-verification.md) | Scripts first, agents second. Two vetoes, not three |
| 11 | [Shipping on Cloudflare](docs/11-shipping-cloudflare.md) | Pages, `_headers`, `_redirects`, caching, WAF |
| 12 | [Artifacts for design review](docs/12-artifacts-for-design-review.md) | Three directions, one switcher, a link instead of a meeting |
| 13 | [Which AI for what](docs/13-which-ai-for-what.md) | Claude, image models, long-context, low-cost — by task shape |

**Start with 5 and 1.** Then the [walkthrough](walkthrough/).

---

## Contents

```
docs/             14 chapters
agents/           8 role definitions, ready to copy into .claude/agents/
walkthrough/      empty folder → live site, with the actual commands
reference/
  skills-catalogue.md   every skill, one line each, by phase
  prompts.md            the handful where wording changes the output
scripts/
  slop_check.py         mechanical detection of machine-written copy
```

---

## Using it

```bash
git clone <repo-url> && cd claude-web-workflow

# the team
cp agents/*.md ~/.claude/agents/

# the check
cp scripts/slop_check.py <your-project>/scripts/

# the design MCP server
claude mcp add --transport http stitch https://stitch.googleapis.com/mcp
```

Then read the [walkthrough](walkthrough/) and follow it once.

The specifics here are a static Astro site on Cloudflare Pages. **The roles and
the sequence transfer; the stack details do not.** Rewrite `CLAUDE.md` for yours
and keep the shape.

---

**Licence** · MIT — copy the agents, copy the script, copy the method.
