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
#Note: Most of these are from A_ee/A__/User:A, so go check out their
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
NUMBER_SPLIT = "÷"
FACTORIAL = "¡"
EMPTY = "ø"
PRINT_ALL = "Ω"
NOT = "¬" #!top
PREDEFINED_CONSTANT = "λ"
PI = "π"
HALVE_TOP = "½" #math(stack, "/")
INCREMENT = "⑨" #perhaps an upside down semi-colon

'''Remind me to create descriptions later'''

#Keg+ Section
PUSH_N_PRINT = "ȦƁƇƉƐƑƓǶȊȷǨȽƜƝǪǷɊƦȘȚȔƲɅƛƳƵ"
for n in range(127234, 127243): PUSH_N_PRINT += chr(n)
#Don't go trying to print PUSH_N_PRINT in IDLE... Tkinter doesn't like some of
#the characters

ALPHA_MAP = "abcdefghijklmnopqrstuvwxyz1234567890"


INTEGER_SCAN = "‡"
TO_INT, TO_FLOAT, TO_STRING, TO_STACK, TO_CHAR = "ℤℝ⅍℠ⁿ"
UPPER, LOWER, TOGGLE = "⟰⟱⟷"
SQUARE_OPERATOR = "²"
STRING_INPUT = "᠀"
ALL_TRUE = "∀"
ALL_EQUAL = "≌"
SUMMATE = "⅀"
EVAL_EXEC = "ß"
END_EFCOM = "™"

VARIABLE_SET = "©"
VARIAGE_GET = "®"

PERFORM_INDEX = "⊙"
INDEX_LEVEL_DOWN = "᠈"
INDEX_LEVEL_0 = "º"
INFINITY = "א"
RANDOM_INSTRUCTION = "⯑" #Chooses an instruction from
#all avaliable commands and puts it in.

DIV_MOD, EQUAL_TYPES, INDEX_LEVEL_UP, MD5_HASH = "①②③④"
FUNCTION_MODIFIERS = "⑤⑥⑦⑧"
ITEM_IN = "⊂"


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
CONDITIONAL = "<>=≬≤≠≥"
NUMBERS = "0123456789"

DESCRIPTIONS[MATHS] = "Pop x and y, and push y {0} x"
DESCRIPTIONS[CONDITIONAL] = "Pop x and y, and push y {0} x"
DESCRIPTIONS[NUMBERS] = "Push {0}"

#Whitespace
TAB = "\t"
NEWLINE = "\n"

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
unicode += "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅↫"


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

        if name == Parse.CMDS.STRING:
            import KegStrings
            item = KegStrings.obj_str_extract("`" + command + "`")
            if type(item) != str:
                if type(item) is list:
                    result += f"{stack}.push(Stack({item}))"
                else:
                    result += f"{stack}.push({item})"
            else:
                result += f"iterable({stack}, '" + command + "')"

        #Handle all functions (built-in)
        elif command == LENGTH:
            result += f"length({stack})"

        elif command == DUPLICATE:
            result += f"duplicate({stack})"

        elif command == POP:
            result += f"pop_top({stack})"

        elif command == PRINT_CHR:
            result += f"nice({stack}); printed = True"

        elif command == PRINT_INT:
            result += f"raw({stack}); printed = True"

        elif command in [L_SHIFT, R_SHIFT]:
            result += f"shift({stack}, '" + ["left", "right"]\
                      [[L_SHIFT, R_SHIFT].index(command)]+ "')"

        elif command == REVERSE:
            result += f"reverse({stack})"

        elif command == RANDOM:
            result += f"random({stack})"

        elif command == SWAP:
            result += f"swap({stack})"

        elif command == INPUT:
            result += f"Input({stack})"

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

        elif command == STRING_INPUT:
            result += f"string_input({stack})"

        elif command == INCREMENT:
            result += f"increment({stack})"

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
            if command[0] == "":
                result += tab_format("pass")
            else:
                result += tab_format(transpile(command[0], stack))

            if command[1]:
                result += "\nelse:\n"
                result += tab_format(transpile(command[1], stack))

        elif name == Parse.CMDS.FOR:
            result += transpile(command[0])
            result += f"\nfor _ in loop_eval({stack}.pop()):"
            result += "\n"



            if command[1] == "":
                result += tab_format("pass")
            else:
                result += tab_format(transpile(command[1]))

        elif name == Parse.CMDS.WHILE:
            if command[0] != "":
                result += "condition = condition_eval(["
                result += ", ".join([f"\"{fn}\"" for fn in transpile(command[0])\
                                     .split("\n")])
                result += f"], {stack})"
            else:
                result += "condition = 1"
            result += "\nwhile condition:\n"

            if command[1] == "":
                result += tab_format("pass")
            else:
                result += tab_format(transpile(command[1]))
            result += "\n"
            if command[0] != "":
                result += "condition = condition_eval(["
                result += ", ".join([f"\"{fn}\"" for fn in transpile(command[0])\
                                     .split("\n")])
                result += f"], {stack})"
            else:
                result += tab_format("condition = 1")

        elif name == Parse.CMDS.FUNCTION:
            if command[0] == 1:
                #Function call
                result += command[1] + f"({stack})"
            else:
                result += "def " + command[0]["name"] + f"({stack}):\n"
                result += "    temp = Stack()"
                result += "\n    for _ in range(" + str(command[0]["number"])\
                          + "): "
                result += f"temp.push({stack}.pop())"
                result += "\n" + tab_format(transpile(command[1], "temp"))
                result += f"\n    for item in temp: {stack}.push(item)"

        elif name == Parse.CMDS.VARIABLE:
            if command[1] == "set":
                result += f"var_set(stack, '{command[0]}')"

            else:
                result += f"var_get(stack, '{command[0]}')"

        #Now, operators.
        elif command in MATHS:
            if command == "Ë":
                command = "^"

            result += f"maths({stack}, '" + command + "')"

        elif command in CONDITIONAL:
            result += f"comparative({stack}, '{command}')"

        elif command in NUMBERS:
            result += f"integer({stack}, " + command + ")"




        #Whitespace
        elif command == TAB:
            continue

        elif command == NEWLINE:
            result += f"integer({stack}, 10)"

        #Keg+

        elif command in PUSH_N_PRINT:
            result += f"print('{ALPHA_MAP[PUSH_N_PRINT.index(command)]}')"

        elif command in [TO_INT, TO_FLOAT, TO_STRING, TO_STACK, TO_CHAR]:
            result += f"try_cast({stack}, '{command}')"

        elif command == SQUARE_OPERATOR:
            result += f"square({stack})"

        elif command == ALL_TRUE:
            result += f"all_true{stack}"

        elif command == ALL_EQUAL:
            result += f"all_equal({stack})"

        elif command == UPPER:
            result += f"case_switch({stack}, 'upper')"

        elif command == LOWER:
            result += f"case_switch({stack}, 'lower')"

        elif command == TOGGLE:
            result += f"case_switch({stack}, 'toggle')"

        elif command == SUMMATE:
            result += f"summate({stack})"

        elif command == EMPTY:
            result += f"empty({stack})"

        elif command == PRINT_ALL:
            result += f"print_all({stack})"

        #Default case

        else:
            result += f"character({stack}, '" + command + "')"

        result += ("\n")

    return result.rstrip("\n")

if __name__ == "__main__":
    '''print(unicode)
    '''
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
    import KegLib
    Stackd.code_page = code_page
    KegLib.code_page = code_page

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
    code = preprocess.balance_strings(code);
    code = uncompress.Uncompress(code); #print("After uncom:", code)

    header = """
from KegLib import *
from Stackd import Stack
stack = Stack()
printed = False
"""

    footer = """

if not printed:
    printing = ""
    for item in stack:
        if type(item) is Stack:
            printing += str(item)

        elif type(item) is str:
            printing += custom_format(item)
        elif type(item) == Coherse.char:
            printing += item.v

        elif item < 10 or item > 256:
            printing += str(item)
        else:
            printing += chr(item)
    print(printing, end="")
"""

    code = transpile(balance(code))
    if args.compiled:
        import sys
        sys.stderr.write("-----\nTranspiled Code:")
        full = header + code + footer
        sys.stderr.write(full)
        sys.stderr.write("-----\n")

    exec(header + code + footer)
