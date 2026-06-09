# 가정 명세 (Assumption Register) — <과제>

> 자료가 부족하면 가정이 불가피하다. 단 **가정은 표시되고, 명세되고, 검증 질문으로 환원되어야 한다.**
> 지어낸 단정(hallucination)을 막을 수는 없지만, 모든 미확인 내용을 **여기로 격리**해 담당자 확인 대상으로
> 만든다. `arch/assumptions/register.md` 에 둔다.

## 상태 정의
- **Open** — 미확인. 담당자/SME 확인 대기. (기본값)
- **Verified** — 담당자 확인 완료(근거 = qna-log 링크 필수).
- **Refuted** — 확인 결과 틀림 → 의존 결정/후보 재검토.

## Confidence × Blast Radius 규칙
- **Blast Radius** = 이 가정이 틀렸을 때 무너지는 범위(설계 결정/후보/QS).
- **Low confidence + High blast = load-bearing 가정** → 그 가정의 분기마다 **후보 구조를 따로 둔다**
  (단일 후보로 확정 금지). 확인이 오면 죽은 가지를 폐기해 수렴.
- 그 외(High conf 또는 영향 국소) → 단일 후보 + 검증 질문만으로 충분.

## 가정 목록
| ID | 가정 | 근거(EV) | 신뢰도 | Blast Radius | 검증 질문(담당자 확인) | 의존 결정/후보 | 상태 |
|---|---|---|---|---|---|---|---|
| AS-001 | `<TBD>` | `<없음/EV-00x>` | `<High/Med/Low>` | `<High/Med/Low>` | `<담당자에게 물을 질문>` | `<ADR-00x / Cand-A,B>` | Open |

> 규칙(archdev가 강제):
> - 가정 문장이 채워졌으면 신뢰도·Blast·상태·검증질문이 비어 있으면 안 된다(Open인데 검증질문 없음 = 위반).
> - load-bearing(Low+High) 가정은 후보가 1개뿐이면 위반 — 분기 후보 ≥2개를 요구.
> - 후보가 참조하는 AS-ID가 이 표에 없으면 위반.

## 분기 후보 매핑 (load-bearing 가정만)
| 가정 | 분기 시나리오 | 대응 후보 | 이 분기가 확정되면 |
|---|---|---|---|
| AS-001 | `<가정이 참일 때>` | [Cand-A](../candidates/candidate-001-*.md) | 채택 후보 |
| AS-001 | `<가정이 거짓일 때>` | [Cand-B](../candidates/candidate-002-*.md) | 대안 후보 |

## 검증 핸드오프
- Open 가정의 검증 질문은 `arch/evaluation/open-questions.md`에도 등재한다(담당자 회신 추적).
- 회신 도착 → 상태를 Verified/Refuted로 갱신 + `reports/qna-log.md`에 근거 링크.
- `python scripts/archdev.py report` 로 "미확인 load-bearing 가정 + 막힌 분기 후보 + 확인 대기 질문"을 추출.
