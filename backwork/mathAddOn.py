
def somme(*args):
    n = args[0]
    a = False
    for i in args:
        if a:
            n+=i
        a = True
    return n


def approach(a: float, b: float, speed: float) -> float:
    if a < b:
        return min(a + speed, b)
    elif a > b:
        return max(a - speed, b)
    else:
        return a
