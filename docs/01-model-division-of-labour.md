# 1. Which model does what

The question everyone asks first, and the one with a short answer:

> **Opus plans and judges. Sonnet builds and checks. Haiku narrates tool output.**

The reason is not that Opus is "better". It is that the cost of a mistake is
wildly different in each of those jobs, and spending should follow that
difference rather than follow prestige.

## The rule

> **Reasoning scales with the irreversibility of the decision, not with the
> prestige of the task.**

A wrong plan wastes every step after it. A wrong paragraph is rewritten in ten
seconds. Those two facts should decide your spending — and in most setups they
do not, because the code feels like the important part.

## How it maps in practice

### Main session — Opus, high effort

The main session is your orchestrator. It reads the request, decides the shape
of the work, routes it, and judges what comes back.

```json
{ "model": "opus[1m]", "modelSettings": { "claude-opus-5": { "effortLevel": "high" } } }
```

What belongs here:

- Deciding what the site *is* — structure, page inventory, what each page is for
- Design direction and taste calls
- Choosing which agents and skills to invoke, and in what order
- Reviewing a subagent's output before accepting it
- Anything ambiguous, contradictory, or with no obvious right answer

### Subagents — Sonnet

Agent definitions pin their own model, which is how you economise without
downgrading your judgment:

```markdown
---
name: web-dev
description: Writes the site code. Pages, components, content collections, schema, styles, routing.
model: sonnet
maxTurns: 40
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

What belongs here:

- Implementing from a spec that is already precise
- Writing content from a brief that is already decided
- Running audits and reporting what the tools found
- Build, verify, report

`maxTurns` matters more than it looks. It is a hard ceiling on a runaway loop,
and a subagent that hits it is telling you the task was underspecified.

### Narrow, mechanical work — Haiku

Classification into a fixed set of labels, extraction into a known schema,
formatting, and reading a checker's output to report it. If the model is a
narrator rather than a thinker, do not pay for thinking.

> And if the work is fully deterministic — counting, validating, diffing — it is
> a **script**, not an agent. See [chapter 10](10-verification.md).

## By phase

| Phase | Where it runs | Model | Why |
|---|---|---|---|
| Deciding page inventory and goals | main session | **Opus** | Wrong here wastes everything downstream |
| Design direction | main session | **Opus** | Taste is the deliverable; it degrades first on a cheaper model |
| Extracting tokens from a design | subagent | Sonnet | Mechanical once the direction is set |
| Writing components | `web-dev` | Sonnet | Execution against a precise spec |
| Writing page copy | `content-writer` | Sonnet | Cheap to correct; escalate for a flagship hero |
| Keyword and cluster planning | main session | **Opus** | Site architecture follows from it, and architecture is expensive to change |
| Content briefs | subagent | Sonnet | Derivation from a decided plan |
| Technical SEO audit | `seo-auditor` | Sonnet → Haiku | The checkers decide; the model reports |
| Schema generation | subagent | Sonnet | Well-specified output shape |
| Build + verify | `release-verifier` | Sonnet | Tool-heavy, but reading a failure is judgment |
| Reviewing everything before ship | main session | **Opus** | Last chance to catch a bad call |

Two things worth noticing.

**The developer is not your top tier.** With a precise design spec and a clear
CLAUDE.md, implementation is execution — the irreversible thinking already
happened upstream. If your developer agent needs Opus, the usual cause is a thin
spec, and upgrading the model hides the real problem.

**The auditor is your cheapest tier.** Its job is to run checkers and explain the
output. Paying frontier prices for narration is the most common waste in this
kind of setup.

## When to escalate mid-task

Tier is a default, not a life sentence. Move a task up when:

1. **The input is contradictory.** Cheap models paper over contradictions;
   expensive ones notice them.
2. **The same step failed twice.** A third identical attempt is waste. Change
   something — tier is the cheapest thing to change.
3. **The blast radius grew.** A component change that now touches the content
   model became less reversible than it started.
4. **A reviewer rejected a writer twice.** Either the spec is wrong or the tier
   is too low. One expensive opinion settles which.

Do it explicitly, so the cost is explainable afterwards.

## When to move down

Where most of the savings are, and where nobody looks:

- The task repeats with the same shape — the reasoning is in the prompt now, not
  in the model
- A script checks the output anyway, so a mistake is caught
- The role only narrates tool output
- A human is waiting, and latency matters more than nuance

## The cost shape

A typical page, built end to end:

| Work | Model | Share of spend |
|---|---|---|
| Planning and routing | Opus | ~20% |
| Design direction and review | Opus | ~25% |
| Implementation | Sonnet | ~30% |
| Content | Sonnet | ~15% |
| Audits and verification | Sonnet / Haiku | ~10% |

Running everything on Opus costs roughly **four to six times** this, and is
better in exactly two of those five rows.

But the number that dominates all of it is **rework**. One avoided rework round
pays for a dozen upgrades, so spend on the steps that *prevent* rework — the
plan and the review — before spending on the ones that do the work.

---

> The general version of this reasoning, independent of Claude and of websites,
> is in the [Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook).
