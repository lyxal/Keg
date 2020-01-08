#The Keg Preprocessor
STRING_CHARS = "`¶“‘«„"

def process(string):
    final = ""
    string_mode = [False, ""]
    escaped = False
    comment = False
    ssl_reference = [False, ""]
    
    for char in string:
        if string_mode[0]:
            if escaped:
                final += char
                escaped = False
                continue
            
            elif char == "\\":
                escaped = True
                final += char
                continue
            else:
                if char == string_mode[1]:
                    string_mode = [False, ""]
                final += char
                continue
        
        if char in STRING_CHARS:
            string_mode = [True, char]
            final += char
            continue
            
        if escaped:
            final += char
            escaped = False
            continue
        
        if char == "\\":
            escaped = True
            final += char
            continue
        
        if char == "₳":
            ssl_reference = [True, ""]
            continue

        if char == "\n" and comment:
            comment = False
        
        if ssl_reference[0] and len(ssl_reference[1]) != 2:
            ssl_reference[1] += char
            if len(ssl_reference[1]) == 2:
                ssl_reference[0] = False
                if ssl_reference[1] in ssls:
                    final += ssls[ssl_reference[1]]
                else:
                    final += f"<SSL:{ssl_reference[1]}>"
                ssl_reference[1] = ""
            continue
        
        if char == "∑":
            final += "(!;|"
            continue
        
        if char == "⑳":
            final += "{!|"
            continue

        if char == "#":
            comment = True
        
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

ssls = {
    "0a" : "`0123456789abcdefghijklmnopqrstuvwxyz`",
    "0b" : "`0123456789`",
    "0c" : "`abcdefghijklmnopqrstuvwxyz`"
}
        
if __name__ == "__main__":
    assert process("₳0a") == "<SSL:0a>"
    assert process("₳0a₳0b") == "<SSL:0a><SSL:0b>"
    assert process("a₳0b") == "a<SSL:0b>"
    assert process("a₳0bc") == "a<SSL:0b>c"
    assert process("m₳0em₳0E") == "m<SSL:0e>m<SSL:0E>"       
