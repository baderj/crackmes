import argparse    
from collections import deque

parser = argparse.ArgumentParser(description="SomeCrypto~03 keygen")
parser.add_argument('name')
args = parser.parse_args()
name = args.name 

correct_key = [9,7,6,0,1,5,4,3,8,2]
cypher = deque(list(range(10)))

for c in name:
    if ord(c) % 2:
        cypher[0], cypher[1] = cypher[1], cypher[0]
    cypher.rotate(-1)
serial = 10*[None]
for c, k in zip(cypher, correct_key):
    serial[c] = k

print('serial: ' + ''.join(str(s) for s in serial))
