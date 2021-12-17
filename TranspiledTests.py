from KegLib import *
from Stackd import Stack
stack = Stack()
printed = False
Input(stack)
condition = condition_eval(["length(stack)", "integer(stack, 1)", "maths(stack, '-')"], stack)
print(condition)
while condition:
    nice(stack); printed = True
    condition = 1

integer(stack, 10)

if not printed:
    printing = ""
    for item in stack:
        if type(item) in [str, Stack]:
            printing += item
        elif type(item) is Coherse.char:
            printing += item.v

        elif item < 10 or item > 256:
            printing += str(item)
        else:
            printing += chr(item)
    print(printing)
