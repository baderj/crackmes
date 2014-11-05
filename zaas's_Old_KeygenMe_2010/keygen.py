import string
import argparse

def keygen(name):
    code_sum = 0x586
    for i in range(4):
        code_sum -= (4-i)*ord(name[i])

    nice_ascii = string.ascii_letters + string.digits
    nice_ascii_nr = [ord(c) for c in nice_ascii]
    code_list = 4*[0]
    for i in  range(3):
        avg = (code_sum - sum(code_list)) // (4-i)
        code_list[i] = min(nice_ascii_nr, key=lambda x: abs(x-avg))
    code_list[3] = code_sum - sum(code_list)
    print(code_list)
    code = "".join([chr(c) for c in code_list] )
    return code

parser = argparse.ArgumentParser("Keygen for Old_KeygenMe.exe")
parser.add_argument("name")
args = parser.parse_args()
print(">{}<".format(args.name))
if len(args.name) < 4:
    print("Name must have at least 4 characters")
    quit()
code = keygen(args.name)
print("enter the following code: {}".format(code))
print("next enter SHIFT+3 and hit OK")
print("-> so on US keyboards enter: {}".format(code+"#"))
