from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED = "unordered"
    ORDERED = "ordered"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    blocks_index = 0
    while True:
        if blocks_index >= len(blocks):
            break
        new_block: str = ""
        excluded_chars = ["\n", "\t", " "]
        in_text = False
        for char in blocks[blocks_index]:
            if in_text or char not in excluded_chars:
                in_text = True
                new_block += char
        blocks[blocks_index] = new_block
        blocks[blocks_index] = blocks[blocks_index].strip()
        if len(blocks[blocks_index]) == 0:
            blocks.pop(blocks_index)
            continue
        while blocks[blocks_index].endswith("\n"):
            blocks[blocks_index] = blocks[blocks_index][:-1]
        blocks_index += 1
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split("\n")

    heading = re.compile(r"^#{1,6} ")
    if heading.match(block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    ordered = re.compile(r"^\d+\. ")
    if all(ordered.match(line) for line in lines):
        return BlockType.ORDERED

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED

    return BlockType.PARAGRAPH
