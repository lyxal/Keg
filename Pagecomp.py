#utf-8
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
chars += "²ⁿ║ṡ⟰⟱ ⟷"

unicode = "Ï§∑¿∂•ɧ÷¡Ëė≬ƒß‘“"
unicode += "„«®©ëλº√₳¬≤Š≠≥Ėπ"
unicode += " !\"#$%&'()*+,-./"
unicode += "0123456789:;<=>?"
unicode += "@ABCDEFGHIJKLMNO"
unicode += "PQRSTUVWXYZ[\\]^_"
unicode += "`abcdefghijklmno"
unicode += "pqrstuvwxyz{|}~ø"
unicode += "¶\n\t⊂½‡™±¦→←↶↷"
unicode += "✏█↗↘□²ⁿ║ṡ⟰⟱⟷"
unicode += "ℤℝ⅍℠א∀≌᠀⊙᠈"


for n in range(127234, 127243): unicode += chr(n)

print(chars, len(chars))
print(len(unicode))

print(set(unicode) - set(chars))
