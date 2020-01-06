from Pyrser import pyrser


if __name__ == "__main__":
    # test_file = "/home/kemri/Projects/pyrser/test_files/test4.py"
    test_file = "/home/kemri/Projects/pyrser/Node.py"
    output = pyrser(test_file)
    print(repr(output))
