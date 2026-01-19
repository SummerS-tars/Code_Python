import tempfile
import unittest
from pathlib import Path

from dataset_stats import compute_stats, write_csv


class DatasetStatsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _touch(self, name: str) -> None:
        path = self.folder / name
        path.write_text("test", encoding="utf-8")

    def test_stats_calculation(self) -> None:
        # app: alpha
        self._touch("alpha_1_1.jpg")
        self._touch("alpha_1_1_visualized.jpg")
        self._touch("alpha_1_1.txt")

        self._touch("alpha_2_1.jpg")
        self._touch("alpha_2_1_visualized.jpg")
        self._touch("alpha_2_1.txt")
        self._touch("alpha_2_2.jpg")
        self._touch("alpha_2_2_visualized.jpg")
        self._touch("alpha_2_2.txt")

        # app: beta
        self._touch("beta_9_1.jpg")
        self._touch("beta_9_1_visualized.jpg")
        self._touch("beta_9_1.txt")

        # unmatched should be ignored
        self._touch("gamma_1_1.jpg")
        self._touch(".__tmp__alpha_3_1.jpg")

        stats = compute_stats(self.folder)

        self.assertIn("alpha", stats)
        self.assertIn("beta", stats)
        self.assertNotIn("gamma", stats)

        self.assertEqual(stats["alpha"]["groups"], 2.0)
        self.assertEqual(stats["alpha"]["total_items"], 3.0)
        self.assertAlmostEqual(stats["alpha"]["single_ratio"], 0.5)
        self.assertEqual(stats["beta"]["groups"], 1.0)
        self.assertEqual(stats["beta"]["total_items"], 1.0)
        self.assertAlmostEqual(stats["beta"]["single_ratio"], 1.0)

        self.assertIn("__total__", stats)
        self.assertEqual(stats["__total__"]["groups"], 3.0)
        self.assertEqual(stats["__total__"]["total_items"], 4.0)

    def test_recursive_scan(self) -> None:
        nested = self.folder / "nested" / "inner"
        nested.mkdir(parents=True)

        (nested / "appx_1_1.jpg").write_text("test", encoding="utf-8")
        (nested / "appx_1_1_visualized.jpg").write_text("test", encoding="utf-8")
        (nested / "appx_1_1.txt").write_text("test", encoding="utf-8")

        stats = compute_stats(self.folder, recursive=True)
        self.assertIn("appx", stats)
        self.assertEqual(stats["appx"]["groups"], 1.0)
        self.assertEqual(stats["appx"]["total_items"], 1.0)

    def test_write_csv(self) -> None:
        self._touch("appcsv_1_1.jpg")
        self._touch("appcsv_1_1_visualized.jpg")
        self._touch("appcsv_1_1.txt")

        stats = compute_stats(self.folder)
        output = self.folder / "stats.csv"
        write_csv(stats, output)

        content = output.read_text(encoding="utf-8")
        self.assertIn("appname,groups,total_items,single_ratio", content)
        self.assertIn("appcsv,1,1,1.000000", content)
        self.assertIn("__total__", content)


if __name__ == "__main__":
    unittest.main()
