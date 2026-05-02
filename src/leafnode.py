from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
    ):
        super(LeafNode, self).__init__(tag, value, None, props)

    def to_html(self, depth: int = 0):
        if self.value == None:
            raise ValueError("LeafNode doesn't have a html value")

        spaces = "  " * depth

        if self.tag == None:
            return f"{spaces}{self.value}"

        return f"{spaces}<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
