#utf-8
#The Uncompressor
from Word_List import *
import KegStrings
sccs = generate_list()

chars = "0123456789"
chars += "abcdefghij"
chars += "klmnopqrst"
chars += "uvwxyzABCD"
chars += "EFGHIJKLMN"
chars += "OPQRSTUVWX"
chars += "YZ!@#$%^&*"
chars += "()_+~[]{}:"
chars += "<>?,./\"'¿"
chars += "¿∂⊂ø®©ëλº√"
chars +=  "₳¬≤Š≠≥Ėπ§∑"
chars += "•™÷‡∞\t\n½±"
chars += "¦ė≬ƒßɧË-=Ï¡"
chars += "→←↶↷✏█↗↘□"
chars += "²ⁿ║ṡ⟰⟱⟷"
chars += "ℤℝ⅍℠א∀≌᠀⊙᠈⅀"
chars += "ȦƁƇƉƐƑƓǶȊȷǨȽƜƝǪǷɊƦȘȚȔƲɅƛƳƵ" #push'n'print
chars += "☭"
chars += "⬠⬡⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯"
chars += "⯑"
chars += "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆"
chars += "↫"

for n in range(127234, 127243): chars += chr(n)

def _ord(char):
    if char in chars:
        return chars.find(char)
    return ord(char) + 256

def numberToBase(n, b): #https://stackoverflow.com/a/28666223/9363594
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

class STRINGS:
    STANDARD = "`"
    STANDARD_SPACED = "¶"
    SCC = "‘"
    SCC_SPACED = "“"
    SPECIAL = "„"
    SPECIAL_SPACED = "«"
    NONE = ""
    STRINGS = {STANDARD, STANDARD_SPACED, SCC, SCC_SPACED, SPECIAL,
               SPECIAL_SPACED}

def Uncompress(source):
    parts = []
    temp = ""
    string_type = STRINGS.NONE
    escaped = False

    for char in source:
        if escaped:
            temp += char
            escaped = False
            continue

        if string_type == STRINGS.NONE:
            if char in "`¶‘“„«":
                string_type = char
                parts.append(temp)
                temp = ""
            else:
                parts.append(char)

        elif char == string_type:
            import KegStrings
            item = KegStrings.obj_str_extract("`" + temp + "`")
            if type(item) != str: #The object is an object string
                parts.append("`" + temp + "`")
            else:
                parts.append("`" + to_standard(temp, string_type) + "`")
            string_type = STRINGS.NONE
            temp = ""

        elif char in STRINGS.STRINGS - {string_type}:
            temp += "\\" + char

        elif char in ["'", '"']:
            temp += "\\" + char

        elif char == "\\":
            temp += char
            escaped = True

        else:
            temp += char

    return "".join(parts)

def to_standard(source, s_type):
    result = ""
    compression_code = ""
    escaped = False

    if type(KegStrings.obj_str_extract(source)) is not str:
        return source

    if s_type in [STRINGS.STANDARD, STRINGS.STANDARD_SPACED]:
        spaces = " " * [STRINGS.STANDARD, STRINGS.STANDARD_SPACED].index(s_type)
        for char in source:
            if escaped:
                compression_code += char
                escaped = False
                continue

            elif char == "\\":
                escaped = True
                continue
            
            if char == ";":
                result += f"{get_scc(compression_code)}{spaces}"
                compression_code = ""
            else:
                compression_code += char
                if len(compression_code) > 2:
                    result += compression_code[0]
                    compression_code = compression_code[1:]

    elif s_type in [STRINGS.SCC, STRINGS.SCC_SPACED]:
        spaces = " " * [STRINGS.SCC, STRINGS.SCC_SPACED].index(s_type)

        if len(source) % 2: source += " "
        codes = [source[i] + source[i + 1] for i in range(0, len(source),
                                                          2)]
        for code in codes:
            result += f"{get_scc(code)}{spaces}"

    elif s_type in [STRINGS.SPECIAL, STRINGS.SPECIAL_SPACED]:
        spaces = " " * [STRINGS.SPECIAL, STRINGS.SPECIAL_SPACED].index(s_type)
        codes, joins = source.split("|", 1)

        codes = [codes[i] + codes[i + 1] for i in range(0, len(codes),
                                                          2)]

        if len(joins) < len(codes):
            for _ in range(len(codes) - len(joins)):
                joins += " "

        for i in range(len(codes)):
            result += f"{get_scc(codes[i])}{joins[i]}{spaces}"



    if compression_code:
        result += compression_code

    if s_type in [STRINGS.STANDARD_SPACED,
                  STRINGS.SCC_SPACED,
                  STRINGS.SPECIAL_SPACED] and result[-1] == " ":
        result = result[:-1]

    return result

def get_scc(code):
    index = _ord(code[1]) + (len(chars) * _ord(code[0]))
    return sccs[index]

def keg_to_utf8(code):
    # Taken from the old 05AB1E interpreter
    processed_code = ""
    for c in code:
        processed_code += chars[c]

    return processed_code

def utf8_to_keg(code):
    # Taken from the old 05AB1E interpreter
    processed_code = ""
    for c in code:
        processed_code += chr(chars.index(c))

    return processed_code

if __name__ == "__main__":
    while 1:
        term = input("Enter a search term: ")
        if term in sccs:
            x = sccs.index(term)
            numbers = numberToBase(x, 248)
            code = "".join([chars[i] for i in numbers])
            print(code, numbers)
        else:
            print(-1)
