# Memory Budget — <프로젝트>
인스턴스/요청/캐시 단위 상한. 메모리 QS의 Response Measure가 이 표 셀을 인용한다.

> **경고:** 샘플 값을 제품 목표로 사용하지 않는다. Owner/Reviewer가 값을 확인하기 전에는 `<TBD>`로 둔다.

| 단위 | 한도 | 측정 조건 | evict/TTL/bound 정책 | 비고 |
|---|---|---|---|---|
| 인스턴스 RSS | `<MAX_RSS_MB>` | 정상부하 정상상태 | `<TBD>` | OOM 마진 `<TBD>` |
| Peak heap | `<PEAK_HEAP_MB>` | p99 | 스트리밍 상한 `<TBD>` | |
| 모델/데이터 캐시 | `<MODEL_CACHE_MB>` | per-instance | TTL/evict `<TBD>` | |
| 동시성 버퍼 | `<TBD>` | `<CONCURRENT_SESSION_COUNT>` | bound `<TBD>` | |

## 승인
- **Owner/Reviewer:** `<TBD>`
- **Approved date:** `<TBD>`
