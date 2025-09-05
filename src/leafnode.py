from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for key, value in self.props.items(): # pyright: ignore[reportOptionalMemberAccess]
            s += f' {key}="{value}"'
        return s 
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag=}, {self.value=}, {self.props=})"