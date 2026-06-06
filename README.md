# YSDA Arch Harness (업무/설계용) v1.0.1

> AI-assisted **architecture design** harness. Deliverable = 설계(결정·다이어그램·평가), not code.
> 코딩은 개인용 `ysda-harness`로. 본 harness는 상품화 설계용이며 **latency·memory** 등 품질속성과 **설계 문서**가
> 코드보다 우선이다.

## 무엇인가
- 거버넌스 코어(§A)는 검증된 개인용 `ysda-harness v2.8.9`에서 파생(Common/mode 분리, AGENTS 미러, Artifact
  Closure Gate + release 일관성 게이트, traceability/qna, redaction).
- 설계 lifecycle(§D)은 SEI **ADD** + AgentK(`arch-with-ai`) 8단계 + arc42/C4 + ATAM + ISO 25010을 조합.
- 다이어그램은 **mermaid-first**(C4 레이어링), 모든 성능 QS는 **latency/memory budget** 수치를 인용.

## 빠른 시작
1. `standards/`와 `AGENTS.md`를 설계 리포에 둔다.
2. `prompts/design-phase-prompts.md`의 Phase 1부터 한 줄씩 호출(`시스템 정의부터 시작하자: <과제>`).
3. 각 phase 산출물은 `arch/`에 쌓이고, 결정은 `arch/adr-*.md`, 평가는 `arch/evaluation/`에 기록.
4. 커밋 전 `python scripts/archdev.py check` 로 closure/일관성 점검.

## 구조 & 주요 파일 역할

### 1. `standards/` — 아키텍처 표준 및 가이드라인
* **[ysda-arch-harness-common.md](file:///D:/Project/ysda-arch-harness/standards/ysda-arch-harness-common.md)**: 하네스 공통 규칙, 품질 모델, 버전/릴리스 정합성 게이트 및 공통 거버넌스 정의.
* **[ysda-arch-design-standard.md](file:///D:/Project/ysda-arch-harness/standards/ysda-arch-design-standard.md)**: 아키텍처 설계 라이프사이클(8단계) 및 품질 속성 기반 아키텍처 전술(Tactic) 설계 방식 정의.
* **[artifact-lifecycle.md](file:///D:/Project/ysda-arch-harness/standards/artifact-lifecycle.md)**: 각 아키텍처 산출물의 생성·갱신·종료 조건 및 아키텍처 불일치(Drift) 방지 매트릭스.
* **[README.md](file:///D:/Project/ysda-arch-harness/standards/README.md)**: 표준 디렉토리 내의 파일 구성 안내.

### 2. `workflow/` — 프로젝트 관리 및 추적성
* **[STATUS.md](file:///D:/Project/ysda-arch-harness/workflow/STATUS.md)**: 현재 진행 단계(Phase), 우선순위 품질 시나리오(Top QS), 활성 작업 및 블로커 관리 대시보드.
* **[traceability-matrix.md](file:///D:/Project/ysda-arch-harness/workflow/traceability-matrix.md)**: Use Case/QS -> 아키텍처 의사결정(ADR) -> 다이어그램 -> 평가 결과를 1대1로 연결하는 추적성 매트릭스.
* **[artifact-registry.md](file:///D:/Project/ysda-arch-harness/workflow/artifact-registry.md)**: 현재 저장소에 등록되어 일관성 검증을 거치는 활성 아키텍처 산출물 목록.
* **[IO-CONTRACT.md](file:///D:/Project/ysda-arch-harness/workflow/IO-CONTRACT.md)**: 단계별 입력값과 출력값에 대한 정합성 및 의존 관계 규약.
* **[ROLES.md](file:///D:/Project/ysda-arch-harness/workflow/ROLES.md)**: Owner, Architect, Reviewer 등 역할 정의 및 승인 권한 명시.

### 3. `templates/` — 아키텍처 설계 템플릿
* **[system-definition.md](file:///D:/Project/ysda-arch-harness/templates/system-definition.md)**: 시스템 목적, 범위, 비즈니스 드라이버, 제약 및 명시적 Non-Goals 정의 템플릿.
* **[quality-scenario.md](file:///D:/Project/ysda-arch-harness/templates/quality-scenario.md)**: SEI 표준 6-part(Source, Stimulus, Artifact, Environment, Response, Response Measure) 품질 시나리오 작성 템플릿.
* **[latency-budget.md](file:///D:/Project/ysda-arch-harness/templates/latency-budget.md)** / **[memory-budget.md](file:///D:/Project/ysda-arch-harness/templates/memory-budget.md)**: 성능 검증용 정량 목표치(p50/p95/p99, RSS, Heap 등) 및 승인 이력 관리 템플릿.
* **[candidate-architecture.md](file:///D:/Project/ysda-arch-harness/templates/candidate-architecture.md)**: 품질 시나리오 만족을 위해 고안된 대안 구조(Runtime & Module 뷰) 설계 템플릿.
* **[candidate-comparison-matrix.md](file:///D:/Project/ysda-arch-harness/templates/candidate-comparison-matrix.md)**: 후보군 간의 아키텍처 전술 대비 품질 속성(Sensitivity, Trade-off) 비교 매트릭스.
* **[adr.md](file:///D:/Project/ysda-arch-harness/templates/adr.md)**: 아키텍처 결정 레코드(ADR) 작성 템플릿.
* **[architecture-description.md](file:///D:/Project/ysda-arch-harness/templates/architecture-description.md)**: arc42 및 C4 모델 기반의 최종 아키텍처 명세 양식.
* **[architecture-evaluation.md](file:///D:/Project/ysda-arch-harness/templates/architecture-evaluation.md)**: ATAM 기반 정량/정성 만족도 평가 양식.
* **[mermaid-cookbook.md](file:///D:/Project/ysda-arch-harness/templates/mermaid-cookbook.md)**: 8대 필수 다이어그램 가이드라인 및 텍스트/QS/ADR 일치 규칙.
* **[scoped-sidecar/](file:///D:/Project/ysda-arch-harness/templates/scoped-sidecar/)**: 수정이 제한된 회사/대형 저장소 분석을 위한 read-only 사이드카 및 redaction 템플릿 세트.

### 4. `reports/` — 보고 및 이력 관리
* **[progress.md](file:///D:/Project/ysda-arch-harness/reports/progress.md)**: 하네스 적용 및 릴리스 마일스톤 달성 기록 보고서.
* **[qna-log.md](file:///D:/Project/ysda-arch-harness/reports/qna-log.md)**: 설계 과정의 Q&A, Owner 결정 사항 및 반려된 옵션의 durable 기록.

### 5. `scripts/` — 자동 검증 도구
* **[archdev.py](file:///D:/Project/ysda-arch-harness/scripts/archdev.py)**: 필수 산출물 존재 여부, 버전 메타데이터, Sample Target 및 canonical 경로 위반을 검사하는 경량(Standard library only) 검증기.

---


## 프로젝트 산출물 경로
적용 프로젝트의 품질 목표와 설계 산출물은 모두 `arch/` 아래에 둔다. 최상위 `quality/`의 placeholder를 제품
목표로 사용하지 않는다.

```text
arch/
  architecture-brief.md
  usecases.md
  usecases/UC-001-xxx.md
  quality/quality-scenarios.md
  quality/QS-001-xxx.md
  quality/latency-budget.md
  quality/memory-budget.md
  views/
  candidates/
  evaluation/
  adr-001-xxx.md
```

상세 생성·갱신·종료 조건은 `standards/artifact-lifecycle.md`, 템플릿 색인은 `templates/README.md`를 따른다.
수정하지 말아야 하는 회사/대형 저장소를 분석할 때는 `templates/scoped-sidecar/README.md`의 read-only sidecar
구조를 사용한다.

## 개인용과의 분리
`doc/personal-vs-arch-harness.md` 참고. 설계는 여기서, 빌드는 개인용 harness에서. 개선은 양쪽 이식.

## 참고
`doc/methodology-references.md` — AgentK / AI-DLC / ADD / QAS / ATAM / arc42 / C4 / MADR / ISO 25010.
