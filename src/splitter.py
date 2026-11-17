from textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        double_delimiter = len(delimiter) > 1
        delimiter_count = 0
        for i in range(len(text)):
            if (not double_delimiter and text[i] == delimiter) or (
                double_delimiter
                and text[i] == delimiter[0]
                and (i <= len(text) - 2 and text[i + 1] == delimiter[1])
            ):
                if delimiter_count == 0:
                    delimiter_count += 1
                else:
                    delimiter_count -= 1
        if delimiter_count > 0:
            raise Exception(f"Delimiter {delimiter} is not being closed")

        begins_with_delimiter = (len(text) > 0) and (
            (not double_delimiter and text[0] == delimiter)
            or (
                double_delimiter and text[0] == delimiter[0] and text[1] == delimiter[1]
            )
        )
        text_slices = text.split(delimiter)
        type: TextType
        start = 0
        if begins_with_delimiter:
            start = 1
        for i in range(start, len(text_slices)):
            if i % 2 != 0:
                type = text_type
            else:
                type = TextType.TEXT
            new_nodes.append(TextNode(text_slices[i], type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    r = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    accepted_types: list[TextType] = [TextType.TEXT, TextType.BOLD, TextType.ITALIC]
    for node in old_nodes:
        if node.text_type in accepted_types:
            current_text = node.text
            images: list[tuple[str, str]] = r.findall(current_text)
            if len(images) <= 0:
                new_nodes.append(node)
                continue
            for img in images:
                if current_text == "":
                    break
                buffer = r.split(current_text, maxsplit=1)
                if buffer[0] != "":
                    new_nodes.append(TextNode(buffer[0], node.text_type))
                new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                if len(buffer) == 4:
                    current_text = buffer[3]
                else:
                    current_text = ""
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    r = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    accepted_types: list[TextType] = [TextType.TEXT, TextType.BOLD, TextType.ITALIC]
    for node in old_nodes:
        if node.text_type in accepted_types:
            current_text = node.text
            links: list[tuple[str, str]] = r.findall(current_text)
            if len(links) <= 0:
                new_nodes.append(node)
                continue
            for link in links:
                if current_text == "":
                    break
                buffer = r.split(current_text, maxsplit=1)
                if buffer[0] != "":
                    new_nodes.append(TextNode(buffer[0], node.text_type))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                if len(buffer) == 4:
                    current_text = buffer[3]
                else:
                    current_text = ""
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    delimiters = {TextType.BOLD: "**", TextType.ITALIC: "_", TextType.CODE: "`"}

    for type, delimiter in delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
