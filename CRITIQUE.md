# Engram Implementation Plan — Adversarial Critique

What follows is a systematic attempt to extend, replace, or falsify claims in the
implementation plan, informed by the latest research (through March 2026), the live
MCP ecosystem, and production agent memory systems.

---

## 1. Things the Plan Gets Right (Unfalsified)

These survived scrutiny and are validated by the current landscape:

- **Temporal validity as the sole versioning primitive.** Graphiti/Zep continues to
  validate bitemporal modeling as the correct abstraction. No competing system has
  found a simpler one. The collapse of four Round 2 mechanisms into `valid_from`/
  `valid_until` remains the plan's strongest architectural insight.

- **Detection decoupled from the write path.** The SQLite WAL bottleneck analysis is
  correct. Turso's recent work (concurrent writes via MVCC, 4x throughput over vanilla
  SQLite) further validates that single-writer serialization is a real constraint. The
  async background worker design is sound.

- **Four-tool MCP surface.** Context7 (2 tools, 44k stars), the Descope hackathon
  winners, and Block's 60+ server playbook all confirm: fewer tools, richer descriptions.
  Engram's 4-tool surface is well-calibrated.

- **Privacy by design / local-first.** Every successful MCP server follows this pattern.
  Mem0's OpenMemory MCP, Cipher (Byterover), and Context7 all default to local-first.
  The plan's stance is validated.

- **NLI as signal, not judge.** The httphangar.com deep-dive on contradiction detection
  (synthesizing 2023–2025 research) confirms: LLMs detect self-contradictions at
  0.6–45.6% accuracy; pairwise contradictions top out at ~89% with chain-of-thought.
  NLI on technical domain text is even worse. The tiered pipeline with deterministic
  rules first is the correct architecture.

---

## 2. Things That Can Be Extended

### 2a. Memory Injection Attacks (MINJA) — Missing Threat Model

The plan's security section covers input validation, parameterized SQL, scope
permissions, and token binding. It explicitly scopes out "full adversarial security."
But it misses a specific, published attack vector that operates *within* the
permissioned trust model.

**MINJA** ([Dong et al., 2025](https://arxiv.org/abs/2503.03704)) demonstrates that
an attacker can inject malicious records into an agent's memory bank through normal
query interactions alone — no direct memory access needed. The attack achieves >95%
injection success rate and 70% attack success rate. A follow-up paper ([Memory
Poisoning Attack and Defense, Jan 2026](https://arxiv.org/abs/2601.05504)) studies
defenses.

**Why this matters for Engram:** Engram's `engram_commit` accepts facts from any
authenticated agent. A compromised or manipulated agent (not a malicious human — a
legitimate agent that was prompt-injected) could commit poisoned facts that propagate
through `engram_query` to other agents. The plan's "rate limiting + agent reliability
scoring" defense is necessary but may be insufficient.

**Extension:** Add a "provenance verification" step to `engram_commit`:
- Facts committed with `confidence >= 0.8` should include a `provenance` field
  (file path, line number, test output, or tool call ID that generated the evidence).
- Facts without provenance are accepted but flagged as `unverified` in query results.
- The AGENTS.md template should instruct agents to always include provenance.
- This doesn't prevent poisoning, but it makes poisoned facts auditable and
  distinguishable from verified ones. It's the "trust but verify" layer the plan lacks.

### 2b. Collaborative Memory's Access Control Model

[Collaborative Memory (OpenReview, 2025)](https://openreview.net/forum?id=pJUQ5YA98Z)
introduces a framework with asymmetric, time-evolving access controls encoded as
bipartite graphs linking users, agents, and resources. Each memory fragment carries
immutable provenance attributes.

**Extension for Engram:** The current `scope_permissions` table is static (boolean
`can_read`/`can_write` per agent per scope). Collaborative Memory's model suggests:
- **Time-bounded permissions:** `valid_from`/`valid_until` on scope permissions
  themselves (reusing the same temporal primitive). An agent might have write access
  to `payments/*` only during a specific sprint or deployment window.
- **Provenance-aware reads:** When `engram_query` returns facts, include which agent
  committed each fact and whether the querying agent has "trust" in that source agent.
  This is richer than the current `agent_trust` score.

This is a Phase 5 extension, not a rewrite. The schema change is minimal:
```sql
ALTER TABLE scope_permissions ADD COLUMN valid_from TEXT;
ALTER TABLE scope_permissions ADD COLUMN valid_until TEXT;
```

### 2c. SEDM's Verifiable Write Admission

[SEDM (Self-Evolving Distributed Memory)](https://arxiv.org/abs/2509.09498) introduces
"verifiable write admission based on reproducible replay" — before a memory entry is
accepted, the system replays the execution context that produced it to verify the claim.

**Extension for Engram:** Full replay verification is too heavy for Engram's use case,
but the principle is sound. A lightweight version:
- For facts that reference specific code artifacts (files, functions, config values),
  `engram_commit` could accept an optional `artifact_hash` — a SHA-256 of the file or
  config value at the time the fact was observed.
- On `engram_query`, facts whose `artifact_hash` no longer matches the current state
  could be flagged as `potentially_stale`.
- This is cheap (one hash comparison) and catches the most common failure mode: facts
  that were true when committed but are no longer true because the code changed.

### 2d. AMP's Privacy Operations

[AMP (ICML 2026)](https://proceedings.mlr.press/v317/wu26a.html) defines three
deterministic operations for privacy: redact at rest, pack for purpose, hydrate on
return. This guarantees no personal identifier leaves the user boundary.

**Extension for Engram:** The plan says "Do not include secrets, API keys, passwords"
in tool descriptions, but relies on the LLM following this instruction. AMP suggests
a deterministic approach:
- Run a lightweight regex/pattern scanner on `content` at commit time to detect
  potential secrets (API key patterns, JWT tokens, connection strings).
- If detected, either reject the commit with an actionable error or auto-redact the
  sensitive portion and store a `[REDACTED:api_key]` placeholder.
- This is a 5-line addition to the commit pipeline and prevents the most common
  accidental secret leakage.

### 2e. Cipher's Dual Memory Layer (System 1 / System 2)

[Byterover Cipher](https://github.com/campfirein/cipher) distinguishes between
System 1 memory (programming concepts, business logic, past interactions) and System 2
memory (reasoning steps the model took when generating code).

**Extension for Engram:** Currently all facts are flat. Adding a `fact_type` field
could distinguish:
- `observation` — what the agent directly observed in code/tests/logs
- `inference` — what the agent concluded from observations
- `decision` — architectural decisions made by humans or agents

This costs one column and enables richer query filtering. An agent debugging a
production issue cares about `observation` facts; an agent making an architectural
decision cares about `decision` facts. The conflict detection pipeline could also
weight these differently — two conflicting observations are more serious than two
conflicting inferences.

---

## 3. Things That Can Be Replaced

### 3a. SQLite → Turso/libSQL for Team Deployment

The plan correctly identifies SQLite WAL's single-writer limitation and works around
it by decoupling detection from writes. But for team deployment (Phase 5+), the
workaround has limits.

[Turso](https://turso.tech/) (Rust rewrite of SQLite with MVCC) now supports
concurrent writes, achieving 4x write throughput over vanilla SQLite and eliminating
`SQLITE_BUSY` errors entirely. It's wire-compatible with SQLite, supports the same
SQL dialect, and adds:
- Concurrent writes via MVCC (no single-writer bottleneck)
- Built-in vector search (could replace the separate `sentence-transformers` embedding
  + numpy cosine similarity pipeline)
- Change Data Capture (useful for federation in Phase 6)
- Edge replication (useful for distributed team deployment)

**Replacement proposal:** Keep SQLite for local/stdio mode (zero dependencies). For
team mode (`--auth`), offer Turso as the storage backend. The schema is identical.
The migration path is: `pip install engram-mcp` (SQLite) → `pip install engram-mcp[team]`
(Turso). This eliminates the write contention concern entirely for team use and gives
federation (Phase 6) for free via Turso's replication.

**Risk:** Turso is newer and less battle-tested than SQLite. The plan's current
approach (SQLite WAL + async detection) is safer for v1. Turso should be a v2 option,
not a v1 replacement.

### 3b. DeBERTa NLI → Smaller/Faster Alternatives

The plan uses `cross-encoder/nli-deberta-v3-base` (86M parameters, ~300ms per pair).
For 30 candidates per commit, that's ~9 seconds if run sequentially, or ~300ms if
batched on GPU.

But the plan targets local CPU deployment (`pip install`, no GPU required). On CPU,
DeBERTa-base takes ~300ms *per pair*. 30 pairs = ~9 seconds. This is too slow for
the "~500ms total" claim in the plan.

**Alternatives:**
- `cross-encoder/nli-MiniLM2-L6-H768` — 6 layers, ~60M params, ~3x faster on CPU,
  ~85% of DeBERTa-base accuracy on MNLI. 30 pairs ≈ 3 seconds.
- `cross-encoder/nli-distilroberta-base` — distilled, ~2x faster, ~90% accuracy.
- ONNX-quantized DeBERTa — INT8 quantization can cut inference time 2-4x on CPU.

**Replacement proposal:** Default to MiniLM2-L6 for CPU deployment (covers the
zero-setup local use case). Offer DeBERTa-base as a `--high-accuracy` flag for
GPU-equipped team servers. Ship ONNX runtime as an optional dependency for further
speedup.

The plan's "~500ms total" latency claim for Tier 1 is only achievable with a smaller
model or ONNX quantization. This should be stated explicitly.

### 3c. `rank_bm25` → SQLite FTS5

The plan lists `rank_bm25` as a dependency for lexical retrieval. SQLite has built-in
full-text search (FTS5) that:
- Requires zero additional dependencies
- Is faster than Python-level BM25 (C implementation)
- Supports BM25 ranking natively
- Integrates with the existing SQLite storage

**Replacement:** Drop `rank_bm25` dependency. Create an FTS5 virtual table:
```sql
CREATE VIRTUAL TABLE facts_fts USING fts5(content, scope, keywords, content=facts, content_rowid=rowid);
```
Query with: `SELECT * FROM facts_fts WHERE facts_fts MATCH ? ORDER BY rank;`

This removes a dependency, improves performance, and keeps everything in one database.
The plan already uses SQLite for everything else — using a Python BM25 library alongside
it is an unnecessary seam.

---

## 4. Things That Can Be Falsified

### 4a. "~40-60% entity extraction via regex" Is Likely Optimistic

The plan claims regex catches "~40-60% of entities in well-structured facts." This
assumes agents write facts like "rate limit is 1000 req/s" rather than "the auth
service throttles at about a thousand requests per second."

The httphangar.com analysis of numeric contradiction detection confirms: "Numbers look
semantically similar to embedding models. Unit mismatches require explicit normalization.
Approximate quantities need fuzzy matching." The plan's own Round 5 finding
acknowledges this but then claims 40-60% regex recall without evidence.

**Falsification:** The 40-60% figure is an unsupported estimate. On well-structured
facts (which the AGENTS.md template encourages), it might be achievable. On natural
prose facts, it's likely 20-30%. The plan should either:
1. Run the regex pipeline on a sample of 100 real codebase facts and measure actual
   recall, or
2. Drop the percentage claim and state "regex is the fast first pass; the NER model
   is the primary extractor."

The hybrid pipeline design is correct regardless of the exact regex recall number.
The risk is that if regex recall is overestimated, the plan underestimates the
importance (and latency cost) of the NER model pass.

### 4b. "~500ms Total Detection Latency" Is Falsified on CPU

The plan claims Tier 1 NLI completes in "~300ms for 30 candidates" and total detection
in "~500ms." This is only true if:
- The NLI model runs on GPU (batch inference), OR
- The candidate set is much smaller than 30

On CPU (the default deployment), `cross-encoder/nli-deberta-v3-base` takes ~200-400ms
*per pair*. 30 pairs on CPU = 6-12 seconds, not 300ms.

**The plan's latency table is GPU-assumed but the deployment model is CPU-first.**

**Fix:** Either:
1. Use a smaller model (MiniLM2-L6) as default, achieving ~100ms/pair → 3s for 30
   pairs. Still not 500ms, but acceptable for a background worker.
2. Reduce the candidate set. If Tier 0 catches the obvious conflicts and Tier 2
   catches numeric ones, the NLI candidate set after dedup might be 5-10, not 30.
   10 pairs × 200ms = 2 seconds on CPU. Acceptable.
3. State the actual latency: "Detection completes in 2-10 seconds on CPU, <500ms
   on GPU." This is honest and doesn't affect the architecture (detection is async
   anyway).

### 4c. "Confidence Removed from Scoring" May Be Premature

The plan removes agent-reported confidence from the query scoring formula because
"LLMs systematically over-report confidence." This is true for uncalibrated confidence.
But the plan also introduces a calibration mechanism (the `detection_feedback` table)
for NLI thresholds. The same calibration principle could apply to confidence.

**Partial falsification:** If Engram tracks which confidence levels correlate with
facts that later get involved in conflicts (i.e., were wrong), it can learn a
per-agent confidence calibration curve. A fact committed at confidence 0.9 by an
agent whose 0.9-confidence facts are wrong 40% of the time should be treated
differently than a 0.9 from an agent whose 0.9s are right 95% of the time.

The current plan already tracks `flagged_commits / total_commits` per agent. Extending
this to `flagged_commits_at_confidence_bucket / total_commits_at_confidence_bucket`
would enable calibrated confidence without the noise of raw self-reported values.

This is a Phase 3+ extension, not a v1 requirement. But "confidence is removed" should
be "confidence is deferred until calibration data exists."

### 4d. The "No Graph Database" Stance May Be Too Absolute for Phase 6+

The plan correctly removes graph databases for v1. SQLite + JSON entities is sufficient
for consistency checking. But Phase 6 (federation) and the dashboard's "timeline view"
start to look like graph problems:
- "Which agents' facts influenced this architectural decision?"
- "Show me the chain of corrections for this lineage."
- "Which scopes have facts from agents that also committed to scope X?"

These are traversal queries. They're expressible in SQL but ugly and slow. The plan
should acknowledge that if federation scales beyond ~10 teams or ~100k facts, a graph
layer (not necessarily Neo4j — something lightweight like [Kùzu](https://kuzudb.com/),
an embedded graph DB) might become justified.

**Not a falsification of v1 design, but a falsification of "never graph."**

### 4e. The Mem0 / Cipher Competitive Landscape Is Closer Than Implied

The plan positions Engram as unique: "There are 400+ MCP servers that give an
individual agent persistent memory. Engram is not that." This is true for v1's
consistency focus. But the landscape is converging:

- **Mem0** (38k+ GitHub stars) now explicitly addresses multi-agent memory with four
  scoping dimensions (user, session, agent, application). Their March 2026 blog post
  directly discusses "agents duplicating and contradicting each other's work" as the
  core problem. They don't have conflict *detection*, but they're framing the same
  problem.

- **Cipher (Byterover)** ships team-level memory sharing across IDEs with real-time
  sync. No conflict detection, but the shared memory layer is production-ready.

- **SAMEP** ([arxiv 2507.10562](https://arxiv.org/abs/2507.10562)) proposes a formal
  protocol for secure agent memory exchange with cryptographic access controls
  (AES-256-GCM) and MCP/A2A compatibility.

- **Agent KB** (ICML 2025) provides cross-domain experience sharing with hybrid
  retrieval — structurally similar to `engram_query`.

**The window for "only system doing consistency" is narrowing.** Engram's moat is the
conflict detection pipeline (Tiers 0-3), not the shared memory layer itself. The plan
should accelerate Phase 3 (conflict detection) relative to other phases, because
that's the defensible differentiator. If Engram ships Phases 1-2 without Phase 3,
it's just another shared memory MCP server in a crowded field.

---

## 5. New Risks Not Addressed

### 5a. Embedding Model Drift Across Team Members

The plan stores `embedding_model` and `embedding_ver` per fact and provides a
re-indexing tool. But in team deployment, different engineers might have different
versions of `sentence-transformers` installed, producing slightly different embeddings
for the same text. The plan doesn't specify how to enforce embedding model consistency
across a team.

**Mitigation:** In team mode, the server should generate all embeddings server-side
(it already does for `engram_query`). The risk is only in local mode where each
engineer runs their own server. The plan should state: "In team mode, the server is
the single source of embeddings. In local mode, embedding version mismatches are
detected at startup and flagged."

### 5b. CLAIRE's 75% AUROC Ceiling Is Understated

The plan cites CLAIRE's ~75% AUROC as the ceiling for automated consistency detection
and uses this to justify the human-in-the-loop dashboard. But CLAIRE operates on
Wikipedia (general knowledge). Engram operates on codebase facts (technical domain).

The actual ceiling for automated detection on technical facts is likely *lower* than
75%, because:
- Technical contradictions often involve implicit context ("the auth service" might
  refer to different services in different scopes)
- Numeric contradictions require unit normalization that NLI models can't do
- Temporal contradictions require knowing what "current" means

The tiered pipeline (Tiers 0+2 for deterministic, Tier 1 for semantic) is the right
response, but the plan should be explicit: **the 75% AUROC figure is an upper bound
from a more favorable domain. Engram's actual automated precision will likely be
60-70% without the deterministic tiers, and 80-85% with them.** The deterministic
tiers aren't just a performance optimization — they're a precision necessity.

### 5c. No Mention of Fact Expiry / TTL

The plan has `valid_until` for supersession but no mechanism for automatic expiry.
A fact committed 18 months ago about a rate limit that nobody has corrected isn't
necessarily still true — it might just be forgotten. The `recency` signal in query
scoring partially addresses this, but there's no explicit TTL or "staleness warning."

**Suggestion:** Add an optional `ttl_days` parameter to `engram_commit` (default:
null = no expiry). When set, the fact's `valid_until` is automatically set to
`valid_from + ttl_days`. Facts approaching expiry could be surfaced in the dashboard
as "needs re-verification." This is especially useful for facts about external
dependencies, API contracts, and infrastructure that change frequently.

---

## Summary

The implementation plan is strong. The temporal validity model, async detection,
tiered NLI pipeline, and minimal MCP surface are all well-grounded. The main gaps:

1. **Latency claims are GPU-assumed but deployment is CPU-first** — needs honest
   numbers or a smaller default model.
2. **Memory injection attacks (MINJA)** are a real threat within the trust model —
   provenance tracking should be added.
3. **The competitive window is narrowing** — Phase 3 (conflict detection) should be
   prioritized as the defensible moat.
4. **SQLite FTS5 should replace `rank_bm25`** — fewer dependencies, better performance.
5. **Turso/libSQL is the natural upgrade path** for team deployment — should be
   acknowledged as a v2 option.
6. **Fact expiry (TTL)** and **secret detection** are cheap additions that
   significantly improve production safety.
