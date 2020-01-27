class Person:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def is_yoda(self):
        if self.age < 500:
            print("Probably not Yoda")
        else:
            print("Quite possibly Yoda")


def test_it_out():
    p = Person("Kyle", 27)
    p.is_yoda()
