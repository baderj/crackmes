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

def read_file(path):
    data = []
    with open(path, 'rb') as r:
        while True:
            dat = r.read(1)
            if dat != "" and len(dat):
                data.append(struct.unpack('B',dat)[0])
            else:
                return data


def decrypt(cipher, key):
    result = len(cipher)*[None]
    varc = 1
    for i, c in enumerate(cipher): 
        result[i] = ( (key[i % len(key)]*varc) ^ c ) & 0xFF
        varc += c
    return result


def list_to_string(l):
    return "".join([chr(c) if 32 <= c <= 126 else "?" for c in l])

def best_key(cipher, weights, l, i, freq):
    wa = weights[i::l]
    ca = cipher[i::l]
    best_score = -1
    best_key = None
    for k in range(32, 126):
        tmp = []
        for w, c in zip(wa, ca):
            tmp.append(((w*k) ^ c) & 0xFF)
        score = 1
        for x in tmp:
            score *= freq.get(int(x),0)
        if score > best_score:
            best_score = score
            best_key = k
    return best_key, best_score

def crack(cipher):
    freq = get_freq()
    weights = len(cipher)*[None]
    s = 1
    for i, c in enumerate(cipher): 
        weights[i] = s  
        s += c
        s = s & 0xFF

    overall_best_score = 0
    overall_best_key = None
    for key_len in range(2,len(cipher)):
        score_sum = 0
        key = key_len*[None]
        for i in range(key_len):
            key[i], score = best_key(cipher, weights, key_len, i, freq)
            score_sum += score
        
        if score_sum > overall_best_score:
            overall_best_score = score_sum
            overall_best_key = key
    return overall_best_key


for nr in ["A", "B", "C"]:
    cipher = read_file("cipher" + nr)
    key = crack(cipher)
    msg = decrypt(cipher, key) 
    print("cipher {}\n========\nkey: {}\nplaintxt: {}\n\n".format(nr, 
        list_to_string(key), list_to_string(msg)))
    
key_txt = "SU5sc0tFUORhp4JziuOpfHspW"
print("The best key is obviously {}".format(key_txt))
key = [ord(k) for k in key_txt]


for nr in ["A", "B", "C"]:
    cipher = read_file("cipher" + nr)
    msg = decrypt(cipher, key) 
    print("cipher {}\n========\nplaintxt: {}\n\n".format(nr, 
        list_to_string(msg)))

