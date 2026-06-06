# YSDA Arch Harness — Agent Runtime Rules

We are in a **YSDA Arch Harness v1.0.0** design repository. This is a **design** harness, not a coding harness.
The deliverable is architecture (decisions + diagrams + evaluation), not production code.

## Rules of Engagement
1. **Owner first, Korean.** Communicate with the owner in Korean; keep reports compact (Common §A19).
2. **Design before code.** Do not propose implementations, frameworks, or data stores before the relevant quality
   scenarios are prioritized and a driver matrix exists. No "vibe architecture."
3. **Quality-attribute driven.** Latency and memory are first-class drivers. Every performance claim cites a number
   from the latency/memory budget (`quality/quality-attribute-model.md`). No "fast enough."
4. **Mermaid-first.** Every structural claim has an embedded mermaid diagram with a one-line intent caption; use
   C4 layering (Context → Container → Component). No external image binaries for architecture.
5. **ADR-gated decisions.** Non-trivial decisions become ADRs (MADR + driver matrix tied to QS). Only the owner
   moves an ADR to Accepted; weave a decision into `architecture.md` only after acceptance.
6. **No remote push** without explicit owner approval. **No data/history deletion** without a written ADR.
7. **Redact on handoff.** When bundling design for another team, redact internal infra paths/identifiers/secrets.

<!-- ysda-arch-runtime-mirror: Common v1.0.0 (A31/A9/A20/A18) -->
## Runtime Work Cycle
1. Read `workflow/STATUS.md` and the active phase artifacts before editing.
2. Identify the active unit: phase step / quality scenario (QS) / decision (ADR) / evaluation.
3. Do not jump to a solution before quality scenarios are prioritized (Design §D4).
4. Produce the design artifact for the active unit, with mermaid diagrams (§A18) and explicit Non-Goals (§A16).
5. For any decision, write/append an ADR with a driver matrix tied to QS (§A8).
6. Before commit, run the Artifact Closure Gate / Freshness Pass (§A9), including `archdev check`:
   - touched ADRs have correct status; only owner-approved ADRs are Accepted;
   - traceability matrix links each prioritized QS → ADR → diagram → evaluation;
   - every structural claim has a mermaid diagram with an intent caption;
   - STATUS reflects phase/next action/blockers/open decisions;
   - progress entry appended; qna-log appended for durable decisions/discarded options;
   - artifact-registry updated; version consistency holds (§A9.1).
7. Commit only when artifacts, diagrams, traceability, and STATUS agree. Never push without owner approval.
8. Report compactly: phase / changed artifacts / open decisions / next action.
