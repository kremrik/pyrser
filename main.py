from Pyrser import pyrser
from utils.algos import xfs


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/test_files/test3.py"
    output = pyrser(test_file)
    xfs(output)
