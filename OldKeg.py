import sys
import Parse
from Stackd import Stack
import Stackd
import Keg_Nums
import uncompress
import preprocess
#Just a nice little error. Very helpful I know

class Bruh(Exception):
    def __init__(self, msg):
        print("I can't believe you've done this...")
#All built-in functions
LENGTH = "!"
DUPLICATE = ":"
POP = "_"
PRINT_CHR = ","
PRINT_INT = "."
INPUT = "?"
L_SHIFT = '"'
R_SHIFT = "'"
RANDOM = "~"
REVERSE = "^"
SWAP = "$"

DESCRIPTIONS = {
    LENGTH: "Push the length of the stack",
    DUPLICATE: "Duplicate the top of stack",
    POP: "Pop the top of stack",
    PRINT_CHR: "Print the top of stack, calling _ord(top)",
    PRINT_INT: "Print the top of stack, as is",
    INPUT: "Get input from user",
    L_SHIFT: "Left shift stack",
    R_SHIFT: "Right shift stack",
    RANDOM: "Push a random number between -inf and inf",
    REVERSE: "Reverse the stack",
    SWAP: "Swap the top two items on stack"
}

#Unofficial built-in functions
#Note: Most of these are from Btup/A__/User:A, so go check out their
#repos/esolang account/code golf userpage and upvote their answers

IOTA = "Ï"
DECREMENT = ";"
SINE = "§"
APPLY_ALL = "∑"
NICE_INPUT = "¿"

DESCRIPTIONS[IOTA] = "Replaces the top of stack with all items from [top->0]"
DESCRIPTIONS[DECREMENT] = "Decrement the top of stack"
DESCRIPTIONS[SINE] = "sin(top)"
DESCRIPTIONS[APPLY_ALL] = "Preprocess as (!;| --> Apply to all stack"
DESCRIPTIONS[NICE_INPUT] = "Peform nice input"

#Some Reg commands not by Btup but by JonoCode9374
EXCLUSIVE_RANGE = "∂"
INCLUSIVE_RANGE = "•"
GENERATE_RANGE = "ɧ"
GENERATE_RANGE_0 = "ø"
NUMBER_SPLIT = "÷"
FACTORIAL = "¡"
EMPTY = "ø"
PRINT_ALL = "Ω"
'''Remind me to create descriptions later'''

# Keg+ Section

DIV_MOD = "①"


#'Keywords'

COMMENT = "#"
BRANCH = "|"
ESCAPE = "\\"
REGISTER = "&"
STRING = "`"
FUNCTION = "@"

DESCRIPTIONS[COMMENT] = "Standard line comment"
DESCRIPTIONS[BRANCH] = "Switch to the next part of the structure"
DESCRIPTIONS[ESCAPE] = "Push the code page value of the next character"
DESCRIPTIONS[STRING] = "Push an uncompressed string"
DESCRIPTIONS[FUNCTION] = "Start/Call the given function"

#Operators
MATHS = "+-*/%Ë"
CONDITIONAL = "<>=≬"
NUMBERS = "0123456789"

DESCRIPTIONS[MATHS] = "Pop x and y, and push y {0} x"
DESCRIPTIONS[CONDITIONAL] = "Pop x and y, and push y {0} x"
DESCRIPTIONS[NUMBERS] = "Push {0}"

#Whitespace
TAB = "\t"
ALT_TAB = "    "
NEWLINE = "\n"

#Structures
START = "start"
END = "end"
BODY = "body"

#Code page

unicode = "Ï§∑¿∂•ɧ÷¡Ëė≬ƒß‘“"
unicode += "„«®©ëλº√₳¬≤Š≠≥Ėπ"
unicode += " !\"#$%&'()*+,-./"
unicode += "0123456789:;<=>?"
unicode += "@ABCDEFGHIJKLMNO"
unicode += "PQRSTUVWXYZ[\\]^_"
unicode += "`abcdefghijklmno"
unicode += "pqrstuvwxyz{|}~ø"
unicode += "¶\n\t⊂½‡™±¦→←↶↷"
unicode += "✏█↗↘□²ⁿ║ṡ⟰⟱⟷"
unicode += "ℤℝ⅍℠א∀≌᠀⊙᠈⅀"
unicode += "ȦƁƇƉƐƑƓǶȊȷǨȽƜƝǪǷɊƦȘȚȔƲɅƛƳƵ" #push'n'print
unicode += "☭" #I don't know what this'll do. But it looks cool
unicode += "⬠⬡⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯"#drawing
unicode += "⯑" #Do something random
unicode += "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇"


for n in range(127234, 127243): unicode += chr(n)

#Variables
main_stack = Stack()
functions = {}
register = None #The register used
comment = False #Whether or not in a comment
escape = False #Escape next character?
printed = False #Used to determine whether or not to do implicit printing
pushed = False #Used to determine whether or not to implicit cat

def keg_input(stack):
    global pushed; pushed = True
    temp = input()
    for char in reversed(temp):
        stack.push(_ord(char))

def generate_range(*args):
    low, high = sorted(args[:2])
    if "e" in args:
        low += 1
    else:
        high += 1
    return range(low, high)

def _ord(char):
    if char in code_page:
        return code_page.find(char)
    return ord(char)

def _chr(integer):
    if integer > 0 and integer < len(code_page):
        return code_page[integer]
    return chr(integer)

def _eval(expr, stack=main_stack):
    #Evaluate the given expression as Keg code
    temp = Stack()
    for Token in Parse.parse(expr):
        #print(Token.name, Token.data, temp)
        if Token.name not in [Parse.CMDS.CMD, Parse.CMDS.NOP,
                              Parse.CMDS.ESC]:
            raise Bruh("""You can't just go placing forbidden characters in
                       expressions and expect to get away with it.""")

        else:
            if Token.name == Parse.CMDS.ESC:
                temp.push(_ord(Token.data))
            elif Token.data in NUMBERS:
                temp.push(int(Token.data))

            elif Token.data in MATHS:
                x, y = temp.pop(), temp.pop()
                op = Token.data
                if op == MATHS[-1]:
                    op = "**"

                temp.push(eval(f"y{op}x"))

            elif Token.data in CONDITIONAL:
                lhs, rhs = temp.pop(), temp.pop()
                op = Token.data
                if op == "=":
                    op = "=="
                elif op == "≬":
                    op = "> 0 and lhs <"

                result = eval(f"lhs{op}rhs")
                if result:
                    temp.push(1)
                else:
                    temp.push(0)

            elif Token.data == LENGTH:
                temp.push(len(stack))

            elif Token.data == DUPLICATE:
                item = temp.pop()
                temp.push(item)
                temp.push(item)

            elif Token.data == RANDOM:
                temp.push(random.randint(Keg_Nums.small_boy,
                                           Keg_Nums.big_boy))

            elif Token.data == POP:
                temp.push(stack.pop())

            elif Token.data == NEWLINE:
                temp.push(10)

            elif Token.data == TAB:
                continue

            elif Token.data in "#|@":
                raise Bruh("You can't just do that in the expression " + expr)

            #Start of Reg's extra commands
            elif Token.data == IOTA:
                k = temp[-1]
                temp.pop()

                for i in range(k, -1, -1):
                    temp.push(i)

            elif Token.data == EXCLUSIVE_RANGE:
                    
                    _range = generate_range(temp.pop(), temp.pop(), "e")
                    query = temp.pop()
                    if query in _range:
                        temp.push(1)
                    else:
                        temp.push(0)
                        
            elif Token.data == INCLUSIVE_RANGE:
                    _range = generate_range(temp.pop(), temp.pop())
                    query = temp.pop()
                    
                    if query in _range:
                        temp.push(1)
                    else:
                        temp.push(0)

            elif Token.data == GENERATE_RANGE:
                _range = generate_range(temp.pop(), temp.pop())
                for item in _range:
                    temp.push(item)
            elif Token.data == GENERATE_RANGE_0:
                _range = generate_range(0, temp.pop())
                for item in _range:
                    temp.push(item)
                    
            elif Token.data == DECREMENT:
                temp[-1] -= 1

            elif Token.data == SINE:
                temp.push(math.sin(temp.pop()))

            elif Token.data == NUMBER_SPLIT:
                item = str(temp.pop())
                for thing in item:
                    temp.push(int(thing))

            elif Token.data == FACTORIAL:
                temp.push(math.factorial(temp.pop()))

            elif Token.data == DIV_MOD:
                quot, remainder = divmod(temp.pop(), temp.pop())
                temp.push(quot)
                temp.push(remainder)

            else:
                temp.push(_ord(Token.data))
    return temp[0]

#Bracket balancer
def balance(source):
    brackets = []
    mapping = {"{" : "}", "[" : "]", "(" : ")", "": ""}
    alt_brackets = {"{" : "z1-", "}" : "z3+", "(" : "85*",
                    ")" : "85*1+", "[" : "Z1+",
                    "]" : "Z3+"}

    escaped = False


    result = ""
    for char in source:
        if escaped:
            if char in alt_brackets:
                result += alt_brackets[char]
            else:
                result += char
            escaped = False
            continue

        elif char == "\\":
            escaped = True
            result += char
            continue

        if char in "[({":
            brackets.append(char)

        elif char in "])}":
            for i in range(len(brackets)):
                if mapping[brackets[i]] == char:
                    brackets[i] = ""
                    break



        result += char


    if brackets:
        for char in reversed(brackets):
            result += mapping[char]

    return result

def run(source, master_stack, sub_stack=None):
    global register, comment, escape, printed, pushed
    code = source
    stack = Stack()
    do_repush = False #Indicate whether or not sub needs to push its contents
                      #back onto master_stack

    if sub_stack is None:
        stack = master_stack
    else:
        stack = sub_stack
        do_repush = True


    for Tkn in code:
        cmd = Tkn.data
        print(Tkn, stack, register)

        #Handle effect of comments and escape chars first
        if comment:
            if cmd == NEWLINE:
                comment = False
            continue

        if Tkn.name == Parse.CMDS.ESC:
            #print(cmd, _ord(cmd))
            escape = False
            stack.push(_ord(cmd))
            continue

        #Now, do all the functions
        if cmd == LENGTH:
            stack.push(len(stack))

        elif cmd == DUPLICATE:
            temp = stack.pop()
            stack.push(temp)
            stack.push(temp)

        elif cmd == POP:
            stack.pop()

        elif cmd == PRINT_CHR:
            #print(stack, stack.pop(), stack)
            print(_chr(stack.pop()), end="")
            printed = True

        elif cmd == PRINT_INT:
            print(stack.pop(), end="")
            printed = True

        elif cmd == L_SHIFT:
            stack.push(stack[0])
            del stack[0]

        elif cmd == R_SHIFT:
            stack._Stack__stack.insert(0, stack.pop())

        elif cmd == REVERSE:
            if not stack:
                keg_input(stack)
            stack._Stack__stack.reverse()

        elif cmd == SWAP:
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif cmd == INPUT:
            keg_input(stack)
            pushed = True

        #Reg starts now

        elif cmd == IOTA:
            k = stack[-1]
            stack.pop()

            for i in range(k, -1, -1):
                stack.push(i)

        elif cmd == DECREMENT:
            stack.push(stack.pop() - 1)

        elif cmd == SINE:
            stack.push(math.sin(stack.pop()))
            continue

        elif cmd == NICE_INPUT:
            temp = input()
            if "." in temp:
                stack.push(float(temp))
            elif temp.isnumeric() or (temp[0] == "-" and temp[1:].isnumeric()):
                stack.push(int(temp))
            else:
                for char in reversed(temp):
                    stack.push(_ord(char))

            pushed = True

        elif cmd == EXCLUSIVE_RANGE:
            _range = generate_range(stack.pop(), stack.pop(), "e")
            query = stack.pop()
            if query in _range:
                stack.push(1)
            else:
                stack.push(0)
                        
        elif cmd == INCLUSIVE_RANGE:
            _range = generate_range(stack.pop(), stack.pop())
            query = stack.pop()
            if query in _range:
                stack.push(1)
            else:
                stack.push(0)

        elif cmd == GENERATE_RANGE:
            _range = generate_range(stack.pop(), stack.pop())
            for item in _range:
                stack.push(item)

        elif cmd == GENERATE_RANGE_0:
            _range = generate_range(0, stack.pop())
            for item in _range:
                stack.push(item)

        elif cmd == NUMBER_SPLIT:
            temp = str(stack.pop())
            for thing in temp:
                stack.push(int(thing))

        elif cmd == FACTORIAL:
            stack.push(math.factorial(stack.pop()))

        #Next step, keywords

        elif cmd == COMMENT:
            comment = True

        elif cmd == BRANCH:
            continue

        elif cmd == ESCAPE:
            escape = True
            #print("ESCCAPE")

        elif cmd == REGISTER:
            if register is None:
                register = stack.pop()
            else:
                stack.push(register)
                register = None

        #Now, structures
        elif Tkn.name == Parse.CMDS.IF:
            condition = stack.pop()
            if condition:
                run(Parse.parse(Tkn.data[0]), stack)
            else:
                run(Parse.parse(Tkn.data[1]), stack)

        elif Tkn.name == Parse.CMDS.FOR:
            n = _eval(Tkn.data[0], stack)

            for q in range(int(n)):
                run(Parse.parse(Tkn.data[1]), stack)

        elif Tkn.name == Parse.CMDS.WHILE:
            condition = Tkn.data[0]
            while _eval(condition):
                run(Parse.parse(Tkn.data[1]), stack)

        elif Tkn.name == Parse.CMDS.FUNCTION:
            if Tkn.data[0] == 1:
                function_name, number_params = Tkn.data[1],\
                int(functions[function_name]["number"])

                function_stack = Stack()
                for _ in range(number_params):
                    function_stack.push(master_stack.pop())

                run(Parse.parse(functions[function_name]["body"]),
                stack, function_stack)

            else:
                function_name, number_params = Tkn.data[0]["name"],\
                int(Tkn.data[0]["number"])

                functions[function_name] = {
                    "number" : number_params,
                    "body" : Tkn.data[1]
                }

        #Now, operators
        elif cmd in MATHS:
            x, y = stack.pop(), stack.pop()
            temp = cmd
            if cmd == "Ë":
                temp = "**"

            stack.push(eval(f"y{temp}x"))

        elif cmd in CONDITIONAL:
            lhs, rhs = stack.pop(), stack.pop()
            temp = cmd
            if cmd == "=":
                temp = "=="

            elif cmd == "≬":
                    temp = "> 0 and lhs <"

            result = eval(f"rhs{temp}lhs")

            if result:
                stack.push(1)
            else:
                stack.push(0)

        elif cmd in NUMBERS:
            stack.push(int(cmd))

        elif Tkn.name == Parse.CMDS.STRING:
            stack.push(Tkn.data)

        #Keg+

        elif Tkn.data == DIV_MOD:
            quot, remainder = divmod(stack.pop(), stack.pop())
            stack.push(quot)
            stack.push(remainder)

        #Whitespace
        elif cmd == TAB:
            continue

        elif cmd == NEWLINE:
            stack.push(10)

        else:
            stack.push(_ord(cmd))

    if do_repush:
        for item in stack:
            master_stack.push(item)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="The location of the Keg file to open")
        parser.add_argument('-ex', '--explain', action='store_true',
                            help="Explains given source")
        args = parser.parse_args()
        file_location = args.file

        if args.explain:
            source = open(file_location, encoding="utf-8").read().strip("\n")
            i = 0
            for char in source:
                if char in DESCRIPTIONS:
                    print(" "*i + char + " "*(len(source) - i) + "#",
                          DESCRIPTIONS[char])
                else:
                    print(" "*i + char + " "*(len(source) - i) + "#",
                          "Push", char, "onto the stack")
                i += 1
            exit()

    else:
        file_location = input("Enter the file location of the Keg program: ")

    source = open(file_location, "r").read()


    

    #Preprocess ∑ as (!;|

    code = ""
    code_page = ""
    import string
    unicode_set = set(unicode) - set(string.printable)
    if any([char in unicode_set for char in source]):
        code_page = unicode

    #print(code_page)

    Stackd.code_page = code_page

    e = False #escaped while preprocessing?
    for c in source:
        if e:
            e = False
            code += c
            continue
        elif c == "\\":
            code += c
            e = True
            continue

        if c == "∑":
            code += "(!;|"
        else:
            code += c
    code = preprocess.process(code); #print("After preprocess:", code)
    code = uncompress.Uncompress(code); #print("After uncom:", code)
    run(Parse.parse(balance(code)), main_stack)

    if not printed:
        printing = ""
        if not pushed:
            try:
                print(input())
            except:
                pass
        for item in main_stack:
            if True: #type(item) is str or item < 10 or item > 256:
                printing += str(item) + " "

            else:
                printing += _chr(item)

        print(printing,end="")
