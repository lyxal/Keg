'''KegLib - Powering the transpilation of Keg since 2019'''

import Coherse
from Coherse import char
from Stackd import Stack

_register = None
variables = {}


# BASIC STACK PUSHING

def character(stack, letter):
    stack.push(char(letter))

def integer(stack, number):
    stack.push(number)

def iterable(stack, item):
    stack.push(item)

# Coherse.py handles mathematics, so no need to define here
# But still:

def maths(stack, operator, debug=False):
    rhs, lhs = stack.pop(), stack.pop() #Sorry about the switched sides, But
                                        #that's the way it has to be in order
                                        #for maths to work as expected.
    if debug:
        print("DEBUG: in maths:", lhs, rhs, operator)
        print("DEBUG:", Coherse.operate(lhs, rhs, operator))
    stack.push(Coherse.operate(lhs, rhs, operator))

# LOGIC

def comparative(stack, operator):
    rhs, lhs = stack.pop(), stack.pop()
    result = Coherse.do_compare(lhs, rhs, operator)
    stack.push(result)


# BUILT-IN FUNCTIONS

def length(stack):
    stack.push(len(stack))

def reverse(stack):
    stack._Stack__stack.reverse() #Lazy moment, using Python built-ins

def swap(stack):
    stack[-1], stack[-2] = stack[-2], stack[-1] #Welcome to python, how may I
                                                #help you?

def duplicate(stack):
    temp = stack.pop() #Can't use stack.push(stack[-1]) because then implicit
                       #input doesn't get a chance to work

    stack.push(temp); stack.push(temp)

def shift(stack, direction):
    if direction == "left":
        stack.push(stack[0])
        del stack[0]
    else:
        stack._Stack__stack.insert(0, stack.pop()) #Wow, reeeal cryptic
        #Legit just put the last item at position 0

def nice(stack):
    #This takes the top of the stack and prints it "nicely"
    #i.e. str() but even nicer. Also, implements some other rules a standard
    #call to a fn like str() might not handle

    item = stack.pop()
    if type(item) == int:
        print(chr(item),
              end="") #Preserve Keg's ability to print integers as chars

    elif type(item) == float:
        print(item,
              end="") #I mean, floats can't really be conv'd to chars, can they?

    elif type(item) == char:
        print(item.v, end="") #Because python doesn't have a char type.

    elif type(item) == Stack:
        print(*[x for x in item], end="")

    else:
        print(custom_format(item), end="")


def raw(stack):
    #Like nice(), but Keg's version of repr()

    item = stack.pop()
    if type(item) == int:
        print(item,
              end="") #Integers are printed as integers

    elif type(item) == float:
        print(item,
              end="") #Floats -> Floats

    elif type(item) == char:
        print(ord(item.v), end="") #Char -> Integer

    elif type(item) == Stack:
        print(repr(stack), end="") #I actually made a repr() fn for Stacks

    else:
        print("`" + custom_format(item) + "`", end="") #Makes quines possible

def Input(stack):
    #This is the first of many input functions.
    #"Why are there more than one input function though?"
    #Well, because ?¿᠀ and implict input. That's why.

    #This one is "take input and push as ord"
    item = input()
    for char in reversed(item):
        stack.push(char)

    #See you soon with another input fn!

def random(stack):
    #Welcome to big_boy and small_boy
    import Keg_Nums, random
    stack.push(random.randint(Keg_Nums.small_boy, Keg_Nums.big_boy))

def pop_top(stack):
    stack.pop()

def register(stack):
    global _register
    if _register is not None:
        stack.push(_register)
        _register = None
    else:
        _register = stack.pop()
        #print("In KegLib, _register equals", _register)

# FOR-LOOP HELPER
def loop_eval(expr):
    if type(expr) is int:
        return range(expr)
    elif type(expr) is char:
        return range(ord(expr.v))
    else:
        return expr

def condition_eval(expr_list, stack):
    for expr in expr_list:
        eval(expr)

    return stack.pop()



# REG EXTENSION

def iota(stack):
    k = stack.pop()

    for i in range(k, -1, -1):
        stack.push(i)

def sine(stack):
    import math
    x = stack.pop()
    stack.push(math.sin(x)) #I FOUND x EVERYONE!!!!!

def decrement(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, 1, "-"))

def nice_input(stack):
    #As aforementioned, round 2 of input has arrived.
    #This one is "take input and best guess what it is the user wants"

    temp = input()

    try:
        stack.push(float(temp))
    except:
        try:
            stack.push(int(temp))
        except:
            try:
                stack.push(eval(temp))
            except:
                stack.push(temp)

    #Float > Integer > List > String

def excl_range(stack):
    query = stack.pop()
    values = [stack.pop(), stack.pop()]
    start, stop = sorted(values)
    range_object = range(start, stop)
    if query in range_object:
        stack.push(1)
    else:
        stack.push(0)

def incl_range(stack):
    query = stack.pop()
    values = [stack.pop(), stack.pop()]
    start, stop = sorted(values)
    range_object = range(start, stop + 1)
    if query in range_object:
        stack.push(1)
    else:
        stack.push(0)

def smart_range(stack):
    values = [stack.pop(), stack.pop()]
    start, stop = sorted(values)
    range_object = range(start, stop + 1)
    for item in range_object:
        stack.push(item)

def item_split(stack):
    item = stack.pop()
    _type = type(item)
    if _type is int:
        for number in str(item):
            stack.push(int(item))
    elif _type is char:
        for number in str(ord(item.v)):
            stack.push(int(item))
    else:
        for value in item:
            stack.push(value)

def factorial(stack):
    number = stack.pop()
    import math
    try:
        result = math.factorial(number)
    except Exception as e:
        result = "" #A whole lot of who knows what?
    stack.push(result)

def empty(stack):
    stack.clear()
    #Yes, it really is that simple.

def print_all(stack):
    for item in stack:
        nice(stack)

def convert(stack, _type):
    item = stack.pop()
    try:
        item = _type(item)
    except:
        pass
    stack.push(item)

def case_switch(stack, how):
    string = stack.pop()
    if type(string) is not string: stack.push(string)
    if how == "upper": stack.push(string.upper())
    elif how == "lower": stack.push(string.lower())
    else: stack.push(string.swapcase())

def square(stack):
    item = stack.pop()
    stack.push(operate(item, item, "*"))

def string_input(stack):
    #The third and final method of input: string input
    stack.push(input())

def all_true(stack):
    if all(stack):
        stack.push(1)
    else:
        stack.push(0)

def all_equal(stack):
    equal = 1
    last = None
    for item in stack:
        if last is None:
            last = item
            continue
        else:
            if item != last:
                equal = 0
                break
    stack.push(equal)

def summate(stack):
    for item in stack:
        stack.push(add(stack.pop(), stack.pop()))

def var_set(stack, name):
    variables[name] = stack.pop()

def var_get(stack, name):
    stack.push(variables[name])

def custom_format(source):
    #Using the © format
    #first space after a © doesn't count and is removed.

    result = ""
    temp = ""
    escaped = False
    var_mode = False

    import string

    for char in source:
        if escaped:
            escaped = False
            result += char
            continue

        elif char == "\\":
            escaped = True
            result += char
            continue

        if var_mode:
            if char in string.ascii_letters:
                temp += char
                continue

            else:
                result += variables.get(temp, '©' + temp)
                temp = ""
                var_mode = False
                if char == " ":
                    continue

        if char == "©":
            var_mode = True
            continue

        result += char

    if var_mode:
        result += variables.get(temp, '©' + temp)
    return result
