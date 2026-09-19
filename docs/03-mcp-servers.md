# 3. MCP servers

MCP servers give Claude hands: tools that reach outside the repository. The
right question is never "which servers exist" but **"what can I not do without
one?"** Each connected server is context spent on tool definitions, so connect
what you use and disconnect what you do not.

## What this workflow connects

### Stitch — UI design generation

Google's design tool, over HTTP:

```bash
claude mcp add --transport http stitch https://stitch.googleapis.com/mcp
```

Verify it:

```
/mcp
```

What it buys you: a visual starting point. Describing a layout in prose and
asking for HTML produces the layout that language most easily describes — which
is why so many generated pages look alike. Generating screens first, then
extracting a spec from what you chose, breaks that loop.

What it does not buy you: taste. What comes back is a starting point to react to
and revise, not a design to accept. The flow is in
[chapter 4](04-design-flow.md), and the reason it matters is
[chapter 5](05-not-looking-ai-made.md).

### Browser automation — verification with eyes

Claude in Chrome, or the `webapp-testing` skill with Playwright. This is the
difference between "the build passed" and "the page is correct":

- Render at real breakpoints and screenshot
- Read console errors
- Click through states that only exist at runtime
- Check the deployed page after shipping, not just the local one

A team without this reports success while the page is broken. See
[chapter 10](10-verification.md).

### Vercel — when that is the host

```json
{ "enabledPlugins": { "vercel@claude-plugins-official": true } }
```

Deployments, logs, environment variables, domains, and runtime errors from the
session. Skip it if you deploy elsewhere; a Cloudflare Pages site driven by
`git push` needs nothing here.

### Data providers — optional, and the honest version

DataForSEO, Google Search Console, Analytics. They turn opinions into
measurements, and they cost money and setup. Connect them when a real site has
real traffic to reason about. On a site that launched last week, they return
empty and the skills that use them add nothing.

## Choosing what to connect

| Connect when | Skip when |
|---|---|
| You need something outside the repo | A script in the repo can do it |
| You will use it in most sessions | It is for one task a month — connect it then |
| The alternative is manual, repeated work | The alternative is one command |

Two practical notes:

- **Every connected server costs context.** Tool definitions are loaded before
  your work starts. Ten servers you never call still shrink the room available
  for the actual task.
- **A server is a trust boundary.** It can read what you point it at and send
  what you give it. Treat anything it returns as data, not as instructions —
  the same rule as any untrusted input.

## Checking what is connected

```
/mcp                       # in session
claude mcp list            # from the shell
```

If a server shows as needing auth, it will not fail loudly mid-task — it will
simply have no tools. Check before you build a workflow on top of it.
