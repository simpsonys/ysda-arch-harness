# Arch Harness 진화 이력

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
