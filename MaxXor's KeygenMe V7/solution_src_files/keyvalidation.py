def string_to_ascii_codes(string, zerobytes=0):
    return [ord(c) for c in string] + zerobytes*[0]

def pseudo_upper(string):
    mapping = [str(c) for c in [5,7,4,1,0,9,8,3,2,6]]
    s = string.upper()
    r = ""
    for c in s:
        if "0" <= c <= "9":
            r += mapping[int(c)]
        else:
            r += c
    return r

def validate(user, serial):
    if len(user) < 3:
        return("ERROR: user needs at least 3 characters")
    if len(user) > 16:
        return("ERROR: user has more than 16 characters")
    if len(serial) != 32:
        return("ERROR: serial needs to have 32 characters")

    v5 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    validity = 0
    check_var = -1
    this_is_var1 = 0
    byte_403020 = 1

    serial = pseudo_upper(serial)
    
    user_ascii = string_to_ascii_codes(user)
    serial_ascii = string_to_ascii_codes(serial)

    four_bytes = 2**32
    lower = 0
    upper = 0
    for i1, ua in enumerate(user_ascii):
        lower += i1*(lower // (i1 + 8) + i1*ua)
        upper += (lower // four_bytes)
        lower %= four_bytes
        upper += user_ascii[i1] 
    if lower < 1000:
        lower = lower**2

    v1 = len(user)
    j = upper
    j = j ^ v1
    j = (15*j + 1)//16
    while j >= 36:
        j -= 7


    ok_flag = False
    valid_serial = ""
    for k in range(32):
        if not k or k % 7: # all except k=7, k=14, k=21
            if 33 % (k + 2) and k % 4:
                # E1A
                feight = lower // (35 - k) + 1337
                feight = lower // feight
                feight = feight % (k + 1)
                feight = (15*feight + 1) // (j//2 + 1)
                serial_ascii[k] = ord(pseudo_upper(serial[k]))
                serial = "".join([chr(c) for c in serial_ascii]) 
                if check_var != -1 and check_var == feight:
                    feight *=2
                while feight > 36:
                    feight -= 2 
                while feight < 0:
                    feight += 2
            else:
                feight = lower // (k + j) + 1337
                feight = lower // feight
                feight = feight ^ (k + 1) 
                serial_ascii[k] = ord(pseudo_upper(serial[k]))
                serial = "".join([chr(c) for c in serial_ascii]) 
                feight = (15*feight + 1) // (j//2 + 1)
                if check_var != -1 and check_var == feight:
                    feight *=2
                while feight >= 34:
                    feight -= 2 
                while feight < 0:
                    feight += 2
            check_var = feight
            ok_flag = (serial[k] == v5[feight])
            if not ok_flag: 
                break
            validity += 1
        else:
            ok_flag = (serial[k] == "-")
            valid_serial += "-"
            if not ok_flag: 
                break
            ok_flag = True
            validity += 1

    byte_403020 = 0
    if ok_flag:
        print("valid serial")
    else:
        print("invalid serial")
