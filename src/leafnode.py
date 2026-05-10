from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
    ):
        super(LeafNode, self).__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode doesn't have a html value")

        if self.tag == None:
            return self.value

        props = self.props_to_html()
        open_tag = f"<{self.tag} {props}>" if props else f"<{self.tag}>"
        return f"{open_tag}{self.value}</{self.tag}>"

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
