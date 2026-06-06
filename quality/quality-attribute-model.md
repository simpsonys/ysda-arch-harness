# 품질 속성 모델 & 예산 (Quality Attribute Model & Budgets)

Common §A14. 본 제품군의 품질 어휘는 **ISO/IEC 25010** 기반이며, 상품화 특성상 **Latency** 와 **Memory/Resource**
를 1순위 드라이버로 둔다. 모든 성능 QS는 아래 budget의 **구체 수치를 인용** 해야 한다(§D4).

## 1. 품질 어휘 (ISO/IEC 25010 발췌)
- **Performance efficiency** — Time behaviour(=Latency/Throughput), Resource utilization(=Memory/CPU), Capacity.
- Reliability(Availability/Fault tolerance/Recoverability), Maintainability(Modifiability/Testability),
  Security, Scalability, Compatibility, Usability, Portability, Observability(운영 보강).

## 2. Latency Budget (예시 — 프로젝트에서 수치 확정)
구간별로 예산을 쪼개 합이 SLO를 넘지 않게 한다(end-to-end = 각 hop 합).

| 경로 / Hop | p50 | p95 | p99 | 비고 |
|---|---|---|---|---|
| End-to-end API SLO | ≤ 40 ms | ≤ 80 ms | ≤ 150 ms | 사용자 체감 |
| 게이트웨이/인증 | ≤ 3 ms | ≤ 8 ms | — | |
| 비즈니스 로직 | ≤ 10 ms | ≤ 25 ms | — | |
| 데이터 액세스(read) | ≤ 15 ms | ≤ 35 ms | — | 캐시 적중 가정 |
| 외부 호출 | ≤ 10 ms | ≤ 20 ms | — | 타임아웃/백프레셔 명시 |

## 3. Memory Budget (예시 — 프로젝트에서 수치 확정)
| 단위 | 한도 | 측정 | 비고 |
|---|---|---|---|
| 인스턴스 RSS | ≤ 512 MB | 정상부하 정상상태 | OOM 마진 20% |
| 캐시 상한 | ≤ 128 MB | per-instance | TTL/evict 정책 명시 |
| 요청당 peak heap | ≤ 4 MB | p99 | 스트리밍 시 상한 |
| 동시성 버퍼 | bounded | 큐 길이 상한 | 백프레셔 트리거 |

## 4. 사용 규칙
- 성능 QS의 Response Measure는 위 표의 셀을 인용한다(예: "QS-001: p95 ≤ 80 ms (End-to-end SLO)").
- Latency↔Memory는 대표적 trade-off(캐시는 latency↓ memory↑) — ADR/평가에서 trade-off point로 명시(§D6).
- budget이 깨지는 후보는 채택 불가 또는 budget 재협상(owner 결정 + ADR).
