import unittest
from unittest import TestCase

from twelf import InputReader, Lexer


class TestInputReader(TestCase):
    def test_baisc(self):
        text = "hello mate!"
        reader = InputReader(text)
        self.assertEqual(reader.peek(), "h")
        self.assertEqual(reader.consume(), "h")
        self.assertEqual(reader.consume(10), "ello mate!")
        self.assertTrue(reader.is_EOF())


class TestLexer(TestCase):
    def test_basic(self):
        text = "hello mate!"
        lexer = Lexer(InputReader(text))
        self.assertEqual(lexer.peek(), ["hello"])
        self.assertEqual(lexer.consume(2), ["hello", "mate!"])


if __name__ == "__main__":
    unittest.main()
