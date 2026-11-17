from slicer import markdown_to_blocks, BlockType, block_to_block_type
import unittest


class Test_Slicer(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("## Hello Title"))

    def test_block_to_block_type_code(self):
        self.assertEqual(
            BlockType.CODE, block_to_block_type("``` Hello Code{\n\treturn True\n}```")
        )

    def test_block_to_block_type_quote(self):
        self.assertEqual(
            BlockType.QUOTE, block_to_block_type(">Hello Title\n> I say to them")
        )

    def test_block_to_block_type_ordered(self):
        self.assertEqual(
            BlockType.ORDERED,
            block_to_block_type("1. Hello Title\n2. Hello life\n13. Hello"),
        )

    def test_block_to_block_type_unordered(self):
        self.assertEqual(
            BlockType.UNORDERED,
            block_to_block_type("- Hello Title\n- Hello you\n- Hello us"),
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("Hello paragraph/nAlso this is multiline"),
        )


if __name__ == "__main__":
    unittest.main()
