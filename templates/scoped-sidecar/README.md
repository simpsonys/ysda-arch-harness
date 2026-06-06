# Scoped Sidecar Template

회사 저장소, 대형 저장소, 또는 수정이 금지된 subsystem을 분석할 때 host repo 밖 또는 허용된 sidecar 경로에
다음 구조를 만든다.

```text
analysis/<slice>/
  scope.md
  architecture-brief.md
  quality-scenarios.md
  views/
  adr-candidates.md
  risk-register.md
  open-questions.md
  review-log.md
  qna-log.md
  redaction-checklist.md
  handoff-bundle-index.md
  .ysda-arch-harness/
```

## 기본 정책
- host repo unchanged
- read-only analysis
- no commit
- no push
- confidential raw source를 exported docs에 복사하지 않음
- 내부 식별자와 미승인 성능 값은 placeholder 또는 redaction tag로 대체

`scope.md`로 읽기 경계를 먼저 고정하고, 공유 전 `redaction-checklist.md`와 `handoff-bundle-index.md`를 닫는다.
