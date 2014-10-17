import itertools
from datetime import datetime
import struct 
import zipfile

def read_file(path):
    data = []
    with open(path, 'rb') as r:
        while True:
            dat = r.read(1)
            if dat != "":
                data.append(struct.unpack('B',dat)[0])
            else:
                return data

def write_file(path, data):
    with open(path, 'wb') as w:
        for d in data:
            w.write(struct.pack('c', chr(d)))

def reverseTransformByte(gc_before, gc_after, nr_iterations):
    valid_mc = []
    gc = gc_before 
    for m in range(256):
        gc = gc_before 
        gc = TransformByte(gc, m, nr_iterations)
        if gc == gc_after:
            valid_mc.append(m)
    return valid_mc

def TransformByte(g, m, nr_iterations):
    shuffle = [0x8, 0xA, 0x0, 0x1, 0x9, 0xC, 0xF, 0x3, 0x6, 0x2, 0xD, 0xE, 
                                                        0x4, 0x2, 0x5, 0x7]
    for i in range(nr_iterations*5):
        nr = g
        g = (shuffle[(nr // 16)] * 0x10) + shuffle[(nr % 16)]
        g = (g + m) & 0xFF
    return g


def PotentialMasterKeys(plaintext, ciphertext, nr_iterations):
    generate_key = [a ^ b for a,b in zip(plaintext, ciphertext)] 
    keys = []
    for gc in generate_key:
        r = reverseTransformByte(0x0, gc, nr_iterations)
        keys.append(r)
    return keys

def decrypt(c, m, nr_iterations):
    g = []
    for mc in m: 
        g.append(TransformByte(0x00, mc, nr_iterations))
    return [gg ^ cc for gg, cc in zip(g, c)]


def print_key_combinations(keys):
    for k in keys:
        if len(k) == 0:
            print "XX ",
        elif len(k) == 1:
            print "{:02x} ".format(list(k)[0]),
        else:
            print "{{{}}} ".format(",".join(["{:02x}".format(h) for h in k])),
    print("")

def is_part_of_ascii_filename(s):
    """ two cases:
        - there is a dot in s -> all chars upto to dot plus one (extension)
          are ASCII chars
        - there is no dot in s -> all chars must be ASCII
    """
    if not '.' in s:
        dot_index = len(s)
    else:
        dot_index = s.index('.')
    return all(32 <= ord(c) <= 126 for c in s[:dot_index+2]) 


""" 
    Bytes 0-3: Local File Header Signature
"""
keys = []
p = [0x50, 0x4B, 0x03, 0x04]     # ZIP local file header signature
c = [0xad, 0x62, 0x1e, 0x10]     # First four bytes of ciphertext
keys += PotentialMasterKeys(p, c, 2)
print_key_combinations(keys)


""" 
    Bytes 4-5: Version Needed to Extract 
"""
p = [0x14, 0x00]     # ZIP local file header signature
c = [0x94, 0xa0]     # First four bytes of ciphertext
keys += PotentialMasterKeys(p, c, 2)
print_key_combinations(keys)


""" 
    Bytes 6-7: General Purpose Bit Flag   
"""
p = [0x00, 0x00]     # ZIP local file header signature
c = [0x17, 0xad]     # First four bytes of ciphertext
keys += PotentialMasterKeys(p, c, 2)
print_key_combinations(keys)


""" 
    Bytes 32-39 - File Name (from second character on)
"""
c = [0xb8, 0x4d, 0xd0, 0x7a, 0x4e, 0xf4, 0x12, 0xdd] # Bytes 32-37 of ciphertxt
valid_names = set()
for m in itertools.product(*keys):
    p = decrypt(c, m, 4)
    fn = "".join(chr(pp) for pp in p[0:8])
    if is_part_of_ascii_filename(fn):
        valid_names.add(fn)

for valid_name in valid_names:
    print("__{}".format(valid_name))
 

p = [ord(f) for f in "ADME.txt"]   # filename[2:] 
c = [0xb8, 0x4d, 0xd0, 0x7a, 0x4e, 0xf4, 0x12, 0xdd] # Bytes 32-37 of ciphertxt
keys2 = PotentialMasterKeys(p, c, 4)
keys_intersection = []

for k1, k2 in zip(keys, keys2):
    keys_intersection.append(set(k1) & set(k2))

print_key_combinations(keys_intersection)

"""
    Bytes 30-31: Start of Filename - "RE" 
"""
p = [ord(f) for f in "RE"]   # filename[:2]
c = [0xc1, 0x94] # Bytes 30-31 of ciphertxt
keys = PotentialMasterKeys(p, c, 3)
print_key_combinations(keys)

"""
    Bytes 12-13: File Last Modification Date
"""
# see msdostime.py
p = [0x30, 0x45] # Bytes 12-13: file last modification date
c = [0xb9, 0xcc] # Bytes 12-13 of ciphertxt
keys = PotentialMasterKeys(p, c, 2)
print_key_combinations(keys)

"""
    Bytes 28-29: Extra field length (m)
"""
c = [0xe9, 0x19]
for m in itertools.product(*keys):
    p = decrypt(c, m, 3)
    print([hex(mm) for mm in m], (p[0] << 8) + p[1])

"""
    Bytes 8-9: Compression method
"""
for cm in list(range(11)) + [12, 14, 18, 19, 97, 98]:
    p = [cm, 0x00] # Bytes 8-9: compression method 
    c = [0x81, 0x64] # Bytes 8-9 of ciphertxt
    keys = PotentialMasterKeys(p, c, 2)
    # print("compression method {}".format(cm))
    # print_key_combinations(keys)

    """
        Bytes 22-25: Uncompressed Size
    """

    keys = [[0x56],[0x3f,0x4f]] + keys # prepend masterkey bytes 6-7
    c = [0x4f, 0x31, 0xe9, 0x09]
    for m in itertools.product(*keys):
        p = decrypt(c, m, 3)
        size = (p[3]<<24) + (p[2]<<16) + (p[1]<<8) + p[3]
        if size < 360745*10:
            print("Compression {}, Key {}: {} Mega Bytes".format(cm, m, size/1024/1024.0))


"""
    Bytes 26-27: File Name Length (n)
"""

p = [len("README.TXT"), 0x0] # Bytes 26-27: file name length 
c = [0x40, 0xb1] # Bytes 26-27 of ciphertxt
keys = PotentialMasterKeys(p, c, 3)
print_key_combinations(keys)

from datetime import datetime
def dos_time_to_datetime(date, time):
    # little endian to big endian
    date = (date[1] << 8) + date[0]
    time = (time[1] << 8) + time[0]
    year = ((date & 0xFE00) >> 9) + 1980
    month = (date & 0x1E0) >> 5
    day = date & 0x1F
    hours = (time & 0xF800) >> 11
    mins = (time & 0x7E0) >> 5
    secs = (time & 0x1F) << 1

    return datetime(year, month, day, hours, mins, secs)

c = [0x2e, 0x7f] # Bytes 10,11 of cipher
for m in itertools.product(*keys): # should only be one combo
    time = decrypt(c, m, 2)
    print(dos_time_to_datetime([0x30, 0x45], time))

"""
    Brute-Forcing
"""

def DecryptFile(data, master_key):
    def GenerateKey(master_key, generate_key):
        for i, mc in enumerate(master_key):
            generate_key[i] = TransformByte(generate_key[i], mc, 1)

    g = 16*[0]
    GenerateKey(master_key, g)
    GenerateKey(master_key, g)
    plaintext = []
    for i in range(0, len(data), 16):
        for j in range(16):
            if i+j < len(data):
                plaintext.append(data[i+j] ^ g[j])
        GenerateKey(master_key, g)
    return plaintext

keys = [[0x7f],[0x17],[0x1b],[0x12],[0x54],[0x08,0x10],[0x56],[0x3f],
        [0xd5,0x57,0x5b,0x63,0xaa],[0x42],[0x3a],[0x19],[0x57],[0x07],
        [0x20,0x50,0x56,0x70],[0x39,0x8f,0xaf,0xf9]]


data = read_file('../ciphertext/crackme.zip.enc')[4:]
for i, m in enumerate(itertools.product(*keys)):
    if i != 104:
        # Skip to the correct key - to crack for real remove the check
        continue
    print "testing key {}...".format(i),
    plaintext = DecryptFile(data, m)
    write_file('tmp.zip', plaintext)
    try:
        zip_file = zipfile.ZipFile('tmp.zip')
    except Exception as e: 
        print("no")
        continue

    if zip_file.testzip():
        print("no")
    else:
        print("yes! Got it.")
        print("Key is: {}".format(" ".join(["{:02x}".format(mc) for mc in m])))
        print("You should be able to unzip tmp.zip now")
        quit()


