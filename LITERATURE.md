# Literature

PDFs are in [`./papers/`](./papers/).

---

## [1] Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead

**Authors:** Zhongming Yu, Naicheng Yu, Hejia Zhang, Wentao Ni, Mingrui Yin, Jiaying Yang, Yujie Zhao, Jishen Zhao
**Affiliations:** UC San Diego, Georgia Tech
**Venue:** Architecture 2.0 Workshop, March 23, 2026, Pittsburgh, PA
**ArXiv:** [2603.10062](https://arxiv.org/abs/2603.10062)
**File:** [`papers/2603.10062v1.pdf`](papers/2603.10062v1.pdf)

### Summary

This position paper — the direct intellectual foundation for Engram — frames multi-agent memory as a **computer architecture problem**. The central observation is that LLM agent systems are hitting a wall that looks exactly like the memory bottleneck in classical hardware: performance limited not by compute but by bandwidth, hierarchy, and consistency.

**Three-layer memory hierarchy:**
- *I/O layer* — interfaces ingesting audio, text, images, network calls (e.g., MCP)
- *Cache layer* — fast, limited-capacity short-term storage: compressed context, recent tool calls, KV caches, embeddings
- *Memory layer* — large-capacity long-term storage: full dialogue history, vector DBs, graph DBs

**Two missing protocols:**
1. *Agent cache sharing* — no principled protocol exists for one agent's cached artifacts to be transformed and reused by another (analogous to cache transfers in multiprocessors)
2. *Agent memory access control* — permissions, scope, and granularity for reading/writing another agent's memory remain under-specified

**Central claim:** The most pressing open challenge is **multi-agent memory consistency**. In single-agent settings, consistency means temporal coherence — new facts must not contradict established ones. In multi-agent settings, the problem compounds: multiple agents read from and write to shared memory concurrently, raising classical challenges of *visibility*, *ordering*, and *conflict resolution*. The difficulty is harder than hardware because memory artifacts are semantic and heterogeneous (evidence, tool traces, plans), and conflicts are often semantic and coupled to environment state.

**Relevance to Engram:** Engram directly implements the consistency layer this paper identifies as the field's most urgent gap. `engram_commit` is the shared write; `engram_query` is the read; `engram_conflicts` is the conflict detection mechanism. The paper's vocabulary — shared vs. distributed memory, hierarchy layers, consistency models — is the conceptual language of this project.

---

## [2] A-Mem: Agentic Memory for LLM Agents

**Authors:** Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
**Affiliations:** Rutgers University, Independent Researcher, AIOS Foundation
**ArXiv:** [2502.12110](https://arxiv.org/abs/2502.12110) (v11, Oct 2025)
**File:** [`papers/2502.12110v11.pdf`](papers/2502.12110v11.pdf)

### Summary

A-Mem proposes a **Zettelkasten-inspired agentic memory system** that dynamically organizes memories without predefined schemas or fixed workflows. Its core contribution is that memory is not static storage — it actively evolves as new experiences arrive.

**Architecture:** Each memory is stored as a structured note:
```
mᵢ = {cᵢ, tᵢ, Kᵢ, Gᵢ, Xᵢ, eᵢ, Lᵢ}
```
where `c` = content, `t` = timestamp, `K` = LLM-generated keywords, `G` = tags, `X` = contextual description, `e` = embedding vector, `L` = links to related memories.

**Three-phase operation:**
1. *Note Construction* — LLM generates rich semantic attributes from raw interaction content
2. *Link Generation* — cosine similarity retrieves top-k neighbors; LLM determines whether semantic links should be established
3. *Memory Evolution* — when a new memory arrives, existing linked memories are updated: their context, keywords, and tags are revised to reflect the new knowledge

The result is a living knowledge graph where memories continuously deepen their connections and semantic representations as the agent accumulates experience.

**Results:** Outperforms MemGPT, MemoryBank, and ReadAgent on the LoCoMo long-form conversation QA benchmark across six foundation models (Llama 3.2, Qwen2.5, GPT-4o).

**Relevance to Engram:** A-Mem solves *single-agent* memory organization. It has no notion of shared state or cross-agent consistency. Engram operates at the layer above: once facts are committed to shared memory, Engram manages what happens when two agents' committed facts contradict each other — a problem A-Mem is not designed to address. A-Mem's note structure is instructive for how Engram might enrich committed facts with semantic metadata.

---

## [3] MIRIX: Multi-Agent Memory System for LLM-Based Agents

**Authors:** Yu Wang, Xi Chen
**Affiliation:** MIRIX AI (Yu Wang: UCSD, Xi Chen: NYU Stern)
**ArXiv:** [2507.07957](https://arxiv.org/abs/2507.07957) (v1, Jul 2025)
**File:** [`papers/2507.07957v1.pdf`](papers/2507.07957v1.pdf)

### Summary

MIRIX proposes a **modular, multi-agent memory system** organized around six specialized memory types — each managed by a dedicated agent — with a Meta Memory Manager handling routing.

**Six memory components:**
| Component | What it stores |
|---|---|
| Core Memory | High-priority persistent facts about user identity and agent persona |
| Episodic Memory | Time-stamped events, activities, interactions (a structured log) |
| Semantic Memory | Abstract concepts, entities, relationships independent of time |
| Procedural Memory | Step-by-step workflows and how-to guides |
| Resource Memory | Full documents, transcripts, multimedia files |
| Knowledge Vault | Sensitive verbatim facts: credentials, contacts, addresses (access-controlled) |

**Active Retrieval:** Rather than requiring explicit retrieval triggers, the system first generates a *topic* from the current query, then retrieves across all six components, injecting results into the system prompt. This eliminates the failure mode where LLMs default to stale parametric knowledge.

**Multi-agent workflow:** A Meta Memory Manager routes incoming data to the appropriate Memory Managers in parallel. On read, the Chat Agent performs coarse retrieval across all components, then targeted retrieval using whichever strategy (embedding_match, bm25_match, string_match) fits.

**Results:** SOTA 85.4% on LOCOMO (long-form conversation QA), outperforming prior best by 8 points. On a new multimodal benchmark (ScreenshotVQA, ~20K high-res screenshots), MIRIX achieves 35% higher accuracy than RAG baseline while using 99.9% less storage.

**Relevance to Engram:** MIRIX is the state-of-the-art in comprehensive single-user memory architecture. Its six-component taxonomy provides a rich vocabulary for what *kinds* of facts agents might commit. However, MIRIX is fundamentally single-user: its multi-agent architecture is internal (multiple agents managing one user's memory), not cross-team. Engram addresses what MIRIX does not: what happens when two engineers' agents independently commit contradictory facts about the same codebase to a shared store.

---

## [4] Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics

**Authors:** Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang, et al. (large collaborative team)
**Affiliations:** NUS, Renmin University of China, Fudan University, Peking University, NTU, Tongji University, UCSD, HKUST(GZ), Griffith University, Georgia Tech, OPPO, Oxford
**ArXiv:** [2512.13564](https://arxiv.org/abs/2512.13564) (v2, Jan 2026)
**File:** [`papers/2512.13564v2.pdf`](papers/2512.13564v2.pdf)

### Summary

The most comprehensive survey of agent memory as of early 2026. Proposes a unified taxonomy organized along three axes: **Forms** (what carries memory), **Functions** (why agents need memory), and **Dynamics** (how memory operates and evolves).

**Forms — three realizations:**
- *Token-level memory* — explicit discrete units (text, visual tokens): flat (1D), planar/graph (2D), or hierarchical (3D)
- *Parametric memory* — information encoded in model weights (fine-tuning, adapters, LoRA)
- *Latent memory* — information in internal hidden states, KV caches, continuous representations

**Functions — three purposes:**
- *Factual memory* — user facts and environment facts that sustain interaction consistency
- *Experiential memory* — case-based, strategy-based, skill-based knowledge accumulated through task execution
- *Working memory* — transient workspace information managed within a single task instance

**Dynamics — three lifecycle operators:**
- *Formation* — extracting and encoding information worth preserving
- *Evolution* — consolidation, updating, forgetting
- *Retrieval* — timing, query construction, strategy selection, post-processing

**Key distinctions:**
- Agent memory ≠ LLM memory (which concerns KV cache management and architecture-level context handling)
- Agent memory ≠ RAG (which retrieves from static external knowledge for single-task inference)
- Agent memory ≠ context engineering (which optimizes the context window as a resource)

**Multi-agent shared memory (Section 7.5):** Identified as a critical frontier. Early MAS used isolated local memories + message passing, suffering from redundancy and high communication overhead. Centralized shared stores helped but introduced *write contention* and *lack of permission-aware access control*. The survey calls for:
- *Agent-aware shared memory* — R/W conditioned on agent roles, expertise, and trust
- *Learning-driven conflict resolution* — training agents when/what/how to contribute based on team performance
- Shared memory that can abstract across heterogeneous signals while maintaining *temporal and semantic coherence*

**RL frontier (Section 7.3):** The field is moving from heuristic/prompt-driven memory management toward fully RL-driven systems where memory architecture and control policy are learned end-to-end.

**Relevance to Engram:** This survey provides the broadest context. It confirms that shared memory for multi-agent systems is an open frontier (Section 7.5) and that conflict detection and resolution are unsolved (referenced alongside RAMDocs, MADAM-RAG, and Zep). Engram's `engram_conflicts()` addresses exactly what this survey identifies as "write contention" and the need for "governance." The survey's taxonomy also gives Engram a precise vocabulary: Engram stores *factual memory* (environment facts about the codebase) in a *flat token-level* form with *append-only formation* and *explicit conflict evolution*.

---

## Landscape at a Glance

| Paper | Scope | Consistency | Conflict Detection | Year |
|---|---|---|---|---|
| Yu et al. [1] | Architecture framing | Named as #1 open problem | Not implemented | 2026 |
| Xu et al. [2] (A-Mem) | Single-agent memory organization | Temporal coherence only | No | 2025 |
| Wang & Chen [3] (MIRIX) | Single-user multi-component memory | Within one user's store | No | 2025 |
| Hu et al. [4] (Survey) | Full landscape | Flagged as unsolved frontier | No | 2026 |
| **Engram** | **Multi-agent shared memory** | **Cross-agent fact consistency** | **Yes (`engram_conflicts`)** | **2026** |

The gap Engram fills is visible in every row of the right two columns: every existing system either does not address cross-agent consistency or names it as unsolved. Engram is the first working implementation of the detection layer.
