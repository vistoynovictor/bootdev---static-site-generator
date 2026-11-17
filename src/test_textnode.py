import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_url_none(self):
        node = TextNode("Hello", TextType.TEXT, None)
        self.assertEqual(node.url, None)

    def test_not_eq(self):
        node = TextNode("Node", TextType.TEXT)
        node2 = TextNode("Node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.net")
        html_node = text_node_to_html_node(node).to_html()
        self.assertEqual(html_node, '<a href="www.link.net">This is a link node</a>')

    def test_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.link.net")
        html_node = text_node_to_html_node(node).to_html()
        self.assertEqual(html_node, '<img src="www.link.net" alt="This is an image"/>')


if __name__ == "__main__":
    unittest.main()
