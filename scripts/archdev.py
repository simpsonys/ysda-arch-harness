#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YSDA Arch Harness DevTool Facade v1.0.0 (design harness).

Lightweight compliance checker for an architecture/design repository. Adapted from the personal
ysda-harness `ysdadev` (file completeness, version metadata, AGENTS mirror marker, and the
release/version consistency gate), plus a mermaid-first presence check.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

TARGET_VERSION = "1.0.0"
META = Path(".ysda-arch-harness") / "harness-version.json"

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    os.path.join("standards", "ysda-arch-harness-common.md"),
    os.path.join("standards", "ysda-arch-design-standard.md"),
    os.path.join("workflow", "STATUS.md"),
    os.path.join("workflow", "ROLES.md"),
    os.path.join("workflow", "IO-CONTRACT.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("quality", "quality-attribute-model.md"),
    os.path.join("reports", "progress.md"),
    os.path.join("reports", "qna-log.md"),
    str(META),
]

TRACKING_DOCS = [
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("reports", "progress.md"),
    os.path.join("doc", "harness-evolution-history.md"),
]


def load_meta() -> dict | None:
    if not META.exists():
        return None
    try:
        return json.loads(META.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_release_consistency(print_errors: bool = False) -> int:
    """ADR(현재 버전) Accepted 여부 + 추적 문서 freshness (Common §A9.1)."""
    errors = 0

    def emit(msg: str) -> None:
        if print_errors:
            print(msg)

    meta = load_meta() or {}
    version = meta.get("harness_version") or TARGET_VERSION
    tag = "v" + version

    arch_dir = Path("arch")
    current = (
        [p for p in sorted(arch_dir.glob("adr-*.md")) if tag in p.name]
        if arch_dir.exists()
        else []
    )
    if not current:
        emit(f"  [ WARN ] 현재 버전({tag}) 태그를 가진 ADR이 arch/에 없습니다 (self-hosting seed면 정상).")
    for adr in current:
        text = adr.read_text(encoding="utf-8")
        m = re.search(r"(?im)^[-*\s]*\**\s*Status:?\**\s*([A-Za-z]+)", text)
        status = m.group(1).lower() if m else "unknown"
        if status == "accepted":
            emit(f"  [ PASS ] {adr.name} Status=Accepted")
        else:
            emit(f"  [ ERROR ] 현재 버전 ADR이 Accepted가 아닙니다: {adr.name} (Status={status}).")
            errors += 1

    for rel in TRACKING_DOCS:
        p = Path(rel)
        if not p.exists():
            emit(f"  [ ERROR ] 추적 문서 누락: {rel}")
            errors += 1
        elif version in p.read_text(encoding="utf-8"):
            emit(f"  [ PASS ] {rel}에 v{version} 반영됨")
        else:
            emit(f"  [ ERROR ] {rel}에 현재 버전(v{version}) 기록이 없습니다 (closure 누락).")
            errors += 1

    if print_errors and errors == 0:
        emit("  [ PASS ] release 일관성(ADR 승인 / 추적 문서 freshness) 동기화")
    return errors


def check_mermaid_first(print_errors: bool = False) -> int:
    """구조 문서/템플릿에 mermaid가 존재하는지 informational 점검 (Common §A18)."""
    targets = [
        os.path.join("templates", "architecture-description.md"),
        os.path.join("templates", "candidate-architecture.md"),
        os.path.join("templates", "mermaid-cookbook.md"),
        os.path.join("standards", "ysda-arch-design-standard.md"),
    ]
    missing = 0
    for rel in targets:
        p = Path(rel)
        if p.exists() and "```mermaid" in p.read_text(encoding="utf-8"):
            if print_errors:
                print(f"  [ PASS ] mermaid 존재: {rel}")
        else:
            if print_errors:
                print(f"  [ WARN ] mermaid 블록을 찾지 못함: {rel}")
            missing += 1
    return missing  # WARN only; not counted as error


def cmd_check(_args=None) -> int:
    print("=" * 41)
    print("YSDA Arch Harness Compliance Checker (check)")
    print("=" * 41)
    errors = 0

    print("1. 필수 구성 파일:")
    for f in REQUIRED_FILES:
        if os.path.exists(f):
            print(f"  [ PASS ] {f}")
        else:
            print(f"  [ ERROR ] 누락: {f}")
            errors += 1

    print("\n2. 버전 메타데이터:")
    meta = load_meta()
    if not meta:
        print("  [ ERROR ] harness-version.json 파싱 실패/누락")
        errors += 1
    else:
        if meta.get("harness_family") == "ysda-arch-harness":
            print("  [ PASS ] harness_family=ysda-arch-harness")
        else:
            print(f"  [ ERROR ] harness_family 오류: {meta.get('harness_family')}")
            errors += 1
        if meta.get("harness_version") == TARGET_VERSION:
            print(f"  [ PASS ] harness_version={meta.get('harness_version')}")
        else:
            print(f"  [ WARN ] harness_version {meta.get('harness_version')} (v{TARGET_VERSION} 권장)")
        if meta.get("agents_md_mirror_version") == TARGET_VERSION:
            print("  [ PASS ] agents_md_mirror_version 동기화")
        else:
            print("  [ ERROR ] agents_md_mirror_version 불일치/누락")
            errors += 1

    print("\n3. AGENTS.md 미러 마커:")
    ap = Path("AGENTS.md")
    if ap.exists():
        m = re.search(r"<!-- ysda-arch-runtime-mirror: Common v([\d.]+) \(A31/A9/A20/A18\) -->", ap.read_text(encoding="utf-8"))
        if m:
            print(f"  [ PASS ] 미러 마커 v{m.group(1)}")
            if meta and m.group(1) != meta.get("agents_md_mirror_version"):
                print("  [ ERROR ] 메타-미러 버전 불일치")
                errors += 1
        else:
            print("  [ ERROR ] AGENTS.md 미러 마커 누락")
            errors += 1
    else:
        print("  [ ERROR ] AGENTS.md 없음")
        errors += 1

    print("\n4. mermaid-first 점검 (Common §A18):")
    check_mermaid_first(print_errors=True)

    print("\n5. Release/version 일관성 (Common §A9.1):")
    errors += check_release_consistency(print_errors=True)

    print("\n" + "=" * 41)
    print(f"결과 - 에러: {errors}건")
    if errors:
        print("[ RESULT ] 표준 위반. 에러를 해결하세요.")
        print("=" * 41)
        return 1
    print(f"[ RESULT ] ysda-arch-harness v{TARGET_VERSION} 표준 충족 (PASS)")
    print("=" * 41)
    return 0


def cmd_info(_args=None) -> int:
    meta = load_meta() or {}
    print(f"YSDA Arch Harness v{meta.get('harness_version','?')} / mode={meta.get('applied_mode','?')}")
    print(f"AGENTS mirror: {meta.get('agents_md_mirror_version','?')}")
    return 0


def cmd_list(_args=None) -> int:
    for name, desc in COMMANDS_DESC.items():
        print(f"  {name:<8} : {desc}")
    return 0


COMMANDS_DESC = {
    "check": "필수 파일/버전/미러/mermaid/release 일관성 점검",
    "info": "하네스 버전·모드 표시",
    "list": "명령 목록",
}
HANDLERS = {"check": cmd_check, "info": cmd_info, "list": cmd_list}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in HANDLERS:
        print("usage: archdev <check|info|list>")
        return 1
    return HANDLERS[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
