# YSDA Arch Harness — Agent Runtime Rules

We are in a **YSDA Arch Harness v1.0.3** design repository. This is a **design** harness, not a coding harness.
The deliverable is architecture (decisions + diagrams + evaluation), not production code.

> **독자 모델(Reader model).** 설계 산출물의 독자는 아키텍트가 아니다. Lab Head·PM·CX·UX·QA·Client/Server 개발자·기획자·임원 등 **모든 stakeholder**다. 문서의 목적은 "설계 저장"이 아니라 **설계 공유·합의·전달**이다. 따라서 모든 공유 산출물은 모든 stakeholder가 정렬·합의·실행할 수 있게 작성한다.

## Rules of Engagement
1. **Owner first, Korean.** Communicate with the owner in Korean; keep reports compact (Common §A19).
2. **Design before code.** Do not propose implementations, frameworks, or data stores before the relevant quality
   scenarios are prioritized and a driver matrix exists. No "vibe architecture."
3. **Quality-attribute driven.** Latency and memory are first-class drivers. Every performance claim cites an
   owner-approved value from `arch/quality/latency-budget.md` or `arch/quality/memory-budget.md`; use `<TBD>` until
   approval. No "fast enough" and no sample value as a product target.
4. **Mermaid-first.** Every structural claim has an embedded mermaid diagram with a one-line intent caption; use
   C4 layering (Context → Container → Component). No external image binaries for architecture.
5. **ADR-gated decisions.** Non-trivial decisions become ADRs (MADR + driver matrix tied to QS). Only the owner
   moves an ADR to Accepted; weave a decision into `arch/architecture-brief.md` and `arch/views/` only after
   acceptance.
6. **No remote push** without explicit owner approval. **No data/history deletion** without a written ADR.
7. **Redact on handoff.** When bundling design for another team, redact internal infra paths/identifiers/secrets,
   confidential raw detail, and performance values not approved for sharing.
8. **Preserve sources.** When ingesting existing material, keep the **original verbatim** in
   `arch/sources/originals/` and write a separate **LLM-readable normalized** artifact (Source Record) in
   `arch/sources/normalized/`. Every Source Record states **출처(origin), 원본 작성·갱신일, 수집 시각(captured-at)**.
   Normalized ≠ original; never overwrite or paraphrase away the source.
9. **Stakeholder-friendly deliverables (not summaries).** Every shared artifact opens with a **한눈에** section
   written for all stakeholders (설계 의도 / 선택 이유 / 기대 효과 / 영향 범위 / 주요 고려사항), renders
   structure/flow as **mermaid** (no prose-only structure), and carries a **용어(Glossary)**. 쉽게 쓰되 정보 손실 금지.
   금지 표현: "비전문가", "임원도 이해", "non-technical", "for non-experts", "executive-friendly" — 누구를 낮춰 부르지 않는다.

10. **Deliverable language policy — Korean-first.** 내부 추론/프롬프트는 영어 가능하나, stakeholder가 보는 **모든 산출물의 서술(narrative)은 기본 한국어**, 기술 용어(Quality Attribute, Latency Budget, Sandbox 등)만 영어 유지. 대상: `Executive Summary`, `Stakeholder Summary`, `Implementation Readiness Report`, `Stakeholder Action Plan`, `Work Breakdown`, **그리고 Source Record(SRC)·as-is 정리물 등 stakeholder가 읽는 모든 normalized 산출물**. owner가 명시 요청할 때만 영어. ADR·상세 기술 register는 필요 시 이중언어 가능.
    - 나쁜 예: `The architecture introduces a command execution sandbox to mitigate unsafe execution risks.`
    - 좋은 예: `본 설계는 안전하지 않은 명령 실행 위험을 줄이기 위해 Command Execution Sandbox를 도입한다.`
11. **Source records are not summaries.** A normalized Source Record must include a **Source-to-Design Impact** section: requirements, constraints, risks, assumptions, open questions, affected architecture elements, and required downstream artifacts. Do not produce a generic digest that only restates the source.
12. **Artifact coverage must close.** When a source introduces a requirement/constraint/risk/assumption/decision candidate, update `workflow/artifact-coverage-matrix.md` and create or update the required artifact. Missing required artifacts are a design-closure violation, not a cosmetic issue.
13. **Stakeholder execution handoff is part of architecture.** Final baseline must include who does what: CX, UX, PM/PO, Client, Server/Cloud, QA, Data/ML, Security/Privacy, Release/Ops, and any project-specific owner. Architecture that cannot be allocated to teams is incomplete.
14. **이해도 테스트.** 모든 공유 산출물은 다음 5개 질문에 답할 수 있어야 한다: (1) 왜 필요한가? (2) 안 하면 어떤 문제가 생기는가? (3) 어떤 선택을 했는가? (4) 왜 다른 선택을 하지 않았는가? (5) 누가 무엇을 해야 하는가? 특히 (5)는 `arch/stakeholder-action-plan.md`로 답한다.

<!-- ysda-arch-runtime-mirror: Common v1.0.3 (A31/A9/A20/A18/A32/A33/A34/A5/A35) -->
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
   - current-version release ADR exists and is Accepted;
   - diagrams agree with referenced text/ADR/QS; latency/memory views link their QS and budgets;
   - scoped bundles keep the host repo unchanged and close the redaction checklist.
7. Commit only when artifacts, diagrams, traceability, and STATUS agree. Never push without owner approval.
8. Report compactly: phase / changed artifacts / open decisions / next action.
