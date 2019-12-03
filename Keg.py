import sys #Used for file parsing
import Parse #Used for Keg source parsing
import uncompress #Used for uncompressing Keg strings
import preprocess #Used for expanding preprocessor cues
import Stackd #The main data type of Keg

'''Constants Section'''
'''The following lines will define all the commands and place them into
more readable/modular constants'''

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
#Note: Most of these are from myu-sername/A̲̲/User:A, so go check out their
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
DOUBLE = "⑵" #dobule the top of stack
NEGATE = "±" #*-1
ONE_ON_X = "⑱" #1/tos
ROUND = "⑲" #uses round function
WHILE_STUFF = "⑳" #Preprocesses as {!|

#Keg+ Section
PUSH_N_PRINT = "ȦƁƇƉƐƑƓǶȊȷǨȽƜƝǪǷɊƦȘȚȔƲɅƛƳƵ"
for n in range(127234, 127243): PUSH_N_PRINT += chr(n)
#NOTE: Don't go trying to print PUSH_N_PRINT in IDLE...
#Tkinter doesn't like some of the characters

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
END_SWITCH = "™"
MULTILINE_INPUT = "᠈"

VARIABLE_SET = "©"
VARIAGE_GET = "®"

PERFORM_INDEX = "⊙"
INFINITY = "א"
RANDOM_INSTRUCTION = "⯑" #Chooses an instruction from
#all avaliable commands and puts it in.

DIV_MOD, EQUAL_TYPES, FIND_POS, PRINT_RAW_NO_POP = "①②③④"
FUNCTION_MODIFIERS = "⑤⑥⑦⑧"
PRINT_NICE_NO_POP = "⑩"
TO_PERCENTAGE = "⑪"
ITEM_IN = "⊂"

EMPTY_STRING, SPACE_STRING = "⑫⑬"
SORT_STACK = "⑭"
SINGULAR_SCC = "⑮"
POP_ITEM = "⑯" #Takes the TOS and removes all instances of TOS
FILTER_BY = "⑰" #Takes a keg-string and pops all items not matching condition

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

#Code page - Special to Keg
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

def balance(source: str) -> str:
    '''

    Takes: source [str]
    Does: Balances any unclosed brackets and replaces any escaped brackets with
    an expression that evaluates to the ordinal value of the bracket. This is
    because it was too hard to have literal brackets in the source and have
    them escaped like other characters.
    Returns: str

    "abc" -> "abc"
    "(+" -> "(+)"
    "{[{[" -> "{[{[]}]}"
    "\{" -> "z1-"

    '''

    brackets = [] #This is kind of equivalent to the loops list found commonly
    #in Python BF interpreters.
    mapping = {"{" : "}", "[" : "]", "(" : ")", "": ""}
    alt_brackets = {"{" : "z1-", "}" : "z3+", "(" : "85*",
                    ")" : "85*1+", "[" : "Z1+",
                    "]" : "Z3+"}

    escaped = False #Whether or not there is currently an escape sequence

    result = ""
    for char in source:
        if escaped: #Either escape the bracket or keep the escape
            if char in alt_brackets:
                result += alt_brackets[char]
            else:
                result += "\\" + char
            escaped = False
            continue

        elif char == "\\":
            escaped = True

            continue

        if char in "[({":
            brackets.append(char)

        elif char in "])}":
            for i in range(len(brackets)): #Close an open bracket
                if mapping[brackets[i]] == char:
                    brackets[i] = ""
                    break

        result += char

    if len(brackets):
        for char in reversed(brackets): #Close all brackets
            result += mapping[char]

    return result

def tab_format(string: str) -> str:
    '''
    Takes: string [str]
    Does: Formats the line with tabs at the start. This also happens to
    recursively format lines within for|while loops/if stmts/functions, which
    is nice.
    Returns: str


    "abc" -> "    abc\n"

    '''
    result = ""
    for line in string.rstrip().split("\n"):
        result += "    " + line + "\n"
    return result

'''Actual Transpiler'''

def transpile(source: str, stack="stack"):
    '''
    Takes: source [str], stack (default="stack") [str]
    Does: This is the primary function here, as it does the actual transpilation
    of Keg programs. Without it, there would be no Keg. It first of all parses
    the source into a list of tokens as defined in `Parse.py`. It then goes
    through and turns these tokens into python.
    Returns: str

    '''

    if type(source) == str:
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
        #^^ used only for debugging while working on the Transpiler


        #Deal with comments and potential escaped characters first
        if comment == True:
            if command == NEWLINE: #End of Comment
                comment = False
            continue

        if name == Parse.CMDS.ESC:
            escape = False
            result += f"character(stack, '{command}')\n"
            continue

        if name == Parse.CMDS.STRING:
            import KegStrings #Allow for the usage of object strings
            item = KegStrings.obj_str_extract("`" + command + "`")
            if type(item) != str: #The object is an object string
                if type(item) is list: #this is generally raw python.
                    result += f"{stack}.push(Stack({item}))"
                else:
                    result += f"{stack}.push({item})"
            else: #It isn't an object string
                result += f"iterable({stack}, \"" + command + "\")"

        #Handle all functions (built-in)
        elif command == LENGTH:
            if args and args.lengthpops:
                result += f"length({stack}, True)"
            else:
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

        elif command == DOUBLE:
            result += f"double({stack})"

        elif command == NEGATE:
            result += f"negate({stack})"

        elif command == ONE_ON_X:
            result += f"reciprocal({stack})"

        elif command == ROUND:
            result += f"keg_round({stack})"

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

            '''

            [ifTrue|ifFalse] -->

            if bool(stack.pop()):
                ifTrue
            else:
                ifFalse

            [ifTrue] -->

            if bool(stack.pop()):
                ifTrue

            [|ifFalse] -->

            if bool(stack.pop()):
                pass
            else:
                ifFalse
            '''

            result += f"if bool({stack}.pop()):\n"
            if Token.data[0] == "":
                result += tab_format("pass")
            else:
                result += tab_format(transpile(command[0], stack))

            if Token.data[1]:
                result += "\nelse:\n"
                result += tab_format(transpile(command[1], stack))

        elif name == Parse.CMDS.FOR:

            '''

            (count|code) -->

            count
            for _ in loop_eval(stack.pop()):
                code


            (code) -->

            length(stack)
            for _ in loop_eval(stack.pop()):
                code

            '''

            result += transpile(Token.data[0])
            result += f"\nfor _ in loop_eval({stack}.pop()):"
            result += "\n"



            if Token.data[1] == "":
                result += tab_format("pass")
            else:
                result += tab_format(transpile(Token.data[1]))

        elif name == Parse.CMDS.WHILE:

            '''
            {condition|code} -->

            for expr in condition: eval(expr)
            while stack.pop():
                code
                for expr in condition: eval(expr)


            {code} -->

            while 1:
                code

            '''

            if Token.data[0]:
                template = "for expr in {0}: eval(expr)\n"

                functions = [] #Transpile all functions into a nice list
                for function in transpile(Token.data[0]).split("\n"):
                    functions.append(function)


                result += template.format(functions)
                result += f"while {stack}.pop():\n"
            else:
                result += "while 1:\n"

            if not Token.data[1]:
                result += tab_format("pass")
            else:
                result += tab_format(transpile(Token.data[1]))
            result += "\n"

            if Token.data[0]:
                result += tab_format(template.format(functions))

        elif name == Parse.CMDS.FUNCTION:
            if command[0] == 1:
                #Function call
                result += command[1] + f"({stack})"
            else:
                result += "def " + command[0]["name"] + f"({stack}):\n"
                result += "    temp = Stack()"
                if command[0]["number"] == "!":
                    result += f"\n    temp = {stack}.copy()"
                else:
                    result += "\n    for _ in range(" + str(command[0]["number"]\
                    ) + "): "
                    result += f"temp.push({stack}.pop())"
                result += "\n" + tab_format(transpile(command[1], "temp"))
                result += f"\n    for item in temp: {stack}.push(item)"

        elif name == Parse.CMDS.VARIABLE:
            if command[1] == "set":
                result += f"var_set({stack}, '{command[0]}')"

            else:
                result += f"var_get({stack}, '{command[0]}')"

        elif name == Parse.CMDS.SWITCH:
            result += f"\nSWITCH_VARIABLE = {stack}.pop()\n"
            result += "for _ in range(1):\n"
            for case in command:
                if len(case) == 1:
                    result += tab_format("else: \n")
                    result += tab_format(tab_format(\
                        f"{stack}.push(SWITCH_VARIABLE)"))
                    result += tab_format(tab_format(transpile(case[:])))
                    result += tab_format(tab_format("\nbreak\n"))
                else:
                    result += tab_format(transpile([case[0]]) + "\n")
                    result += tab_format(f"{stack}.push(SWITCH_VARIABLE)")
                    result += tab_format(f"comparative({stack}, '=')")
                    result += tab_format(f"if bool({stack}.pop()):\n")
                    result += tab_format(tab_format(transpile(case[1:])))
                    result += tab_format(tab_format("\nbreak\n"))


        #Now, operators.
        elif command in MATHS:
            if command == "Ë":
                result += f"exponate({stack})"
            else:
                result += f"maths({stack}, '" + command + "')"

        elif command in CONDITIONAL:
            result += f"comparative({stack}, '{command}')"

        elif command in NUMBERS:
            result += f"integer({stack}, " + command + ")"

        elif command == HALVE_TOP:
            result += f"halve_top({stack})"



        #Whitespace
        elif command == TAB:
            continue

        elif command == NEWLINE:
            if args and args.ignorenewlines:
                pass
            else:
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

        elif command == EVAL_EXEC:
            result += f"keg_exec({stack})"

        elif name == Parse.CMDS.INTEGER:
            result += f"integer({stack}, {command})"

        elif command == PERFORM_INDEX:
            result += f"perform_index({stack})"

        elif command == MULTILINE_INPUT:
            result += f"multiline({stack})"

        elif command == PRINT_RAW_NO_POP:
            result += f"raw({stack}, True)"

        elif command == PRINT_NICE_NO_POP:
            result += f"nice({stack}, True)"

        elif command == TO_PERCENTAGE:
            result += f"to_percentage({stack})"

        elif command == EMPTY_STRING:
            result += f"iterable({stack}, \"\")"

        elif command == SPACE_STRING:
            result += f"iterable({stack}, \" \")"

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

        #Custom Keg flags
        #-hd --head : prints only the head of the stack upon finishing

        parser.add_argument("-hd", "--head",
                            help="Only prints the top item",
                            action='store_true')

        #-no --newoutput : prints everything 'as-is'/no conversion of ints to
        #chars

        parser.add_argument("-no", "--newoutput",
                    help="Prints everything 'as-is'",
                    action='store_true')

        #-hr --headraw : prints only the top of stack raw

        parser.add_argument("-hr", "--headraw",
            help="Only prints the top item raw",
            action='store_true')

        #-rr --reverseraw : reverse then perform -hr

        parser.add_argument("-rr", "--reverseraw",
            help="Reverse stack then -rr",
            action='store_true')

        #-rn --reversenice : reverse then perform -hd

        parser.add_argument("-rn", "--reversenice",
            help="Reverse stack then -rd",
            action='store_true')

        #-ir --inputraw : implicit input uses ? not ¿

        parser.add_argument("-ir", "--inputraw",
            help="Make implicit input _not_ evaluate everything",
            action='store_true')

        #-oc --outputcharacters : Output everything as characters if possible
        parser.add_argument("-oc", "--outputcharacters",
            help="Output _everything_ as characters if possible",
            action='store_true')

        #-lp --lengthpops : Length pops if the stack has 0 items
        parser.add_argument("-lp", "--lengthpops",
            help="Length (!) pops if the stack has 0 items",
            action='store_true')

        #-in --ignorenewlines : newlines DON'T push 10

        parser.add_argument("-in", "--ignorenewlines",
            help="newlines DON'T push 10",
            action='store_true')







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
        args = 0

    source = open(file_location, encoding="utf-8").read()



    code = source
    code_page = ""
    import string
    unicode_set = set(unicode) - set(string.printable)
    if any([char in unicode_set for char in source]):
        code_page = unicode

    #print(code_page)
    import KegLib, Coherse
    Stackd.code_page = code_page
    KegLib.code_page = code_page
    Coherse.code_page = code_page

    code = preprocess.process(code); #print("After preprocess:", code)
    code = preprocess.balance_strings(code);
    code = uncompress.Uncompress(code); #print("After uncom:", code)
    code += "\t"

    header = """
from KegLib import *
from Stackd import Stack
stack = Stack()
printed = False
"""

    if args and args.inputraw:
        Stackd.input_raw = True

    #Conditionally determine the footer

    if args and args.head:
        footer = """
if not printed:
    nice(stack)
"""

    elif args and args.newoutput:
        footer = """
if not printed:
    for item in stack:
        if type(item) in [str, KegLib.Coherese.char]:
            nice(stack)
        else:
            raw(stack)"""

    elif args and args.headraw:
        footer = """
if  not printed:
    raw(stack)
"""

    elif args and args.reverseraw:
        footer = """
if not printed:
    reverse(stack)
    raw(stack)
"""

    elif args and args.reversenice:
        footer = """
if not printed:
    reverse(stack)
    nice(stack)
"""

    elif args and args.outputcharacters:
        footer = """
if not printed:
    for item in stack:
        if type(item) in [int, float]:
            print(chr(int(item)), end="")
        else:
            print(str(item), end="")
"""

    else:
        footer = """

if not printed:
    printing = ""
    for item in stack:
        if type(item) in [Stack, list]:
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
    if args and args.compiled:
        import sys
        sys.stderr.write("-----\nTranspiled Code:")
        full = header + code + footer
        sys.stderr.write(full)
        sys.stderr.write("-----\n")


    #First, load the BFL

    import os

    prepend = os.path.dirname(__file__)
    source = open(prepend + "/docs/BFL.keg", encoding="utf-8").read()
    exec(header + transpile(source))



    if code.strip():
        exec(header + code + footer)
    else:
        try:
            print(input())
        except:
            pass
