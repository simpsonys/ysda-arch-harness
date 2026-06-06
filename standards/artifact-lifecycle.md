# 아키텍처 산출물 Lifecycle Matrix

이 문서는 각 산출물이 언제 생성·갱신·종료되는지 정의한다. 상세 내용보다 **동기화 상태**가 우선이며, 어느 한
산출물만 최신인 상태는 closure가 아니다.

## 공통 종료 규칙
- 구조적 주장은 intent caption이 있는 Mermaid 다이어그램과 일치해야 한다.
- 우선순위 QS는 ADR, 관련 view, 평가 결과까지 `workflow/traceability-matrix.md`에서 추적되어야 한다.
- 제품 성능 값은 `arch/quality/`의 owner/reviewer 승인 값만 사용하며 승인 전에는 `<TBD>`로 둔다. `<TBD>`가
  남은 High QS는 Baseline closure를 막는다.
- 결정 근거는 ADR에, durable clarification은 `reports/qna-log.md`에, 위험은 risk register에 둔다.
- Scoped bundle은 `redaction-checklist.md`를 닫기 전 공유할 수 없다.

## Lifecycle Matrix
| Artifact | Create condition | Update condition | Closure condition | Minimum done criteria | Common failure modes |
|---|---|---|---|---|---|
| `architecture-brief.md` | 과제·범위가 확인됨 | 범위, 승인 ADR, 주요 view 변경 | 관련 text/view/ADR/QS 일치 | 목적, 범위, 제약, Non-Goals, view 링크 | 승인 전 결정을 반영; 오래된 구조 설명 |
| `usecases.md` | 구조 영향 use case 식별 | use case 추가·우선순위 변경 | 상세 UC와 active 범위가 일치 | ID, 요약, 구조 영향, 상세 링크 | 구현 세부 목록으로 팽창 |
| `usecases/UC-nnn-*.md` | 상세 흐름이 구조 결정을 좌우 | actor·flow·예외 변경 | runtime/QS와 흐름 일치 | actor, precondition, main/exception flow, Non-Goals | runtime view와 불일치 |
| `domain/model.md` | 핵심 개념·경계가 필요 | 개념·관계·경계 변경 | use case/brief와 일치 | 개념, 관계, 경계, intent caption Mermaid | 구현 클래스/DB schema로 조기 하강 |
| `quality-scenarios.md` | 비즈니스·품질 드라이버 식별 | 우선순위·환경·측정값 변경 | High QS가 budget/ADR/view/평가로 추적 | 6-part, 우선순위, 근거, `<TBD>` 책임자 | QS 변경 후 budget 미갱신; 측정 불가 표현 |
| `quality/QS-nnn-*.md` | 개별 품질 드라이버 상세화 | 6-part·우선순위·measure 변경 | budget/ADR/view/evaluation 행과 일치 | 6-part, priority, rationale, Non-Goals | 승인 전 sample 숫자 사용 |
| `latency-budget.md` | latency가 드라이버임 | 경로, 환경, 승인 목표 변경 | QS와 latency critical path가 같은 승인 값 참조 | p50/p95/p99 또는 `<TBD>`, 환경, 승인자 | 샘플 숫자를 제품 목표로 오인 |
| `memory-budget.md` | memory/resource가 드라이버임 | 배치, cache, heap, 동시성 변경 | QS와 memory lifecycle이 같은 승인 값 참조 | RSS/heap/cache/buffer 또는 `<TBD>`, 승인자 | latency 변경 후 memory 영향 누락 |
| `system-context.md` | 시스템 경계·외부 액터 식별 | 경계·외부 의존 변경 | brief와 ADR에 모순 없음 | 시스템, 외부 액터/시스템, trust boundary | 내부 컴포넌트를 context에 혼합 |
| `container-view.md` | 배포 가능 단위 후보 식별 | 단위·책임·연결 변경 | component/deployment/text와 일치 | 주요 container, 책임, protocol/data | diagram만 변경하고 text 방치 |
| `component-view.md` | 핵심 container 내부 책임 분해 | 책임·의존성 변경 | container/runtime/text와 일치 | 주요 component와 허용 의존성 | 구현 클래스 수준으로 과도하게 하강 |
| `runtime-view.md` | 핵심 use case 상호작용 필요 | 순서·fallback·오류 흐름 변경 | 관련 use case/QS/ADR와 일치 | actor, 주요 participant, 정상·실패 흐름 | 오래된 sequence |
| `deployment-view.md` | 배치·자원 경계가 드라이버임 | node, topology, resource 변경 | memory budget/ADR와 일치 | node, runtime unit, 외부 연결, resource placeholder | 승인되지 않은 자원 수치 |
| `dataflow-view.md` | 데이터 이동·보안·소유가 중요 | source/sink/transform 변경 | text/security/risk와 일치 | source, transform, sink, boundary | raw confidential detail 노출 |
| `latency-critical-path.md` | latency High QS 존재 | hop, fallback, budget 변경 | 관련 QS와 latency budget 링크·값 일치 | participant, hop, budget placeholder, 측정점 | QS/budget 링크 누락 |
| `memory-lifecycle.md` | memory High QS 존재 | allocation/cache/release 정책 변경 | 관련 QS와 memory budget 링크·값 일치 | allocate/retain/evict/release 상태 | 해제·상한·백프레셔 누락 |
| `candidates/candidate-nnn-*.md` | High QS를 만족할 대안 필요 | tactic·구조·trade-off 변경 | comparison matrix와 관련 views 일치 | target QS, tactics, runtime/module view, Non-Goals | 단일 옵션만 제시; 구현 선결정 |
| `candidates/comparison-matrix.md` | 비교 가능한 후보 존재 | 후보·driver·근거 변경 | ADR의 선택·근거와 일치 | 후보별 QS driver matrix, risk, recommendation | 평가와 ADR의 선택 불일치 |
| ADR | 비자명한 결정 필요 | driver, option, 상태, 결과 변경 | owner 승인 상태와 downstream 문서 일치 | context, QS driver matrix, options, brief, consequences | 결정 근거가 qna-log에만 존재; STATUS와 상태 불일치 |
| `architecture-evaluation.md` | 후보/승인 결정 평가 가능 | QS, ADR, view, budget 변경 | 모든 High QS 판정·근거·후속 조치 존재 | sensitivity, trade-off, risk/non-risk, 판정 | 근거 없는 통과 |
| `risk-register.md` | 설계 위험 식별 | 확률·영향·완화·owner 변경 | 종료/수용/이관 상태와 근거 명시 | risk, trigger, impact, mitigation, owner | risk를 assumption/open question과 혼합 |
| `open-questions.md` | 답이 없어 설계가 분기됨 | 답·owner·기한·영향 변경 | 답을 적절한 QS/ADR/risk에 승격 | 질문, 영향, owner, next action | 답이 chat에만 존재 |
| `review-log.md` | 리뷰 수행 | finding/결론/후속 변경 | 모든 finding이 처리·수용·이관됨 | 대상, reviewer, finding, disposition | 리뷰 결과와 실제 문서 불일치 |
| `qna-log.md` | durable clarification/폐기 옵션 발생 | 답·연결 문서 확정 | ADR/QS/risk로 승격 후 링크 유지 | 질문, 답, 근거 링크 | 결정 rationale을 qna-log에 묻음 |
| `STATUS.md` | 작업 시작 | phase, next action, blocker, open ADR 변경 | 실제 artifact/ADR 상태와 일치 | phase, active unit, open decisions, next action | STATUS는 complete지만 ADR은 Proposed |
| `traceability-matrix.md` | 첫 우선순위 QS 또는 ADR 생성 | QS/ADR/view/evaluation 변경 | 모든 High QS가 완전한 행을 가짐 | QS → driver → ADR → diagram → evaluation | High QS 누락 |
| scoped `scope.md` | host repo를 수정하지 않는 분석 시작 | read boundary·정책·assumption 변경 | allowed/forbidden boundary와 정책 확인 | 질문, 범위, read boundary, commit/share 정책 | 범위를 넘는 읽기·수정 |
| `redaction-checklist.md` | sidecar/handoff bundle 생성 | bundle 내용 변경 | 모든 항목 확인·redact·승인 | identifier/secret/raw data/performance 검토 | 내부 식별자·raw confidential detail 포함 |
| `handoff-bundle-index.md` | 공유 후보 bundle 구성 | 포함 파일·상태 변경 | redaction 완료, 누락·금지 내용 없음 | artifact, purpose, status, redaction 결과 | 미승인 값 또는 host 경로 포함 |

## Drift 차단 규칙
다음 상태는 모두 closure 실패다.

- `STATUS.md`는 완료인데 관련 ADR이 `Proposed`다.
- QS가 바뀌었지만 latency/memory budget 또는 traceability가 갱신되지 않았다.
- 다이어그램과 text/ADR/QS가 서로 다른 구조를 설명한다.
- owner clarification이 chat에만 있고 `qna-log.md`에 없다.
- decision rationale이 ADR이 아니라 `qna-log.md`에만 있다.
- risk, assumption, open question이 구분되지 않았다.
- 구체 sample performance 값이 제품 목표로 취급됐다.
- scoped bundle에 내부 식별자나 raw confidential detail이 남았다.
- 우선순위 QS가 traceability matrix에서 빠졌다.
