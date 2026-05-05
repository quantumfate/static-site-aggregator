from typing import Callable
from htmlnode import HTMLNode
from textnode import TextNode, TextType, TextTypeToMd
import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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


def split_abritary_link(
    old_nodes: list[TextNode],
    text_type: TextType,
    matcher: Callable[[str], list[tuple[str, str]]],
) -> list[TextNode]:

    split_nodes = []
    for old_node in old_nodes:
        matches = matcher(old_node.text)
        if len(matches) == 0:
            split_nodes.append(old_node)
        else:
            current_text = old_node.text

            for match in matches:
                image_alt, image_link = match
                split_text = (
                    f"[{image_alt}]({image_link})"
                    if text_type == TextType.LINK
                    else f"![{image_alt}]({image_link})"
                )
                sections = current_text.split(split_text, 1)

                if sections[0] != "":
                    split_nodes.append(TextNode(sections[0], old_node.text_type))

                split_nodes.append(TextNode(image_alt, text_type, image_link))

                current_text = sections[1]

            if current_text != "":
                split_nodes.append(TextNode(current_text, old_node.text_type))

    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_abritary_link(old_nodes, TextType.IMAGE, extract_markdown_images)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_abritary_link(old_nodes, TextType.LINK, extract_markdown_links)


def text_to_textnodes(text: str) -> list[TextNode]:
    splitted = [TextNode(text, TextType.TEXT)]
    for member in TextTypeToMd:
        delimiter = member.value
        text_type_idx = member.name
        splitted = split_nodes_delimiter(splitted, delimiter, TextType[text_type_idx])

    splitted = split_nodes_image(splitted)
    splitted = split_nodes_link(splitted)

    return splitted
