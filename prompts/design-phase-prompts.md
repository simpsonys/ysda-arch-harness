# 설계 단계별 프롬프트 (AgentK 흐름 차용)

> 각 프롬프트는 해당 phase의 산출물 1개를 만든다. owner는 한 줄로 던지고, 에이전트는 AGENTS.md 규칙대로 동작.

**Phase 1 — 시스템 정의**
- `시스템 정의를 작성해줘: <과제 한 줄>. 비즈니스 드라이버와 Non-Goals 포함.`

**Phase 2 — 기능 명세**
- `구조에 영향 주는 핵심 use case를 식별해줘.`
- `UC-001 상세 명세를 작성해줘.`

**Phase 3 — 도메인 모델**
- `use case를 분석해 도메인 모델(mermaid ERD/class)을 만들어줘.`

**Phase 4 — 품질 시나리오 (핵심)**
- `품질 시나리오를 6-part로 도출해줘. latency/memory는 budget 수치를 인용.`
- `QS-001 상세 명세를 작성하고 우선순위를 매겨줘.`
- `우선순위 QS를 qualities.md에 확정해줘.`

**Phase 5 — 후보 구조**
- `QS-001(latency)을 만족시키는 후보 구조를 동작/개발 view로, 적용 전술과 함께 설계해줘.`
- `메모리 관점 후보 구조도 설계하고 latency 후보와의 trade-off를 노출해줘.`

**Phase 6 — 평가 & 결정**
- `후보들을 driver matrix로 평가하고 채택 ADR(Proposed)을 작성해줘.`
- (owner) `ADR-00x를 Accepted로 승인.`

**Phase 7 — 구조 명세**
- `채택 결정으로 arch/architecture-brief.md와 arch/views/를 arc42/C4 스켈레톤으로 통합 명세해줘.`

**Phase 8 — 구조 평가**
- `구조를 ATAM 방식으로 평가하고 우선순위 QS를 budget 대비 판정해줘. Design Baseline 게이트 점검.`

**Hand-off (owner 승인)**
- `Design Baseline 기준으로 다운스트림 코딩 하네스용 hand-off 패키지를 만들어줘.`


---

## 업무용 보강 프롬프트

**Source ingestion — 요약 금지**
- `첨부/원본 자료를 arch/sources/originals에 보존한 것으로 간주하고 Source Record를 작성해줘. 단순 요약이 아니라 Source-to-Design Impact를 반드시 포함해. Requirements, Constraints, Risks, Assumptions, Open Questions, Required Artifacts, Stakeholder Action까지 뽑고 workflow/artifact-coverage-matrix.md 업데이트 항목도 제안해줘.`

**Artifact coverage 점검**
- `현재 Source Record와 요구사항을 기준으로 workflow/artifact-coverage-matrix.md를 갱신하고 Missing required artifact를 모두 찾아줘. Missing은 설계 closure blocker로 표시해.`

**Korean stakeholder package**
- `현재 산출물을 바탕으로 한국어 Stakeholder Summary, Decision Dashboard, Implementation Readiness Report, Stakeholder Action Plan을 생성/갱신해줘. 기술 용어는 English 유지하고 CX/UX/PM/Client/Server/QA/Security/Ops별 해야 할 일과 출력 산출물을 명시해.`

**Baseline regeneration**
- `개선된 v1.0.2 규칙 기준으로 기존 arch 산출물을 재검토해. 영어로 된 공유 산출물은 한국어로 바꾸고, Source Record가 요약집이면 Source-to-Design Impact로 보강하고, 누락 산출물은 artifact-coverage-matrix에 Missing으로 등록한 뒤 필요한 문서를 생성해. 마지막에 archdev check와 report 기준의 남은 gap을 정리해.`
