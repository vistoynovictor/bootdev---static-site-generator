from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    tag: str | None
    value: str | None
    props: dict[str, str] | None

    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.tag in self.self_closing_tags:
            return f"<{self.tag}{self.props_to_html()}/>"
        if self.value == None:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        if not self.tag and self.value:
            return self.value
        return f'LeafNode [{self.tag}]:\n\tvalue = "{self.value}"\n\tprops = "{self.props}"'
