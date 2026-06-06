# 구조 평가 (ATAM-style) — <마일스톤>

## 1. 평가 대상 결정 (Architectural decisions)
- <ADR-00x 요약>

## 2. 분석
| 결정 | 영향 QS | Sensitivity | Trade-off | Risk / Non-risk | 근거 |
|---|---|---|---|---|---|
| <결정> | QS-001/002 | <민감점> | <Latency↔Memory 등> | Risk/Non-risk | <근거> |

## 3. 우선순위 QS 만족도 (budget 대비)
`<TBD>`가 남은 High QS는 `미평가/Blocked`로 기록하며 Design Baseline을 승인할 수 없다. `조건부/미달`은 owner
승인 예외 ADR이 있어야 Baseline에 포함할 수 있다.

| QS | 목표(budget) | 설계 추정/측정 | 판정 | 후속 |
|---|---|---|---|---|
| QS-001 Latency | `p95 ≤ <P95_TARGET_MS>` 또는 `<TBD>` | <추정> | 만족/조건부/미달 | <ADR/open-q> |
| QS-002 Memory | `<MAX_RSS_MB>` 또는 `<TBD>` | <추정> | 만족/조건부/미달 | |

## 4. 리스크 / 기술부채 / 미해결 (open questions)
- <항목 → 후속 ADR 또는 `arch/evaluation/risk-register.md` / `open-questions.md` 링크>

리뷰 finding과 disposition은 `arch/evaluation/review-log.md`에 기록한다.
