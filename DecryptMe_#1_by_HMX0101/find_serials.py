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

def solve_equation(a, b):
    answers = set() 
    for s in range(0, 256):
        if (((a - s) ^ s) - b) & 0xFF == 0:
            answers.add(s)
    return answers

plaintext = 'Well Done!, Congratulations!!!'
c = read_file('cc')
c_len = 0x1E
equations = []
c_len = len(plaintext)
for i in range(c_len):
    plaintext_char = c[i] - 0x2644
    plaintext_char ^= 0x0DEAD
    plaintext_char += 10
    a = plaintext_char & 0xFF
    b = ord(plaintext[i])
    equations.append(solve_equation(a, b))

answer = equations[0] 
for e in equations:
    answer &= e

print("the following serials are valid")
ans = ",".join([str(a) for a in sorted(answer)])
print("serial \in {{{}}} mod 256".format(ans))
