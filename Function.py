#Function @name n|...ƒ

def extract(string):
    result = {1: "", 0: ""}
    mode = 1
    escape = False
    opened = 0
    loops = {"for" : 0, "while" : 0}

    for char in string:
        if escape:
            result[mode] += char
            escape = False
            continue
        
        if char == "\\":
            escape = True
            result[mode] += char
            continue

        elif char == "(":
            loops["for"] += 1
            result[mode] += char

        elif char == ")":
            loops["for"] -= 1
            result[mode] += char

        elif char == "{":
            loops["while"] += 1
            result[mode] += char

        elif char == "}":
            loops["while"] -= 1
            result[mode] += char
            
        elif char == "[":
            if opened > 0:
                result[mode] += char
            opened += 1

        elif char == "|":
            if opened > 1:
                result[mode] += char
            elif max(list(loops.values())) != 0:
                result[mode] += char
            else:
                mode = 0

        elif char == "]":
            if opened > 1:
                result[mode] += char
                opened -= 1
            else:
                break
            
        else:
            if opened == 0:
                continue
            result[mode] += char

    return result
            

