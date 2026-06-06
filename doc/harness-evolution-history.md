# Arch Harness 진화 이력

## v1.0.1 — 업무 적용 전 일관성 개선
* **안전:** 실제 제품 목표처럼 보이는 sample latency/memory 수치를 placeholder로 교체하고 승인 전 `<TBD>` 정책 추가.
* **정합성:** current version Accepted ADR을 release 필수 조건으로 명문화하고 `archdev check`와 일치시킴.
* **Lifecycle:** canonical `arch/` 경로, artifact lifecycle matrix, Mermaid text/ADR/QS sync 규칙 추가.
* **Scoped:** host repo unchanged/read-only/no commit/no push 기본 sidecar와 redaction/handoff 템플릿 추가.

## v1.0.0 — 설계 전용 하네스 분기
* **배경:** 개인용 `ysda-harness`(코딩)에 모든 요구를 넣기보다, 용도별로 harness를 분리. 업무용은 상품화 설계용으로,
  품질속성(특히 latency·memory)과 설계 문서가 코드보다 우선.
* **차용:** AgentK(arch-with-ai)의 ADD 8단계 워크플로우, SEI 6-part 품질 시나리오, ATAM 평가, arc42/C4 문서, ISO
  25010 품질 모델, AWS AI-DLC의 설계/구현 단계 분리.
* **이식(개인 harness v2.8.9에서):** Common/mode 분리, AGENTS 미러+버전 마커, Artifact Closure Gate + release/version
  일관성 게이트, ROLES/IO-CONTRACT/traceability/qna, git+handoff redaction, versionless 파일, lightweight escape
  hatch.
* **신규:** A14 latency/memory budget(1순위 드라이버), A18 mermaid-first, A16 Non-Goals, A30 다운스트림 코드 hand-off,
  D8 Design Baseline 게이트. 코딩/테스트 중심 규칙은 제외.
