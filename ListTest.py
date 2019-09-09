list_obj = []
def f(n):
    x = list_obj
    for i in range(n):
        x.append(i)

print(list_obj)
f(9)
print(list_obj)
