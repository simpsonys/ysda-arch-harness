# 추적성 매트릭스 (Traceability) — Arch Harness

Common §A13. 모든 **우선순위 QS** 는 ADR과 평가 행을 가져야 Design Baseline(§D8) 승인 가능.

| Use case / Quality scenario | 결정 드라이버 | ADR | 아키텍처 요소 / 다이어그램 | 평가 결과 (budget 대비) |
|---|---|---|---|---|
| QS-001 Latency (p95 ≤ <n> ms) | Latency | [ADR-00x] | <요소> / Runtime sequence | <만족/조건부/미달> |
| QS-002 Memory (≤ <n> MB/inst) | Memory | [ADR-00x] | <요소> / Deployment | <만족/조건부/미달> |
| (하네스 자체) 거버넌스 코어 파생 | Maintainability | [ADR-001](../arch/adr-001-derive-governance-core-from-ysda-harness.md) | Common/mode 분리 | Passed |

> harness v1.0.0
