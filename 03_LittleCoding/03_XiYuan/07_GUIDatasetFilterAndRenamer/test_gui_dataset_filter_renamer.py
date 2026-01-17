import tempfile
import unittest
from pathlib import Path

from gui_dataset_filter_renamer import DatasetConfig, process_dataset_folder


class TestGuiDatasetFilterRenamer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.dataset = self.root / "dataset_demo"
        self.dataset.mkdir(parents=True)

        self._write("mainpage_1_20260115_120000.jpg")
        self._write("mainpage_1_20260115_120000_visualized.jpg")
        self._write("mainpage_1_20260115_120000.txt")
        self._write("mainpage_1_20260115_120500_visualized.jpg")

        self._write("detail_2_20260115_120200_visualized.jpg")
        self._write("detail_2_20260115_120200.jpg")

        # Same id but different senary should start dul_times at 1
        self._write("other_2_20260115_120300_visualized.jpg")
        self._write("other_2_20260115_120300.jpg")

        # Orphan (no visualized)
        self._write("mainpage_3_20260115_130000.jpg")
        self._write("mainpage_3_20260115_130000.txt")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write(self, name: str):
        (self.dataset / name).write_text("data", encoding="utf-8")

    def test_filter_and_rename(self):
        config = DatasetConfig(dry_run=False, verbose=False, process_all=False)
        report = process_dataset_folder(self.dataset, config)

        self.assertEqual(len(report.deleted), 2)
        self.assertFalse((self.dataset / "mainpage_3_20260115_130000.jpg").exists())
        self.assertFalse((self.dataset / "mainpage_3_20260115_130000.txt").exists())

        expected_files = {
            "demo_mainpage_1_1.jpg",
            "demo_mainpage_1_1_visualized.jpg",
            "demo_mainpage_1_1.txt",
            "demo_mainpage_1_2_visualized.jpg",
            "demo_detail_2_1.jpg",
            "demo_detail_2_1_visualized.jpg",
            "demo_other_2_1.jpg",
            "demo_other_2_1_visualized.jpg",
        }
        existing_files = {path.name for path in self.dataset.iterdir()}
        self.assertTrue(expected_files.issubset(existing_files))


if __name__ == "__main__":
    unittest.main()
