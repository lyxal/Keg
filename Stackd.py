#Stackd library for Keg

def _ord(char):
    if char in code_page:
        return code_page.find(char)
    return ord(char)

code_page = "Set me in Keg.py"
input_raw = False #Set me in Keg.py using flags

class Stack:
    def __init__(self, iterable=()):
        if iterable:
            self.__stack = list(iterable)
            self.stacks = self.__stack.copy()
        else:
            self.__stack = []
            self.stacks = [self.__stack]

        self.level = 0
        self.inputs = []

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
        if self.__stack:
            return self.__stack.pop()
        try:
            temp = input()
        except:
            return None

        if input_raw:
            from Coherse import char
            for Char in reversed(temp):
                self.__stack.append(char(Char))
            return self.__stack.pop()

        try:
            if type(eval(temp)) is float:
                temp = float(temp)
            elif type(eval(temp)) is int:
                temp = int(temp)
            elif type(eval(temp)) is list:
                temp = Stack(eval(temp))
            elif type(eval(temp)) is str:
                for Char in reversed(temp):
                    self.__stack.append(Char)
                return self.__stack.pop()
        except:
            temp = temp

        self.inputs.append(temp)
        return temp

    def __repr__(self):
        return str(self.__stack)

    def clear(self):
        self.__stack.clear()

    def index(self, *pos_list):
        #Iteratively index the stack

        temp = self.__stack
        for indx in pos_list:
            temp = temp[indx]

        return temp

    def __str__(self):
        return "".join([str(item) for item in self.__stack])


if __name__ == "__main__":
    x = Stack([1, 2, 3, [4, 5, [6, 7, 8]]])
    print(x.index(3, 2, 2))
