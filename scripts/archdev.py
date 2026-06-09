#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YSDA Arch Harness DevTool Facade v1.1.0 (design harness).

v1.1.0 changes (additive, stdlib-only):
- **Mode-aware `check`.** Reads `applied_mode` from `.ysda-arch-harness/harness-version.json`.
  * `self-hosted`  → harness-authoring checks (unchanged: scoped-sidecar present,
    release/version ADR tagged+Accepted, evolution-history freshness, sample-target safety).
  * `design`/`audit`/`scoped`/`upgrade` → **project** checks only. Drops the harness-release-ADR
    requirement and the scoped-sidecar template requirement, and validates project closure
    (required project files + arch/ skeleton + traceability/STATUS freshness). This is what stopped
    a freshly-adopted project repo from ever passing `check`.
- **`init`** — scaffolds an applied design repo from this canonical clone: copies standards/AGENTS/
  prompts/templates, blanks the workflow/report trackers, writes a fresh project `harness-version.json`,
  and **excludes** the harness's own release ADRs and evolution history. Answers "what do I copy".
- **`report`** — leader digest: ADR table (status/owner-approval/drivers), open risks, and
  High-QS traceability gaps. Answers "extract risks/ADRs for review and allocation".
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

TARGET_VERSION = "1.0.3"
META = Path(".ysda-arch-harness") / "harness-version.json"
AUTHORING_MODE = "self-hosted"
PROJECT_MODES = {"design", "audit", "scoped", "upgrade"}

# ── file sets ────────────────────────────────────────────────────────────────
SCOPED_SIDECAR_FILES = [
    os.path.join("templates", "scoped-sidecar", name)
    for name in [
        "README.md", "scope.md", "architecture-brief.md", "quality-scenarios.md",
        "redaction-checklist.md", "handoff-bundle-index.md", "risk-register.md",
        "open-questions.md", "qna-log.md", "adr-candidates.md", "review-log.md",
        os.path.join("views", "README.md"),
        os.path.join(".ysda-arch-harness", "README.md"),
    ]
]

# Harness-authoring repo (self-hosted) required files.
AUTHORING_REQUIRED_FILES = [
    "AGENTS.md", "README.md",
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

# Applied design/audit project minimum. No scoped-sidecar template library, no harness-release ADR.
PROJECT_REQUIRED_FILES = [
    "AGENTS.md", "README.md",
    os.path.join("prompts", "design-phase-prompts.md"),
    os.path.join("workflow", "STATUS.md"),
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("workflow", "artifact-coverage-matrix.md"),
    os.path.join("reports", "progress.md"),
    os.path.join("reports", "qna-log.md"),
    str(META),
]
# Recommended-but-not-fatal in a project repo (frozen standards snapshot).
PROJECT_RECOMMENDED_FILES = [
    os.path.join("standards", "ysda-arch-harness-common.md"),
    os.path.join("standards", "ysda-arch-design-standard.md"),
]

TRACKING_DOCS = [
    os.path.join("workflow", "traceability-matrix.md"),
    os.path.join("workflow", "artifact-registry.md"),
    os.path.join("workflow", "artifact-coverage-matrix.md"),
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
    "System Context", "Container View", "Component View", "Runtime Scenario",
    "Deployment View", "Data Flow", "Latency Critical Path", "Memory Lifecycle",
    "Create condition", "Update condition", "Text sync rule",
]


def load_meta() -> dict | None:
    if not META.exists():
        return None
    try:
        return json.loads(META.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_mode(meta: dict | None) -> str:
    """Default to authoring so an un-stamped repo keeps the strict legacy behavior."""
    mode = (meta or {}).get("applied_mode") or AUTHORING_MODE
    return mode


# ── authoring-only checks (unchanged semantics) ───────────────────────────────
def check_release_consistency(print_errors: bool = False) -> int:
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
    existing = [path for path in FORBIDDEN_PLAN_FILES if path.exists()]
    if print_errors:
        for path in existing:
            print(f"  [ ERROR ] 금지된 범용 planning 파일: {path}")
        if not existing:
            print("  [ PASS ] 금지된 범용 planning 파일 없음")
    return len(existing)


def check_canonical_path_references(print_errors: bool = False) -> int:
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
    path = Path("templates") / "mermaid-cookbook.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    missing = [t for t in MERMAID_CONTRACT_TOKENS if t not in text]
    if print_errors:
        for t in missing:
            print(f"  [ ERROR ] Mermaid contract 누락: {t}")
        if not missing:
            print("  [ PASS ] 필수 Mermaid view lifecycle/sync contract 존재")
    return len(missing)


def check_mermaid_first(print_errors: bool = False) -> int:
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


# ── project-mode checks (new) ──────────────────────────────────────────────────
def check_project_freshness(print_errors: bool = False) -> int:
    """Light project closure: trackers exist & non-trivial; produced views are mermaid-first.

    Deliberately does NOT require a harness-release ADR — an applied project has its own
    decision ADRs (adr-001-<decision>.md), not a version-tagged release ADR.
    """
    errors = 0

    def emit(msg: str) -> None:
        if print_errors:
            print(msg)

    for rel in [os.path.join("workflow", "STATUS.md"),
                os.path.join("workflow", "traceability-matrix.md"),
                os.path.join("reports", "progress.md")]:
        p = Path(rel)
        if p.exists() and len(p.read_text(encoding="utf-8").strip()) > 0:
            emit(f"  [ PASS ] tracker 존재: {rel}")
        else:
            emit(f"  [ ERROR ] tracker 누락/빈 파일: {rel}")
            errors += 1

    arch = Path("arch")
    if not arch.exists():
        emit("  [ WARN ] arch/ 디렉토리가 아직 없습니다 (Phase 1 시작 전이면 정상).")
    else:
        # mermaid-first only applies to views that were actually produced.
        views = list((arch / "views").rglob("*.md")) if (arch / "views").exists() else []
        for v in views:
            if "```mermaid" not in v.read_text(encoding="utf-8"):
                emit(f"  [ ERROR ] 구조 view에 mermaid 없음 (§A18): {v}")
                errors += 1
        if views and errors == 0:
            emit("  [ PASS ] 생성된 arch/views/* 모두 mermaid 포함")
    if print_errors and errors == 0:
        emit("  [ PASS ] 프로젝트 tracker freshness OK")
    return errors


def _scan_adrs():
    arch = Path("arch")
    rows = []
    if not arch.exists():
        return rows
    for adr in sorted(arch.glob("adr-*.md")):
        text = adr.read_text(encoding="utf-8")
        sm = re.search(r"(?im)^[-*\s]*\**\s*Status:?\**\s*([A-Za-z]+)", text)
        om = re.search(r"(?im)^[-*\s]*\**\s*Owner Approval:?\**\s*([^\n]+)", text)
        dm = re.search(r"(?im)^[-*\s]*\**\s*Drivers?\s*\(QS\):?\**\s*([^\n]+)", text)
        rows.append({
            "file": adr.name,
            "status": (sm.group(1) if sm else "unknown"),
            "owner": ("granted" if om and "granted" in om.group(1).lower() else "—"),
            "drivers": (dm.group(1).strip() if dm else "—"),
        })
    return rows


def _scan_open_risks():
    rows = []
    for p in list(Path(".").rglob("risk-register.md")):
        if "templates" in p.parts:
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if re.match(r"\s*\|\s*R-\d+", line) and "TBD" not in line and "Open" in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if cells:
                    rows.append((p.as_posix(), cells[0], cells[1] if len(cells) > 1 else ""))
    return rows


# ── assumption / provenance gate (new) ─────────────────────────────────────────
PLACEHOLDER_RE = re.compile(r"^\s*(?:<[^>]*>|`<[^>]*>`|-|—|n/a|tbd)?\s*$", re.I)


def _is_blank(cell: str) -> bool:
    c = (cell or "").strip().strip("`")
    return bool(PLACEHOLDER_RE.match(c)) or c == ""


def _md_tables(text: str):
    """Return list of (header_cells, [row_cells, ...]) for each markdown pipe-table."""
    tables, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i]); i += 1
            if len(block) >= 2:
                header = [c.strip() for c in block[0].strip().strip("|").split("|")]
                rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in block[2:]]
                tables.append((header, rows))
        else:
            i += 1
    return tables


def _col(header, *tokens):
    for idx, h in enumerate(header):
        for t in tokens:
            if t.lower() in h.lower():
                return idx
    return -1


def check_assumption_provenance(print_errors: bool = False) -> int:
    """Force: provenance on as-is rows, full assumption specs, and branch candidates for
    load-bearing assumptions. No-op when arch/ has none of these (e.g. a fresh starter)."""
    errors = 0

    def emit(msg: str):
        if print_errors:
            print(msg)

    arch = Path("arch")
    if not arch.exists():
        emit("  [ INFO ] arch/ 없음 — provenance 게이트 건너뜀.")
        return 0

    # 1) as-is provenance: filled module/seam rows must cite evidence.
    asis_rows = 0
    for f in sorted((arch / "as-is").rglob("*.md")) if (arch / "as-is").exists() else []:
        for header, rows in _md_tables(f.read_text(encoding="utf-8")):
            ev = _col(header, "근거", "ev", "evidence")
            if ev < 0:
                continue
            name = 0
            for r in rows:
                if len(r) <= ev or _is_blank(r[name]):
                    continue
                asis_rows += 1
                if _is_blank(r[ev]):
                    emit(f"  [ ERROR ] 근거 없는 as-is 단정: {f.name} → '{r[name]}' (근거 EV 비어 있음).")
                    errors += 1
    if asis_rows and errors == 0:
        emit(f"  [ PASS ] as-is 행 {asis_rows}건 모두 근거(EV) 보유")

    # 2) assumption register: collect specs + enforce completeness.
    assumptions = {}  # AS-ID -> dict(status, load_bearing)
    reg_dir = arch / "assumptions"
    for f in sorted(reg_dir.rglob("*.md")) if reg_dir.exists() else []:
        for header, rows in _md_tables(f.read_text(encoding="utf-8")):
            i_id = _col(header, "id")
            i_stmt = _col(header, "가정", "assumption", "statement")
            if i_id < 0 or i_stmt < 0:
                continue
            i_conf = _col(header, "신뢰도", "confidence")
            i_blast = _col(header, "blast")
            i_q = _col(header, "검증", "verification", "질문")
            i_status = _col(header, "상태", "status")
            for r in rows:
                if len(r) <= i_stmt or _is_blank(r[i_stmt]):
                    continue  # template stub
                asid = r[i_id].strip().strip("`") if i_id < len(r) else "?"
                conf = r[i_conf] if 0 <= i_conf < len(r) else ""
                blast = r[i_blast] if 0 <= i_blast < len(r) else ""
                status = (r[i_status] if 0 <= i_status < len(r) else "open").strip().lower()
                q = r[i_q] if 0 <= i_q < len(r) else ""
                load_bearing = ("low" in conf.lower()) and ("high" in blast.lower())
                assumptions[asid] = {"status": status, "load_bearing": load_bearing, "file": f.name}
                for label, val in (("신뢰도", conf), ("Blast", blast), ("상태", status)):
                    if _is_blank(val):
                        emit(f"  [ ERROR ] {asid}: {label} 미기재 ({f.name}).")
                        errors += 1
                if status.startswith("open") and _is_blank(q):
                    emit(f"  [ ERROR ] {asid}: Open 가정인데 검증 질문(담당자 확인)이 없습니다 ({f.name}).")
                    errors += 1
    if assumptions and errors == 0:
        emit(f"  [ PASS ] 가정 {len(assumptions)}건 명세 완결(신뢰도/Blast/상태/검증질문)")

    # 3) candidates: branch coverage for load-bearing assumptions + reverse reference check.
    cand_files = sorted((arch / "candidates").glob("candidate-*.md")) if (arch / "candidates").exists() else []
    cand_text = {f.name: f.read_text(encoding="utf-8") for f in cand_files}
    referenced = set()
    for name, txt in cand_text.items():
        for asid in re.findall(r"\bAS-\d+\b", txt):
            referenced.add(asid)
            if asid not in assumptions:
                emit(f"  [ ERROR ] {name}이 register에 없는 가정 {asid}을 참조합니다.")
                errors += 1
    if cand_files:  # Phase 5+ reached → enforce branch rule
        for asid, meta in assumptions.items():
            if meta["load_bearing"] and meta["status"].startswith("open"):
                n = sum(1 for txt in cand_text.values() if asid in txt)
                if n < 2:
                    emit(f"  [ ERROR ] load-bearing 가정 {asid}(Low+High)이 분기 후보 {n}개뿐 — "
                         f"분기 후보 ≥2개 필요(가정이 틀릴 수 있으므로).")
                    errors += 1
        if errors == 0 and referenced:
            emit("  [ PASS ] load-bearing 가정에 분기 후보 충족 / 후보-가정 참조 정합")

    # 4) verification handoff linkage (WARN only).
    oq = arch / "evaluation" / "open-questions.md"
    oq_text = oq.read_text(encoding="utf-8") if oq.exists() else ""
    for asid, meta in assumptions.items():
        if meta["status"].startswith("open") and asid not in oq_text:
            emit(f"  [ WARN ] {asid}(Open) 검증 질문이 open-questions.md에 미등재 — 담당자 추적 누락 가능.")

    if print_errors and not assumptions and not asis_rows:
        emit("  [ INFO ] as-is/가정/후보 산출물 없음 — 게이트 대상 없음(정상).")
    return errors


# ── source preservation + accessibility gate (new) ─────────────────────────────
SOURCE_META_TOKENS = {
    "출처": ["출처", "origin"],
    "수집 시각": ["수집", "captured"],
    "원본": ["원본", "original"],
}


def check_accessibility_and_sources(print_errors: bool = False) -> int:
    """Force: Source Records carry origin+timestamp; shared artifacts open with 한눈에 + 용어.
    No-op when the relevant arch/ files don't exist (fresh starter stays green)."""
    errors = 0

    def emit(msg: str):
        if print_errors:
            print(msg)

    arch = Path("arch")
    if not arch.exists():
        return 0

    # 1) Source Records: origin + captured-at timestamp + original pointer mandatory.
    norm = arch / "sources" / "normalized"
    recs = 0
    for f in sorted(norm.rglob("*.md")) if norm.exists() else []:
        text = f.read_text(encoding="utf-8")
        if "Source ID" not in text and "SRC-" not in text:
            continue
        recs += 1
        for label, toks in SOURCE_META_TOKENS.items():
            # find a "- **<tok> ...:** value" line with a non-blank value
            ok = False
            for line in text.splitlines():
                if any(t.lower() in line.lower() for t in toks) and ":" in line:
                    val = line.split(":", 1)[1].strip().strip("*").strip()
                    if not _is_blank(val):
                        ok = True
                        break
            if not ok:
                emit(f"  [ ERROR ] Source Record {f.name}: '{label}' 표기 누락/빈 값 (원본 보존·출처·타임스탬프 필수).")
                errors += 1
    if recs and errors == 0:
        emit(f"  [ PASS ] Source Record {recs}건 모두 출처·수집시각·원본 표기")

    # originals presence (WARN): if normalized records exist, originals/ should not be empty.
    orig = arch / "sources" / "originals"
    if recs:
        has_orig = orig.exists() and any(
            p.is_file() and p.name not in (".gitkeep", "_manifest.md") for p in orig.rglob("*")
        )
        if not has_orig:
            emit("  [ WARN ] arch/sources/originals/ 가 비어 있습니다 — 원본 보존 또는 접근 포인터를 두세요.")

    # 2) Accessibility: shared artifacts open with 한눈에 + 용어.
    accessible_targets = [
        arch / "architecture-brief.md",
        arch / "as-is" / "intake.md",
    ]
    for f in accessible_targets:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        if len(text.strip()) < 40:
            continue
        if "한눈에" not in text:
            emit(f"  [ ERROR ] {f.name}: '한눈에' 절 없음 — 모든 stakeholder 진입점 필수.")
            errors += 1
        if "```mermaid" not in text:
            emit(f"  [ ERROR ] {f.name}: 구조 산출물에 mermaid 없음 — 도면/흐름은 다이어그램으로(§A18).")
            errors += 1
        if "용어" not in text and "Glossary" not in text:
            emit(f"  [ WARN ] {f.name}: '용어(Glossary)' 절 권장(약어/전문용어 풀이).")
    if errors == 0 and any(f.exists() for f in accessible_targets):
        emit("  [ PASS ] 공유 산출물 접근성(한눈에 + mermaid) 충족")
    if recs == 0 and not any(f.exists() for f in accessible_targets):
        emit("  [ INFO ] source record / 공유 산출물 없음 — 게이트 대상 없음(정상).")
    return errors




SHARED_DELIVERABLES = [
    "architecture-brief.md", "as-is/intake.md", "executive-summary.md",
    "stakeholder-summary.md", "implementation-readiness-report.md",
    "stakeholder-action-plan.md", "decision-dashboard.md",
]
BANNED_PHRASES = ["비전문가", "임원도 이해", "non-technical", "for non-experts",
                  "executive-friendly", "layperson", "non-specialist"]
_HANGUL = re.compile(r"[\uac00-\ud7a3]")
_LATIN = re.compile(r"[A-Za-z]")


def _prose_lines(text: str):
    """Yield narrative lines, skipping code fences, tables, and link/badge-only lines."""
    in_code = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code; continue
        if in_code or not s or s.startswith("|") or s.startswith(">"):
            continue
        yield s


def check_korean_first(print_errors: bool = False) -> int:
    """Shared deliverables (incl. Source Records) must be Korean-narrative (tech terms English ok).
    No-op when none exist."""
    errors = 0
    def emit(m):
        if print_errors: print(m)
    arch = Path("arch")
    if not arch.exists():
        return 0
    targets = [arch / f for f in SHARED_DELIVERABLES if (arch / f).exists()]
    norm = arch / "sources" / "normalized"
    if norm.exists():
        targets += [f for f in sorted(norm.rglob("*.md"))]
    checked = 0
    for f in targets:
        text = f.read_text(encoding="utf-8")
        if len(text.strip()) < 60:
            continue
        checked += 1
        english_lines = 0; korean_lines = 0
        for s in _prose_lines(text):
            latin = len(_LATIN.findall(s))
            if latin < 25:
                continue
            if _HANGUL.search(s):
                korean_lines += 1
            else:
                english_lines += 1
        if english_lines >= 3 and korean_lines == 0:
            emit(f"  [ ERROR ] {f.name}: 서술이 영어로 작성됨 — stakeholder 산출물은 한국어 우선(기술용어만 영어). (영문 문장 {english_lines}줄)")
            errors += 1
        elif english_lines >= 5 and english_lines > korean_lines:
            emit(f"  [ ERROR ] {f.name}: 영문 서술 비중 과다({english_lines} > 한글 {korean_lines}) — 한국어로 다시 작성.")
            errors += 1
    if checked and errors == 0:
        emit(f"  [ PASS ] 공유 산출물 {checked}건 한국어 우선 충족")
    elif checked == 0:
        emit("  [ INFO ] 공유 산출물 없음 — 한국어-우선 게이트 대상 없음.")
    return errors


def check_forbidden_phrasing(print_errors: bool = False) -> int:
    """Deliverables must not condescend to readers ('비전문가', 'for non-experts', ...)."""
    errors = 0
    def emit(m):
        if print_errors: print(m)
    arch = Path("arch")
    if not arch.exists():
        return 0
    hits = 0
    for f in sorted(arch.rglob("*.md")):
        low = f.read_text(encoding="utf-8").lower()
        for ph in BANNED_PHRASES:
            if ph.lower() in low:
                emit(f"  [ ERROR ] {f.name}: 낮춤 표현 '{ph}' 사용 — '모든 stakeholder를 위한 쉬운 설명'으로 바꾸세요.")
                errors += 1; hits += 1
    if hits == 0:
        emit("  [ PASS ] 낮춤 표현(비전문가/임원도 이해/non-expert 등) 없음")
    return errors


def check_source_design_impact(print_errors: bool = False) -> int:
    errors = 0
    def emit(msg: str):
        if print_errors:
            print(msg)
    norm = Path("arch") / "sources" / "normalized"
    if not norm.exists():
        emit("  [ INFO ] normalized Source Record 없음 — 게이트 대상 없음(정상).")
        return 0
    recs = [p for p in sorted(norm.rglob("*.md")) if p.is_file() and p.name != ".gitkeep"]
    if not recs:
        emit("  [ INFO ] normalized Source Record 없음 — 게이트 대상 없음(정상).")
        return 0
    required = ["설계 영향", "Requirements", "Constraints", "Risks", "Assumptions", "Open Questions", "Architecture Impact"]
    for f in recs:
        text = f.read_text(encoding="utf-8")
        missing = [t for t in required if t.lower() not in text.lower()]
        if missing:
            emit(f"  [ ERROR ] Source Record가 요약집 수준입니다: {f} — 누락: {', '.join(missing)}")
            errors += 1
    if errors == 0:
        emit(f"  [ PASS ] Source Record {len(recs)}건이 Source-to-Design Impact 포함")
    return errors


def check_stakeholder_handoff(print_errors: bool = False) -> int:
    errors = 0
    def emit(msg: str):
        if print_errors:
            print(msg)
    required_files = [
        Path("arch") / "stakeholder-action-plan.md",
        Path("arch") / "implementation-readiness-report.md",
    ]
    # Only enforce after architecture brief or ADRs exist; fresh starter should pass.
    active = (Path("arch") / "architecture-brief.md").exists() or bool(list(Path("arch").glob("adr-*.md"))) if Path("arch").exists() else False
    if not active:
        emit("  [ INFO ] baseline 산출물 전 단계 — stakeholder handoff 게이트 대기.")
        return 0
    roles = ["CX", "UX", "PM", "Client", "Server", "QA"]
    for f in required_files:
        if not f.exists() or len(f.read_text(encoding="utf-8").strip()) < 80:
            emit(f"  [ ERROR ] stakeholder/implementation handoff 산출물 누락 또는 빈 파일: {f}")
            errors += 1
            continue
        text = f.read_text(encoding="utf-8")
        missing_roles = [r for r in roles if r.lower() not in text.lower()]
        if missing_roles:
            emit(f"  [ ERROR ] {f}: 담당 role 누락 — {', '.join(missing_roles)}")
            errors += 1
    if errors == 0:
        emit("  [ PASS ] stakeholder handoff / implementation readiness 산출물 존재")
    return errors


def check_artifact_coverage(print_errors: bool = False) -> int:
    p = Path("workflow") / "artifact-coverage-matrix.md"
    if not p.exists():
        if print_errors: print("  [ ERROR ] artifact-coverage-matrix.md 누락")
        return 1
    text = p.read_text(encoding="utf-8")
    # Do not fail fresh template-only starter. Fail only when there are real SRC/REQ/Risk rows marked Missing.
    real_missing = []
    for line in text.splitlines():
        if line.lstrip().startswith("|") and "Missing" in line and not "<TBD>" in line:
            real_missing.append(line.strip())
    if print_errors:
        for line in real_missing:
            print(f"  [ ERROR ] Required artifact Missing: {line}")
        if not real_missing:
            print("  [ PASS ] 실제 Missing coverage blocker 없음")
    return len(real_missing)

# ── commands ───────────────────────────────────────────────────────────────────
def cmd_check(_args=None) -> int:
    meta = load_meta()
    mode = resolve_mode(meta)
    authoring = mode == AUTHORING_MODE

    print("=" * 41)
    print(f"YSDA Arch Harness Compliance Checker (check) — mode={mode}")
    print("=" * 41)
    errors = 0

    print("1. 필수 구성 파일:")
    required = AUTHORING_REQUIRED_FILES if authoring else PROJECT_REQUIRED_FILES
    for f in required:
        if Path(f).is_file():
            print(f"  [ PASS ] {f}")
        else:
            print(f"  [ ERROR ] 누락: {f}")
            errors += 1
    if not authoring:
        for f in PROJECT_RECOMMENDED_FILES:
            if not Path(f).is_file():
                print(f"  [ WARN ] 권장(표준 스냅샷) 누락: {f}")

    print("\n2. 버전 메타데이터:")
    if not meta:
        print("  [ ERROR ] harness-version.json 파싱 실패/누락")
        errors += 1
    else:
        if meta.get("harness_family") == "ysda-arch-harness":
            print("  [ PASS ] harness_family=ysda-arch-harness")
        else:
            print(f"  [ ERROR ] harness_family 오류: {meta.get('harness_family')}")
            errors += 1
        if meta.get("agents_md_mirror_version"):
            print(f"  [ PASS ] agents_md_mirror_version={meta.get('agents_md_mirror_version')}")
        else:
            print("  [ ERROR ] agents_md_mirror_version 누락")
            errors += 1
        if not meta.get("applied_mode"):
            print("  [ WARN ] applied_mode 미기재 — self-hosted로 간주됨")

    print("\n3. AGENTS.md 미러 마커:")
    ap = Path("AGENTS.md")
    if ap.exists():
        m = re.search(r"<!-- ysda-arch-runtime-mirror: Common v([\d.]+)", ap.read_text(encoding="utf-8"))
        if m:
            print(f"  [ PASS ] 미러 마커 v{m.group(1)}")
        else:
            print("  [ ERROR ] AGENTS.md 미러 마커 누락")
            errors += 1
    else:
        print("  [ ERROR ] AGENTS.md 없음")
        errors += 1

    if authoring:
        print("\n4. mermaid-first 점검 (Common §A18):")
        errors += check_mermaid_first(print_errors=True)
        errors += check_mermaid_contract(print_errors=True)
        print("\n5. Release/version 일관성 (Common §A9.1, self-hosted):")
        errors += check_release_consistency(print_errors=True)
        print("\n6. Sample target 안전성:")
        errors += check_sample_target_values(print_errors=True)
        print("\n7. 범용 planning 파일 금지:")
        errors += check_forbidden_plan_files(print_errors=True)
        print("\n8. Canonical 산출물 경로:")
        errors += check_canonical_path_references(print_errors=True)
    else:
        print("\n4. 프로젝트 closure (tracker/뷰 freshness):")
        errors += check_project_freshness(print_errors=True)
        print("\n5. 범용 planning 파일 금지:")
        errors += check_forbidden_plan_files(print_errors=True)
        print("  [ INFO ] 프로젝트 모드 — 하네스 release-ADR/스코프드 사이드카 요건은 건너뜀.")

    if authoring:
        print("\n9. 프로젝트 산출물 게이트(가정/원본/접근성/impact/coverage/stakeholder/한국어/낮춤표현):")
        print("  [ INFO ] self-hosted(하네스 자체) — 프로젝트 산출물 게이트는 대상 없음, 건너뜀.")
    else:
        print("\n9. 가정 명세 / provenance 게이트:")
        errors += check_assumption_provenance(print_errors=True)

        print("\n10. 원본 보존 / 접근성 게이트:")
        errors += check_accessibility_and_sources(print_errors=True)

        print("\n11. Source-to-Design Impact 게이트:")
        errors += check_source_design_impact(print_errors=True)

        print("\n12. Artifact Coverage 게이트:")
        errors += check_artifact_coverage(print_errors=True)

        print("\n13. Stakeholder Handoff 게이트:")
        errors += check_stakeholder_handoff(print_errors=True)

        print("\n14. 한국어 우선 게이트:")
        errors += check_korean_first(print_errors=True)

        print("\n15. 낮춤 표현 금지 게이트:")
        errors += check_forbidden_phrasing(print_errors=True)

    print("\n" + "=" * 41)
    print(f"결과 - 에러: {errors}건")
    if errors:
        print("[ RESULT ] 표준 위반. 에러를 해결하세요.")
        print("=" * 41)
        return 1
    print(f"[ RESULT ] ysda-arch-harness (mode={mode}) 표준 충족 (PASS)")
    print("=" * 41)
    return 0


COPY_TREES = ["standards", "prompts", "templates", "quality"]
COPY_FILES = [
    "AGENTS.md", "README.md", ".clinerules",
    os.path.join("workflow", "ROLES.md"),
    os.path.join("workflow", "IO-CONTRACT.md"),
    os.path.join("doc", "methodology-references.md"),
    os.path.join("doc", "personal-vs-arch-harness.md"),
    os.path.join("doc", "adoption-and-brownfield.md"),
    os.path.join("scripts", "archdev.py"),
]
BLANK_TRACKERS = {
    os.path.join("workflow", "STATUS.md"):
        "# 설계 저장소 상태 대시보드 (STATUS)\n\n## 0. 개요\n- **Project:** <과제명>\n"
        "- **Owner:** <owner>\n- **Harness:** ysda-arch-harness {ver} / mode={mode}\n\n"
        "## 1. 현재 단계\n- **Phase:** <P0 as-is 흡수 / P1 시스템 정의 ...>\n- **Health:** Green\n\n"
        "## 2. 우선순위 품질 시나리오 (Top QS)\n- [ ] <TBD>\n\n## 3. 활성 작업\n- [ ] <TBD>\n\n"
        "## 4. 열린 결정 (Open ADRs)\n- 없음\n\n## 5. 블로커\n- 없음\n\n## 7. 다음 액션\n- <TBD>\n",
    os.path.join("workflow", "traceability-matrix.md"):
        "# 추적성 매트릭스 (Traceability)\n\nCommon §A13. 모든 우선순위 QS는 ADR과 평가 행을 가져야 "
        "Design Baseline(§D8) 승인 가능.\n\n"
        "| Use case / Quality scenario | 결정 드라이버 | ADR | 아키텍처 요소 / 다이어그램 | 평가 결과 |\n"
        "|---|---|---|---|---|\n| <TBD> | <TBD> | <TBD> | <TBD> | <TBD> |\n",
    os.path.join("workflow", "artifact-registry.md"):
        "# 산출물 레지스트리 (Artifact Registry)\n\n| Artifact | Status | Last update |\n"
        "|---|---|---|\n| arch/architecture-brief.md | <TBD> | <TBD> |\n",
    os.path.join("workflow", "artifact-coverage-matrix.md"):
        "# Artifact Coverage Matrix\n\n| Coverage ID | Source / Trigger | Extracted Item | Required Artifact | Owner | Status | Gap / Next Action |\n"
        "|---|---|---|---|---|---|---|\n| COV-001 | <TBD> | <TBD> | <TBD> | <TBD> | Missing | <TBD> |\n",
    os.path.join("reports", "progress.md"):
        "# Progress\n\n- <date> 프로젝트 부트스트랩 (archdev init).\n",
    os.path.join("reports", "qna-log.md"):
        "# Q&A Log (append-only)\n\n| # | 질문 | 답/결정 | 근거 링크 |\n|---|---|---|---|\n",
}
ARCH_SKELETON = [
    "arch/sources/originals", "arch/sources/originals/.gitkeep",
    "arch/sources/normalized", "arch/sources/normalized/.gitkeep",
    "arch/as-is", "arch/as-is/.gitkeep",
    "arch/assumptions", "arch/assumptions/.gitkeep",
    "arch/usecases", "arch/usecases/.gitkeep",
    "arch/quality", "arch/quality/.gitkeep",
    "arch/views", "arch/views/.gitkeep",
    "arch/candidates", "arch/candidates/.gitkeep",
    "arch/evaluation", "arch/evaluation/.gitkeep",
    "arch/domain", "arch/domain/.gitkeep",
]


def cmd_init(args=None) -> int:
    """Scaffold an applied design repo. Run from a canonical clone.

    usage: archdev init <target-dir> [--mode design|audit] [--name "<project>"]
    """
    args = args or sys.argv[2:]
    if not args:
        print("usage: archdev init <target-dir> [--mode design|audit] [--name <project>]")
        return 1
    target = Path(args[0])
    mode = "design"
    name = "<과제명>"
    for i, a in enumerate(args):
        if a == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
        if a == "--name" and i + 1 < len(args):
            name = args[i + 1]
    if mode not in PROJECT_MODES:
        print(f"  [ ERROR ] --mode 는 {sorted(PROJECT_MODES)} 중 하나여야 합니다.")
        return 1
    if not Path("AGENTS.md").exists() or not META.exists():
        print("  [ ERROR ] 이 명령은 canonical arch-harness 클론 루트에서 실행하세요.")
        return 1
    target.mkdir(parents=True, exist_ok=True)

    for tree in COPY_TREES:
        if Path(tree).exists():
            shutil.copytree(tree, target / tree, dirs_exist_ok=True)
    for f in COPY_FILES:
        if Path(f).exists():
            (target / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target / f)

    ver = (load_meta() or {}).get("harness_version", TARGET_VERSION)
    for rel, body in BLANK_TRACKERS.items():
        (target / rel).parent.mkdir(parents=True, exist_ok=True)
        (target / rel).write_text(body.format(ver=ver, mode=mode), encoding="utf-8")
    for entry in ARCH_SKELETON:
        p = target / entry
        if entry.endswith(".gitkeep"):
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("", encoding="utf-8")
        else:
            p.mkdir(parents=True, exist_ok=True)
    # seed the originals manifest so batch ingestion is ready out of the box
    man_src = Path("templates") / "sources-manifest.md"
    if man_src.exists():
        (target / "arch" / "sources" / "originals" / "_manifest.md").write_text(
            man_src.read_text(encoding="utf-8"), encoding="utf-8")

    meta = {
        "harness_family": "ysda-arch-harness",
        "harness_version": ver,
        "applied_mode": mode,
        "adoption_depth": "standard",
        "applied_date": date.today().isoformat(),
        "canonical_root": "<git url of ysda-arch-harness>",
        "source_common": "standards/ysda-arch-harness-common.md",
        "source_mode": "standards/ysda-arch-design-standard.md",
        "common_checksum": "<sha256>",
        "mode_checksum": "<sha256>",
        "agents_md_mirror_version": ver,
        "notes": [f"Applied project ({mode}). Excludes harness release ADRs / evolution history."],
    }
    (target / META).parent.mkdir(parents=True, exist_ok=True)
    (target / META).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    inv = ("# 이 프로젝트 단축 프롬프트\n"
           "- 기존 자산 흡수: `기존 설계도면/모듈설명으로 as-is부터 시작하자: <과제>`\n"
           "- 원본 정리: `이 자료를 원본 보존하고 출처·타임스탬프 붙인 Source Record로 정리해줘`\n"
           "- 가정 명세화: `미확인 항목을 가정(AS-)으로 명세하고, 신뢰도·blast·확인질문을 채워줘`\n"
           "- 분기 후보: `load-bearing 가정별로 분기 후보 구조를 따로 설계해줘`\n"
           "- 쉽게 정리: `모든 stakeholder가 이해하게 한국어로 한눈에 절 + mermaid + 용어표로 정리해줘 (요약 말고)`\n"
           "- 설계 시작: `시스템 정의부터 시작하자: <과제>`\n"
           "- 점검: `archdev check`  / 리더 digest: `archdev report`\n")
    (target / META.parent / "invocation-prompts.md").write_text(inv, encoding="utf-8")

    print(f"[ OK ] '{target}' 에 applied 프로젝트(mode={mode}) 부트스트랩 완료.")
    print("  - 제외됨: arch/adr-*(하네스 릴리스), doc/harness-evolution-history.md")
    print(f"  - 다음: cd {target} && python scripts/archdev.py check")
    print(f"  - 과제명: {name}")
    return 0


def cmd_report(_args=None) -> int:
    """Leader digest — ADR status, open risks, High-QS coverage gaps."""
    print("=" * 41)
    print("YSDA Arch — Leader Digest (report)")
    print("=" * 41)

    adrs = _scan_adrs()
    print("\n[ ADR 현황 ]")
    if not adrs:
        print("  (arch/adr-*.md 없음)")
    else:
        print(f"  {'file':<34} {'status':<10} {'owner':<8} drivers")
        for r in adrs:
            print(f"  {r['file']:<34} {r['status']:<10} {r['owner']:<8} {r['drivers']}")
        proposed = [r['file'] for r in adrs if r['status'].lower() == 'proposed']
        if proposed:
            print(f"  ↳ owner 승인 대기: {', '.join(proposed)}")

    risks = _scan_open_risks()
    print("\n[ Open Risks ]")
    if not risks:
        print("  (open risk 없음 또는 risk-register 미작성)")
    else:
        for src, rid, desc in risks:
            print(f"  {rid}: {desc}  ({src})")

    # Load-bearing unverified assumptions + pending verification questions.
    print("\n[ 미확인 가정 / 담당자 확인 대기 ]")
    reg_dir = Path("arch") / "assumptions"
    found = 0
    for f in sorted(reg_dir.rglob("*.md")) if reg_dir.exists() else []:
        for header, rows in _md_tables(f.read_text(encoding="utf-8")):
            i_id = _col(header, "id"); i_stmt = _col(header, "가정", "assumption")
            if i_id < 0 or i_stmt < 0:
                continue
            i_conf = _col(header, "신뢰도", "confidence"); i_blast = _col(header, "blast")
            i_q = _col(header, "검증", "verification", "질문"); i_status = _col(header, "상태", "status")
            for r in rows:
                if len(r) <= i_stmt or _is_blank(r[i_stmt]):
                    continue
                status = (r[i_status] if 0 <= i_status < len(r) else "open").strip().lower()
                if not status.startswith("open"):
                    continue
                conf = r[i_conf] if 0 <= i_conf < len(r) else ""
                blast = r[i_blast] if 0 <= i_blast < len(r) else ""
                lb = "★load-bearing" if ("low" in conf.lower() and "high" in blast.lower()) else ""
                q = r[i_q].strip() if 0 <= i_q < len(r) else ""
                asid = r[i_id].strip().strip("`")
                print(f"  {asid} {lb}: Q→ {q or '<검증질문 없음>'}")
                found += 1
    if not found:
        print("  (미확인 Open 가정 없음)")

    tm = Path("workflow") / "traceability-matrix.md"
    print("\n[ Traceability 경고 ]")
    if tm.exists():
        gaps = 0
        for line in tm.read_text(encoding="utf-8").splitlines():
            if re.search(r"QS-\d+", line) and ("<TBD>" in line or "| [ADR" in line and "미달" in line):
                print(f"  ↳ {line.strip()}")
                gaps += 1
        if gaps == 0:
            print("  (눈에 띄는 미완 QS 행 없음 — 상세는 archdev check)")
    else:
        print("  traceability-matrix.md 없음")
    print("=" * 41)
    return 0


def cmd_info(_args=None) -> int:
    meta = load_meta() or {}
    print(f"YSDA Arch Harness v{meta.get('harness_version','?')} / mode={meta.get('applied_mode','self-hosted')}")
    print(f"AGENTS mirror: {meta.get('agents_md_mirror_version','?')}")
    return 0


def cmd_list(_args=None) -> int:
    for name, desc in COMMANDS_DESC.items():
        print(f"  {name:<8} : {desc}")
    return 0


COMMANDS_DESC = {
    "check": "mode-aware 일관성 점검(self-hosted=하네스 / design·audit=프로젝트)",
    "init": "applied 프로젝트 저장소 부트스트랩 (canonical 클론에서 실행)",
    "report": "리더 digest — ADR/risk/QS 갭 추출",
    "info": "하네스 버전·모드 표시",
    "list": "명령 목록",
}
HANDLERS = {"check": cmd_check, "init": cmd_init, "report": cmd_report,
            "info": cmd_info, "list": cmd_list}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in HANDLERS:
        print("usage: archdev <check|init|report|info|list>")
        return 1
    return HANDLERS[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
