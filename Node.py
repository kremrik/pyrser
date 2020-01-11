from Utils.NodeHelpers import dfs_printer


class Node(object):

    def __init__(self, location: str, name: str):
        self.location = location
        self.name = name
        self.parent = None
        self.children = {}

    def add_child(self, child: "Node") -> None:
        self.children[child.name] = child

    def __eq__(self, other):
        # TODO: can't compare parent due to recursive loop
        return self.location == other.location and \
            self.name == other.name and \
            self.children == other.children

    def __str__(self):
        cls_nm = type(self).__name__
        name = self.name
        loc = self.location

        return f"{cls_nm}(name='{name}', location='{loc}')"

    def __repr__(self):
        """
        TODO: output can look weird when doing normal things, may want to add dict-like method:
        >>> list(output.children.values())
        [FncNode(name='test', location='/home/kemri/Projects/pyrser/test_files/test3.py'),
         FncNode(name='test2', location='/home/kemri/Projects/pyrser/test_files/test3.py')
          |-- FncNode(name='test2_1', location='/home/kemri/Projects/pyrser/test_files/test3.py')]
        """
        return dfs_printer(self)


class DirNode(Node):

    def __init__(self, location: str, name: str):
        super().__init__(location, name)


class FileNode(Node):

    def __init__(self, location, name):
        super().__init__(location, name)
        self.scope = None
    
    def __eq__(self, other):
        return self.location == other.location and \
            self.name == other.name and \
            self.children == other.children and \
            self.scope == other.scope

    def __str__(self):
        cls_nm = type(self).__name__
        name = self.name
        scope = self.scope
        loc = self.location

        return f"{cls_nm}(name='{name}', scope={scope}, location={loc})"


class ClsNode(FileNode):

    def __init__(self, location, name):
        super().__init__(location, name)

    def __str__(self):
        cls_nm = type(self).__name__
        name = self.name
        scope = self.scope

        return f"{cls_nm}(name='{name}', scope={scope})"


class FncNode(FileNode):

    def __init__(self, location, name):
        super().__init__(location, name)
        self.calls = []

    def __str__(self):
        cls_nm = type(self).__name__
        name = self.name
        scope = self.scope

        return f"{cls_nm}(name='{name}', scope={scope})"
