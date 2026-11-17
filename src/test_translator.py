from translator import markdown_to_html_node
import unittest


class Test_Translator(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
    **This is an ordered list**

    1. Hello
    2. text in li
    3. tag here

    This is another _list_, but unordered

    - Uno
    - Two
    - Tre

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><b>This is an ordered list</b></p><ol><li>Hello</li><li>text in li</li><li>tag here</li></ol><p>This is another <i>list</i>, but unordered</p><ul><li>Uno</li><li>Two</li><li>Tre</li></ul></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
    Here comes the **multiline** quote

    > This is text that _should_ remain
    >quoted, my friend
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here comes the <b>multiline</b> quote</p><blockquote>This is text that <i>should</i> remain quoted, my friend</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
