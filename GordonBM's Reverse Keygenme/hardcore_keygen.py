"""Reverse key generator for GordonBM's Reverse Keygenme
   see http://www.crackmes.de/users/gordonbm/reverse_keygenme/ 
   (hardcore mode)"""
import argparse

ASCII_RANGE = [32, 126] 

def ran_values(length, values=None, pos=0, val=0):
    """get all potential random values for length as list """

    if values is None:
        values = set()
    if pos == length:
        values.add(val)
    else:
        xor = (2*pos) ^ 6
        pos += 1

        # case 1: rand is 0
        next_val = 9*val
        ran_values(length, values, pos, next_val)

        # case 2: rand is 1
        next_val = 3*(val*3 + xor)
        ran_values(length, values, pos, next_val)

    return sorted(values)

def guess_length(key):
    """get the best guess for the length of the message based on hardcoded 
       mean key lengths"""

    len_db = [0,2,5,9,16,23,33,44,56,72,90,110,132,156,182]
    len_msg = len(key)
    diffs = [abs(c-len_msg) for c in len_db]
    val, idx = min((val, idx) for (idx, val) in enumerate(diffs))
    return (idx, val)


def brute_force(crypt, msg_len, noises, pos=0, res=""):
    """brute-force potential messages

        Prints all potential messages (characters in ASCII_RANGE)

        Args:
            crypt: the key that should be reverse
            msg_len: the length of the message
            noises: the list of potential noise values for the given length

        Returns:
            nothing, prints all strings to stdout
    """
    for noise in noises:
        low, upp = (tmp + noise for tmp in ASCII_RANGE)
        for span in range(len(str(low)), len(str(upp))+1):
            digits = crypt[pos:pos+span]
            code = int(digits)
            if low <= code <= upp:
                msg_char = chr(code - noise)
                concat = res + msg_char
                if pos+span >= len(crypt):
                    if len(concat) == msg_len:
                        print(concat)
                    else:
                        pass # string does not match expected nr of chars
                else:
                    brute_force(crypt, msg_len, noises, pos+span, concat)

def crack(key):
    """crack the key"""
    msg_len, error = guess_length(key)
    print("message length is probably {}, (delta {})".format(msg_len, error))
    noise = ran_values(msg_len)
    print("there are {} different noise values".format(len(noise)))
    print("potential messages are:")
    brute_force(key, msg_len, noise)

if __name__ == "__main__":
    """ reverses keys like:
        142641551691142
        9247109931023928283286380308924708453882326686447837
    """
    parser = argparse.ArgumentParser(description="Hardcore Reverse Keygen")
    parser.add_argument('key', help="the key to be reversed")
    args = parser.parse_args()
    crack(args.key)

