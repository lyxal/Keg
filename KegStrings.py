#Object strings
''' There are four types of object strings:
 - (N)ew Object
 - (C)onvert Type
 - (M)ethod
 - (P)ython code

 This are in the form of

 `@[Letter]|[Information];`


 `N` object strings can create:

 - Stacks (`@N|[]`, `@N|[1, 2, 3];`)
 - Strings (`@N|"";`)
 - Files (`@N|file(addr);`)
 - Websocket Instances (`@N|https://addr;")
 - Other objects (`@N|obj`)

 `C` object strings can:

 - Convert one type to another
 - Actually, that's it
 - `@C|t;`  t = type to convert

 `M` object strings can:

 - Call functions of the objects on the stack

 `P` object strings can:
 - Run raw python
'''

def obj_str_extract(string):
    
    import re
    pobj = re.compile(r"`@(?P<type>[NCMP])\|(?P<data>.+);`")
    mobj = pobj.match(string)

    if mobj:
        str_type, obj_data = mobj.groups()
        if str_type == "N": #New Object
            return eval(obj_data)

        if str_type == "C":
            return obj_data

        if str_type == "P":
            exec(obj_data)
    
    else:
        return string




if __name__ == "__main__":
    print(obj_str_extract("`09;`"))
    

 
