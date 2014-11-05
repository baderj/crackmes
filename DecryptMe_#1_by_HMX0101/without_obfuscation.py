import struct
import re

def read_file(path):
    data = []
    with open(path, 'rb') as r:
        while True:
            dat = r.read(1)
            if dat != "" and len(dat):
                data.append(struct.unpack('B',dat)[0])
            else:
                return data

c = read_file('cc')
c_len = 0x1E
serial = 254 
plaintext = ""
for i in range(c_len):
    plaintext_char = c[i] - 0x2644
    plaintext_char ^= 0x0DEAD
    plaintext_char += 10
    plaintext_char -= serial 
    plaintext_char ^= serial
    plaintext += chr(plaintext_char & 0xFF)

print(plaintext)


