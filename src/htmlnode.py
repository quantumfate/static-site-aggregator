class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        html = []
        for tag in self.props.keys():
            html.append(f'{tag}="{self.props[tag]}"')
        return " ".join(html)

    def __repr__(self):
        to_string = f"HTMLNode({self.tag}, {self.value}, {self.children}"
        props = self.props_to_html()
        return f"{to_string}, no_props)" if props == "" else f"{to_string}, {props})"
