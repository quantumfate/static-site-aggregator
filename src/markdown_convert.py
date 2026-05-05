from htmlnode import HTMLNode
from textnode import TextNode, TextType, TextTypeToMd
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            split_node = old_node.text.split(delimiter)

            if len(split_node) % 2 == 0:
                raise ValueError(
                    f"{old_node.text} is not a valid markdow syntax, '{delimiter}' is not balanced."
                )

            for idx, text in enumerate(split_node):
                if text == "":
                    continue
                if idx % 2 == 1:
                    new_nodes.append(TextNode(text, text_type))
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))

        else:
            new_nodes.append(old_node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
