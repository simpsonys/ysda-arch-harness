# 품질 속성 모델 & 예산 (Quality Attribute Model & Budgets)

Common §A14. 본 하네스가 사용하는 품질 어휘는 **ISO/IEC 25010** 기반이며, 상품화 특성상 **Latency** 와 **Memory/Resource**
를 1순위 드라이버로 둔다. 이 문서는 하네스 자체 가이드이며 제품별 승인 목표는 `arch/quality/`에 작성한다.

> **경고:** 샘플 값을 제품 목표로 사용하지 않는다. Owner/Reviewer가 값을 확인하기 전에는 `<TBD>`로 둔다.

## 1. 품질 어휘 (ISO/IEC 25010 발췌)
- **Performance efficiency** — Time behaviour(=Latency/Throughput), Resource utilization(=Memory/CPU), Capacity.
- Reliability(Availability/Fault tolerance/Recoverability), Maintainability(Modifiability/Testability),
  Security, Scalability, Compatibility, Usability, Portability, Observability(운영 보강).

## 2. Latency Budget Placeholder
구간별로 예산을 쪼개 합이 SLO를 넘지 않게 한다(end-to-end = 각 hop 합).

| 경로 / Hop | p50 | p95 | p99 | 비고 |
|---|---|---|---|---|
| End-to-end SLO | `<P50_TARGET_MS>` | `<P95_TARGET_MS>` | `<P99_TARGET_MS>` | 사용자 체감 |
| 주요 구간 | `<TBD>` | `<TBD>` | `<TBD>` | 타임아웃/백프레셔 명시 |

Cold start는 hop 합산 대상이 아닌 별도 환경 시나리오다.

| 시나리오 | 목표 | 환경 |
|---|---|---|
| Cold start | `<COLD_START_TARGET_MS>` | `<DEVICE_CLASS>` / `<NETWORK_CONDITION>` |

## 3. Memory Budget Placeholder
| 단위 | 한도 | 측정 | 비고 |
|---|---|---|---|
| 인스턴스 RSS | `<MAX_RSS_MB>` | 정상부하 정상상태 | 승인 전 `<TBD>` |
| Peak heap | `<PEAK_HEAP_MB>` | p99 | 스트리밍 상한 |
| 모델/데이터 캐시 | `<MODEL_CACHE_MB>` | per-instance | TTL/evict 정책 명시 |
| 동시성 버퍼 | `<TBD>` | `<CONCURRENT_SESSION_COUNT>` | 백프레셔 트리거 |

## 4. 사용 규칙
- 제품별 성능 QS의 Response Measure는 `arch/quality/`의 owner/reviewer 승인 셀을 인용한다.
- 값이 승인되지 않았으면 임의 숫자 대신 `<TBD>`와 승인 책임자를 남긴다.
- Latency↔Memory는 대표적 trade-off(캐시는 latency↓ memory↑) — ADR/평가에서 trade-off point로 명시(§D6).
- budget이 깨지는 후보는 채택 불가 또는 budget 재협상(owner 결정 + ADR).
