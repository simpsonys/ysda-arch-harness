# 역할 정의서 (Roles) — Arch Harness

Common §A6 기반. 본 harness는 **설계 역할** 만 둔다(코드 Implementer/QA 없음). 다운스트림 구현은 코딩 하네스로 이관(§A30).

## 1. 소유자 (Owner)
- **정의:** 최종 결정자(항상 필수).
- **입력:** Architect/Analyst가 작성한 검토 대상(시스템 정의, QS, Proposed ADR, 후보/평가, architecture.md).
- **출력:** 승인(Approve)/수정(Revise)/반려(Reject), 우선순위 QS 확정, Design Baseline 승인, hand-off 승인.
- **권한 한계:** **무한 최종 권한.** ADR `Accepted`, Design Baseline 확정, 원격 push, 다운스트림 코드 이관은 오직 owner.

## 2. 아키텍트 (Architect)
- **입력:** 승인된 시스템 정의/우선순위 QS, 제약, 품질 모델/budget.
- **출력:** 후보 구조(동작/개발 view), 채택 ADR 제안(Proposed), `architecture.md`(arc42/C4).
- **금지:** owner 승인 없이 ADR을 Accepted로 바꾸기, QS 우선순위 없이 솔루션 확정, 다이어그램 없는 구조 주장.

## 3. 품질 분석가 (Quality Analyst)
- **입력:** 비즈니스 드라이버, use case, 제약.
- **출력:** 6-part 품질 시나리오(QS-nnn), 우선순위/근거, latency·memory budget 초안.
- **금지:** 측정 불가능한("빠르게") response measure, budget 수치 없는 성능 QS.

## 4. 도메인 모델러 (Domain Modeler)
- **입력:** use case.
- **출력:** 도메인 모델(mermaid ERD/class), 핵심 개념/관계/경계.
- **금지:** 구현 클래스/DB 스키마로의 조기 하강(개념 모델 유지).

## 5. 평가자/리뷰어 (Reviewer / Evaluator)
- **입력:** 후보 구조, 우선순위 QS, architecture.md.
- **출력:** ATAM-style 평가(sensitivity/trade-off/risk), budget 대비 QS 만족도 판정, open-question.
- **금지:** 정량 근거 없는 "통과" 선언.
