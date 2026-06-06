import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import archdev  # noqa: E402


class ArchdevTests(unittest.TestCase):
    def _chdir_root(self):
        self._cwd = Path.cwd()
        os.chdir(ROOT)

    def tearDown(self):
        if hasattr(self, "_cwd"):
            os.chdir(self._cwd)

    def test_release_consistency_passes_on_self(self):
        self._chdir_root()
        self.assertEqual(archdev.check_release_consistency(), 0)

    def test_required_files_exist(self):
        self._chdir_root()
        for f in archdev.REQUIRED_FILES:
            self.assertTrue(Path(f).is_file(), f"missing {f}")

    def test_mermaid_present_in_key_docs(self):
        self._chdir_root()
        self.assertEqual(archdev.check_mermaid_first(), 0)

    def test_mermaid_contract_present(self):
        self._chdir_root()
        self.assertEqual(archdev.check_mermaid_contract(), 0)

    def test_sample_target_values_absent(self):
        self._chdir_root()
        self.assertEqual(archdev.check_sample_target_values(), 0)

    def test_forbidden_plan_files_absent(self):
        self._chdir_root()
        self.assertEqual(archdev.check_forbidden_plan_files(), 0)

    def test_canonical_path_references_absent(self):
        self._chdir_root()
        self.assertEqual(archdev.check_canonical_path_references(), 0)

    def test_release_consistency_requires_current_version_adr(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                archdev.META.parent.mkdir(parents=True)
                archdev.META.write_text(
                    '{"harness_version": "' + archdev.TARGET_VERSION + '"}',
                    encoding="utf-8",
                )
                for rel in archdev.TRACKING_DOCS:
                    path = Path(rel)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("v" + archdev.TARGET_VERSION, encoding="utf-8")
                self.assertEqual(archdev.check_release_consistency(), 1)
            finally:
                os.chdir(previous)

    def test_release_consistency_requires_owner_approval(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                archdev.META.parent.mkdir(parents=True)
                archdev.META.write_text(
                    '{"harness_version": "' + archdev.TARGET_VERSION + '"}',
                    encoding="utf-8",
                )
                Path("arch").mkdir()
                Path("arch/adr-001-v" + archdev.TARGET_VERSION + "-test.md").write_text(
                    "- **Status:** Accepted\n- **Owner Approval:** Needed\n",
                    encoding="utf-8",
                )
                for rel in archdev.TRACKING_DOCS:
                    path = Path(rel)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("v" + archdev.TARGET_VERSION, encoding="utf-8")
                self.assertEqual(archdev.check_release_consistency(), 1)
            finally:
                os.chdir(previous)

    def test_sample_target_values_detect_numeric_target(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("templates").mkdir()
                Path("templates/example.md").write_text("p95 ≤ 80", encoding="utf-8")
                self.assertEqual(archdev.check_sample_target_values(), 1)
            finally:
                os.chdir(previous)

    def test_canonical_path_references_detect_alias(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("AGENTS.md").write_text("write `architecture.md`", encoding="utf-8")
                self.assertEqual(archdev.check_canonical_path_references(), 1)
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
