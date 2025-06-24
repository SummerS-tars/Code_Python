"""
assert 断言，用于判断一个表达式是否为True
如果为False程序会报错

常用的用于测试的库有unittest
并且我们一般将用于测试的代码放在独立的源文件中
启动时使用
python -m unittest <文件名>
其要求是文件名必须以test_开头（不需要指定文件名）
或者是直接指定文件名

这里就涉及到导入其他代码文件的相关语法
不过很简单就是
from 文件名 import 函数名/类名
"""

from calculator import add
import unittest

"""
测试用类，可以在其下定义不同的测试用例
每个测试用例均表现为类下的一个方法
命名有要求，必须以test_开头
"""
class TestCalculator(unittest.TestCase):
    def test_positive_with_positive(self):
        self.assertEqual(add(1, 2), 3)
    def test_positive_with_negative(self):
        self.assertEqual(add(1, -2), -1)
    def test_negative_with_positive(self):
        self.assertEqual(add(-1, 2), 1)
    def test_negative_with_negative(self):
        self.assertEqual(add(-1, -2), -3)

"""
除上述Equal方法外
还有类似于
assertEqual(a, b)
assertNotEqual(a, b)
assertTrue(a)
assertFalse(a)
assertIsNone(a)
assertIsNotNone(a)
assertIn(a, b)
assertNotIn(a, b)
assertGreater(a, b)
assertGreaterEqual(a, b)
assertLess(a, b)
assertLessEqual(a, b)
assertAlmostEqual(a, b)
assertNotAlmostEqual(a, b)
assertSequenceEqual(a, b)
assertListEqual(a, b)
assertTupleEqual(a, b)

推荐使用更为精确的对应方法
因为有更为准确的报错
"""