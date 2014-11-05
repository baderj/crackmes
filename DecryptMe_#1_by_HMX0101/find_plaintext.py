import struct
import re

def get_freq():
    frequencies = {}
    with open("ascii_frequencies.txt", "r") as r: 
        for f in r:
            m = re.search("(\d+)\s.*\(\s*([\d.]+)", f)
            if m:
                frequencies[int(m.group(1))] = float(m.group(2))
    return frequencies

def rate_plaintext(plaintext, freq):
    score = 1
    for s in plaintext:
        score *= freq.get(ord(s),0)
    return score

def read_file(path):
    data = []
    with open(path, 'rb') as r:
        while True:
            dat = r.read(1)
            if dat != "" and len(dat):
                data.append(struct.unpack('B',dat)[0])
            else:
                return data

freq = get_freq()

c = read_file('cc')
c_len = 0x1E

best_rating = 0
for serial in range(0,1000):
    plaintext = ""
    for i in range(c_len):
        var1 = c_len 
        ea = c[i]
        c_minus_a = ea - 0x2644
        ea = 2*(c_minus_a)
        var1 += ea
        c_minus_a ^= 0x0DEAD
        var1_old = var1
        var1 = var1//2
        if var1:
            var1 += (var1_old % 2)

        s = serial + 10
        c_minus_a += s
        var1 += 0x1337
        s = serial
        s *= 2

        edx = c_minus_a - s
        c_minus_a = edx ^ serial
        edx = c_minus_a*serial
        var1 -= edx

        for j in range(1,37):
            eax = 0xFF - (j-1) - 10*((j-1)//6)
            eax *= 2
            var1 ^= eax
            c_minus_a ^= eax
            eax = (var1 // j)
            var1 = eax
        var1 += 0xAB
        c_minus_a -= 0x100
        eax = c_minus_a
        eax += 0xDEAD
        var1 *= eax
        var1 = 0
        c_minus_a += var1
        plaintext += chr(c_minus_a & 0xFF)

    rating = rate_plaintext(plaintext, freq)
    if rating > best_rating:
        print("new best rating {} for serial {} and plaintext:\n{}".format(
            rating, serial, plaintext))
        best_rating = rating
