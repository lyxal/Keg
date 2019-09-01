SQUARE = ["[", "]"]
ROUND = ["(", ")"]
CURLY = ["{", "}"]
FUNCTION = ["@", "ƒ"]

OPEN, CLOSE = "[({@", "])}ƒ"


class CMDS:
    CMD = "cmd"
    IF = "if"
    FOR = "for"
    WHILE = "while"
    NOP = "nop"
    FUNCTION = "function"


class Token():
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return str(self.name) + " " + str(self.data)


def parse(prog):
    temp, parts, structures, escaped = "", [], [], False
    ast = []

    for char in prog:
        #print(temp, parts, structures, [str(x) for x in ast])
        if escaped:
            escaped = not escaped

                  
        elif char == "\\":
            escaped = True
            continue

    
        if char in OPEN:
            if structures:
                temp += char

            if char == SQUARE[0]:
                structures.append(CMDS.IF)

            elif char == ROUND[0]:
                structures.append(CMDS.FOR)

            elif char == CURLY[0]:
                structures.append(CMDS.WHILE)

            elif char == FUNCTION[0]:
                structures.append(CMDS.FUNCTION)

        elif char in CLOSE:

            struct = structures.pop()

            if len(structures) == 0:
                parts.append(temp)
                temp = ""
                if struct == CMDS.IF:
                    if len(parts) == 0:
                        ast.append(CMDS.NOP)

                    elif len(parts) == 1:
                        ast.append(Token(struct, [parts[0],
                                                  CMDS.NOP]))

                    elif len(parts) == 2:
                        ast.append(Token(struct, [parts[0],
                                                  parts[1]]))

                    else:
                        #raise SyntaxError("Too many if parts")
                        ast.append(CMDS.NOP)

                    parts = []

                elif struct == CMDS.FOR:
                    if len(parts) == 0:
                        ast.append(CMDS.NOP)

                    elif len(parts) == 1:
                        ast.append(Token(struct, ["!",
                                                  parts[0]]))

                    elif len(parts) == 2:
                        ast.append(Token(struct, [parts[0],
                                                  parts[1]]))

                    else:
                        # raise SyntaxError("Too many for parts)
                        ast.append(CMDS.NOP)
                    parts = []

                elif struct == CMDS.WHILE:
                    if len(parts) == 0:
                        ast.append(CMDS.NOP)

                    elif len(parts) == 1:
                        ast.append(Token(struct, ["1",
                                                  parts[0]]))
                    elif len(parts) == 2:
                        ast.append(Token(struct, [parts[0],
                                                  parts[1]]))
                    else:
                        # raise SyntaxError("Too many while parts)
                        ast.append(CMDS.NOP)
                    parts = []

                elif struct == CMDS.FUNCTION:
                    if len(parts) == 0:
                        ast.append(CMDS.NOP)
                    if len(parts) == 1:
                        ast.append(Token(struct, [1, parse(parts[0])]))

                    elif len(parts) == 2:
                        ast.append(Token(struct, [[func(parts[0]),
                                                   parse(parts[1])]]))
                    else:
                        # raise SyntaxError("Too many function parts)
                        ast.append(CMDS.NOP)
                    parts = []

            else:
                temp += char

        elif char == "|" and len(structures) == 1:
            parts.append(temp)
            temp = ""

        elif structures:
            temp += char
        else:
            ast.append(Token(CMDS.CMD, char))

    return ast

def func(source):
    if source.count(" ") != 1:
        name
        name, n = source.split()
        name = source
        n = "0"

    if n.isnumeric():
        n = int(n)
    else:
        n = 0
    
    return {"name": name, "n": n}

