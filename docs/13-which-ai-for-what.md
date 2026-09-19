# 13. Which AI for what

This chapter dates faster than the rest of the repository. Capabilities move
every few months, so what follows is organised by **task shape** rather than by
model name — the shapes are stable even when the rankings are not.

## The principle

> **Choose by where the work lives and what shape it has, not by a benchmark.**

The single biggest factor is not capability, it is **integration**. A model with
your repository, your `CLAUDE.md`, your agents and your tools will beat a
marginally stronger model that has none of those and has to be told everything by
hand. Context does not transfer between tools; every switch costs you all of it.

So the question is never "which is best?" but "**which one already has what this
task needs?**"

## The map

### Work that lives in the repository — Claude Code

Multi-file edits, agent teams, tool use, running builds, reading test output,
sustained work across a long session. This is the whole of chapters 0–11: it has
your files, your conventions and your roles.

Everything below is something you reach *out* to, for a specific reason, and come
back from.

### Image generation — an image tool, not a coding tool

Icons you should not generate at all ([chapter 6](06-visual-assets.md)) — use a
real icon library. What an image tool is for: **illustration, avatars, textures,
social preview art, section backgrounds.**

ChatGPT's image generation is the common choice and it is strong at this. The
workflow that matters is not the generator, it is the loop: locked style anchor,
generate the whole set in one batch, compare side by side, regenerate only the
outliers. Chapter 6 has it in full.

### UI layout exploration — Stitch

Screens to react against, so you are not choosing the first layout language
happened to describe. [Chapter 3](03-mcp-servers.md) has the connection,
[chapter 4](04-design-flow.md) the flow.

### Very large ingestion — a long-context model

Reading a 300-page brand guideline, a full competitor site crawl, a year of
support tickets to find what customers actually ask. Gemini's long context is the
usual pick, and the Google ecosystem integration matters if the data is already
in Drive or Sheets.

The output you want from this is **a summary you bring back**, not decisions made
over there. Three pages of extracted constraints beat a model that read everything
and has no access to your repo.

### Bulk, cheap, mechanical volume — a low-cost model

Classifying two thousand URLs, extracting a field from a thousand pages,
normalising a product feed. DeepSeek and similar low-cost models are genuinely
well-suited here, and open weights mean you can self-host if the data should not
leave your machine.

Two caveats worth stating plainly: if the task is fully deterministic it is a
**script**, not a model call; and a cheap model on a task with no verification
step is how bad data enters quietly.

### A second opinion — deliberately a different model

The most valuable cross-model use, and the least obvious.

A model reviewing its own output is the same structural failure as an agent
approving its own work ([chapter 10](10-verification.md)). It shares the blind
spot that produced the problem. So when the stakes justify it:

```
Claude writes the copy  ──►  a different model reviews it cold,
                             with no knowledge of the brief
```

Ask the reviewer the sharp question, not a polite one:

> "This is marketing copy for a locksmith. Which sentences say nothing? Which
> claims would a competitor also make? What reads as machine-written?"

The second model has no investment in the text and no memory of why each choice
was made. That is exactly what makes it useful — and it is the same reason
`design-critic` may not be the agent that designed the page.

Worth doing for: a flagship page's hero copy, a pricing page, anything legal or
medical, anything a business will be held to.

## The table

| Task | Where | Why |
|---|---|---|
| Repo work, agents, builds, multi-file edits | **Claude Code** | It has your files, roles and tools |
| Planning, architecture, final judgment | **Claude, Opus tier** | Irreversible decisions ([chapter 1](01-model-division-of-labour.md)) |
| Implementation from a precise spec | **Claude, Sonnet tier** | Execution, not invention |
| Narrating checker output | **Claude, Haiku tier** | Do not pay for thinking that is not happening |
| UI layout directions | **Stitch** | Something to react against |
| Illustration, avatars, OG art | **An image model** | Claude does not generate images |
| UI icons | **An icon library** | Consistency by construction, not by luck |
| Reading a very large corpus | **A long-context model** | Bring back a summary, not decisions |
| Bulk classification at volume | **A low-cost model, or a script** | Volume is a cost problem, not a capability one |
| Cold review of finished copy | **Any model that did not write it** | No shared blind spot |
| Deciding between design directions | **An Artifact** ([chapter 12](12-artifacts-for-design-review.md)) | A link beats a meeting |

## The costs nobody counts

Every tool you add to the workflow costs something that is not on the invoice:

| Cost | What it looks like |
|---|---|
| **Context loss** | Explaining the project again, in every tool, every time |
| **Drift** | The style anchor in one tool, the tokens in another, slowly disagreeing |
| **Provenance** | Six weeks later, nobody knows which tool produced which asset |
| **Data exposure** | What you paste into a consumer chat is governed differently from an API call. Client data, unreleased prices, anything under NDA — check before pasting, not after |

This is the same argument as MCP servers in [chapter 3](03-mcp-servers.md) and
third-party scripts in [chapter 9](09-security.md), and it lands in the same
place: **connect what you use, drop what you do not.**

## The honest summary

For a static marketing site, you need two tools and one connector:

1. **Claude Code** — planning, code, agents, audits, verification, shipping
2. **An image tool** — illustration and avatars, in a locked style
3. **Stitch** — layout directions to react against

Everything else on this page is a *specific answer to a specific problem*: a
corpus too large, a volume too expensive, a page too important to review itself.
Reach for them then. Adding them because they exist is how a workflow becomes a
collection of tools that each know a third of the project.
