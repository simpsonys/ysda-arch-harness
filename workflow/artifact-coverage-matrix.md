# Artifact Coverage Matrix

> 목적: source를 읽고도 필요한 산출물을 빼먹는 문제를 막는다. Source Record, Requirement, Constraint, Risk, Assumption, ADR Candidate가 생기면 이 표를 갱신한다.

| Coverage ID | Source / Trigger | Extracted Item | Required Artifact | Owner | Status | Gap / Next Action |
|---|---|---|---|---|---|---|
| COV-001 | SRC-001 | `<requirement / constraint / risk / assumption / decision>` | `<arch/... 또는 workflow/...>` | `<owner>` | `<Status>` | `<다음 액션>` |

## Closure Rule
- `Missing` 항목이 있으면 Design Baseline을 닫지 않는다.
- source가 단순 참고자료라 required artifact가 없을 경우 `N/A — reason`을 명시한다.
- stakeholder handoff 관련 항목은 `Stakeholder Action Plan` 또는 `Work Breakdown`에 연결한다.

> v1.0.3: stakeholder/언어 정책 반영 (self-hosted closure).
