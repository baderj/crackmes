import random

def digit_to_ascii(digit):
    s = 0
    for i in range(8):
        s += digit[i]*(1 << i)
    return chr(s)

def key_from_digits(digits):
    key = ""
    for d in digits:
        key += digit_to_ascii(d)
    return key

def calc_q(l):
    q = 0xBEED
    for i in range(l):
        q = (q*32 + 1) 
        q ^= 0x12345678
        q = q & 0xFFFFFFFF
    return q 

def get_equations(l):
    terms = [[] for i in range(32)]
    even_odd = 32*[0]
    for i in range(32):
        terms[i] = []

    for i in range(l):
        """ do the shl by 5 bl """
        terms = [[] for i in range(5)] + terms[:-5] 
        for j in range(8):
            """ the last bit of digl must be zero for ASCII """
            if j < 7:
                terms[j].append((i,j))

    """ q is the constant term """
    q = calc_q(l)
    for i in range(32):
        even_odd[i] ^= ((q & (1 << i) ) >> i)

    wanted = 0x0B528B18B
    for i in range(32):
        even_odd[i] ^= ((wanted & (1 << i) ) >> i)

    return terms, even_odd

def generate_key_with_given_length(l):
    terms, even_odd = get_equations(l)
    while True:
        digits = [8*[0] for i in range(l)]
        for d in digits:
            while True:
                for p in range(7):
                    d[p] = random.randint(0,1) 
                if digit_to_ascii(d).isalnum():
                    break
        for t, eo in zip(terms, even_odd):
            """ we can randomly pick all but one term """
            s = 0
            for i in range(len(t)-1):
                digit, place = t[i]
                digits[digit][place] = random.randint(0,1)
                s += digits[digit][place]

            digit, place = t[-1]
            digits[digit][place] = eo ^ s

        """ only return alpha numeric keys, try again if key isn't """
        key = key_from_digits(digits)
        if key.isalnum():
            return key

def generate_key_with_random_length():
    """ any length greater than 5 should do """
    l = random.randint(6,20)
    return generate_key_with_given_length(l)

for i in range(100):
    print(generate_key_with_random_length())
