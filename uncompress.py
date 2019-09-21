#utf-8
#The Uncompressor
from Word_List import *
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
chars += "•™÷‡∞"
def Uncompress(source):
    result = ""
    string_type = ""
    temp = {"type" : None, "data" : ""}
    cont = False
    
    for char in source:
        if cont:
            temp["data"] += char
            cont = False
            continue
        if string_type != "":
            if char is string_type:
                string_type = ""
                result += standard(temp)
                temp = {"type" : None, "data" : ""}
            else:
                temp["data"] += char

        elif char == "\\":
            temp["data"] += char
            cont = True
            continue

        elif char in "`¶‘“«„":
            string_type = char
            #temp["data"] += char
            temp["type"] = char

        else:
            result += char

    if temp["type"] is None:
        result += temp["data"]

    return result

def standard(string):
    result = "`"
    escaped = False
    #print(string["type"])
    
    if string["type"] == "`":
        code = ""
        for char in string["data"]:
            if escaped:
                escaped = False
                continue
            elif char == ";":
                if len(code) == 2:
                    result += f"<SCC:{code}>"
                else:
                    result += code + ";"

                code = ""
            elif char == "\\":
                escaped = True
                continue

            elif len(code) == 2:
                result += code[0]
                code = code[1] + char

            else:
                code += char
        result += code
    elif string["type"] == "¶":
        code = ""
        escaped = False
        for char in string["data"]:
            if escaped:
                escaped = False
                continue
            elif char == ";":
                if len(code) == 2:
                    result += f"<SCC:{code}>"
                    result += " "
                else:
                    result += code + ";"

                code = ""
            elif char == "\\":
                escaped = True
                continue

            elif len(code) == 2:
                result += code[0]
                code = code[1] + char

            else:
                code += char

    elif string["type"] == "\u2018":
        if len(string["data"]) % 2 != 0:
            string["data"] += " "

        #print(string["data"])
        for scc in [string["data"][i:i+2] for i in range\
                    (0, len(string["data"]), 2)]:
            result += f"<SCC:{scc}>"

    elif string["type"] == "“":
        if len(string["data"]) % 2 != 0:
            string["data"] += " "

        #print(string["data"])
        for scc in [string["data"][i:i+2] for i in range\
                    (0, len(string["data"]), 2)]:
            result += f"<SCC:{scc}>" + " "
            
    elif string["type"] == "«":
        codes, seps = string["data"].split("|")
        codes = [codes[i:i+2] for i in range(0, len(codes), 2)]

        if len(codes) > len(seps):
            seps += " "*(len(codes) - len(seps))


        for i in range(len(codes)):
            scc = codes[i]
            result += f"<SCC:{scc}>" + seps[i] + " "
    elif string["type"] == "„":
        codes, seps = string["data"].split("|")
        codes = [codes[i:i+2] for i in range(0, len(codes), 2)]

        if len(codes) > len(seps):
            seps += " "*(len(codes) - len(seps))


        for i in range(len(codes)):
            scc = codes[i]
            result += f"<SCC:{scc}>" + seps[i]
        

    return result + "`"

if __name__ == "__main__":
    assert (Uncompress("`Hello, World!`") == "`Hello, World!`")
    assert Uncompress("`ab;`") == "`<SCC:ab>`"
    assert Uncompress("¶ab;cd;¶") == "`<SCC:ab> <SCC:cd> `"
    assert Uncompress("123") == "123"
