import tempfile
import unittest
from pathlib import Path

from renamer2 import process_folder


class TestRenamer2(unittest.TestCase):
    def _touch(self, folder: Path, name: str) -> None:
        path = folder / name
        path.write_text("x", encoding="utf-8")

    def test_renames_by_senary_and_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            files = [
                "app_main_1_1.jpg",
                "app_main_1_1_visualized.jpg",
                "app_main_1_1.txt",
                "app_personal_1_1.jpg",
                "app_personal_1_1_visualized.jpg",
                "app_personal_1_1.txt",
                "app_main_2_1.jpg",
                "app_main_2_1_visualized.jpg",
                "app_main_2_1.txt",
            ]
            for name in files:
                self._touch(folder, name)

            summary = process_folder(folder)
            self.assertEqual(summary["remaining_sets"], 3)
            self.assertEqual(summary["renamed"], 9)

            expected = {
                "app_1_1.jpg",
                "app_1_1_visualized.jpg",
                "app_1_1.txt",
                "app_2_1.jpg",
                "app_2_1_visualized.jpg",
                "app_2_1.txt",
                "app_3_1.jpg",
                "app_3_1_visualized.jpg",
                "app_3_1.txt",
            }
            self.assertEqual({p.name for p in folder.iterdir()}, expected)

    def test_preserves_dul_times(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            files = [
                "app_main_1_1.jpg",
                "app_main_1_1_visualized.jpg",
                "app_main_1_1.txt",
                "app_main_1_2.jpg",
                "app_main_1_2_visualized.jpg",
                "app_main_1_2.txt",
            ]
            for name in files:
                self._touch(folder, name)

            process_folder(folder)
            self.assertTrue((folder / "app_1_1.jpg").exists())
            self.assertTrue((folder / "app_1_2.jpg").exists())


if __name__ == "__main__":
    unittest.main()
