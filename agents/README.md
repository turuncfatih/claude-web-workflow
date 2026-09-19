# The team

Eight roles, plus the main session. Every definition follows the ten-field spec
from the [Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook),
so they can be read side by side.

| Role | Artifact | Writes? | Model | Veto |
|---|---|:---:|---|:---:|
| *main session* | The plan, and the final call | ✗ | **Opus**, high effort | — |
| [`designer`](designer.md) | Design spec | ✗ | **Opus** | ✗ |
| [`content-writer`](content-writer.md) | Page copy | ✗ | Sonnet | ✗ |
| [`web-dev`](web-dev.md) | Working pages | ✅ | Sonnet | ✗ |
| [`design-critic`](design-critic.md) | Visual findings | ✗ | Sonnet | ✗ |
| [`slop-auditor`](slop-auditor.md) | Copy findings | ✗ | Sonnet | ✗ |
| [`seo-auditor`](seo-auditor.md) | SEO findings | ✗ | Haiku → Sonnet | ✗ |
| [`security-reviewer`](security-reviewer.md) | Security findings | ✗ | **Opus** | ✅ judgment |
| [`release-verifier`](release-verifier.md) | Pass/fail report | ✗ | Sonnet | ✅ fact |

**One writer. Two vetoes, different in kind. Four critics that produce findings.**

## On team size — the honest version

The playbook says three to six roles, and that **seven or more is almost always
a bad cut**. This is eight. That deserves an argument rather than a shrug.

### The merges that were done

| Considered | Merged into | Why |
|---|---|---|
| `react-dev` + `css-dev` | `web-dev` | Same write permission, same artifact |
| `image-optimiser` | a build step | Deterministic |
| `deployer` | `git push` | Deterministic |
| `researcher` | the brief | Produced notes only one role read — that is a prompt section, not an artifact |
| `accessibility-reviewer` | `release-verifier`'s definition of done | Its checks are mechanical, and a third veto would deadlock the team |
| `performance-reviewer` | `release-verifier` + `seo-technical` | No distinct failure mode at this size |
| `schema-writer` | `web-dev` + the `seo-schema` skill | A skill, not a role |

### The four that survived as separate critics

`design-critic`, `slop-auditor`, `seo-auditor` and `security-reviewer` each
catch a **different failure**, which is the test that matters:

| Role | The failure it catches |
|---|---|
| `design-critic` | "This looks like a template" |
| `slop-auditor` | "This reads like a machine wrote it" |
| `seo-auditor` | "Nobody will find this" |
| `security-reviewer` | "This is unsafe to ship" |

The first two look adjacent, and merging them was genuinely considered. They stay
separate for the reason the playbook's chapter 2 gives: **they need wildly
different context.** One reads screenshots at three breakpoints; the other reads
prose and a script's output. A merged role would carry both contexts into every
invocation and be worse at each.

So: eight, knowingly, with the reasoning written down. If this team stops earning
it — if `seo-auditor` fires on 5% of tasks, or `design-critic` never finds
anything — the answer is to delete a role, not to defend the number.

## The flow

```
main session (Opus) plans
   ├─ designer ───────┐   (parallel — neither reads the other)
   └─ content-writer ─┤
                      ▼
                 web-dev  ← the only role that touches the repo
                      ▼
          [ scripts: build · slop_check.py ]
                      ▼
            release-verifier   ── FACT VETO
                      ▼
   ┌──────────┬───────────────┬──────────────────┐   (parallel)
   ▼          ▼               ▼                  ▼
design-critic  slop-auditor  seo-auditor  security-reviewer
  findings      findings      findings    ── JUDGMENT VETO
   └──────────┴───────────────┴──────────────────┘
                      ▼
      main session (Opus): ship · revise · escalate
```

`release-verifier` runs alone and first. Critiquing a page that does not render
is wasted work.

## Installing them

```bash
cp agents/*.md ~/.claude/agents/          # available everywhere
cp agents/*.md <project>/.claude/agents/  # this project only
```

Then edit. These are written against a static Astro site on Cloudflare Pages;
the roles transfer, the specifics do not.

```
/agents      # confirm they loaded
```
