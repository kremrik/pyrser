class test_poo:
    def print_name(self):
        print(type(self).__name__)


if __name__ == "__main__":
    t = test_poo()
    t.print_name()
