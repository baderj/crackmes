"""
    compile with
    dot -Tpng tree.dot  -o tree.png
"""

import re
from collections import defaultdict
header = """
digraph G {
    nodesep=0.3;
    ranksep=0.2;
    margin=0.1;
    node [shape=circle];
    edge [arrowsize=0.8];
    graph [ordering="out"];
"""
footer = """
}
"""

instructions = """
  ptr[0]->enc_letter = 'e';
  ptr[1]->enc_letter = 'r';
  ptr[2]->enc_letter = 'T';
  ptr[3]->enc_letter = 'l';
  ptr[4]->enc_letter = 'S';
  ptr[5]->enc_letter = 'v';
  ptr[6]->enc_letter = 'n';
  ptr[7]->enc_letter = 'i';
  ptr[8]->enc_letter = 'N';
  ptr[9]->enc_letter = 'F';
  ptr[10]->enc_letter = 'n';
  ptr[11]->enc_letter = 'l';
  ptr[12]->enc_letter = 'r';
  ptr[13]->enc_letter = 'l';
  ptr[14]->enc_letter = 'e';
  ptr[15]->enc_letter = 'e';
  ptr[16]->enc_letter = 'c';
  ptr[17]->enc_letter = 'i';
  ptr[18]->enc_letter = 's';
  ptr[19]->enc_letter = 'o';
  ptr[20]->enc_letter = 'i';
  ptr[21]->enc_letter = 'g';
  ptr[22]->enc_letter = 'a';
  ptr[23]->enc_letter = 'g';
  ptr[0]->right = ptr[1];
  ptr[1]->right = 0;
  ptr[1]->left = ptr[5];
  ptr[5]->right = ptr[15];
  ptr[15]->right = 0;
  ptr[5]->left = ptr[8];
  ptr[8]->right = ptr[14];
  ptr[8]->left = 0;
  ptr[14]->right = 0;
  ptr[14]->left = 0;
  ptr[0]->left = ptr[2];
  ptr[2]->right = ptr[3];
  ptr[3]->right = ptr[4];
  ptr[4]->right = ptr[6];
  ptr[6]->right = ptr[16];
  ptr[16]->right = 0;
  ptr[16]->left = 0;
  ptr[6]->left = ptr[17];
  ptr[17]->left = 0;
  ptr[17]->right = 0;
  ptr[4]->left = ptr[7];
  ptr[7]->left = 0;
  ptr[7]->right = ptr[10];
  ptr[10]->left = 0;
  ptr[10]->right = ptr[21];
  ptr[21]->right = 0;
  ptr[21]->left = 0;
  ptr[3]->left = ptr[11];
  ptr[11]->right = 0;
  ptr[11]->left = ptr[12];
  ptr[12]->left = 0;
  ptr[12]->right = ptr[19];
  ptr[19]->right = 0;
  ptr[19]->left = 0;
  ptr[2]->left = ptr[9];
  ptr[9]->left = 0;
  ptr[9]->right = ptr[13];
  ptr[13]->left = 0;
  ptr[13]->right = ptr[18];
  ptr[18]->right = 0;
  ptr[18]->left = ptr[20];
  ptr[20]->right = 0;
  ptr[20]->left = ptr[22];
  ptr[22]->left = 0;
  ptr[22]->right = ptr[23];
  ptr[23]->right = 0;
  ptr[23]->left = 0;
"""

enc_letters = {}
tree = defaultdict(dict) 
for instr in instructions.split("\n"):
    m = re.search("ptr\[(\d+)\]->enc_letter\s+=\s+'(.*)';", instr.strip())
    if m:
        enc_letters[m.group(1)] = m.group(2) 
    m = re.search("ptr\[(\d+)\]->(right|left)\s+=\s+ptr\[(\d+)", instr.strip())
    if m:
        tree[m.group(1)][m.group(2)] = m.group(3)
    m = re.search("ptr\[(\d+)\]->(right|left)\s+=\s+0", instr.strip())

with open("tree.dot", "w") as w:
    w.write(header)
    for x, y in enc_letters.items():
        w.write("     {} [label={}]\n".format(x, y))
        
    empty = 1000
    for t, v in tree.items():
        if not 'left' in v and not 'right' in v: 
            continue
        for d in ['left', 'right']:
            if d in v:
                w.write("    {} -> {}\n".format(t, v[d])) 
            else:
                w.write('    {} [label="."]\n'.format(empty))
                w.write("    {} -> {}\n".format(t, empty)) 
                empty += 1

    w.write(footer)


    """
        get flag
    """
    def get_list(tree, node):
        if node is None:
            return []
        l = tree[node].get('left', None)
        r = tree[node].get('right', None)
        return get_list(tree, l) + [enc_letters[node]] + get_list(tree, r) 


    print(''.join(get_list(tree, "0")))
