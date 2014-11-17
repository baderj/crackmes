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

freq = get_freq()
ciphertext = [0x74,0x66,0x6f,0x6f,0xc3,0x47,0x6c,0x6d,0x66,0xc2,0xaf,
        0xc3,0x60,0x6c,0x6d,0x64,0x71,0x82,0x17,0x16,0x6f,0x82,0x17,
        0x6a,0x6c,0x6d,0x70,0xc2,0xc2,0xc2]

best_rating = 1
for key in range(0,256):
    plaintext = ""
    for c in ciphertext: 
        plaintext_char = c - 0x2644
        plaintext_char ^= 0x0DEAD
        plaintext_char += 10
        plaintext_char -= key 
        plaintext_char ^= key
        plaintext += chr(plaintext_char & 0xFF)

    rating = rate_plaintext(plaintext, freq)
    if rating >= best_rating:
        print("best rating {} for key {} and plaintext:\n{}".format(
            rating, key, plaintext))
        best_rating = rating
