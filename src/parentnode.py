from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode] | None = None, props=None):
        super(ParentNode, self).__init__(tag, None, children, props)

    def to_html(self, depth: int = 0):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")

        if self.children == None:
            raise ValueError("ParentNode without children is not allowed")

        spaces = "  " * depth

        html = f"{spaces}<{self.tag}>\n"

        if self.children != None:
            for html_nodes in self.children:
                html += html_nodes.to_html(depth + 1) + "\n"

        return f"{html}{spaces}</{self.tag}>"

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
