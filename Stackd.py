#Stackd library for Keg

class Stack:
    def __init__(self, iterable=()):
        if iterable:
            self.__stack = list(iterable)
        else:
            self.__stack = []

    def __len__(self):
        return len(self.__stack)

    def __setitem__(self, index, value):
        self.__stack[index] = value

    def __getitem__(self, index):
        return self.__stack[index]

    def __delitem__(self, what):
        del self.__stack[what]

    def push(self, value):
        self.__stack.append(value)

    def pop(self):
        if len(self.__stack):
            return self.__stack.pop()
        else:
            temp = input("Implicit input: ")
            for char in reversed(temp):
                self.__stack.append(ord(char))
            return self.__stack.pop()

    def __repr__(self):
        return str(self.__stack)

if __name__ == "__main__":
    x = Stack()
    y = x.pop() + x.pop()
