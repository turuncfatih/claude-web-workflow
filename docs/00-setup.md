# 0. Setup — from an empty folder

What has to exist before the first useful prompt. Fifteen minutes, once per
machine, then once more per project.

## Per machine

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude          # first run walks through auth
```

### Global settings

`~/.claude/settings.json` decides which model drives your main session and how
hard it thinks. This is the single highest-leverage file in the setup:

```json
{
  "model": "opus[1m]",
  "modelSettings": {
    "claude-opus-5": { "effortLevel": "high" }
  },
  "theme": "dark"
}
```

Why the strongest model in the **main session** specifically: the main session is
where planning, routing and judgment happen, and a wrong plan wastes every
subagent that runs after it. The subagents are where you economise — see
[chapter 1](01-model-division-of-labour.md).

### Where things live

```
~/.claude/
  settings.json     model, effort, plugins, theme
  agents/*.md       agent definitions available to every project
  skills/           installed skills
  plugins/          installed plugins
```

Project-local equivalents override the global ones:

```
<project>/
  CLAUDE.md              project context, loaded into every session
  .claude/
    agents/*.md          project-specific roles
    settings.json        project settings
    settings.local.json  machine-specific, gitignored
```

## Per project

### CLAUDE.md — the file that does the most work

Everything Claude should know before it reads a single source file. Keep it
short; anything vague in here becomes vague output.

```markdown
# <site name>

Static marketing site for <business>. Deployed to <host> on push to main.

## Stack
- Astro 5, `output: 'static'`, `trailingSlash: 'never'`
- Zero runtime JavaScript target; small inline scripts only where unavoidable
- Languages: TR at root, `/en` and `/ru` prefixed

## Single sources of truth
- `src/lib/site.ts`   — address, phone, hours, team, social. Never inline these.
- `src/lib/schema.ts` — JSON-LD builders. Pages pass `schemas={[...]}`.

## Invariants
1. Check `site.ts` before adding any constant.
2. Title ≤ 60 characters, meta description ≤ 160, exactly one `<h1>` per page.
3. No delivery-time promises. Use written scope and fixed-price language.
4. No invented metrics. Percentages, ratings and customer counts need a source.

## Output discipline
1. Create no file the task did not ask for. No SUMMARY.md, NOTES.md, CHANGES.md.
2. Comments explain why, never what. Rename instead of explaining.
3. No commented-out code. Git remembers it.
4. Report in one or two sentences. The diff is the summary.

## Commands
- `npx astro build`  — must pass with zero errors before anything ships
```

The **output discipline** block is there because an agent left alone optimises
for *looking* diligent: a summary file after every task, a comment on every line,
a bulleted recap at the end of every reply. None of it was asked for, and all of
it rots — a stale summary actively misleads the next reader, and a comment
restating code becomes a lie the first time the code changes.

> **The diff is the report. The code is the documentation. Everything else has to
> earn its place.**

Treat a `SUMMARY.md` appearing in a diff as a review finding, the same category
as a hardcoded colour. The full argument is
[anti-pattern 12 in the playbook](https://github.com/turuncfatih/agent-team-playbook/blob/main/docs/07-anti-patterns.md).

The four invariants above are worth copying almost verbatim. Numbers 3 and 4
prevent the two failure modes that make a site read as machine-written, and no
model will apply them unless you write them down.

### The first three questions to answer

Before any code, and the answers belong in `CLAUDE.md`:

| Question | Why it has to be first |
|---|---|
| **What is this page's single goal?** | A page with two goals gets a hedged design and hedged copy |
| **Who reads it, and what do they already know?** | Decides vocabulary, length and what can be assumed |
| **What may never be claimed without evidence?** | The boundary that stops fabricated social proof |

## Verifying the setup

```bash
claude
> /agents      # the roles available here
> /skills      # what can be invoked
> /mcp         # connected servers — see chapter 3
```

If `/agents` is empty, nothing is wrong yet — [chapter 2](02-skills-map.md) and
the [agents/](../agents/) directory in this repo are where the roles come from.
