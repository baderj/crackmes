import struct 

def read_file(path):
    data = []
    with open(path, 'rb') as r:
        while True:
            dat = r.read(1)
            if dat != "":
                data.append(struct.unpack('B',dat)[0])
            else:
                return data

def print_row(fmt, data):
    for d in data: 
        print fmt.format(d),
    print("")

path = '../ciphertext/crackme.zip.enc'
# ciphertext = read_file(path)
ciphertext = read_file(path)[4:]

for i in range(3):
    f = i*16
    l = (i+1)*16
    print_row("{: >2}", range(f, l))
    print_row("{:02x}", ciphertext[f:l])
    print_row("{: >2}", [chr(c) if 32 < c < 127 else "?" for c in ciphertext[f:l]])
    print("")

