from leafnode import LeafNode
import unittest


class Test_LeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_raw_test(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node, "Hello world!")


if __name__ == "__main__":
    unittest.main()
