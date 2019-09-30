import sys
import Parse
import uncompress
import preprocess
import Stackd

'''Constants Section'''

#Built-ins

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

#Keg+ Section
PUSH_N_PRINT = "ȦƁƇƉƐƑƓǶȊȷǨȽƜƝǪǷɊƦȘȚȔƲɅƛƳƵ"
for n in range(127234, 127243): PUSH_N_PRINT += chr(n)
#Don't go trying to print PUSH_N_PRINT in IDLE... Tkinter doesn't like some of
#the characters


INTEGER_SCAN = "‡"
TO_INT, TO_FLOAT, TO_STRING, TO_STACK = "ℤℝ⅍℠"
UPPER, LOWER, TOGGLE = "⟰⟱⟷"
SQUARE_OPERATOR = "²"
STRING_INPUT = "᠀"
ALL_TRUE = "∀"
ALL_EQUAL = "≌"
SUMMATE = "⅀"

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

'''Transpiler Helpers'''

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

    if len(brackets):
        for char in reversed(brackets):
            result += mapping[char]

    return result

def tab_format(string):
    result = ""
    for line in string.rstrip().split("\n"):
        result += "    " + line + "\n"
    return result

'''Actual Transpiler'''

def transpile(source: str, stack="stack"):

    source = Parse.parse(source)

    comment = False #Whether or not the transpiler is parsing a comment
    escaped = False #Whether or not the transpiler needs to use escape()

    #Wow, this feels odd. Normally, this would be the interpreter part, but now,
    #it's just a transpiler. I.e. There would normally be variables here getting
    #ready for the interpreting that would be about to happen, but not this time

    result = ""
    tabs = ""
    #The variable storing the end result

    for Token in source:
        name, command = Token.name, Token.data
        #print(name, command)

        #Deal with comments and potential escaped characters first
        if comment == True:
            if command == NEWLINE: #End of Comment
                comment = False
            continue

        if name == Parse.CMDS.ESC:
            escape = False
            result += f"integer(stack, {ord(command)})\n"
            continue

        #Handle all functions (built-in)
        if command == LENGTH:
            result += f"length({stack})"

        elif command == DUPLICATE:
            result += f"duplicate({stack})"

        elif command == POP:
            result += f"pop_top({stack})"

        elif command == PRINT_CHR:
            result += f"nice({stack})"

        elif command == PRINT_INT:
            result += f"raw({stack})"

        elif command in [L_SHIFT, R_SHIFT]:
            result += f"shift({stack}, " + ["left", "right"]\
                      [L_SHIFT, R_SHIFT].index(command) + ")"

        elif command == REVERSE:
            result += f"reverse({stack})"

        elif command == SWAP:
            result += f"swap({stack})"

        elif command == INPUT:
            result += f"_input({stack})"

        #Now, for Reg's commands
        elif command == IOTA:
            result += f"iota({stack})"

        elif command == DECREMENT:
            result += f"decrement({stack})"

        elif command == SINE:
            result += f"sine({stack})"

        elif command == NICE_INPUT:
            result += f"nice_input({stack})"

        elif command == EXCLUSIVE_RANGE:
            result += f"excl_range({stack})"

        elif command == INCLUSIVE_RANGE:
            result += f"incl_range({stack})"

        elif command == GENERATE_RANGE:
            result += f"smart_range({stack})"

        elif command == NUMBER_SPLIT:
            result += f"item_split({stack})"

        elif command == FACTORIAL:
            result += f"factorial({stack})"

        #Now, keywords and structures
        elif command == COMMENT:
            comment = True

        elif command == BRANCH:
            continue

        elif command == ESCAPE:
            escaped = True

        elif command == REGISTER:
            result += f"register({stack})"

        elif name == Parse.CMDS.IF:
            result += f"if bool({stack}.pop()):\n"
            result += tab_format(transpile(command[0]))

            if command[1]:
                result += "\nelse:\n"
                result += tab_format(transpile(command[1]))

        elif name == Parse.CMDS.FOR:
            result += transpile(command[0])
            result += f"\nfor _ in loop_eval({stack}.pop()):"
            result += "\n" + tab_format(transpile(command[1]))

        elif name == Parse.CMDS.WHILE:
            result += "exec('condition = " + transpile(command[0]) + "')"
            result += "\nwhile condition:\n"
            result += tab_format(transpile(command[1]))
            result += "\n"
            result += "exec('condition = " + transpile(command[0]) + "')"

        elif name == Parse.CMDS.FUNCTION:
            if command[0] == 1:
                #Function call
                result += command[1] + f"({stack})"
            else:
                result += "def " + command[0]["name"] + f"({stack}):\n"
                result += "    temp = Stack()"
                result += "\n    for _ in range(" + str(command[0]["number"])\
                          + "):"
                result += f"\n    temp.push({stack}.pop())"
                result += "\n" + tab_format(transpile(command[1]))
                result += f"\n    for item in temp: {stack}.push(item)"

        #Now, operators.
        elif command in MATHS:
            if command == "Ë":
                command = "^"

            result += f"maths({stack}, '" + command + "')"

        elif command in CONDITIONAL:
            mapping = {"<" : "lt", ">" : "gt", "≤" : "le", "≥" : "ge",
                       "=" : "eq", "≠" : "nq", "≬" : "l0"}

            result += mapping[command] + f"({stack})"

        elif command in NUMBERS:
            result += f"integer({stack}, " + command + ")"

        elif name == Parse.CMDS.STRING:
            result += f"iterable({stack}, '" + command + "')"

        #Whitespace
        elif command == TAB:
            continue

        elif command == NEWLINE:
            result += f"integer({stack}, 10)"

        else:
            result += f"character({stack}, '" + command + "')"

        result += "\n"

    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="The location of the Keg file to open")
        parser.add_argument('-ex', '--explain',
                            help="Explains given source", action='store_true')
        parser.add_argument("-cm", "--compiled",
                            help="Shows the compiled code", action='store_true')
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

    source = open(file_location, encoding="utf-8").read()


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

    header = """
from KegLib import *
from Stackd import Stack
stack = Stack()
printed = False
_register = None
"""

    footer = """

if not printed:
    printing = ""
    for item in stack:
        if type(item) in [str, Stack]:
            printing += item
        elif type(item) == Coherse.char:
            printing += item.v

        elif item < 10 or item > 256:
            printing += str(item)
        else:
            printing += chr(item)
    print(printing)
"""

    code = transpile(code)
    if args.compiled:
        import sys
        sys.stderr.write("-----\nTranspiled Code:")
        full = header + code + footer
        sys.stderr.write(full)
        sys.stderr.write("-----\n")

    exec(header + code + footer)
