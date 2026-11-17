import unittest
from htmlnode import HTMLNode


class Test_HTMLNode(unittest.TestCase):
    def test_no_tag(self):
        node = HTMLNode(None, "Hello world", None, None)
        txt = "Hello world"
        self.assertEqual(node, txt)


if __name__ == "__main__":
    unittest.main()
