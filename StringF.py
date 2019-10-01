def custom_format(source):
    #Using the © format
    #first space after a © doesn't count and is removed.

    result = ""
    temp = ""
    escaped = False
    var_mode = False

    import string
    
    for char in source:
        if escaped:
            escaped = False
            result += char
            continue
            
        elif char == "\\":
            escaped = True
            result += char
            continue

        if var_mode:
            if char in string.ascii_letters:
                temp += char
                continue

            else:
                result += variables.get(temp, '©' + temp)
                temp = ""
                var_mode = False
                if char == " ":
                    continue

        if char == "©":
            var_mode = True
            continue

        result += char

    if var_mode:
        result += variables.get(temp, '©' + temp)
    return result


