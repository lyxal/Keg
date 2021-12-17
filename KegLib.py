'''KegLib - Powering the transpilation of Keg since 2019'''

import Coherse
from Coherse import char
from Stackd import Stack

_register = None
variables = {}
code_page = ""
function_list = []
seperator = ""
inputs = Stack()

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

def length(stack, pop_if_empty=False):
    if pop_if_empty:
        if len(stack) == 0:
            stack.push(stack.pop())
    stack.push(len(stack))

def reverse(stack):
    length(stack)
    stack.pop()
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

def nice(stack, keep=False):
    #This takes the top of the stack and prints it "nicely"
    #i.e. str() but even nicer. Also, implements some other rules a standard
    #call to a fn like str() might not handle

    item = stack.pop()
    if type(item) is int:
        print(_chr(item),
              end=seperator) #Preserve Keg's ability to print integers as chars

    elif type(item) is float:
        print(item,
              end=seperator) #I mean, floats can't really be conv'd to chars, can they?

    elif type(item) is char:
        print(item.v, end=seperator) #Because python doesn't have a char type.

    elif type(item) is Stack:
        print(*[x for x in item], end=seperator)

    else:
        print(custom_format(item), end=seperator)

    if keep:
        stack.push(item)


def raw(stack, keep=False):
    #Like nice(), but Keg's version of repr()

    item = stack.pop()
    if type(item) is int:
        print(item,
              end=seperator) #Integers are printed as integers

    elif type(item) is float:
        print(item,
              end=seperator) #Floats -> Floats

    elif type(item) is char:
        print(_ord(item.v), end=seperator) #Char -> Integer

    elif type(item) is Stack:
        print(repr(stack), end=seperator) #I actually made a repr() fn for Stacks

    else:
        print("`" + custom_format(item) + "`", end=seperator) #Makes quines possible

    if keep:
        stack.push(item)

def Input(stack):
    #This is the first of many input functions.
    #"Why are there more than one input function though?"
    #Well, because ?¿᠀ and implict input. That's why.

    #This one is "take input and push as ord"
    item = input()
    if item:
        for Char in reversed(item):
            stack.push(char(Char))
        inputs.push(item)
    else:
        item = inputs.pop()
        inputs.push(item)
        if type(item) is str:
            for Char in reversed(item):
                stack.push(char(Char))
        else:
            stack.push(item)
    shift(inputs, "R")

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
    if type(expr) in [float, int]:
        return range(int(expr))
    if type(expr) is char:
        return range(ord(expr.v))
    return expr

def condition_eval(expr_list, stack):
    for expr in expr_list:
        eval(expr)

    return stack.pop()



# REG EXTENSION

def iota(stack):
    try_cast(stack, 'ℤ')
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

def increment(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, 1, "+"))

def nice_input(stack):
    #As aforementioned, round 2 of input has arrived.
    #This one is "take input and best guess what it is the user wants"

    temp = input()

    try:
        if type(eval(temp)) is float:
            temp = float(temp)
        elif type(eval(temp)) is int:
            temp = int(temp)
        elif type(eval(temp)) is list:
            temp = Stack(eval(temp))
        elif type(eval(temp)) is str:
            temp = temp
        else:
            for char in reversed(temp):
                stack.push(char)
            return
    except:
        temp = temp

    if temp:
        stack.push(temp)
        inputs.push(temp)
    else:
        item = inputs.pop()
        inputs.push(item)
        stack.push(item)
    shift(inputs, "R")

    #Float > Integer > List > String

def excl_range(stack):
    query = stack.pop()
    x, y = stack.pop(), stack.pop()
    values = [to_integer(x), to_integer(y)]
    start, stop = sorted(values)
    range_object = range(start, stop)
    if to_integer(query) in range_object:
        stack.push(1)
    else:
        stack.push(0)

def incl_range(stack):
    query = stack.pop()
    x, y = stack.pop(), stack.pop()
    values = [to_integer(x), to_integer(y)]
    start, stop = sorted(values)
    range_object = range(start, stop + 1)
    if to_integer(query) in range_object:
        stack.push(1)
    else:
        stack.push(0)

def smart_range(stack):
    x, y = stack.pop(), stack.pop()
    values = [to_integer(x), to_integer(y)]
    start, stop = sorted(values)
    range_object = range(start, stop + 1)
    for item in range_object:
        stack.push(item)

def to_integer(item):
    return _ord(item.v) if type(item) is char else int(item)

def item_split(stack):
    item = stack.pop()
    _type = type(item)
    if _type is int:
        for number in str(item):
            stack.push(int(number) if number in "0123456789" else number)

    elif _type is float:
        for number in str(item):
            stack.push(int(number) if number in "0123456789" else number)
    elif _type is char:
        for number in str(_ord(item.v)):
            stack.push(int(number))
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

def not_top(stack):
    item = stack.pop()
    stack.push(0 if item else 1)

def pi(stack):
    import math
    stack.push(math.pi)

def halve_top(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, 2, "/"))

def double(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, 2, "*"))

def negate(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, -1, "*"))

#Keg+ Functions

def convert(stack, _type):
    item = stack.pop()
    try:
        item = _type(item)
    except:
        pass
    stack.push(item)

def case_switch(stack, how):
    string = stack.pop()
    if type(string) is not str:
        stack.push(string)
        return
    if how == "upper": stack.push(string.upper())
    elif how == "lower": stack.push(string.lower())
    else: stack.push(string.swapcase())

def square(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, item, "*"))

def string_input(stack):
    #The third and final method of input: string input
    item = input()
    if item:
        stack.push(item)
        inputs.push(item)
    else:
        item = inputs.pop()
        inputs.push(item)
        stack.push(item)
    shift(inputs, "R")

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
    x = len(stack) - 1
    for n in range(x):
        maths(stack, "+")


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
                result += to_string(variables.get(temp, '©' + temp))
                temp = ""
                var_mode = False
                if char == " ":
                    continue

        if char == "©":
            var_mode = True
            continue

        result += char

    if var_mode:
        result += to_string(variables.get(temp, '©' + temp))
    return result

def to_string(item):
    if type(item) in [float, int]:
        return str(item)

    if type(item) == char:
        return str(_ord(item.v))

    if type(item) == str:
        return item
    return str(item)

def _ord(character):
    if str(character) in code_page:
        return code_page.index(str(character))
    return ord(character)

def _chr(i):
    if code_page:
        if i == 10:
            return "\n"
        if 0 < i < 256:
            return code_page[i]
        return chr(i)
    else:
        return chr(i)

def try_cast(stack, what_type):
    INTEGER, FLOAT, STRING, STACK, CHARACTER = "ℤℝ⅍℠ⁿ"
    if what_type == INTEGER:
        item = stack.pop()
        try:
            item = int(item)
        except:
            pass
        stack.push(item)

    elif what_type == FLOAT:
        item = stack.pop()
        try:
            item = float(item)
        except:
            pass
        stack.push(item)

    elif what_type == STRING:
        stack.push(str(stack.pop()))

    elif what_type == CHARACTER:
        item = stack.pop()
        if Coherse._type(item) == "Number":
            stack.push(_chr(int(item)))
        elif Coherse._type(item) == "Character":
            stack.push(item)
        elif Coherse._type(item) == "String":
            stack.push(char(item[0]))
        elif Coherse._type(item) == "Stack":
            stack.push(try_cast(item, CHARACTER))

def keg_exec(big_stack):
    import Keg
    code = big_stack.pop()
    code = Keg.balance(code)
    code = Keg.transpile(code)


    header = f"""
from KegLib import *
from Stackd import Stack
stack = Stack()
"""

    footer = """
for item in stack:
    big_stack.push(item)
    """

    exec(header + code + footer)

def item_in(stack):
    query = stack.pop()

    if query in stack:
        stack.push(1)
    else:
        stack.push(0)

def perform_index(stack):
    position = stack.pop()
    stack.push(stack.index([position]))

def multiline(stack):
    temp = 1
    while temp:
        temp = input()
        for Char in temp:
            stack.push(char(Char))
        stack.push("\n")
    stack.pop()

def exponate(stack):
    power = stack.pop()
    base = stack.pop()
    result = base

    if type(power) in [float, int] and type(base) in [float, int]:
        stack.push(pow(base, power))
    else:
        for n in loop_eval(Coherse.operate(power, 1, "-")):
            base = Coherse.operate(base, result, "*")

        stack.push(base)

def to_percentage(stack):
    item = stack.pop()
    stack.push(Coherse.operate(item, 100, "/"))

def reciprocal(stack):
    item = stack.pop()
    stack.push(Coherse.operate(1, item, "/"))

def keg_round(stack):
    item = stack.pop()
    if type(item) in [int, float]:
        stack.push(round(item))
    else:
        stack.push(item)

def length_top(stack):
    item = stack.pop()
    if type(item) in [int, float]:
        stack.push(len(str(item)))
    else:
        stack.push(len(item))

def reverse_top(stack):
    item = stack.pop()
    if type(item) is int:
        if item < 0:
            item = int(str(item)[::-1][:-1]) * -1
        else:
            item = int(str(item)[::-1])

    elif type(item) is float:
        if item < 0:
            item = float(str(item)[::-1][:-1]) * -1
        else:
            item = float(str(item)[::-1])
    else:
        item = item[::-1]

    stack.push(item)

def pop_item(stack):
    item = stack.pop()
    for i in range(len(stack)):
        temp = stack.pop()
        if not Coherse.do_compare(item, temp, '='):
            stack.push(temp)

def sort_stack(stack):
    stack._Stack__stack.sort()

def increment_register(stack):
    register(stack)
    integer(stack,1)
    maths(stack, "+")
    register(stack)

def decrement_register(stack):
    register(stack)
    integer(stack,1)
    maths(stack, "-")
    register(stack)

def register_dont_empty(stack):
    register(stack)
    duplicate(stack)
    register(stack)

def register_aug_assign(stack, operator):
    register(stack)
    maths(stack, operator)
    register(stack)

def set_register_dont_empty(stack):
    _register = stack.pop()

def register_length(stack):
    register_dont_empty(stack)
    length_top(stack)

def reverse_register(stack):
    register_dont_empty(stack)
    reverse_top(stack)

def keg_map(stack, functions):
    import Keg
    for i in range(len(stack)):
        small = Stack([stack[i]])
        code = Keg.balance(functions)
        code = Keg.transpile(code)

        header = f"""
from KegLib import *
from Stackd import Stack
stack = small
"""

        exec(header + code)
        stack[i] = smart_summate(small)


def smart_summate(stack):
    if all(map(lambda x : type(x) in [float, int], stack)):
        return stack.pop()

    if all(map(lambda x : type(x) == char, stack)):
        return "".join([c.v for c in stack])
    return str(stack)

def truthify(stack):
    temp = stack.pop()
    if bool(temp):
        stack.push(1)
    else:
        stack.push(0)

def keg_filter(stack):
    import Keg

    code = stack.pop()
    code = Keg.balance(code)
    code = Keg.transpile(code)

    final = Stack()

    header = f"""
from KegLib import *
from Stackd import Stack
stack = item
"""

    for i in range(len(stack)):
        item = Stack([stack[i]])
        temp = stack[i]
        exec(header + code)
        if bool(item.pop()):
            final.push(temp)

    stack._Stack__stack = final._Stack__stack

# https://stackoverflow.com/a/2267446/9363594


def int2base(stack):

    import string
    digs = string.digits + string.ascii_letters

    base = stack.pop()
    x = stack.pop()

    if x < 0:
        sign = -1
    elif x == 0:
        stack.push(digs[0])
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x // base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    stack.push(''.join(digits))
