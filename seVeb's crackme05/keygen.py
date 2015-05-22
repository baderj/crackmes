import string
import random

class NoChoices(Exception):
    pass

def random_serial():
    def random_crit(crit, valid_chars):
        candidates = filter(crit, valid_chars)
        if len(candidates) == 0:
            raise NoChoices("Can't satisfy {}".format(repr(crit)))
        return random.choice(candidates)

    ## Rock
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    minus = '-'
    valid_chars = [ord(o) for o in lowercase + uppercase + digits + minus]
    serial = [random.choice(valid_chars) for i in range(19)]

    ## Paper
    serial[8] = random_crit(lambda x: (x^serial[10]) <= 9, valid_chars)
    serial[5] = random_crit(lambda x: (x^serial[13]) <= 9, valid_chars)
    t1 = (serial[8] ^ serial[10]) + 48
    serial[3] = t1
    serial[15] = t1 
    t2 = (serial[5] ^ serial[13]) + 48
    serial[0] = t2 
    serial[18] = t2 

    ## Scissors
    serial[1] = random_crit(lambda x: x + serial[2] > 170, valid_chars)
    serial[16] = random_crit(lambda x: x + serial[17] > 170 and 
            serial[1] + serial[2] != x + serial[17],
            valid_chars)

    ## Cracker
    serial[4], serial[9], serial[14] = 45,45,45 

    return "".join([chr(c) for c in serial])

def create_serial():
    while True:
        try:
            return random_serial()
        except NoChoices:
            # 6.2 % chance of failure
            pass

print(create_serial())
