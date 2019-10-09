#The Preprocessor


STRING_CHARS = "`¶“‘«„"

def process(source):
    final = ""
    string_type = ""
    escaped = False
    SSL_needed = False

    for char in source:
        if char in STRING_CHARS:
            if string_type == char:
                if escaped:
                    escaped = False
                else:
                    string_type = ""
            elif string_type == "":
                if escaped:
                    escaped = False
                else:
                    string_type = char

        elif char == "\\":
            if escaped: escaped = False
            else: escaped = True

        elif char == "₳":
            SSL_needed = True
            continue

        elif SSL_needed:
            final += f"<SSL:{char}>"
            SSL_needed = False
            continue

        final += char

    return final

def balance_strings(source):
    symbol = ""
    string_mode = False
    escaped = False

    alt_strings = {"`" : "834**", "¶" : "882**",
                   "‘" : "27*", "“" : "35*",
                   "«" : "25*7+", "„" : "82*"}
                   
                   


    result = ""
    for char in source:
        if escaped:
            if char in alt_strings:
                if string_mode:
                    result += "\\" + char
                else:
                    result += alt_strings[char]
            else:
                result += "\\" + char
            escaped = False
            continue

        elif char == "\\":
            escaped = True
            continue

        elif string_mode:
            if char == symbol:
                symbol = None
                string_mode = False

            result += char
            continue

        elif char in alt_strings:
            string_mode = True
            symbol = char
            result += char

        else:
            result += char


    if symbol:
        result += symbol

    return result

if __name__ == "__main__":
    assert process("₳a") == "<SSL:a>"
    assert process("₳a₳b") == "<SSL:a><SSL:b>"
    assert process("a₳b") == "a<SSL:b>"
    assert process("a₳bc") == "a<SSL:b>c"
    assert process("m₳em₳E") == "m<SSL:e>m<SSL:E>"
    assert process("\\`") == "834**"
