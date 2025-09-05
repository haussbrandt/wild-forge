
import unittest

from block import BlockType, block_to_block_type
from convert import markdown_to_blocks


class TestBlockToBlocktype(unittest.TestCase):
        def test_block_to_blocktype(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. This is
2. an ordered
3. list

10. But this
100. is
3. not

>We can also
>quote some
>  smart stuff

# Headings

## More headings

###### Up to 6 hash symbols

```
closing it off
with some code block
```
"""
            blocks = markdown_to_blocks(md)
            results = [block_to_block_type(block) for block in blocks]
            expected = [BlockType.PARAGRAPH,
                        BlockType.PARAGRAPH,
                        BlockType.UNORDERED_LIST,
                        BlockType.ORDERED_LIST,
                        BlockType.PARAGRAPH,
                        BlockType.QUOTE,
                        BlockType.HEADING,
                        BlockType.HEADING,
                        BlockType.HEADING,
                        BlockType.CODE]
            self.assertListEqual(results, expected)