# Template Index

## 프로젝트 설계
- `system-definition.md` → `arch/architecture-brief.md` 시작점
- `quality-scenario.md` → `arch/quality/QS-nnn-*.md`
- `latency-budget.md`, `memory-budget.md` → `arch/quality/`
- `candidate-architecture.md` → `arch/candidates/`
- `candidate-comparison-matrix.md` → `arch/candidates/comparison-matrix.md`
- `adr.md` → `arch/adr-nnn-*.md`
- `architecture-description.md` → `arch/architecture-brief.md` + `arch/views/`
- `architecture-evaluation.md` → `arch/evaluation/architecture-evaluation.md`
- `risk-register.md`, `open-questions.md`, `review-log.md` → `arch/evaluation/`
- `mermaid-cookbook.md` → required view 생성·동기화 규칙

## 기존 과제(Brownfield) · 통합 · 리더십
- `sources-manifest.md` → `arch/sources/originals/_manifest.md` (원본 다수 일괄 흡수용 출처·날짜 매핑표)
- `source-record.md` → `arch/sources/normalized/SRC-nnn-*.md` (원본 보존 + LLM-readable 정리물; 출처·타임스탬프 필수)
- `stakeholder-action-plan.md` → `arch/stakeholder-action-plan.md` (담당자별 실행: CX/UX/PM/Client/Server/QA/Security/Ops)
- `accessibility-checklist.md` → 공유 산출물이 모든 stakeholder에게 쉬운지(언어·구조·책임) closure
- `assumption-register.md` → `arch/assumptions/register.md` (가정 명세; load-bearing 가정은 분기 후보 강제)
- `as-is-intake.md` → `arch/as-is/intake.md` (Phase 0, 소스 없는 기존자산 흡수; 모든 as-is는 Assumption)
- `interface-contract.md` → 통합 이음새(seam)별 제품 모듈 계약 (하네스 IO-CONTRACT와 구분)
- `work-breakdown.md` → Design Baseline 후 작업패키지 분해·할당·크리티컬 패스
> 흐름·근거는 `doc/adoption-and-brownfield.md` 참고. 리더 digest는 `python scripts/archdev.py report`.

## Scoped Sidecar
`scoped-sidecar/`는 host repo를 변경하지 않는 read-only 분석과 redacted handoff bundle의 시작점이다.

> 샘플 값을 제품 목표로 사용하지 않는다. Owner/Reviewer가 확인하기 전에는 `<TBD>`로 둔다.
