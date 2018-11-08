#While {...|...} Extractor

def extract(string):
    result = {"condition": "", "body": ""}
    mode = "condition"
    escape = False
    opened = 0
    loops = {"if" : 0, "for" : 0}

    for char in string:
        if escape:
            result[mode] += char
            escape = False
            continue
        
        if char == "\\":
            escape = True
            result[mode] += char
            continue

        elif char == "[":
            loops["if"] += 1
            result[mode] += char

        elif char == "]":
            loops["if"] -= 1
            result[mode] += char

        elif char == "(":
            loops["for"] += 1
            result[mode] += char

        elif char == ")":
            loops["for"] -= 1
            result[mode] += char
            
        elif char == "{":
            if opened > 0:
                result[mode] += char
            opened += 1

        elif char == "|":
            if opened > 1:
                result[mode] += char
            elif max(list(loops.values())) != 0:
                result[mode] += char
            else:
                mode = "body"

        elif char == "}":
            if opened > 1:
                result[mode] += char
                opened -= 1
            else:
                break
            
        else:
            if opened == 0:
                continue
            result[mode] += char
    if result["body"] == "":
        result["body"] = result["condition"]
        result["condition"] = "1"
    return result
