import tempfile
import unittest
from pathlib import Path

from preprocess_case_renumber import process


class TestPreprocessCaseRenumber(unittest.TestCase):
    def _touch(self, folder: Path, name: str) -> None:
        path = folder / name
        path.write_text("x", encoding="utf-8")

    def test_lowercase_and_renumber(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset_3 = root / "dataset_3"
            dataset_5 = root / "dataset_5"
            dataset_3.mkdir()
            dataset_5.mkdir()

            for folder, appname in [(dataset_3, "taobao"), (dataset_5, "TaoBao")]:
                self._touch(folder, f"{appname}_1_1.jpg")
                self._touch(folder, f"{appname}_1_1_visualized.jpg")
                self._touch(folder, f"{appname}_1_1.txt")

            output = root / "backup"
            summary = process(root, output_root=output, recursive=False, dry_run=False)

            self.assertEqual(summary["datasets"], 2)
            self.assertEqual(summary["groups"], 2)
            self.assertEqual(summary["copies"], 6)

            self.assertTrue((output / "dataset_3" / "taobao_1_1.jpg").exists())
            self.assertTrue((output / "dataset_5" / "taobao_2_1.jpg").exists())


if __name__ == "__main__":
    unittest.main()
