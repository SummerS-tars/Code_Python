import tempfile
import unittest
from pathlib import Path

from cleaner_renamer1 import process_folder


class CleanerRenamer1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _touch(self, name: str) -> None:
        path = self.folder / name
        path.write_text("test", encoding="utf-8")

    def test_removes_unmatched_and_renames(self) -> None:
        # 完整三件套
        self._touch("WeChat_99_1.jpg")
        self._touch("WeChat_99_1_visualized.jpg")
        self._touch("WeChat_99_1.txt")

        # 缺少 visualized
        self._touch("QQ_88_1.jpg")
        self._touch("QQ_88_1.txt")

        # 只有 visualized
        self._touch("QQ_77_1_visualized.jpg")

        summary = process_folder(self.folder)

        self.assertEqual(summary["remaining_sets"], 1)
        self.assertTrue((self.folder / "WeChat_1_1.jpg").exists())
        self.assertTrue((self.folder / "WeChat_1_1_visualized.jpg").exists())
        self.assertTrue((self.folder / "WeChat_1_1.txt").exists())
        self.assertFalse((self.folder / "WeChat_99_1.jpg").exists())
        self.assertEqual(summary["deleted"], 3)

    def test_dul_times_reindexed_per_appname_and_id(self) -> None:
        self._touch("huya_6_1.jpg")
        self._touch("huya_6_1_visualized.jpg")
        self._touch("huya_6_1.txt")

        self._touch("huya_6_5.jpg")
        self._touch("huya_6_5_visualized.jpg")
        self._touch("huya_6_5.txt")

        self._touch("douyu_6_2.jpg")
        self._touch("douyu_6_2_visualized.jpg")
        self._touch("douyu_6_2.txt")

        process_folder(self.folder)

        self.assertTrue((self.folder / "huya_1_1.jpg").exists())
        self.assertTrue((self.folder / "huya_1_2.jpg").exists())
        self.assertTrue((self.folder / "douyu_1_1.jpg").exists())

    def test_id_reindexed_per_appname(self) -> None:
        self._touch("alipay_1_1.jpg")
        self._touch("alipay_1_1_visualized.jpg")
        self._touch("alipay_1_1.txt")

        self._touch("alipay_4_1.jpg")
        self._touch("alipay_4_1_visualized.jpg")
        self._touch("alipay_4_1.txt")

        self._touch("wechat_2_1.jpg")
        self._touch("wechat_2_1_visualized.jpg")
        self._touch("wechat_2_1.txt")

        process_folder(self.folder)

        self.assertTrue((self.folder / "alipay_1_1.jpg").exists())
        self.assertTrue((self.folder / "alipay_2_1.jpg").exists())
        self.assertTrue((self.folder / "wechat_1_1.jpg").exists())

    def test_ignores_temporary_files(self) -> None:
        self._touch(".__tmp__Weibo_4_1.jpg")
        self._touch(".__tmp__Weibo_4_1_visualized.jpg")
        self._touch(".__tmp__Weibo_4_1.txt")

        self._touch("Weibo_4_1.jpg")
        self._touch("Weibo_4_1_visualized.jpg")
        self._touch("Weibo_4_1.txt")

        summary = process_folder(self.folder)

        self.assertEqual(summary["remaining_sets"], 1)
        self.assertTrue((self.folder / "Weibo_1_1.jpg").exists())


if __name__ == "__main__":
    unittest.main()
