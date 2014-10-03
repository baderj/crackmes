import math
def quad(a,b,c):
    d = b**2-4*a*c # discriminant

    if d < 0:
        return None 
    elif d == 0:
        x = (-b+math.sqrt(b**2-4*a*c))/2*a
        return x
    else:
        x1 = (-b+math.sqrt((b**2)-(4*(a*c))))/(2*a)
        x2 = (-b-math.sqrt((b**2)-(4*(a*c))))/(2*a)
        return [x1,x2]

x = 4278967296
for offset in range(10):
    res = quad(4,-16000,-x - offset*(2**32))
    if int(res[0]) == res[0]:
        print("solution: {}, {}".format(res[0], hex(int(res[0])) ))
    if int(res[1]) == res[1]:
        print("solution: {}, {}".format(res[1], hex(int(res[1])) ))


