# AGENTS.md — Engram Shared Memory

This file is read automatically by Claude Code, Kiro, Cursor, Windsurf, and
other AI coding assistants. It tells your agent how to connect to the team's
shared memory and what to do with it.

---

## Connect at the start of every session

Check for `.engram.env` in the workspace root:

```
ENGRAM_SERVER_URL=https://www.engram-memory.com
ENGRAM_INVITE_KEY=ek_live_...
```

**If you have Engram MCP tools** (`engram_status`, `engram_commit`, …):

Call `engram_status()` — it reads `.engram.env` and connects automatically.
Follow the `next_prompt` field in the response.

**If you do not have Engram MCP tools:**

Use the REST API with the credentials above.

Query before starting any task:
```
GET {ENGRAM_SERVER_URL}/api/query?topic=<task description>
Authorization: Bearer {ENGRAM_INVITE_KEY}
```

Commit a verified fact:
```
POST {ENGRAM_SERVER_URL}/api/commit
Authorization: Bearer {ENGRAM_INVITE_KEY}
Content-Type: application/json

{"content": "...", "scope": "general", "confidence": 0.9, "fact_type": "observation"}
```

---

## Before every task

Query what the team already knows. Don't repeat verified work or contradict
established facts without first checking for conflicts.

---

## While working

Commit facts you have verified — hidden side-effects, failed approaches,
architectural decisions, config details that tripped you up. Batch related
discoveries into one commit. Max 5 commits per task.

Check for conflicts before making architectural decisions:
- MCP: `engram_conflicts()`
- REST: `GET {ENGRAM_SERVER_URL}/api/conflicts` with Bearer auth

---

## Rules

- Only commit what you have verified. Never commit speculation.
- Never commit secrets, API keys, or passwords.
- Do not call `engram_query` more than 3 times per task.
