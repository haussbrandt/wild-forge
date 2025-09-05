import re
from block import BlockType, block_to_block_type
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text.split(delimiter)
            if len(text) % 2 != 1:
                raise ValueError(f"Incorrect markdown - a delimiter {delimiter} was not closed")
            for idx, part in enumerate(text):
                if idx % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.finditer(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return re.finditer(r"(?<!!)\[(.+?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = list(extract_markdown_images(node.text))
            if not matches:
                new_nodes.append(node)
                continue
            matches_len = len(matches)
            first_text = node.text[:matches[0].span()[0]]
            if first_text != "":
                new_nodes.append(TextNode(first_text, TextType.TEXT))
            for idx, match in enumerate(matches):
                alt_text, url = match.groups()
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                if idx < matches_len - 1:
                    new_nodes.append(TextNode(node.text[match.span()[1]: matches[idx+1].span()[0]], TextType.TEXT))
            if matches[-1].span()[1] < len(node.text):
                new_nodes.append(TextNode(node.text[matches[-1].span()[1]:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = list(extract_markdown_links(node.text))
            if not matches:
                new_nodes.append(node)
                continue
            matches_len = len(matches)
            first_text = node.text[:matches[0].span()[0]]
            if first_text != "":
                new_nodes.append(TextNode(first_text, TextType.TEXT))
            for idx, match in enumerate(matches):
                alt_text, url = match.groups()
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                if idx < matches_len - 1:
                    new_nodes.append(TextNode(node.text[match.span()[1]: matches[idx+1].span()[0]], TextType.TEXT))
            if matches[-1].span()[1] < len(node.text):
                new_nodes.append(TextNode(node.text[matches[-1].span()[1]:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for idx, block in enumerate(blocks):
        blocks[idx] = block.strip()
    new_blocks = []
    for block in blocks:
        if block:
            new_blocks.append(block)
    return new_blocks 

def text_to_chlidren(text):
    children = []
    children = text_to_textnodes(text)
    html_children = []
    for child in children:
        match child.text_type:
            case TextType.TEXT:
                html_children.append(LeafNode(tag=None, value=child.text.replace("\n", " ")))
            case TextType.BOLD:
                html_children.append(LeafNode(tag="b", value=child.text))
            case TextType.ITALIC:
                html_children.append(LeafNode(tag="i", value=child.text))
            case TextType.CODE:
                html_children.append(LeafNode(tag="code", value=child.text))
            case TextType.LINK:
                html_children.append(LeafNode(tag="a", value=child.text, props={"href": child.url}))
            case TextType.IMAGE:
                html_children.append(LeafNode(tag="img", value=child.text, props={"src": child.url}))
    return html_children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    top_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_chlidren(block)
                node = ParentNode(tag="p", children=children)
                top_children.append(node)
            case BlockType.HEADING:
                for line in block.split("\n"):
                    level, new_text = re.search(r"(^#{1,6}) (.+)", line).groups() # type: ignore
                    children = text_to_chlidren(new_text)
                    node = ParentNode(tag=f"h{len(level)}", children=children)
                    top_children.append(node)
            case BlockType.CODE:
                inner_node = LeafNode(tag="code", value=block.strip("`\n") + "\n")
                outer_node = ParentNode(tag="pre", children=[inner_node])
                top_children.append(outer_node)
            case BlockType.QUOTE:
                children = []
                for line in block.split("\n"):
                    children.extend(text_to_chlidren(line.lstrip("> ")))
                    children.append(LeafNode(tag=None, value=" "))
                children = children[:-1]
                node = ParentNode(tag="blockquote", children=children)
                top_children.append(node)
            case BlockType.UNORDERED_LIST:
                children = []
                for line in block.split("\n"):
                    inner_children = text_to_chlidren(line.lstrip("- "))
                    children.append(ParentNode(tag="li", children=inner_children))
                node = ParentNode(tag="ul", children=children)
                top_children.append(node)
            case BlockType.ORDERED_LIST:
                children = []
                for line in block.split("\n"):
                    inner_children = text_to_chlidren(line.lstrip("1234567890. "))
                    children.append(ParentNode(tag="li", children=inner_children))
                node = ParentNode(tag="ol", children=children)
                top_children.append(node)
    return ParentNode(tag="div", children=top_children)