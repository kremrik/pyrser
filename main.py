from utils.algos import xfs
from Node import DirNode, FileNode, FncNode


if __name__ == "__main__":
    dirnode = DirNode("./test_files", "test_files")

    filenode = FileNode("./test_files/test1.py", "test1.py")
    filenode.scope = [1, 3]

    fncnode = FncNode("./test_files/test1.py", "test")
    fncnode.scope = [1, 2]

    dirnode.add_child(filenode)
    filenode.add_child(fncnode)

    res = xfs(dirnode, tgt_nm="test", tgt_typ=FncNode)
    print(res)
    print(res.scope)
