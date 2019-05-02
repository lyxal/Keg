import sys
import For, If, While, random

#Functions

LENGTH = "!" #Pushes the length of the stack onto the stack
DUPLICATE = ":" #Duplicates the last item on the stack
POP = "_" #Pops the last item from the stack
PRINT_CHR = "," #Prints the last item on the stack as a string (ord(char))
PRINT_INT = "." #Prints the last item on the stack as an integer
INPUT = "?" #Gets input from the user, pushing -1 as EOI
L_SHIFT = "'" #Left shift stack
R_SHIFT = '"' #Right shift stack
RANDOM = "~" #Pushes a random number between -infinity and infinity
REVERSE = "^" #Reverses the stack
SWAP = "$" #Swap the last two items on the stack

#Keywords

COMMENT = "#" #Creates a comment, which ignores all code thereafter
BRANCH = "|" #Switches to the other part of a structure
ESCAPE = "\\" #Pushes the next command as a string (ord(char))
C_STRING = "`" #Toggles string compression mode
REGISTER = "&" #Gets/sets the register
FUNCTION = "@" #Starts/ends a function definiton OR calls a function

#Operators

MATHS = "+-*/%"
CONDITIONAL = "<>="
NUMBERS = "0123456789"

#Whitespace

TAB = "\t"
ALT_TAB = "    "
NEWLINE = "\n"

#Structures

START = "start"
END = "end"
BODY = "body"

FOR_LOOP = {START : "(", END : ")"}
IF_STMT = {START : "[", END : "]"}
WHILE_LOOP = {START : "{", END : "}"}

stack = []
register = None
comment = False
escape = False
printed = False

def _eval(expression):
    #Evaulate the given expression as Keg code
    temp = []
    for char in expression:
        if char in NUMBERS:
            temp.append(int(char))

        elif char in MATHS:
            x, y = temp.pop(), temp.pop()
            temp.append(eval("y{0}x".format(char)))

        elif char in CONDITIONAL:
            lhs, rhs = temp.pop(), temp.pop()

            if char == "=":
                char = "=="
            
            result = eval("lhs{0}rhs".format(char))

            if result:
                temp.append(1)
            else:
                temp.append(0)

        elif char == LENGTH:
            temp.append(len(stack))

        elif char == DUPLICATE:
            temp.append(stack[-1])

        elif char == RANDOM:
            temp.append(random.randint(0, 32767))

        elif char == POP:
            temp.append(stack.pop())

        elif char == NEWLINE or char == TAB:
            continue

        elif char in "#|`@":
            raise SyntaxError("Invalid symbol in expression: " + expression)

        else:
            temp.append(ord(char))

    return temp[0]

def split(source):
    source = list(source.replace(TAB, ""))
    structures = {"If" : 0, "While" : 0, "For" : 0}
    indexes = []
    index = {START : 0, END : 0, BODY : None}
    structure = None

    for i in range(len(source)):
        char = source[i]
        
        if char in FOR_LOOP.values():
            if char == FOR_LOOP[START]:
                if max(structures.values()) == 0:
                    structure = "For"
                    index[START] = i

                structures["For"] += 1

            else:
                if list(structures.values()).count(0) == 2:
                    if structures["For"] == 1 and structure == "For":
                        index[END] = i
                        index[BODY] = For.extract(
                            "".join(source[index[START] : index[END] + 1]))
                        indexes.append(index)
                        index = {START : 0, END : 0, BODY : None}
                        structure = None


                structures["For"] -= 1
                    
        elif char in WHILE_LOOP.values():
            if char == WHILE_LOOP[START]:
                if max(structures.values()) == 0:
                    structure = "While"
                    index[START] = i

                structures["While"] += 1

            else:
                if list(structures.values()).count(0) == 2:
                    if structures["While"] == 1 and structure == "While":
                        index[END] = i
                        index[BODY] = While.extract(
                            "".join(source[index[START] : index[END] + 1]))
                        indexes.append(index)
                        index = {START : 0, END : 0, BODY : None}
                        structure = None

                structures["While"] -= 1
                    
        elif char in IF_STMT.values():
            if char == IF_STMT[START]:
                if max(structures.values()) == 0:
                    structure = "If"
                    index[START] = i

                structures["If"] += 1

            else:
                if list(structures.values()).count(0) == 2:
                    if structures["If"] == 1 and structure == "If":
                        index[END] = i
                        index[BODY] = If.extract(
                            "".join(source[index[START] : index[END] + 1]))
                        indexes.append(index)
                        index = {START : 0, END : 0, BODY : None}
                        structure = None

                structures["If"] -= 1

        else:               
            if structure is None:
                index[START] = i
                index[END] = i
                index[BODY] = source[i]
                indexes.append(index)
                index = {START : 0, END : 0, BODY : None}
            
    new = []
    
    for index in indexes:
        new.append(index[BODY])

    return new
                                
    
def run(source):
    global stack, register, comment, escape, printed

    if type(source) == str:
        #print(source)
        code = split(source)

    elif type(source) != list:
        raise TypeError("The given code is not of a supported type")

    else:
        code = source

    for cmd in code:

        #Handle any effects from keywords first

        if comment:
            if cmd == NEWLINE:
                comment = False
        
            continue

        if escape:
            escape = False
            stack.append(ord(cmd))
            continue
        
        #Functions first
        if cmd == LENGTH:
            stack.append(len(stack))

        elif cmd == DUPLICATE:
            stack.append(stack[-1])

        elif cmd == POP:
            stack.pop()

        elif cmd == PRINT_CHR:
            print(chr(stack.pop()), end="")
            printed = True

        elif cmd == PRINT_INT:
            print(stack.pop(), end="")
            printed = True

        elif cmd == L_SHIFT:
            stack.append(stack[0])
            del stack[0]

        elif cmd == R_SHIFT:
            stack.insert(0, stack.pop())

        elif cmd == RANDOM:
            stack.append(random.randint(0, 32767))

        elif cmd == REVERSE:
            stack.reverse()

        elif cmd == SWAP:
            stack[-1], stack[-2] = stack[-2], stack[-1] #only in python you see
                                                        #this
        elif cmd == INPUT:
            x = input()
            stack.append(-1)
            for char in reversed(x):
                stack.append(ord(char))
                

        #Now keywords

        elif cmd == COMMENT:
            comment = True

        elif cmd == BRANCH:
            #Just continue on this one, because hypothetically, all |'s
            #should be dealt with earlier
            continue

        elif cmd == ESCAPE:
            escape = True

        #elif cmd == C_STRING:
            #Code to handle string compression

        elif cmd == REGISTER:
            if register is None:
                register = stack.pop()

            else:
                stack.append(register)
                register = None

        #elif cmd == FUNCTION:
                #Code to handle functions here

        #Now, structures
        elif type(cmd) == dict:
            if 1 in cmd:
                #Must be an if
                test = stack.pop()

                if test:
                    run(cmd[1])

                else:
                    run(cmd[0])

            elif 'count' in cmd:
                #Must be a for loop
                n = _eval(cmd["count"])

                for q in range(n):
                    run(cmd["body"])

            elif 'condition' in cmd:
                #Must be a while loop
                condition = cmd["condition"]
                #print(condition, _eval(condition), stack)

                while _eval(condition):
                    run(cmd["body"])

            else:
                raise Exception("Oh, uh, could you get me the milk!")
        
        #Now, operators
        elif cmd in MATHS:
            x, y = stack.pop(), stack.pop()
            stack.append(eval("y{0}x".format(cmd)))

        elif cmd in CONDITIONAL:
            lhs, rhs = stack.pop(), stack.pop()

            if cmd == "=":
                cmd = "=="

            result = eval("rhs{0}lhs".format(cmd))

            if result:
                stack.append(1)
            else:
                stack.append(0)

        elif cmd in NUMBERS:
            stack.append(int(cmd))

        #Deal with whitespace
        elif cmd == TAB:
            continue

        elif cmd == ALT_TAB:
            continue

        elif cmd == NEWLINE:
            continue

        #Don't do anything with normal spaces, as they are pushed

        else:
            stack.append(ord(cmd))

        #print(cmd, stack)

def grun(code, prepop):
    for item in prepop.split():
        stack.append(int(item))

    run(code)

    if not printed:
        printing = ""
        for item in stack:
            if item < 10 or item > 256:
                printing += str(item) + " "

            else:
                printing += chr(item)

        print(printing)

        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_location = sys.argv[1]
    else:
        file_location = input("Enter the file location of the Keg program: ")
        prepop = input("Enter values to prepopulate the stack: ")

        for item in prepop.split():
            stack.append(int(item))

    code = open(file_location, encoding="utf-8").read().strip("\n")
    run(code)

    if not printed:
        printing = ""
        for item in stack:
            if item < 10 or item > 256:
                printing += str(item) + " "

            else:
                printing += chr(item)

        print(printing)
