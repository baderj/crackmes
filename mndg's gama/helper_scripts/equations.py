import random

serial = "123456"
edx = 0xBEED


def pattern(its):
    edx = 0xBEED
    for i in range(its):
        edx = (edx*32 + 1) 
        edx = edx
        edx ^= 0x12345678
        edx = edx & 0xFFFFFFFF
    return edx 

def equations(its, rel=False, asc=False):
    pat = pattern(its)
    equ = [[] for i in range(32)]
    even_odd = 32*[0]
    for i in range(32):
        equ[i] = []

    for i in range(its):
        equ = [[] for i in range(5)] + equ[:-5] 
        for j in range(8):
            if rel:
                ind = str("{}-{}".format("l", its-i))
            else:
                ind = i
            if not asc or j < 7:
                s = "s^{{{}}}_{{{}}}".format(ind, j)
                equ[j].append(s)

    for i in range(32):
        val = ((pat & (1 << i) ) >> i)
        equ[i].insert(0, str(val))

    wanted = 0x0B528B18B
    for i in range(32):
        val = ((wanted & (1 << i) ) >> i)
        equ[i] = " \oplus ".join(equ[i])
        equ[i] += " &\stackrel{!}{=} " + str(val) 

    print("$$\n\\begin{aligned}")
    for i in range(32):
        print("{}".format(equ[i]), end="")
        if i%4 == 3:
            print("\\\\")
        else:
            print(", & ", end="")

    print("\\end{aligned}\n$$")


""" any length greater than 5 should do """
l = 7
equations(l, rel=True, asc=True)
