#Coherse.py

import textwrap

code_page = "set me in Keg.py"

class char():
    def __init__(self, what):
        self.v = str(what)

    def __str__(self):
        return self.v

    def __int__(self):
        return _ord(self.v)

def split_list(list_obj: list, n: int) -> list:
    return [list_obj[i:i+n] for i in range(0, len(list_obj), n)]

def sub_strings(source: str, subtractant: str) -> str:
    result = source
    if len(subtractant) == 1:
        return source.replace(subtractant, "", 1)
    for char in subtractant:
        result = sub_strings(result, char)
    return result

def multiply(lhs: str, rhs: str) -> list:
	result = []
	for char in lhs:
		for char_2 in rhs:
			result.append(char + char_2)
	return result

def list_mult(lhs: list, rhs: str) -> list:
    result = []
    for item in lhs:
            result.append(operate(item, rhs, "*"))
    return result

def list_divide(lhs: list, rhs: str) -> list:
    result = []
    for item in lhs:
        result.append(operate(item, rhs, "/"))
    return result

def special_divide(lhs: list, rhs: list) -> list:
    result = []
    for item in lhs:
        for item_1 in rhs:
            result += operate(item, item_1, "/")
    return result


relations = {"Number": {
                    "Number": ["x + y", "x - y", "x * y", "x / y", "x % y"],
                    "Character": ["x + _ord(y.v)", "x - _ord(y.v)",
                                        "x * _ord(y.v)", "x / _ord(y.v)",
                                  "x % _ord(y.v)"],
                    "String": ["str(x) + y", "str(x).replace(y, '')",
                                 "y * x", "textwrap.wrap(y, x)",
                               "textwrap.wrap(y, x)[-1]"],
                    "Stack": ["y + [x]", "y.remove(x)", "y * x",
                                "split_list(y, x)", "split_list(y, x)[-1]"]
                    },

             "Character": {

                     "Number": ["y + _ord(x.v)", "_ord(x.v) - y",
                                        "y * _ord(x.v)", "_ord(x.v) / y",
                                "_ord(x.v) % y"],

                     "Character" : ["_ord(x.v) + _ord(y.v)",
                                    "_ord(x.v) - _ord(y.v)",
                                    "_ord(x.v) * _ord(y.v)",
                                    "_ord(x.v) / _ord(y.v)",
                                    "_ord(x.v) % _ord(y.v)"],

                     "String" : ["x.v + y", "y.replace(x.v, '')",
                                 "y * _ord(x.v)", "y.split(x.v)",
                                 "y.split(x.v)[-1]"],

                     "Stack" : ["y + [x.v]", "y.remove(x.v)", "y * _ord(x.v)",
                                "split_list(y, _ord(x.v))",
                                "split_list(y, _ord(x.v))[-1]"]
                    },

             "String": {
                 "Number" : ["x + str(y)", "sub_strings(x, str(y))", "x * y",
                             "textwrap.wrap(x, y)", "textwrap.wrap(x, y)[-1]"],
                 "Character" : ["x + y.v", "sub_strings(x, y.v)",
                                "x * _ord(y.v)", "x.split(y.v)",
                                "x.split(y.v)[-1]"],

                 "String": ["x + y", "sub_strings(x, y)", "multiply(x, y)",
                            "x.split(y)", "x.split(y)[-1]" ],

                 "Stack": ["y + [x]", "y.remove(x)", "list_mult(y, x)",
                           "list_divide(y, x)", "list_divide(y, x)[-1]" ]
                 },

             "Stack": {
                 "Number": ["x + [y]", "x.remove(y)", "x * y",
                            "split_list(x, y)", "split_list(x, y)[-1]"],

                 "Character": ["x + [y.v]", "x.remove(y.v)", "x * _ord(y.v)",
                               "split_list(x, _ord(y.v))",
                               "split_list(x, _ord(y.v))[-1]"],

                 "String": ["x + [y]", "x.remove(y)", "list_mult(x, y)",
                            "list_divide(x, y)", "list_divide(x, y)[-1]"],

                 "Stack": ["x + y", "list(set(x) - set(y))",
                           "[list(pair) for pair in zip(x, y)]",
                           "special_divide(x, y)", "special_divide(x, y)[-1]"]}
             }


second = {
"Number" : {
        "Number" : ["x < y", "x > y", "x <= y", "x >= y", "x == y", "x != y",
        "x < y and x > 0"],
        "Character" : ["x < _ord(y.v)", "x > _ord(y.v)", "x <= _ord(y.v)",
         "x >= _ord(y.v)", "x == _ord(y.v)", "x != _ord(y.v)",
        "x < _ord(y.v) and x > 0"],
        "String" : ["str(x) < y", "str(x) > y", "str(x) <= y", "str(x) >= y",
         "str(x) == y", "str(x) != y",
        "str(x) < y and str(x) > '0'"],
        "Stack": ["1", "1", "1", "1", "1", "1", "1"]
    },
"Character" : {
        "Number": ["_ord(x.v) < y", "_ord(x.v) > y", "_ord(x.v) <= y",
         "_ord(x.v) >= y", "y == _ord(x.v)", "y != _ord(x.v)",
        "_ord(x.v) < y and y > 0"],
        "Character" : ["_ord(x.v) < _ord(y.v)", "_ord(x.v) > _ord(y.v)",
         "_ord(x.v) <= _ord(y.v)", "_ord(x.v) >= _ord(y.v)",
          "_ord(x.v) == _ord(y.v)", "_ord(x.v) != _ord(y.v)",
        "_ord(x.v) < _ord(y.v) and _ord(x.v) > 0"],
        "String": ["x.v < y", "x.v > y", "x.v <= y", "x.v >= y", "x.v == y",
         "x.v != y",
        "x.v < y and x.v > '0'"],
        "Stack": ["1", "1", "1", "1", "1", "1", "1"]
    },

"String" : {
    "Number" :  ["str(y) > x", "str(y) < x", "str(y) >= x", "str(y) <= x",
             "str(y) == x", "str(x) != y",
            "str(y) > x and y > '0'"],
    "Character" : ["y.v > x", "y.v < x", "y.v >= x", "y.v <= x", "y.v == x",
     "y.v != x",
    "y.v > x and y.v < '0'"],
    "String" : ["x < y", "x > y", "x <= y", "x >= y", "x == y", "x != y",
    "x < y and x > 0"],
    "Stack": ["1", "1", "1", "1", "1", "1", "1"]
    },

"Stack" : {
        #TODO: Replace everything here with something more reasonable
        "Number" : ["1", "1", "1", "1", "1", "1", "1"],
        "Character": ["1", "1", "1", "1", "1", "1", "1"],
        "String": ["1", "1", "1", "1", "1", "1", "1"],
        "Stack": ["1", "1", "1", "1", "1", "1", "1"],
    }
}

def _type(item):
    if type(item) in [float, int]:
        return "Number"

    if type(item) == char:
        return "Character"

    if type(item) == str:
        return "String"
    return "Stack"

def operate(lhs, rhs, op):
    from Stackd import Stack
    tLhs, tRhs = _type(lhs), _type(rhs)
    choices = relations[tLhs][tRhs]
    expr = choices["+-*/%".index(op)]
    x, y = lhs, rhs

    if type(lhs) is Stack:
        x = eval(str(lhs))
    if type(rhs) is Stack:
        y = eval(str(rhs))

    z = eval(expr)
    if type(z) is list:
        z = Stack(z)
    return z


def do_compare(lhs, rhs, op):
    tLhs, tRhs = _type(lhs), _type(rhs)
    choices = second[tLhs][tRhs]
    expr = choices["<>≤≥=≠≬".index(op)]
    x, y = lhs, rhs

    return 1 if eval(expr) else 0

def _ord(character):
    if str(character) in code_page:
        return code_page.index(str(character))
    return ord(character)

def _chr(i):
    if code_page:
        if i == 10:
            return "\n"
        if 0 < i < 256:
            return code_page[i]
        return chr(i)
    else:
        return chr(i)
