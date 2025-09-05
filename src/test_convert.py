import unittest

from convert import extract_markdown_images, markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected) 
    
    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected)
    
    def test_incorrect_markdown(self):
        node = TextNode("This is text with a _broken italic block word", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertTrue("Incorrect markdown" in str(context.exception), "Incorrect markdown exception was not correctly raised")
    
    def test_multiple_code(self):
        node = TextNode("This is text with `multiple` separate `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("multiple", TextType.CODE),
            TextNode(" separate ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" words", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected) 
    
    def test_multiple_various(self):
        node = TextNode("This is text with **bold** and `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with **bold** and ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" words", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches = [match.groups() for match in matches]
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitLinks(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(expected, result)

class TestMarkdownToBlocks(unittest.TestCase):
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

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a level 1 heading
## Level 2
### Level 3
#### Getting smaller
##### Five?
###### SIX!
"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><h1>This is a level 1 heading</h1><h2>Level 2</h2><h3>Level 3</h3><h4>Getting smaller</h4><h5>Five?</h5><h6>SIX!</h6></div>",
        )

    def test_quote(self):
        md = """
>This is a quote
>It should **preserve** the _types_.
"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote It should <b>preserve</b> the <i>types</i>.</blockquote></div>",
        )

    def test_unorderedlist(self):
        md = """
- unordered list
- looks **like** this
"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><ul><li>unordered list</li><li>looks <b>like</b> this</li></ul></div>",
        )


    def test_orderedlist(self):
        md = """
1. ordered list
2. looks _like_ this
"""

        node = markdown_to_html_node(md)
        html = node.to_html() # pyright: ignore[reportAttributeAccessIssue]
        self.assertEqual(
            html,
            "<div><ol><li>ordered list</li><li>looks <i>like</i> this</li></ol></div>",
        )