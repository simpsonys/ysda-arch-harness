# Q&A 로그 — Arch Harness (Common §A11)

## 2026-06-06
### Q1: 왜 개인 harness에 mode만 추가하지 않고 별도 family로 분리했나?
* **A:** 코딩용과 설계용은 lifecycle·게이트·1순위 품질이 다르고, 한 리포에 혼재하면 §A0 목적이 흐려진다. 거버넌스
  코어만 파생(ADR-001)하고 lifecycle은 분리하는 것이 유지보수에 유리. 개선은 양쪽 이식 원칙으로 관리.
* **연결:** [ADR-001](../arch/adr-001-derive-governance-core-from-ysda-harness.md), `doc/personal-vs-arch-harness.md`.

### Q2: latency/memory를 어떻게 "1순위"로 강제하나?
* **A:** 품질 모델에 latency/memory budget을 1급 산출물로 두고(§A14), 성능 QS의 Response Measure가 budget 수치를
  인용하도록 강제(§D4). Design Baseline 게이트(§D8)에서 우선순위 QS의 budget 대비 판정을 필수화.
* **연결:** `quality/quality-attribute-model.md`, 표준 §D4/§D8.
