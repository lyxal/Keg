#Stackd library for Keg

def _ord(char):
    if char in code_page:
        return code_page.find(char)
    else:
        return ord(char)

code_page = "Set me in Keg.py"

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
            temp = input()
            try:
                if type(eval(temp)) is float:
                    temp = float(temp)
                elif type(eval(temp)) is int:
                    temp = int(temp)
                elif type(eval(temp)) is list:
                    temp = Stack(eval(temp))
                elif type(eval(temp)) is str:
                    temp = temp[-1]
            except:
                temp = temp[-1]
            return temp

    def __repr__(self):
        return str(self.__stack)

    def clear(self):
        self.__stack.clear()

if __name__ == "__main__":
    x = Stack()
    y = x.pop() + x.pop()
