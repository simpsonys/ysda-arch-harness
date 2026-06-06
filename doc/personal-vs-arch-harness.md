# 개인용 vs 업무용 하네스 — 언제 무엇을

| 구분 | ysda-harness (개인/코딩) | ysda-arch-harness (업무/설계) |
|---|---|---|
| 목적 | 기능 구현, 코드 산출 | 아키텍처 설계, 의사결정·다이어그램·평가 산출 |
| 1순위 | 동작하는 코드 + 테스트 | 품질속성(특히 latency/memory) 충족 설계 |
| 게이트 | Implementation Readiness Gate | Design Baseline 게이트(§D8) |
| 핵심 산출물 | task/code/test | QS / ADR / architecture-brief + views / 평가 |
| 다이어그램 | 보조 | **mermaid-first 필수**(C4/runtime/deployment) |
| 코드 | 목표 | 다운스트림 hand-off(§A30), 본체 아님 |
| 공유 | 개인 | 팀 간 핸드오프(redaction 중요) |

## 분리 운영 원칙
- 두 harness는 **거버넌스 코어를 공유**(Common/mode 분리, AGENTS 미러, Closure Gate, traceability)하되 lifecycle만
  다르다. 개선(예: release 일관성 게이트)은 양쪽에 이식한다.
- 설계(업무) → 구현 단계로 갈 때 arch harness의 hand-off 패키지를 코딩 harness가 받아 구현한다. "설계는 여기서,
  빌드는 거기서."
- 한 리포에 둘을 섞지 않는다. 설계 리포는 arch harness, 구현 리포는 personal harness.
