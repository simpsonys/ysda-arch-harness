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
- `채택 결정으로 architecture.md를 arc42/C4 스켈레톤으로 통합 명세해줘.`

**Phase 8 — 구조 평가**
- `구조를 ATAM 방식으로 평가하고 우선순위 QS를 budget 대비 판정해줘. Design Baseline 게이트 점검.`

**Hand-off (owner 승인)**
- `Design Baseline 기준으로 다운스트림 코딩 하네스용 hand-off 패키지를 만들어줘.`
