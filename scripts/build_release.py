#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a clean applied-project starter zip from this canonical arch-harness clone.

Reuses `archdev init` to stage the starter (single source of truth), then zips it to
`dist/ysda-arch-starter-<version>-<mode>.zip`. The zip is a ready-to-use project skeleton:
unzip, set owner/name in workflow/STATUS.md, start. Brownfield(소스 없음) 과제는 --mode audit.
Harness 자신의 release ADR / evolution history는 제외된다.

usage: python scripts/build_release.py [--mode design|audit] [--out dist]
"""
from __future__ import annotations
import json, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / ".ysda-arch-harness" / "harness-version.json"

def version() -> str:
    try:
        return json.loads(META.read_text(encoding="utf-8")).get("harness_version", "0.0.0")
    except Exception:
        return "0.0.0"

def main() -> int:
    args = sys.argv[1:]; mode = "design"; out_dir = ROOT / "dist"
    for i, a in enumerate(args):
        if a == "--mode" and i + 1 < len(args): mode = args[i + 1]
        if a == "--out" and i + 1 < len(args): out_dir = Path(args[i + 1])
    ver = version(); out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"ysda-arch-starter-{ver}-{mode}.zip"
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "ysda-arch-starter"
        rc = subprocess.run([sys.executable, str(ROOT / "scripts" / "archdev.py"),
             "init", str(stage), "--mode", mode, "--name", "<NEW PROJECT>"], cwd=ROOT).returncode
        if rc != 0:
            print("[ ERROR ] archdev init 실패"); return 1
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(stage.rglob("*")):
                if p.is_file(): zf.write(p, p.relative_to(stage.parent))
    print(f"[ OK ] starter zip 생성: {zip_path}  (mode={mode}, v{ver})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
