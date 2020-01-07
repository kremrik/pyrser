from Pyrser import pyrser
from Utils.PyrserHelpers import get_next_nonempty_line


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/Node.py"
    output = pyrser(test_file)
    print(repr(output))
