# Candidate — <후보 구조 제목> (drives QS-NNN)

- **Target QS:** [QS-NNN](...) (priority High)
- **Applied tactics:** <예: 캐싱 + CQRS read 분리 (Latency); 캐시 상한+TTL (Memory)>
- **Premised assumptions (AS-ID):** [AS-001](../assumptions/register.md) — 이 후보가 전제하는 가정. load-bearing 가정이면 분기 후보 중 하나임을 명시.

## 동작(runtime) view
> 이 다이어그램은 <…> 요청이 컴포넌트를 거치는 흐름을 보여준다.
```mermaid
sequenceDiagram
  participant C as Client
  participant G as Gateway
  participant S as Service
  participant K as Cache
  C->>G: request
  G->>S: forward
  S->>K: lookup
  K-->>S: hit/miss
  S-->>C: response (p95 목표 표기)
```

## 개발(module) view
> 이 다이어그램은 모듈/레이어 의존성을 보여준다.
```mermaid
flowchart TD
  API[api layer] --> APP[application]
  APP --> DOM[domain]
  APP --> INFRA[infrastructure: cache/db/queue]
```

## QS 영향 분석
| QS | 영향(정성) | 추정(정량) | trade-off |
|---|---|---|---|
| QS-001 Latency | ↓ | `p95 ~<TBD>` | memory 영향 `<TBD>` |
| QS-002 Memory | ↑ | `<TBD>` | budget 내 여부 |

## 전제 가정 / 수렴 조건
| 전제 AS-ID | 이 후보가 전제하는 분기 | 가정이 Verified면 | Refuted면 |
|---|---|---|---|
| AS-001 | `<참/거짓 분기>` | 채택 후보로 유지 | 이 후보 폐기 → 대안 후보 |

## Non-Goals
- <이 후보가 다루지 않는 범위>
