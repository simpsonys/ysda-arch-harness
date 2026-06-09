# Originals Manifest — 원본 ↔ 출처 매핑

> 원본 파일은 출처·날짜가 파일 안에 안 남으므로, **여기에 매핑**한다. 여러 파일을 originals/에 넣고
> "이 manifest 보고 각 원본을 Source Record로 정리해줘" 한 줄로 일괄 처리한다.
> 파일명 통일은 강제 아님(원하면 의미 있는 이름 권장 — `1.jpg`보다 `auth-flow.jpg`). 원본 파일명을 그대로 적는다.

| 원본 파일 | 내용(무엇) | 출처(Origin) | 원본 작성·갱신일 | 받은 경로/채널 | 기밀/Redaction | 부여할 SRC-ID |
|---|---|---|---|---|---|---|
| `auth-flow.jpg` | 인증 흐름도 | 플랫폼팀 김OO | 2025-11-02 | 사내위키/메일 | redact(IP) | SRC-001 |
| `api-spec.pdf` | API 명세 v2 | 백엔드팀 위키 | 2026-01-15 | <경로> | none | SRC-002 |
| `<파일>` | `<내용>` | `<출처>` | `<YYYY-MM-DD/unknown>` | `<경로>` | `<none/redact>` | `SRC-00x` |

## 일괄 정리 절차
1. 원본 파일들을 `arch/sources/originals/`에 넣는다.
2. 위 표를 채운다(출처·날짜는 사람이 입력 — LLM이 추측 금지).
3. Cline에 `originals/_manifest.md 보고 각 원본을 출처·타임스탬프 붙인 Source Record로 정리해줘`.
4. 결과는 `arch/sources/normalized/SRC-00x-*.md`로 생성된다(`templates/source-record.md` 형식).
5. `python scripts/archdev.py check` 로 각 Source Record의 출처·수집 시각·원본 표기 누락을 검증.

> 주의: 출처/날짜를 모르면 `unknown`으로 두고, 그 자체를 담당자 확인 질문(가정)으로 올린다. 빈칸을 LLM이 지어내지 않는다.
