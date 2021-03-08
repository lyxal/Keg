SQUARE = ["[", "]"]
ROUND = ["(", ")"]
CURLY = ["{", "}"]
FUNCTION = ["@", "ƒ"]
INTEGER_SCAN = "‡"
SWITCH = ["¦", "™"]
MAP = ["⑷", "⑸"]

OPEN, CLOSE = "[({@¦⑷", "])}ƒ™⑸"


class CMDS:
    CMD = "cmd"
    IF = "if"
    FOR = "for"
    WHILE = "while"
    NOP = ""
    FUNCTION = "function"
    ESC = "escape"
    STRING = "string"
    VARIABLE = "variable"
    INTEGER = "integer"
    SWITCH = "switch"
    MAP = "map"


class Token():
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return str(self.name) + " " + str(self.data)


def parse(prog):
    temp, parts, structures, escaped = "", [], [], False
    string_mode, string = False, ""
    variable_mode, variable, call_set = False, "", ""
    integer_mode, number = False, ""
    #call_set will be whether or not to set the variable

    ast = []
    #print(prog)
    for char in prog:
        # print(char, temp, parts, structures, [str(x) for x in ast])

        if integer_mode:
            if char not in "0123456789":
                integer_mode = False
                if structures:
                    temp += "‡" + number
                else:
                    ast.append(Token(CMDS.INTEGER, number))
                number = ""
            else:
                number += char
                continue

        if string_mode:
            if escaped:
                escaped = False
                string += char
            else:
                if char == "`":
                    string_mode = False
                    if structures:
                        temp += "`" + string + "`"
                    else:
                        ast.append(Token(CMDS.STRING, string))
                    string = ""
                elif char == "\\":
                    escaped = True
                    string += char
                else:
                    string += char
            continue

        if variable_mode:
            import string as STRING_MODULE
            if char not in STRING_MODULE.ascii_letters:
                variable_mode = False
                if structures:
                    temp += {"call" : "©", "set" : "®"}[call_set] + variable
                else:
                    ast.append(Token(CMDS.VARIABLE, [variable, call_set]))
                variable = ""
                call_set = ""

            else:
                variable += char
                continue

        if escaped:
            escaped = False
            if structures:
                temp += char
            else:
                ast.append(Token(CMDS.ESC, char))
            continue

        elif char == "\\":
            escaped = True
            if structures:
                temp += char
            continue

        elif char == "‡":
            integer_mode = True
            continue

        elif char == "`":
            string_mode = True
            continue

        elif char == "®":
            variable_mode = True
            call_set = "set"
            continue

        elif char == "©":
            variable_mode = True
            call_set = "call"
            continue



        if char in OPEN and not string_mode:
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

            elif char == SWITCH[0]:
                structures.append(CMDS.SWITCH)

            elif char == MAP[0]:
                structures.append(CMDS.MAP)

        elif char in CLOSE and not string_mode:
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
                        ast.append(Token(struct, [1,
                                                  parts[0]]))

                    elif len(parts) == 2:
                        ast.append(Token(struct, [func(parts[0]),
                                                   parts[1]]))
                    else:
                        # raise SyntaxError("Too many function parts)
                        ast.append(CMDS.NOP)
                    parts = []

                elif struct == CMDS.SWITCH:
                    if len(parts) == 0:
                        ast.append(CMDS.NOP)
                    else:
                        switch_temp = [parse(part) for part in parts[:-1]]
                        if parts[-1][0] == "║":
                            default = parse(parts[-1])
                            switch_temp.append([default[:], "default"])
                        ast.append(Token(struct, switch_temp))

                elif struct == CMDS.MAP:
                    ast.append(Token(struct, "'" + parts[0] + "'"))
                    parts = []
                    temp = ""

            else:
                temp += char

        elif char == "|" and len(structures) == 1:
            parts.append(temp)
            temp = ""

        elif char == "║":
            if len(structures) == 1 and structures[-1] == CMDS.SWITCH:
                default = True
                parts.append(temp)
                temp = "║"

            else:
                temp += char

        elif structures:
            temp += char
        else:
            ast.append(Token(CMDS.CMD, char))

    if variable_mode:
        ast.append(Token(CMDS.VARIABLE, [variable, call_set]))
    return ast

def func(source):
    if source.count(" ") == 1:
        name, n = source.split()

    else:
        n = ""
        j = len(source) - 1
        for i in range(len(source) - 1, -1, -1):
            if source[i] not in "0123456789":
                break
            n += source[i]
            j -= 1
        n = n[::-1]
        name = source[:j + 1]

    if n.isnumeric():
        n = int(n)
    else:
        if n == "*":
            n = "!"
        else:
            n = 0

    return {"name": name, "number": n}

if __name__ == "__main__":
    test = parse("`]`")
    print([str(x) for x in test])
