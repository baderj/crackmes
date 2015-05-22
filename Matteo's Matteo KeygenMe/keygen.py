import random
import sys


def keygen(name):

    def get_int_from_string(s):
        val = 0
        for x in s[::-1]:
            val <<= 8
            val += ord(x)
        return val


    def get_str_from_int(val):
        s = ""
        for i in range(4):
            s += chr(val & 0xFF)
            val >>= 8

        return s 

    def rol(val, places):
        shift = places % 32;
        val = (val << shift)  + (val >> (32-shift))
        val &= 0xFFFFFFFF
        return val

    def ror(val, places):
        shift = places % 32;
        val = (val >> shift)  + (val << (32-shift))
        val &= 0xFFFFFFFF
        return val

    def make_alphanumeric(txt_codes):
        for i in range(len(txt_codes)):
            c = 37 
            while not chr(txt_codes[i]).isalnum():
                txt_codes[i] += c
                c += 1
                txt_codes[i] &= 0xFF
                c &= 0xFF
        return txt_codes

    def random_alphanumeric(l):
        return ''.join(random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), l))

    def hash1(line):
        eax = get_int_from_string(line[:4])
        eax += get_int_from_string(line[4:8])
        ecx = get_int_from_string(line[8:12])
        eax = rol(eax, ecx & 0xFF)
        ecx = get_int_from_string(line[12:16])
        eax = ror(eax, ecx & 0xFF)
        ecx = get_int_from_string(line[16:20]) 
        eax ^= ecx
        return eax

    def find_line3_seed1(line1, line3):
        #valid_seed1 = [0x1a01234, 0x41a01234, 0x81a01234, 0xc1a01234]
        valid_seed1 = [0x1a01234, 0x41a01234, 0xc1a01234]
        eax = hash1(line3)
        edx = hash1(line1)
        eax ^= edx
        for s in valid_seed1:
            diff = eax ^ s
            ecx = get_int_from_string(line3[16:20])
            ecx ^= diff 
            new_str = get_str_from_int(ecx)
            if new_str.isalnum():
                return line3[0:16] + new_str
        return None


    def find_line3_seed2():
        line3 = random_alphanumeric(20)
        valid_seed2 = 0x6f445a ^ 0x210e
        s = get_str_from_int(valid_seed2)[:3]
        line3 = line3[0:9] + s + line3[12:]
        return line3


    """
        check if name is alphanumeric, crackme won't accept other names
    """
    if not name.isalnum():
        print("The name must be alphanumeric")
        return

    if not 3 <= len(name) <= 20:
        print("Name too long or too short")
        return


    """
        generate second line from name
    """
    line1 = name 
    line1_len = len(line1)
    line1_codes = [ord(c) for c in line1]
    line1_codes[0] ^= line1_len ^ 0x5c

    i = 1
    j = line1_len-1
    while i < j:
        line1_codes[i] ^= line1_codes[j]
        i += 1
        j -= 1

    i = (line1_len-1)//2 + 1
    c = line1_codes[0]
    for i in range(i, line1_len):
        line1_codes[i] ^= c
        c += 1

    x = make_alphanumeric(line1_codes)
    line2 = ''.join([chr(xx) for xx in x])

    """
        semi brute force valid third line
    """
    while True:
        line3 = find_line3_seed2()
        line3 = find_line3_seed1(line1, line3)
        if line3:
            break

    with open("TheKey.k", "wb") as w:
        w.write("{}\r\n".format(line1))
        w.write("{}\r\n".format(line2))
        w.write("{}".format(line3))

keygen(sys.argv[1])
    
