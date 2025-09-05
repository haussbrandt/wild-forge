from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag but has None")
        if self.children is None:
            raise ValueError("ParentNode has to have children but has None")
        children_value = ""
        for child in self.children:
            children_value += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_value}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for key, value in self.props.items(): # pyright: ignore[reportOptionalMemberAccess]
            s += f' {key}="{value}"'
        return s 
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag=}, {self.children=}, {self.props=})"