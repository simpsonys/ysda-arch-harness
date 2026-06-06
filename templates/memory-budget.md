# Memory Budget — <프로젝트>
인스턴스/요청/캐시 단위 상한. 메모리 QS의 Response Measure가 이 표 셀을 인용한다.

| 단위 | 한도 | 측정 조건 | evict/TTL/bound 정책 | 비고 |
|---|---|---|---|---|
| 인스턴스 RSS |  | 정상부하 정상상태 |  | OOM 마진 |
| 캐시 상한 |  | per-instance | TTL/evict | |
| 요청당 peak |  | p99 | 스트리밍 상한 | |
