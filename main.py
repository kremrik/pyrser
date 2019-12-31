from Pyrser import pyrser


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/test_files/test2.py"
    output = pyrser(test_file)

    print(output, output.children.values(), sep="\n")
    print(output.scope, list(output.children.values())[0].scope, sep="\n")
