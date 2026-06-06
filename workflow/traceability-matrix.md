# 추적성 매트릭스 (Traceability) — Arch Harness

Common §A13. 모든 **우선순위 QS** 는 ADR과 평가 행을 가져야 Design Baseline(§D8) 승인 가능.

| Use case / Quality scenario | 결정 드라이버 | ADR | 아키텍처 요소 / 다이어그램 | 평가 결과 (budget 대비) |
|---|---|---|---|---|
| QS-001 Latency (`p95 ≤ <P95_TARGET_MS>`) | Latency | [ADR-00x] | `arch/views/latency-critical-path.md` | <만족/조건부/미달> |
| QS-002 Memory (`<MAX_RSS_MB>`) | Memory | [ADR-00x] | `arch/views/memory-lifecycle.md` | <만족/조건부/미달> |
| (하네스 자체) v1.0.0 초기 baseline | Maintainability | [ADR-001](../arch/adr-001-v1.0.0-initial-arch-harness-baseline.md) | Common/mode 분리 | Passed |
| (하네스 자체) v1.0.1 consistency polish | Safety / Consistency | [ADR-002](../arch/adr-002-v1.0.1-consistency-polish.md) | lifecycle / sidecar / validation | Passed |

> harness v1.0.1
