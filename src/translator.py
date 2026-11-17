from sys import exception

from htmlnode import HTMLNode
import leafnode
import parentnode
from slicer import markdown_to_blocks, block_to_block_type, BlockType
from splitter import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
import textnode
import textwrap
import re


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    leaf_nodes: list[LeafNode] = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes


def block_type_to_tag(type: BlockType, block_string: str | None = None) -> str:
    if type == BlockType.HEADING:
        if not block_string:
            raise Exception("Missing block text to calculate heading level")
        level = 0
        for char in block_string:
            if char != "#":
                break
            level += 1
        return f"h{level}"

    if type == BlockType.CODE:
        return "pre"

    if type == BlockType.QUOTE:
        return "blockquote"

    if type == BlockType.ORDERED:
        return "ol"

    if type == BlockType.UNORDERED:
        return "ul"

    return "p"


def normalize_block_string(block: str, type: BlockType) -> str:
    if type == BlockType.HEADING:
        normalized_string = ""
        for char in block:
            if char == "#":
                continue
            normalized_string += char
        return normalized_string[1:]

    if type == BlockType.CODE:
        text = block
        skip_symbols_start = ["\n", "`", " "]
        skip_symbols_end = ["`", " "]
        while text[0] in skip_symbols_start:
            text = text[1:]
        while text[-1] in skip_symbols_end:
            text = text[:-1]
        return f"<code>{text}</code>"

    if (
        type == BlockType.ORDERED
        or type == BlockType.UNORDERED
        or type == BlockType.QUOTE
    ):
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if type != BlockType.QUOTE:
                if type == BlockType.ORDERED:
                    while line[0] != ".":
                        line = line[1:]
                new_lines.append(f"<li>{line[2:]}</li>")
            else:
                line = line[1:]
                new_lines.append(line.strip())
        if type == BlockType.QUOTE:
            return " ".join(new_lines)
        return "".join(new_lines)

    return block


def markdown_to_html_node(markdown: str) -> ParentNode:
    md = textwrap.dedent(markdown)
    blocks: list[str] = markdown_to_blocks(md)
    nodes: list[ParentNode] = []

    for block in blocks:
        type = block_to_block_type(block)
        # raise Exception(f"👋 type = {type} block = {block}")
        multiline = (
            type == BlockType.ORDERED
            or type == BlockType.UNORDERED
            or type == BlockType.QUOTE
        )

        if type == BlockType.CODE:
            block_text = normalize_block_string(block, type)
            tag = block_type_to_tag(type, block)
            nodes.append(ParentNode(tag, [LeafNode(None, block_text)]))
        elif multiline:
            block_text = normalize_block_string(block, type)
            tag = block_type_to_tag(type, block_text)
            children: list[LeafNode] = text_to_children(block_text)
            nodes.append(ParentNode(tag, children))
        else:
            joined_block = " ".join(block.split("\n"))
            block_text = normalize_block_string(joined_block, type)
            tag = block_type_to_tag(type, block)
            children: list[LeafNode] = text_to_children(block_text)
            nodes.append(ParentNode(tag, children))

    return ParentNode("div", nodes)
