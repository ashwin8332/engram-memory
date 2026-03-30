<div align="center">

<br />

```
███████╗███╗   ██╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
█████╗  ██╔██╗ ██║██║  ███╗██████╔╝███████║██╔████╔██║
██╔══╝  ██║╚██╗██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
███████╗██║ ╚████║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
```

**Persistent, shared agent memory as MCP infrastructure.**

[![Status](https://img.shields.io/badge/status-early%20development-orange?style=flat-square)](https://github.com/Agentscreator/Engram)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](./LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-8b5cf6?style=flat-square)](https://modelcontextprotocol.io)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](./CONTRIBUTING.md)

<br />

</div>

---

Every agent session starts from zero.

No memory of why a decision was made last week. No record of which approaches already failed. No awareness of the constraints that are non-negotiable. Another engineer's agent re-discovered the same thing the day before. That knowledge evaporated when the session ended.

**Engram fixes that.**

<br />

## The Problem

```
Day 1 — Agent A discovers: "Don't touch the auth middleware.
         Session token format changed. Old code breaks mobile."

Day 3 — Agent B touches the auth middleware.
         Re-discovers it the hard way.

Day 7 — Agent C touches the auth middleware.
```

This is not a hypothetical. This is the default state of every multi-agent, multi-session codebase today. Knowledge is generated constantly — and lost constantly.

<br />

## What Engram Does

Engram is an **MCP server** that gives your agents a shared, versioned knowledge base that persists across sessions. When an agent discovers something real — a hidden side effect, a failed approach, an undocumented constraint — it commits that to Engram.

The next agent, in a separate session days later, pulls that fact before touching the relevant code.

> It does not re-discover. It builds on.

<br />

## API Surface

Engram exposes three tools any MCP-compatible agent can call:

<br />

### `query(topic)`

```typescript
// Before beginning work, pull what is already known.
const facts = await engram.query("auth middleware");

// Returns: relevant facts, past decisions, known constraints,
// confidence levels, and the context behind each discovery.
```

> Called at the start of any session touching a known area. Surfaces accumulated team intelligence before a single line is written.

<br />

### `commit(fact, context)`

```typescript
// When you discover something worth preserving, write it.
await engram.commit({
  fact: "Auth middleware caches tokens in memory. Restart clears all sessions.",
  context: "Discovered during load testing — 2k concurrent users caused cascade logout.",
  scope: "src/middleware/auth.ts",
  confidence: 0.95
});
```

> Entries are **append-only and never deleted.** The record of what was known, and when, is permanent.

<br />

### `conflicts()`

```typescript
// Surface contradictions before they become bugs.
const contradictions = await engram.conflicts();

// Returns: pairs of semantically contradictory facts,
// flagged automatically via embedding similarity scoring.
```

> Not an error that blocks you. A structured artifact you review and resolve — a signal that something in the codebase changed and the knowledge base needs reconciling.

<br />

## Works With Your Existing Stack

Engram is MCP-native. No changes to how you work.

| Agent / IDE | Status |
|---|---|
| Claude Code | Compatible |
| Cursor | Compatible |
| Windsurf | Compatible |
| Any MCP client | Compatible |

Connect to the server. Every session starts with accumulated team intelligence instead of nothing.

<br />

## Roadmap

```
 ○  MCP server — query, commit, and conflicts tools
 ○  SQLite backend — append-only fact store
 ○  Semantic search over committed facts
 ○  Embedding-based conflict detection
 ○  Two-engineer reproducible demo
```

<br />

## Current Status

Engram is in early development. The core design is solid — the architecture, API surface, and storage model are defined. Implementation is underway.

If you're interested in what's being built, **star the repo** to follow along. If you want to help shape it, open an issue or start a discussion. Early feedback on the design changes real decisions.

<br />

## Contributing

Engram is being built in the open.

If the problem resonates with you — if you've felt the pain of agents re-discovering things that were already known — contributions are welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to get involved.

Not sure where to start? Open a discussion and say what you're thinking. That counts.

<br />

## Feedback

Thoughts on the design, the API surface, or the problem itself?

Open an issue or reach out directly at **joshnathbrown884@gmail.com**. This is early enough that real feedback changes real decisions.

<br />

---

<div align="center">

*A biological engram is the physical trace a memory leaves in the brain.*
*That's the idea.*

<br />

</div>
