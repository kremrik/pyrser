from Pyrser import pyrser, add_calls
from Utils.PyrserHelpers import reader, xfs, dfs_generator
from Node import FileNode, FncNode


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/Utils/PyrserHelpers.py"
    output = pyrser(test_file)
    
    for node in dfs_generator(output):
        print(node)
