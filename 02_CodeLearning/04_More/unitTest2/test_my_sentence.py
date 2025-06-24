from sentence import Sentence
import unittest

class TestMySentence(unittest.TestCase):
    # * 初始化测试环境，在所有测试方法执行前执行
    def setUp(self):
        self.sentence1 = Sentence("test1", "Hello, world!")
        self.sentence2 = Sentence("test2", "Hello, world!")

    def test_init(self):
        self.assertEqual(self.sentence1.type, "test1")
    
    def test_str(self):
        self.assertEqual(str(self.sentence1), "test1: Hello, world!")
    
    def test_repr(self):
        self.assertEqual(repr(self.sentence1), "Sentence(type=test1, text=Hello, world!)")
