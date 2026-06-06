#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YSDA Arch Harness DevTool Facade v1.0.1 (design harness).

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

TARGET_VERSION = "1.0.1"
META = Path(".ysda-arch-harness") / "harness-version.json"

SCOPED_SIDECAR_FILES = [
    os.path.join("templates", "scoped-sidecar", name)
    for name in [
        "README.md",
        "scope.md",
        "architecture-brief.md",
        "quality-scenarios.md",
        "redaction-checklist.md",
        "handoff-bundle-index.md",
        "risk-register.md",
        "open-questions.md",
        "qna-log.md",
        "adr-candidates.md",
        "review-log.md",
        os.path.join("views", "README.md"),
        os.path.join(".ysda-arch-harness", "README.md"),
    ]
]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    os.path.join("standards", "ysda-arch-harness-common.md"),
    os.path.join("standards", "ysda-arch-design-standard.md"),
    os.path.join("standards", "README.md"),
    os.path.join("standards", "artifact-lifecycle.md"),
    os.path.join("templates", "README.md"),
    os.path.join("templates", "candidate-comparison-matrix.md"),
    os.path.join("templates", "risk-register.md"),
    os.path.join("templates", "open-questions.md"),
    os.path.join("templates", "review-log.md"),
    os.path.join("workflow", "STATUS.md"),
    os.path.join("workflow", "ROLES.md"),
    os.path.join("workflow", "IO-CONTRACT.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("quality", "quality-attribute-model.md"),
    os.path.join("reports", "progress.md"),
    os.path.join("reports", "qna-log.md"),
    str(META),
] + SCOPED_SIDECAR_FILES

TRACKING_DOCS = [
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("reports", "progress.md"),
    os.path.join("doc", "harness-evolution-history.md"),
]

SAMPLE_TARGET_ROOTS = [Path("standards"), Path("templates"), Path("quality")]
SAMPLE_TARGET_RE = re.compile(
    r"(?i)(?<![<\w])\d+(?:\.\d+)?\s*(?:ms|mb)\b|"
    r"\b(?:p50|p95|p99|rss|cache)\s*(?:≤|<=|<)\s*\d+"
)
FORBIDDEN_PLAN_FILES = [Path("implementation_plan.md"), Path("plan.md")]
CANONICAL_PATH_POLICY_FILES = [
    Path("AGENTS.md"),
    Path("workflow") / "IO-CONTRACT.md",
    Path("workflow") / "ROLES.md",
    Path("workflow") / "STATUS.md",
    Path("prompts") / "design-phase-prompts.md",
    Path("templates") / "system-definition.md",
]
FORBIDDEN_PATH_RE = re.compile(
    r"`(?:arch/)?(?:architecture|system)\.md`|"
    r"`(?:usecase|candidate|decision|evaluation)/|"
    r"\b(?:usecase|candidate|decision)/\*"
)
MERMAID_CONTRACT_TOKENS = [
    "System Context",
    "Container View",
    "Component View",
    "Runtime Scenario",
    "Deployment View",
    "Data Flow",
    "Latency Critical Path",
    "Memory Lifecycle",
    "Create condition",
    "Update condition",
    "Text sync rule",
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
        emit(f"  [ ERROR ] 현재 버전({tag}) 태그를 가진 Accepted ADR이 arch/에 없습니다.")
        errors += 1
    for adr in current:
        text = adr.read_text(encoding="utf-8")
        m = re.search(r"(?im)^[-*\s]*\**\s*Status:?\**\s*([A-Za-z]+)", text)
        status = m.group(1).lower() if m else "unknown"
        if status == "accepted":
            emit(f"  [ PASS ] {adr.name} Status=Accepted")
        else:
            emit(f"  [ ERROR ] 현재 버전 ADR이 Accepted가 아닙니다: {adr.name} (Status={status}).")
            errors += 1
        if re.search(r"(?im)^[-*\s]*\**\s*Owner Approval:?\**\s*granted\b", text):
            emit(f"  [ PASS ] {adr.name} Owner Approval=granted")
        else:
            emit(f"  [ ERROR ] 현재 버전 ADR에 owner 승인 기록이 없습니다: {adr.name}.")
            errors += 1

    for rel in TRACKING_DOCS:
        p = Path(rel)
        if not p.exists():
            emit(f"  [ ERROR ] 추적 문서 누락: {rel}")
            errors += 1
        elif tag in p.read_text(encoding="utf-8"):
            emit(f"  [ PASS ] {rel}에 v{version} 반영됨")
        else:
            emit(f"  [ ERROR ] {rel}에 현재 버전(v{version}) 기록이 없습니다 (closure 누락).")
            errors += 1

    if print_errors and errors == 0:
        emit("  [ PASS ] release 일관성(ADR 승인 / 추적 문서 freshness) 동기화")
    return errors


def check_sample_target_values(print_errors: bool = False) -> int:
    """Standards/templates/quality에 실제 목표처럼 보이는 숫자 단위가 없는지 점검."""
    violations = []
    for root in SAMPLE_TARGET_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if SAMPLE_TARGET_RE.search(line):
                    violations.append((path, lineno, line.strip()))
    if print_errors:
        for path, lineno, line in violations:
            print(f"  [ ERROR ] sample target 후보: {path}:{lineno}: {line}")
        if not violations:
            print("  [ PASS ] standards/templates/quality에 구체 sample target 없음")
    return len(violations)


def check_forbidden_plan_files(print_errors: bool = False) -> int:
    """범용 durable planning 파일이 저장소 root에 생기지 않았는지 점검."""
    existing = [path for path in FORBIDDEN_PLAN_FILES if path.exists()]
    if print_errors:
        for path in existing:
            print(f"  [ ERROR ] 금지된 범용 planning 파일: {path}")
        if not existing:
            print("  [ PASS ] 금지된 범용 planning 파일 없음")
    return len(existing)


def check_canonical_path_references(print_errors: bool = False) -> int:
    """Runtime/discovery 문서가 금지된 이전 산출물 경로를 안내하지 않는지 점검."""
    violations = []
    for path in CANONICAL_PATH_POLICY_FILES:
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FORBIDDEN_PATH_RE.search(line):
                violations.append((path, lineno, line.strip()))
    if print_errors:
        for path, lineno, line in violations:
            print(f"  [ ERROR ] 이전 산출물 경로 참조: {path}:{lineno}: {line}")
        if not violations:
            print("  [ PASS ] runtime/discovery 문서가 canonical arch/ 경로 사용")
    return len(violations)


def check_mermaid_contract(print_errors: bool = False) -> int:
    """Mermaid cookbook이 필수 view lifecycle/sync 계약을 포함하는지 점검."""
    path = Path("templates") / "mermaid-cookbook.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    missing = [token for token in MERMAID_CONTRACT_TOKENS if token not in text]
    if print_errors:
        for token in missing:
            print(f"  [ ERROR ] Mermaid contract 누락: {token}")
        if not missing:
            print("  [ PASS ] 필수 Mermaid view lifecycle/sync contract 존재")
    return len(missing)


def check_mermaid_first(print_errors: bool = False) -> int:
    """구조 문서/템플릿에 mermaid가 존재하는지 점검 (Common §A18)."""
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
                print(f"  [ ERROR ] mermaid 블록을 찾지 못함: {rel}")
            missing += 1
    return missing


def cmd_check(_args=None) -> int:
    print("=" * 41)
    print("YSDA Arch Harness Compliance Checker (check)")
    print("=" * 41)
    errors = 0

    print("1. 필수 구성 파일:")
    for f in REQUIRED_FILES:
        if Path(f).is_file():
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
            print(f"  [ ERROR ] harness_version {meta.get('harness_version')} (v{TARGET_VERSION} 필요)")
            errors += 1
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
    errors += check_mermaid_first(print_errors=True)
    errors += check_mermaid_contract(print_errors=True)

    print("\n5. Release/version 일관성 (Common §A9.1):")
    errors += check_release_consistency(print_errors=True)

    print("\n6. Sample target 안전성:")
    errors += check_sample_target_values(print_errors=True)

    print("\n7. 범용 planning 파일 금지:")
    errors += check_forbidden_plan_files(print_errors=True)

    print("\n8. Canonical 산출물 경로:")
    errors += check_canonical_path_references(print_errors=True)

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
    "check": "필수 파일/버전/미러/mermaid/release/sample-target 일관성 점검",
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
