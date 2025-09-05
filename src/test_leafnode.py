import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = LeafNode("p", "This is a test", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">This is a test</p>')

    def test_empty_props_to_html(self):
        node = LeafNode("p", "This is a test")
        self.assertEqual(node.to_html(), "<p>This is a test</p>")
    
    def test_none_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.to_html(), "test")

if __name__ == "__main__":
    unittest.main()