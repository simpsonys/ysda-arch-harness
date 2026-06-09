# 채택(Adoption) · 기존과제(Brownfield) · 리더십 가이드

이 문서는 arch-harness v1.0.1을 실제 업무에 적용하며 드러난 3가지 갭과 그 해결을 정리한다.

## 1) 기존 과제(소스 없음)에 적용 — 별도 하네스 만들 필요 없음
**진단.** 설계 lifecycle(§D2)은 전부 greenfield(Phase 1 시스템 정의부터 *생성*) 가정이다. `scoped-sidecar`는
존재하지만 "수정 금지된 회사/대형 저장소를 **read-only로 분석**"하는 모드로, **소스가 있는** 감사용이다.
당신의 경우는 (a) 소스가 없고 도면·흐름·모듈 설명·지식만 있으며, (b) 목적이 분석이 아니라 **모듈 통합·설계**다.

**결론: 분리하지 말 것.** 거버넌스 코어(QS/ADR/budget/traceability/baseline)는 그대로 재사용 가치가 크고,
개선이 양쪽에 전파되어야 한다. 대신 **같은 하네스 안에 Phase 0 "as-is 흡수"** 를 추가한다.
- `templates/as-is-intake.md` 로 기존 자산을 **증거(Provenance)+신뢰도**와 함께 흡수하되, 소스로 검증 못 하므로
  **모든 as-is는 `Assumption`**, owner/SME 확인 후 `Verified`로 승격.
- 흐름: **P0(as-is) → P4(QS) → P5~P8(to-be 통합 설계)**. P1~P3는 도면에서 재구성되면 압축 가능.
- 통합 **이음새(seam)** 가 최대 리스크 → 각 seam은 `templates/interface-contract.md` 1건 + risk/open-question.
- `applied_mode`: 소스 없는 문서기반 = `audit`, read-only 소스 동반 = `scoped`.

## 2) self-hosting 혼동 해소 — "무엇을 복사하나" 자동화
**진단(가장 명확한 문제).** 이 repo는 `applied_mode: self-hosted` 로 **하네스를 자기 자신에 적용**한다. 그래서:
- `archdev check`의 `REQUIRED_FILES`가 **하네스 저작용 파일**(scoped-sidecar 전체 등)을 요구하고,
- release 게이트가 **하네스 버전 태그(`v1.0.1`) Accepted ADR + evolution-history**를 요구한다.
- `arch/`에는 **하네스 자신의 릴리스 ADR**(adr-001/002)이 들어 있다.

→ 신규 과제에 그대로 복사하면, 프로젝트엔 불필요한 저작용 파일을 끌고 오고, `archdev check`는 **프로젝트 설계
closure가 아니라 하네스 릴리스 불변식**을 검사해 **즉시 실패**한다. 이게 "어디를 살려 복사하나" 혼동의 원인이다.

**해결(첨부 `scripts/archdev.py` v1.1.0).**
- **mode-aware `check`**: `self-hosted`는 기존 그대로(검증됨, 0 errors). `design/audit/scoped/upgrade`는
  **프로젝트 검사만** — 릴리스-ADR/스코프드-사이드카 요건을 **건너뛰고** tracker/뷰 freshness만 본다.
- **`archdev init <target> --mode design`**: canonical 클론에서 실행하면 신규 과제 저장소를 부트스트랩.
  standards/AGENTS/prompts/templates는 복사, tracker는 **빈 프로젝트용으로 초기화**, 신규 `harness-version.json`
  작성, **하네스 릴리스 ADR과 evolution-history는 제외**. → "무엇을 복사하나"가 한 줄로 해결.
- **릴리스로 빼기:** GitHub Release(현재 0건)에 `init`가 만드는 starter subset만 올리거나, CI에서 `init`로
  생성한 트리를 `dist/ysda-arch-starter-<ver>.zip`으로 배포. 신규 과제는 이 zip만 받으면 된다.

복사해 살릴 것 / 버릴 것 요약:
| 살린다(프로젝트) | 버린다(하네스 저작 전용) |
|---|---|
| AGENTS.md, prompts/, standards 스냅샷, templates/(참조) | arch/adr-*(하네스 릴리스), doc/harness-evolution-history.md |
| 빈 STATUS/traceability/registry/progress/qna | self-hosted용 release 게이트 통과 흔적 |
| 빈 arch/ 스켈레톤 | scoped-sidecar를 "필수"로 요구하던 검사 |

## 3) 파트 리더(아키텍트) 관점 — 설계·리스크/ADR·할당
**이미 강함:** ROLES, ADR(driver matrix), risk-register, ATAM 비교행렬, traceability, Design Baseline 게이트.
**갭:** 설계→**할당** 사이가 비어 있다. 단일 owner·단일 에이전트 설계 중심이라 work-breakdown/할당/제품 인터페이스
계약 레이어가 없다.

**해결(첨부).**
- `templates/work-breakdown.md`: module view+ADR을 **작업 패키지(담당·의존·DoD·연결 QS/ADR)**로 분해, 크리티컬
  패스까지. traceability와 1:1.
- `templates/interface-contract.md`: 통합 이음새별 제품 계약(IO-CONTRACT와 구분). 통합 과제의 핵심 리스크 관리점.
- `archdev report`: 리더 digest — ADR 표(status/owner-approval/drivers) + open risks + 미완 High-QS 행을 추출.
  리뷰·할당 회의 입력으로 "리스크/ADR 추출"을 자동화.
- **ROLES 보강 제안:** Owner(결정 권한)와 별개로 **Part Leader/Tech Lead**(분해·할당·리뷰 오케스트레이션) 역할 추가.

## 4) 자료 부족 → 가정 거버넌스 (hallucination 격리)
**문제.** 자료를 다 못 올리고 일부는 존재하지도 않으니 설계 중 가정이 불가피하다. LLM이 가정을 자신 있게
단정하면(hallucination) 그대로 설계에 섞인다. harness는 가정/검증 분리 *규칙*은 있었지만 *강제*하지 못했다.

**해결(이 버전).** 가정을 **1급 산출물**로 올리고, archdev가 기계적으로 강제한다.
- `templates/assumption-register.md` → `arch/assumptions/register.md`: 가정마다 ID·근거(EV)·신뢰도·**Blast
  Radius(틀렸을 때 영향)**·**검증 질문(담당자 확인)**·의존 결정·상태(Open/Verified/Refuted).
- **가정이 틀릴 수 있으니 분기 후보:** Low confidence + High blast = **load-bearing 가정** → 그 가정의 분기마다
  후보 구조를 따로 둔다(단일 후보 확정 금지). 확인이 오면 죽은 가지를 폐기해 수렴.
- **archdev `check` 게이트(design/audit):**
  * 근거(EV) 없는 as-is 단정 → ERROR (지어낸 단정 차단)
  * Open 가정인데 검증 질문 없음 → ERROR (모든 미확인은 담당자 질문으로 환원)
  * load-bearing 가정인데 분기 후보 < 2 → ERROR (가정 분기 강제)
  * 후보가 register에 없는 AS-ID 참조 → ERROR
  * Open 가정이 open-questions 미등재 → WARN
  * arch/에 해당 산출물이 없으면 게이트는 no-op(빈 스타터는 그대로 PASS).
- **archdev `report`:** ★load-bearing 미확인 가정 + 담당자 확인 질문을 추출 → 그대로 담당자 핸드오프 목록.

**워크플로:** 자료 부족 → 가정 명세화(분기 후보까지) → `archdev report`로 확인 질문 추출 → 담당자 회신 →
가정 Verified/Refuted 갱신 → 죽은 가지 폐기 → 설계 수렴. 지어내기가 "표시된 분기 + 확인 질문"으로 환원된다.

## 적용 순서
1. `scripts/archdev.py` 교체(v1.1.0). self-hosted에서 `archdev check`가 여전히 PASS인지 확인.
2. 새 템플릿 3개를 `templates/`에 추가, `templates/README.md` 색인에 등재.
3. 신규 과제: `python scripts/archdev.py init ../<repo> --mode design`(또는 `audit`).
4. 기존 과제: `audit` 모드 + `as-is-intake.md`로 P0부터.
5. 설계 후: `work-breakdown.md` + seam별 `interface-contract.md`, 리뷰 때 `archdev report`.
