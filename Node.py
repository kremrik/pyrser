class Node(object):

    def __init__(self, location: str, name: str):
        self.location = location
        self.name = name
        self.children = {}

    def add_child(self, child: "Node") -> None:
        self.children[child.name] = child

    def get_child(self, name: str) -> "Node":
        return self.children[name]

    def __str__(self):
        return self._pretty_print()

    def __repr__(self):
        return self._pretty_print()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _pretty_print(self):
        cls_nm = type(self).__name__
        name = self.name
        loc = self.location
        has_chld = bool(self.children)

        return f"{cls_nm}(name='{name}', location='{loc}', children='{has_chld}')"


class DirNode(Node):

    def __init__(self, location: str, name: str):
        super().__init__(location, name)


class PyNode(Node):

    def __init__(self, location, name):
        super().__init__(location, name)

        self.scope = None
        self.calls = None
