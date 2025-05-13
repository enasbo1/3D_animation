
def somme(*args):
    n = args[0]
    a = False
    for i in args:
        if a:
            n+=i
        a = True
    return n