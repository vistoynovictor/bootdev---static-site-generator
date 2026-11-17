from splitter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType
import unittest


class Test_Splitter(unittest.TestCase):
    def test_text_to_bold_middle(self):
        original_splitted_text = [TextNode("Hello **world**!", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(original_splitted_text, "**", TextType.BOLD),
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_text_to_italic_start(self):
        original_splitted_text = [TextNode("_Hello_ world?", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(original_splitted_text, "_", TextType.ITALIC),
            [
                TextNode("Hello", TextType.ITALIC),
                TextNode(" world?", TextType.TEXT),
            ],
        )

    def test_double_split(self):
        original_splitted_text = [TextNode("_Hello_ **world**!?", TextType.TEXT)]
        combos = [("_", TextType.ITALIC), ("**", TextType.BOLD)]
        for combo in combos:
            original_splitted_text = split_nodes_delimiter(
                original_splitted_text, combo[0], combo[1]
            )
        self.assertEqual(
            original_splitted_text,
            [
                TextNode("Hello", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!?", TextType.TEXT),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "[first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) What do you think about it?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" What do you think about it?", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        desired_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        output: list[TextNode] = text_to_textnodes(markdown)
        self.assertEqual(desired_output, output)


if __name__ == "__main__":
    unittest.main()
