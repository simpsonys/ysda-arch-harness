# YSDA Arch Harness (업무/설계용) v1.0.0

> AI-assisted **architecture design** harness. Deliverable = 설계(결정·다이어그램·평가), not code.
> 코딩은 개인용 `ysda-harness`로. 본 harness는 상품화 설계용이며 **latency·memory** 등 품질속성과 **설계 문서**가
> 코드보다 우선이다.

## 무엇인가
- 거버넌스 코어(§A)는 검증된 개인용 `ysda-harness v2.8.9`에서 파생(Common/mode 분리, AGENTS 미러, Artifact
  Closure Gate + release 일관성 게이트, traceability/qna, redaction).
- 설계 lifecycle(§D)은 SEI **ADD** + AgentK(`arch-with-ai`) 8단계 + arc42/C4 + ATAM + ISO 25010을 조합.
- 다이어그램은 **mermaid-first**(C4 레이어링), 모든 성능 QS는 **latency/memory budget** 수치를 인용.

## 빠른 시작
1. `standards/` 2개와 `AGENTS.md`를 설계 리포에 둔다.
2. `prompts/design-phase-prompts.md`의 Phase 1부터 한 줄씩 호출(`시스템 정의부터 시작하자: <과제>`).
3. 각 phase 산출물은 `arch/`에 쌓이고, 결정은 ADR로, 평가는 `evaluation/`로.
4. 커밋 전 `python scripts/archdev.py check` 로 closure/일관성 점검.

## 구조
```text
standards/   Common Core(§A) + Design mode(§D)
AGENTS.md    설계 에이전트 런타임 규칙(영어, 미러 마커)
workflow/    STATUS / ROLES / IO-CONTRACT / artifact-registry / traceability-matrix
quality/     품질 모델 + latency/memory budget (1순위 드라이버)
templates/   system / QS(6-part) / ADR(MADR+driver matrix) / candidate / architecture(arc42+C4)
             / evaluation(ATAM) / budget / mermaid-cookbook
prompts/     단계별 owner 단축 프롬프트(AgentK 흐름)
doc/         방법론 레퍼런스 / personal-vs-arch 비교 / 진화 이력
arch/        설계 산출물(런타임 채워짐) + 하네스 자체 ADR
scripts/     archdev.py (compliance check)
```

## 개인용과의 분리
`doc/personal-vs-arch-harness.md` 참고. 설계는 여기서, 빌드는 개인용 harness에서. 개선은 양쪽 이식.

## 참고
`doc/methodology-references.md` — AgentK / AI-DLC / ADD / QAS / ATAM / arc42 / C4 / MADR / ISO 25010.
