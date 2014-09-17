import argparse

def double_reverse(string):
    mapping = [str(c) for c in [2,7,6,1,8,4,5,3,9,0]]
    s = string.upper()
    r = ""
    for c in s:
        if "0" <= c <= "9":
            r += mapping[int(c)]
        else:
            r += c
    return r

def keygen(user):
    if len(user) < 3:
        return("ERROR: user needs at least 3 characters")
    if len(user) > 16:
        return("ERROR: user has more than 16 characters")

    v5 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    check_var = -1
    four_bytes = 2**32
    lower, upper = 0, 0
    for i1, u in enumerate(user):
        ua = ord(u)
        lower += i1*(lower // (i1 + 8) + i1*ua)
        upper += (lower // four_bytes)
        lower %= four_bytes
        upper += ua 
    if lower < 1000:
        lower = lower**2

    v1 = len(user)
    j = upper
    j = j ^ v1
    j = (15*j + 1)//16
    while j >= 36:
        j -= 7

    valid_serial = ""
    for k in range(32):
        if not k or k % 7: 
            flag = (33 % (k + 2) and k % 4)
            if flag: 
                index = lower // (35 - k) 
            else:
                index = lower // (k + j) 
            index += 1337
            index = lower // index
            if flag:
                limit = 37
                index = index % (k + 1)
            else:
                limit = 34
                index = index ^ (k + 1) 
            index = (15*index + 1) // (j//2 + 1)
            if check_var != -1 and check_var == index:
                index *=2
            while index >= limit:
                index -= 2
            while index < 0:
                index += 2
            valid_serial += double_reverse(v5[index])
            check_var = index
        else:
            valid_serial += "-"

    return valid_serial

            

if __name__=="__main__":
    parser = argparse.ArgumentParser("Keygen")
    parser.add_argument("user")
    args = parser.parse_args()
    user = args.user
    serial = keygen(user)
    print("user:   {}".format(user))
    print("serial: {}".format(serial))
