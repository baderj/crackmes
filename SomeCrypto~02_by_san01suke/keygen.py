import argparse    
from collections import deque

parser = argparse.ArgumentParser(description="SomeCrypto~02 keygen")
parser.add_argument('name')
args = parser.parse_args()
name = args.name 

correct_key = [6, 4, 1, 3, 5, 0, 2]
cypher = deque(list(range(7)))

for c in name:
    if ord(c) % 2:
        cypher[0], cypher[1] = cypher[1], cypher[0]
    cypher.rotate(-1)

serial = 7*[None]
for c, k in zip(cypher, correct_key):
    serial[c] = k

print('serial: ' + ''.join(str(s) for s in serial))
