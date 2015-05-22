def ran_values(length, values=None, pos=0, val=0):
    """get all potential random values for length as list """

    if values is None:
        values = set()
    if pos == length:
        values.add(val)
    else:
        xor = (2*pos) ^ 6
        pos += 1

        # case 1: rand is 0
        next_val = 9*val
        ran_values(length, values, pos, next_val)

        # case 2: rand is 1
        next_val = 3*(val*3 + xor)
        ran_values(length, values, pos, next_val)

    return sorted(values)

if __name__ == "__main__":
    for i in range(1,7):
        tmp = "<tr><td>{}</td><td>{}</td></tr>"
        print(tmp.format(i, ', '.join([str(x) for x in ran_values(i)])))
