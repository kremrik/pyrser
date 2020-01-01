class Node(object):

    def __init__(self, location: str, name: str):
        self.location = location
        self.name = name
        self.parent = None
        self.children = {}

    def add_child(self, child: "Node") -> None:
        self.children[child.name] = child

    def __str__(self):
        return self._pretty_print()

    def __repr__(self):
        return self._pretty_print()

    def __eq__(self, other):
        # TODO: can't compare parent due to recursive loop
        return self.location == other.location and \
            self.name == other.name and \
            self.children == other.children

    def _pretty_print(self):
        cls_nm = type(self).__name__
        name = self.name
        loc = self.location
        par = self.parent
        has_chld = bool(self.children)

        return f"{cls_nm}(name='{name}', location='{loc}', parent={par}, children='{has_chld}')"


class DirNode(Node):

    def __init__(self, location: str, name: str):
        super().__init__(location, name)


class FileNode(Node):

    def __init__(self, location, name):
        super().__init__(location, name)
        self.scope = None
    
    def __eq__(self, other):
        # TODO: can't compare parent due to recursive loop
        return self.location == other.location and \
            self.name == other.name and \
            self.children == other.children and \
            self.scope == other.scope


class ClsNode(FileNode):

    def __init__(self, location, name):
        super().__init__(location, name)


class FncNode(FileNode):

    def __init__(self, location, name):
        super().__init__(location, name)
        self.calls = []
