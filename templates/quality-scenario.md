# QS-NNN — <품질 시나리오 제목>

- **Quality attribute:** Performance/Latency | Performance/Memory | Availability | Modifiability | ...
- **Priority:** High | Med | Low
- **Business rationale:** <왜 중요한가 1~2줄>

## 6-part scenario (SEI)
| 항목 | 내용 |
|---|---|
| **Source** (자극원) | <예: 사용자 / 상위 서비스 / 스케줄러> |
| **Stimulus** (자극) | <예: 조회 요청 도착 / 트래픽 2배 급증> |
| **Artifact** (대상) | <예: 조회 API / 캐시 / 전체 시스템> |
| **Environment** (환경) | <예: 정상부하 정상상태 / 피크 / 장애 복구 중> |
| **Response** (응답) | <예: 요청을 처리하고 결과 반환> |
| **Response Measure** (측정) | <`arch/quality/` 승인 budget 인용: `p95 ≤ <P95_TARGET_MS>` 또는 `<TBD>`> |

## Non-Goals
- <이 QS가 다루지 않는 것>
