from enum import Enum
from re import sub
import re


class BlockTypeToHTML(Enum):
    PARAGRAPH = "p"
    HEADING = "h{n}"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"

    @classmethod
    def _get_tag(cls, block_type: BlockType, heading_level: int | None = None) -> str:
        return (
            cls[block_type.name].value
            if heading_level is None
            else cls[block_type.name].value.format(n=heading_level)
        )


def get_block_tag(block_type: BlockType, heading_level: int | None = None) -> str:
    return BlockTypeToHTML._get_tag(block_type, heading_level)


class BlockType(Enum):
    PARAGRAPH = BlockTypeToHTML.PARAGRAPH
    HEADING = BlockTypeToHTML.HEADING
    CODE = BlockTypeToHTML.CODE
    QUOTE = BlockTypeToHTML.QUOTE
    UNORDERED_LIST = BlockTypeToHTML.UNORDERED_LIST
    ORDERED_LIST = BlockTypeToHTML.ORDERED_LIST
    LIST_ITEM = BlockTypeToHTML.LIST_ITEM


class BlockTypeToRegEx(Enum):
    HEADING = r"^#{1,6} "
    CODE = r"```(?:\w+)?\n?(.*?)\n?```"
    QUOTE = r"^> "
    UNORDERED_LIST = r"^- "
    ORDERED_LIST = r"^\d.\ "


def get_heading_level(block: str) -> int:
    return block.count("#", 0, 6)


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(
        line.startswith(f"{idx + 1}. ") for idx, line in enumerate(block.split("\n"))
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def sanitize_md_text(line: str) -> str:
    if re.match(BlockTypeToRegEx.HEADING.value, line):
        return re.sub(BlockTypeToRegEx.HEADING.value, "", line)
    elif re.match(BlockTypeToRegEx.QUOTE.value, line):
        return re.sub(BlockTypeToRegEx.QUOTE.value, "", line, flags=re.MULTILINE)
    elif re.match(BlockTypeToRegEx.CODE.value, line, re.DOTALL):
        return re.sub(BlockTypeToRegEx.CODE.value, r"\1", line, flags=re.DOTALL)
    elif re.match(BlockTypeToRegEx.UNORDERED_LIST.value, line):
        return re.sub(BlockTypeToRegEx.UNORDERED_LIST.value, "", line)
    elif re.match(BlockTypeToRegEx.ORDERED_LIST.value, line):
        return re.sub(BlockTypeToRegEx.ORDERED_LIST.value, "", line)
    else:
        # Paragraph
        return line


def determine_heading_level(line: str) -> int | None:
    m = re.match(BlockTypeToRegEx.HEADING.value, line)
    return m.group().count("#") if m else None
