import json
import tempfile
import unittest
from pathlib import Path

from selector4 import load_config, process


class TestSelector4(unittest.TestCase):
    def _touch(self, folder: Path, name: str) -> None:
        path = folder / name
        path.write_text("x", encoding="utf-8")

    def test_process_splits_single_and_multi(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "dataset_app"
            dataset.mkdir()

            # single group (dul_times max == 1)
            self._touch(dataset, "app_1_1.jpg")
            self._touch(dataset, "app_1_1_visualized.jpg")
            self._touch(dataset, "app_1_1.txt")

            # small multi group (dul_times max == 2)
            self._touch(dataset, "app_2_1.jpg")
            self._touch(dataset, "app_2_1_visualized.jpg")
            self._touch(dataset, "app_2_1.txt")
            self._touch(dataset, "app_2_2.jpg")
            self._touch(dataset, "app_2_2_visualized.jpg")
            self._touch(dataset, "app_2_2.txt")

            # large multi group (dul_times max == 4)
            for dul in range(1, 5):
                self._touch(dataset, f"app_3_{dul}.jpg")
                self._touch(dataset, f"app_3_{dul}_visualized.jpg")
                self._touch(dataset, f"app_3_{dul}.txt")

            config_path = root / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "val_ratio": 0.5,
                        "prob_pick_single_from_small_multi": 1.0,
                        "small_group_threshold": 3,
                        "random_seed": 0,
                    }
                ),
                encoding="utf-8",
            )

            summary = process(
                root=root,
                output_root=root / "out",
                config=load_config(config_path),
                recursive=False,
                dry_run=False,
            )

            self.assertEqual(summary["groups"], 7)
            self.assertEqual(summary["val_groups"], 3)
            self.assertEqual(summary["data_groups"], 4)

            val_images = list((root / "out" / "images" / "val").iterdir())
            self.assertEqual(len(val_images), 3)


if __name__ == "__main__":
    unittest.main()
