# Latency Budget — <프로젝트>
end-to-end SLO를 hop별로 분해(합 ≤ SLO). 성능 QS의 Response Measure가 이 표 셀을 인용한다.

> **경고:** 샘플 값을 제품 목표로 사용하지 않는다. Owner/Reviewer가 값을 확인하기 전에는 `<TBD>`로 둔다.

| 경로 / Hop | p50 | p95 | p99 | 타임아웃/백프레셔 | 비고 |
|---|---|---|---|---|---|
| End-to-end SLO | `<P50_TARGET_MS>` | `<P95_TARGET_MS>` | `<P99_TARGET_MS>` | `<TBD>` | 사용자 체감 |
| `<주요 구간>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | |

## Non-additive Scenarios
Cold start처럼 hop 합산 대상이 아닌 시나리오는 별도 관리한다.

| 시나리오 | 목표 | 환경 | 비고 |
|---|---|---|---|
| Cold start | `<COLD_START_TARGET_MS>` | `<DEVICE_CLASS>` / `<NETWORK_CONDITION>` | non-additive |

## 승인
- **Owner/Reviewer:** `<TBD>`
- **Approved date:** `<TBD>`
