class HTMLNode:
    tag: str | None
    value: str | None
    children = None
    props: dict[str, str] | None
    self_closing_tags: list[str] = ["img", "video", "audio"]

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children=None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        attrs_line: str = ""
        for attr, val in self.props.items():
            attrs_line += f' {attr}="{val}"'
        return attrs_line

    def __repr__(self) -> str:
        if self.tag == None and self.value:
            return self.value
        return f'HTMLNode [{self.tag}]:\n\tvalue = "{self.value}"\n\tprops = "{self.props}"\n\tchildren = {self.children}\n'

    def __eq__(self, node) -> bool:
        if not self.tag:
            if type(node) != str:
                return False
            return self.value == node

        if not node.isinstance(node, HTMLNode):
            return False

        same_tag = self.tag == node.tag
        same_value = self.value == node.value
        same_children = self.children == node.children
        same_props = self.props == node.props
        return same_tag and same_value and same_children and same_props
