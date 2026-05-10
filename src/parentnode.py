from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode] | None = None, props=None):
        super(ParentNode, self).__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")

        if self.children == None:
            raise ValueError("ParentNode without children is not allowed")

        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{inner}</{self.tag}>"

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
