import argparse

def hash_name(name):
    h = 0xdeadca7
    for n in [ord(x) for x in name]:
        h = ( ~((n >> 2) + (h ^ 0xf28437*n)) - 0xd23664*n ) & 0xFFFFFFFF
    return h

def name_to_values(name):
    h = hash_name(name)
    x, y = [], []
    for i in range(6):
        val = (h & 0xF) + 1
        if h & 0x10:
            val *= -1;
        if not i%2:
            x.append(val)
        else:
            y.append(val)

        if i%2:
            for j in range(i//2):
                if x[j] == x[i//2]:
                    x[j] += 1
        h = h >> 5;

    return x, y

def keygen(name):
    if not 3 <= len(name) <= 20:
        return "name needs to be 3 to 20 characters long"
    x, y = name_to_values(name)
    serial_comp = []
    for xx, yy in zip(x, y):
        sign = "_" if xx >= 0 else "#"
        serial_comp.append("[0$[X{}{}$2&800]?[{}]]".format(sign,abs(xx), yy))
    return "#".join(serial_comp) 

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    print(keygen(args.name))

