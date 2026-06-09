# Prompt: Regenerate Architecture Artifacts with YSDA Arch Harness v1.0.2

You are working inside a YSDA Arch Harness repository that has been upgraded to v1.0.2.

Goal:
Regenerate and repair the existing architecture artifacts so they follow the updated business-oriented design harness rules. This is an architecture design project, not an implementation project. The output must support stakeholder alignment, requirement refinement, and downstream work allocation.

Context:
- The harness is for work/business architecture design, not a personal coding project.
- Focus on architecture, requirements refinement, stakeholder alignment, and implementation-readiness handoff.
- Do not jump into coding.
- The final deliverables must help assign work to CX, UX, PM/PO, Client, Server/Cloud, QA, Security/Privacy, Release/Ops, and any project-specific owners.

Required policy updates:
1. Shared stakeholder deliverables must be Korean by default. Keep technical terms in English.
2. ADRs and detailed technical registers may be English or bilingual if useful, but Executive Summary, Stakeholder Summary, Implementation Readiness Report, Stakeholder Action Plan, and Work Breakdown must be Korean unless explicitly requested otherwise.
3. Source Records must not be generic summaries. Each normalized source must include Source-to-Design Impact:
   - Requirements extracted
   - Constraints extracted
   - Risks
   - Assumptions
   - Open Questions
   - Architecture Impact
   - Required downstream artifacts
   - Stakeholder action impact
4. Every source-derived requirement, constraint, risk, assumption, or decision candidate must be registered in `workflow/artifact-coverage-matrix.md`.
5. Missing required artifacts are closure blockers. Mark them as `Missing`, then create or update the required artifacts where possible.
6. The final baseline must include stakeholder execution handoff, not only architecture description.

Tasks:

## 1. Read current repository state
- Read `AGENTS.md`.
- Read `workflow/STATUS.md`.
- Read `workflow/artifact-registry.md`.
- Read `workflow/traceability-matrix.md`.
- Read `workflow/artifact-coverage-matrix.md` if present.
- Inspect `arch/sources/originals/` and `arch/sources/normalized/`.
- Inspect existing architecture artifacts under `arch/`.

## 2. Repair source processing
For every normalized Source Record:
- Preserve provenance metadata.
- If it is only a summary/digest, rewrite it into the v1.0.2 Source Record structure.
- Add Source-to-Design Impact.
- Extract requirement/constraint/risk/assumption/open-question entries.
- Register required artifacts in `workflow/artifact-coverage-matrix.md`.

## 3. Repair missing artifacts
Using the artifact coverage matrix:
- Identify all `Missing` required artifacts.
- Create or update required artifacts when enough information exists.
- If information is insufficient, keep the item as `Missing` or `Blocked` with owner/check question.
- Do not hide gaps by writing vague filler.

## 4. Korean stakeholder deliverables
Create or update these deliverables in Korean, keeping technical terms in English:
- `arch/executive-summary.md`
- `arch/stakeholder-summary.md`
- `arch/decision-dashboard.md`
- `arch/stakeholder-action-plan.md`
- `arch/implementation-readiness-report.md`

Each stakeholder-facing document must include:
- `한눈에` section
- mermaid diagram when structure/flow is involved
- glossary/용어 section when jargon appears
- clear team actions and outputs

## 5. Stakeholder work allocation
In `arch/stakeholder-action-plan.md`, explicitly cover at least:
- CX: customer journey, VOC, error/fallback experience, validation points
- UX: confirmation UI/voice flow, failure state, fallback, screen/interaction flow
- PM/PO: scope, milestone, release boundary, decision schedule
- Client: local component, permission/storage/API integration, component design
- Server/Cloud: policy sync, metadata/API, remote config, data contract if applicable
- QA: test matrix, failure injection, safety validation, regression strategy
- Security/Privacy: data boundary, logging, redaction, permission/privacy review
- Release/Ops: rollout, telemetry, monitoring, rollback, launch gate

## 6. Completion definition
Update `arch/implementation-readiness-report.md` so it clearly states whether the current design is:
- Ready
- Conditionally Ready
- Not Ready

Use evidence from:
- Source coverage
- Quality scenarios
- ADRs
- Risk register
- Traceability matrix
- Stakeholder action plan

## 7. Workflow trackers
Update:
- `workflow/STATUS.md`
- `workflow/artifact-registry.md`
- `workflow/artifact-coverage-matrix.md`
- `workflow/traceability-matrix.md`
- `reports/progress.md`
- `reports/qna-log.md` if durable decisions or discarded options were found

## 8. Validation
Run:
```bash
python scripts/archdev.py check
python scripts/archdev.py report
```

Then fix any real errors. If a check remains failing because information is genuinely missing, leave it as an explicit blocker with owner/question rather than inventing facts.

Final response format:
- Changed artifacts
- New artifacts
- Remaining blockers
- Stakeholder action highlights
- Validation result
