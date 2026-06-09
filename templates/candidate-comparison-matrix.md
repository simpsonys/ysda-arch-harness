# Candidate Comparison Matrix — <결정 주제>

- **Target High QS:** <QS links>
- **Evaluation scope:** <비교 범위>
- **Non-Goals:** <이번 비교에서 결정하지 않는 것>

| Candidate | 전제 가정(AS-ID) | Latency | Memory | Availability | Modifiability | Risk | Evidence | 가정 확정 시 수렴/폐기 |
|---|---|---|---|---|---|---|---|---|
| Candidate A | AS-001(참) | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | <QS/view link> | AS-001 Verified→채택 / Refuted→폐기 |
| Candidate B | AS-001(거짓) | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | <QS/view link> | AS-001 Refuted→채택 |

추천 결과는 `arch/adr-nnn-*.md`의 driver matrix 및 Decision brief와 일치해야 한다.

> load-bearing 가정(Low conf+High blast)은 **분기 후보 ≥2개**가 이 표에 있어야 한다(archdev 강제). 가정이 확정되면 죽은 가지를 폐기해 수렴한다.
