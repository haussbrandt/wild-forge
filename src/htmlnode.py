class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for key, value in self.props.items(): # pyright: ignore[reportOptionalMemberAccess]
            s += f' {key}="{value}"'
        return s 
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"
