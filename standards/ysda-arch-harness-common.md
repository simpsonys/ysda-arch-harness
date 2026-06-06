# YSDA Arch Harness Common Core v1.0.0

> Single source of the reusable, project-neutral rules shared by the YSDA Arch Harness (architecture/design)
> mode adapters. The governance core is **derived from YSDA Harness (personal/coding) v2.8.9** and re-oriented
> from a *coding* lifecycle to a *design* lifecycle. Coding-specific rules are intentionally dropped; design,
> quality-attribute, and documentation rules are added. All §A rules below apply to every Arch mode.

Paired with a **mode adapter**: `ysda-arch-design-standard.md` — the architecture design lifecycle (default for
업무용/상품화 설계).

---

## A0. Purpose & non-purpose
This harness makes **AI-assisted architecture design** reproducible, reviewable, and quality-attribute driven. The
deliverable is a **design** (decisions + diagrams + evaluation), not production code. Code generation, if it
happens, is a downstream hand-off (§A30), not the goal. If the work is "implement this feature," use the
**personal/coding** `ysda-harness` instead. Use this harness when the work is "decide and document how a product
should be built so it meets its quality attributes."

## A1. Bootstrap vs runtime
Standards are bootstrap/reference docs. Rules needed every session — Runtime Work Cycle (§A31), Artifact Closure
Gate (§A9), git safety (§A20), compact output (§A19), mermaid-first (§A18) — are summarized into `AGENTS.md` at
init so daily prompts stay short. The agent reads `AGENTS.md`, not the full standard, during normal work.

## A2. Common Core + mode-adapter split
Shared rules live here (§A*). Lifecycle rules live in the mode adapter (§D*). A mode file references Common and must
not restate Common rules (drift control). Inherited from personal harness ADR-001 lineage.

## A3. Project-local snapshot & version metadata
Project-local home is `.ysda-arch-harness/` (frozen `harness-common.md` + `harness-mode.md`, agent-maintained
`harness-version.json`, `invocation-prompts.md`, ignored `local/ tmp/ run/ cache/`). Minimal version shape:

```json
{
  "harness_family": "ysda-arch-harness",
  "harness_version": "1.0.0",
  "applied_mode": "design | audit | scoped | upgrade | self-hosted",
  "applied_date": "YYYY-MM-DD",
  "canonical_root": "<git url or local sync path>",
  "source_common": "standards/ysda-arch-harness-common.md",
  "source_mode": "standards/ysda-arch-design-standard.md",
  "common_checksum": "<sha256>",
  "mode_checksum": "<sha256>",
  "agents_md_mirror_version": "1.0.0",
  "notes": ["Project-local snapshot. Update through harness init/upgrade, not manual edits."]
}
```

Active canonical files are **versionless** in filename; version lives in the header + `harness-version.json`.
History is carried by Git and `doc/harness-evolution-history.md`, not by hoarding `*_v1_*` copies (`doc/` for
internal docs; `docs/` only for a published site).

## A4. AGENTS.md runtime mirror + version marker
The mirrored runtime block opens with `<!-- ysda-arch-runtime-mirror: Common v1.0.0 (A31/A9/A20/A18) -->`, and the
same version is stamped as `agents_md_mirror_version`. A lagging marker means the runtime block is stale and must be
re-mirrored. (Inherited from personal harness v2.8.7.)

## A5. Language
Owner communication and durable Korean docs are **Korean**. `AGENTS.md` stays **English**. Design artifacts are
Korean by default, but diagram labels, quality-attribute names, and tactic names may stay in English where that is
the standard term.

## A6. Roles
See `workflow/ROLES.md`. Owner is always required and is the only role that moves an ADR to `Accepted`, authorizes a
design baseline, or authorizes a downstream code hand-off. Design roles: Owner, Architect, Quality Analyst, Domain
Modeler, Reviewer/Evaluator (no code Implementer/QA in this harness).

## A7. Source of truth & artifact set
```text
arch/
  system.md                 # system + business drivers (Phase 1)
  usecases.md               # use case list (Phase 2); usecase/UC-nnn.md for detail
  domain/model.md           # domain model (Phase 3)
  quality/
    quality-scenarios.md    # QS index (Phase 4)
    QS-nnn-<title>.md        # one quality attribute scenario each (6-part)
    qualities.md            # selected/prioritized quality requirements
  candidate/
    candidates.md           # candidate index
    QS-nnn-<title>.md        # per-driver candidate structures (behavioral + dev views)
  decision/
    adr-nnn-<title>.md       # ADRs (MADR + driver matrix, §A8)
    evaluations.md           # candidate evaluation (ATAM-style, §D6)
  architecture.md           # consolidated architecture description (arc42/C4, §D7)
  evaluation/
    decisions.md             # identified architectural decisions
    evaluation.md            # final quality-attribute satisfaction evaluation (Phase 8)
```

## A8. ADR discipline (2-step + driver matrix)
Every non-trivial decision is an ADR (`templates/adr.md`, MADR-style):
1. **Proposed**: context, decision drivers **linked to QS-nnn**, ≥2 options in a driver/quality-attribute matrix
   with pros/cons, recommended option + Decision brief.
2. **Accepted/Rejected/Superseded**: only the **owner** sets `Accepted`. The decision is woven into
   `architecture.md` **after** acceptance, never before.
Matrix columns must include the prioritized quality attributes for the decision (e.g. Latency, Memory,
Modifiability) so every decision traces to the driver it serves.

## A9. Artifact Closure Gate (design Freshness Pass)
Before any completion commit:
1. **Decision Closure** — touched ADRs have correct status.
2. **Traceability Sync** — matrix links each prioritized QS → ADR → diagram → evaluation; no prioritized QS
   without a decision and an evaluation.
3. **Diagram Freshness** — every structural claim has a mermaid diagram; every diagram has an intent caption (§A18).
4. **Status Sync** — STATUS reflects phase/next action/blockers/open decisions.
5. **Progress + Q&A** — append progress; append qna-log for durable decisions/discarded options.
6. **Registry Sync** — artifact-registry updated.
7. **Version Consistency** — §A9.1.
8. **Stage & Inspect** before commit.

### A9.1 Release/version consistency gate (mechanical)
`archdev check` fails if the ADR(s) matching the current `harness_version` are not `Accepted` (a version stamp must
not run ahead of approval) and if `traceability-matrix.md`/`artifact-registry.md`/`reports/progress.md`/
`doc/harness-evolution-history.md` don't reference the current version. Run it before every completion commit.
(Adapted from personal harness v2.8.9.)

## A10. Concept capture & A11. Q&A logging
Reusable knowledge → `doc/{title}.md` + register. Project-relevant Q&A/rationale/discarded options/owner decisions
→ `reports/qna-log.md` (append-only, ≤~5/session). Promote concept→doc, decision→ADR; leave a link.

## A12. ID allocation
`UC-nnn`/`QS-nnn`/`ADR-nnn` zero-padded, never reused. Reserve IDs via the index file, not `max+1` (race-safe).

## A13. Traceability
`workflow/traceability-matrix.md` is the single grid: Use case / Quality scenario → Decision driver → ADR →
Architecture element / Diagram → Evaluation result. Every *prioritized* QS traces to ≥1 ADR and ≥1 evaluation row
before a design baseline (§D8).

## A14. Quality attribute model
`quality/quality-attribute-model.md` defines the quality vocabulary (ISO/IEC 25010 based) and the first-class
**latency budget** and **memory budget** for this product family. Every performance QS references a concrete number
in those budgets (no "fast enough").

## A15. Lightweight design escape hatch
Depth modes Lite/Standard/Full (§D3). Lite still needs ≥1 prioritized QS, ≥1 ADR with a driver matrix, ≥1 context
diagram, and an evaluation note. Below that it is a sketch, not a design, and must be labeled so.

## A16. Non-goals discipline
Every system/QS/ADR states explicit **Non-Goals** and out-of-scope quality attributes. Unbounded scope is the top
failure mode of design; name what you are *not* solving.

## A18. Mermaid-first diagram rule
Diagrams are **mermaid** embedded in markdown (not image binaries) so they version/diff in Git. Each diagram
declares its **view** (context/container/component/runtime-sequence/deployment/state/domain-ERD per
`templates/mermaid-cookbook.md`), carries a one-line **intent caption**, and uses C4 layering rather than one giant
diagram. A structural prose claim without a diagram, or a diagram without a caption, fails §A9.

## A19. Compact output
Owner reports: what changed / which phase / open decisions / next action. Long reasoning lives in artifacts.

## A20. Git & confidentiality safety
Never `git push` without explicit owner approval. No destructive data/history op without an ADR. For Scoped/handoff
bundles (§D10), redact internal infra paths/identifiers (incl. `canonical_root`/`source_*`) and secrets before
sharing — critical for 업무용, where design docs cross teams.

## A30. Downstream code hand-off (bridge to coding harness)
When the owner authorizes implementation, produce a **hand-off package** (accepted `architecture.md`, module view,
latency/memory budgets, a generated `AGENTS.md` for the downstream repo) — not code. The downstream repo adopts the
**personal/coding `ysda-harness`** to build. Design here, build there.

## A31. Runtime Work Cycle (mirrored into AGENTS.md)
1. Read STATUS + active phase artifacts before editing.
2. Identify the active unit: phase step / quality scenario / ADR / evaluation.
3. Do not jump to a solution before quality scenarios are prioritized (§D4). No "vibe architecture."
4. Produce the artifact for the active unit, with mermaid diagrams (§A18) and Non-Goals (§A16).
5. For any decision, write/append an ADR with a driver matrix tied to QS (§A8).
6. Before commit, run the Closure Gate / Freshness Pass (§A9) incl. `archdev check`.
7. Commit only when artifacts, diagrams, traceability, STATUS agree. Never push without owner approval.
8. Report compactly (§A19).

## Changelog
```text
v1.0.0 — initial Arch Harness Common Core.
  Forked governance core from personal ysda-harness v2.8.9 (Common/mode split, AGENTS mirror+marker, Artifact
  Closure Gate + release/version consistency gate, ROLES/IO-CONTRACT/traceability/qna, git+handoff redaction,
  versionless active files, lightweight escape hatch). Replaced the coding lifecycle with a quality-attribute-
  driven design lifecycle (design mode adapter). Added A14 latency/memory budgets, A18 mermaid-first, A16
  Non-Goals, A30 downstream hand-off. Dropped coding/test-centric rules.
```
