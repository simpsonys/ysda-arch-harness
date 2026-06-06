import os
import sys
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
            self.assertTrue(os.path.exists(f), f"missing {f}")

    def test_mermaid_present_in_key_docs(self):
        self._chdir_root()
        self.assertEqual(archdev.check_mermaid_first(), 0)


if __name__ == "__main__":
    unittest.main()
