# 방법론 레퍼런스 (Arch Harness가 따르는 것)

본 harness는 새로 발명한 게 아니라 검증된 설계 방법론을 조합한다.

## 차용한 워크플로우
- **AgentK (`arch-with-ai`, YongJin-Cho/bosornd)** — 8~9단계 구조 설계 워크플로우(시스템 정의→기능→도메인→품질
  시나리오→후보 구조[동작/개발]→평가→구조 명세→구조 평가→코드 생성)와 단계별 전문 에이전트 구성. 본 harness의
  Phase 골격(§D2)이 여기서 옴.
- **AWS AI-DLC** — 요구사항 정의(Inception)/구현(Construction) 단계 분리, common/ 표준 + docs/ 산출물 추적이 전
  단계에 적용되는 구조. "설계용/코딩용 harness 분리"의 정당화.

## 설계 방법론
- **SEI Attribute-Driven Design (ADD)** — 품질속성을 드라이버로 구조를 도출.
- **Quality Attribute Scenario (6-part)** — Source/Stimulus/Artifact/Environment/Response/Response Measure.
- **ATAM** — sensitivity / trade-off / risk-nonrisk 로 구조 평가(§D6).
- **arc42** — 경량 아키텍처 문서 골격(§D7).
- **C4 model** — Context/Container/Component/Code 레이어링(§A18, 다이어그램).
- **MADR** — Markdown ADR 템플릿(§A8).
- **ISO/IEC 25010** — 품질 모델 어휘(Performance efficiency의 Time behaviour=Latency, Resource utilization=Memory 등).

## 거버넌스 출처
- **YSDA Harness (personal/coding) v2.8.9** — Common/mode 분리, AGENTS 미러+마커, Artifact Closure Gate +
  release/version 일관성 게이트, ROLES/IO-CONTRACT/traceability/qna, git+handoff redaction, versionless 파일,
  lightweight escape hatch. 본 harness의 §A 거버넌스가 여기서 파생(ADR-001).
