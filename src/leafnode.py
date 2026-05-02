from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError

        if self.tag == None:
            return self.value

        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
