from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    block_type = None
    if re.search(r"^#{1,6} +.", markdown):
        block_type = BlockType.HEADING
    elif re.search(r"^```[\s\S]+```$", markdown):
        block_type = BlockType.CODE
    elif all([t.startswith(">") for t in markdown.split("\n")]):
        block_type = BlockType.QUOTE
    elif all([t.startswith("- ") for t in markdown.split("\n")]):
        block_type = BlockType.UNORDERED_LIST
    else:
        block_type = BlockType.ORDERED_LIST
        for idx, line in enumerate(markdown.split("\n")):
            if not line.startswith(f"{idx+1}. "):
                block_type = BlockType.PARAGRAPH
                break
    return block_type