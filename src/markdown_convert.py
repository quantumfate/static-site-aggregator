from pydoc import text
from typing import Callable, Iterator
from collections.abc import Iterator
from blocktype import (
    BlockType,
    BlockTypeToHTML,
    block_to_block_type,
    get_block_tag,
    get_heading_level,
)
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, TextTypeToMd, text_node_to_html_node
import re


def match_images(text: str) -> Iterator[re.Match[str]]:
    return re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)").finditer(text)


def match_links(text: str) -> Iterator[re.Match[str]]:
    return re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)").finditer(text)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            split_node = old_node.text.split(delimiter)

            if len(split_node) % 2 == 0:
                raise ValueError(
                    f"{old_node.text} is not a valid markdown syntax, '{delimiter}' is not balanced."
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


def split_arbitrary_link(
    old_nodes: list[TextNode],
    text_type: TextType,
    matcher: Callable[[str], Iterator[re.Match]],  # yields match objects
) -> list[TextNode]:
    split_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        cursor = 0
        for m in matcher(text):
            alt, link = m.group(1), m.group(2)
            start, end = m.span()
            if start > cursor:
                split_nodes.append(TextNode(text[cursor:start], old_node.text_type))
            split_nodes.append(TextNode(alt, text_type, link))
            cursor = end
        if cursor == 0:
            split_nodes.append(old_node)
        elif cursor < len(text):
            split_nodes.append(TextNode(text[cursor:], old_node.text_type))
    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_arbitrary_link(old_nodes, TextType.IMAGE, match_images)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_arbitrary_link(old_nodes, TextType.LINK, match_links)


def text_to_textnodes(text: str) -> list[TextNode]:
    splitted = [TextNode(text, TextType.TEXT)]
    for member in TextTypeToMd:
        delimiter = member.value
        text_type_idx = member.name
        splitted = split_nodes_delimiter(splitted, delimiter, TextType[text_type_idx])

    splitted = split_nodes_image(splitted)
    splitted = split_nodes_link(splitted)

    return splitted


def markdown_to_blocks(markdown: str) -> list[str]:

    # O(2n) for chaining filter and map -> collapses to O(n)
    # simple O(n) for list comprehension
    return list(
        map(
            lambda x: x.strip(), list(filter(lambda x: x != "", markdown.split("\n\n")))
        )
    )


def markdown_to_html_node(markdown: str) -> HTMLNode:

    markdown_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)

        parent = None
        match block_type:
            case BlockType.PARAGRAPH:
                # Paragrah
                # ParentNode, tag p
                # Child: LeafNode List for inline md
                parent = ParentNode(
                    get_block_tag(block_type),
                    [
                        text_node_to_html_node(text_node)
                        for text_node in text_to_textnodes(markdown_block)
                    ],
                )

            case BlockType.HEADING:
                # Heading
                # ParentNode, tag h
                # Child: LeafNode List for inline md
                parent = ParentNode(
                    get_block_tag(block_type, get_heading_level(markdown_block)),
                    [
                        text_node_to_html_node(text_node)
                        for text_node in text_to_textnodes(markdown_block)
                    ],
                )
            case BlockType.CODE:
                # Code
                # ParentNode with pre, to keep whitespace
                # Child: LeafNode, tag code, no inline markdown
                parent = ParentNode(
                    "pre",
                    [
                        ParentNode(
                            get_block_tag(block_type),
                            [
                                LeafNode(None, markdown_block)
                            ],  # TODO: not sure about this construct
                        )
                    ],
                )
            case BlockType.QUOTE:
                # Blockquote
                # ParentNode, tag blockquote
                # Child: LeafNode List for inline md
                parent = ParentNode(
                    get_block_tag(block_type),
                    [
                        text_node_to_html_node(text_node)
                        for text_node in text_to_textnodes(markdown_block)
                    ],
                )
            case BlockType.UNORDERED_LIST:
                # Unordered Lists
                # ParentNode, tag ul
                # Child: ParentNode, tag il per member
                # member child: LeafNode List for inline md
                parent = ParentNode(
                    get_block_tag(block_type),
                    [
                        # TODO: sanitize the strings for list items, parse into parentnode, process inline tags
                    ],
                    # ParentNode(
                    #     get_block_tag(BlockType.LIST_ITEM)
                    #     )
                    # )
                )

        # Ordered Lists
        # ParentNode, tag ol
        # Child: ParentNode, tag il per member
        # member child: LeafNode List for inline md

        # TODO: text_to_textnodes for the inline md

        # TODO: add in order to list html_blocks

    return ParentNode(
        "div", None, html_blocks
    )  # Must be parent node and not HTML node because to_html will crash otherwise
