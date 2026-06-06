# Q&A 로그 — Arch Harness (Common §A11)

## 2026-06-06
### Q1: 왜 개인 harness에 mode만 추가하지 않고 별도 family로 분리했나?
* **A:** 코딩용과 설계용은 lifecycle·게이트·1순위 품질이 다르고, 한 리포에 혼재하면 §A0 목적이 흐려진다. 거버넌스
  코어만 파생(ADR-001)하고 lifecycle은 분리하는 것이 유지보수에 유리. 개선은 양쪽 이식 원칙으로 관리.
* **연결:** [ADR-001](../arch/adr-001-v1.0.0-initial-arch-harness-baseline.md), `doc/personal-vs-arch-harness.md`.

### Q2: latency/memory를 어떻게 "1순위"로 강제하나?
* **A:** 하네스 품질 모델은 placeholder 정책을 제공하고, 적용 프로젝트의 `arch/quality/`에 승인
  latency/memory budget을 1급 산출물로 둔다(§A14). 성능 QS의 Response Measure가 승인 budget 값을 인용하도록
  강제하며(§D4), Design Baseline 게이트(§D8)에서 `<TBD>` 없는 우선순위 QS 판정을 필수화한다.
* **연결:** `quality/quality-attribute-model.md`, `arch/quality/`, 표준 §D4/§D8.

### Q3: 왜 최상위 quality와 적용 프로젝트의 arch/quality를 분리하나?
* **A:** 최상위 `quality/`는 하네스 자체 placeholder 가이드다. 제품 승인 목표는 `arch/quality/`에만 두어 sample
  값을 실제 목표로 오인하는 위험을 차단한다.
* **연결:** [ADR-002](../arch/adr-002-v1.0.1-consistency-polish.md), Common §A7/§A14.

### Q4: 회사/대형 저장소 분석의 기본 변경 정책은 무엇인가?
* **A:** host repo unchanged, read-only analysis, no commit, no push가 기본이다. 결과는 scoped sidecar에 기록하고
  공유 전 redaction checklist를 닫는다.
* **연결:** `templates/scoped-sidecar/README.md`, Common §A20.
