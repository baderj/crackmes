import argparse

def generate_key(username):
    if not 8 <= len(username) <= 12:
        print("username must be between 8 and 12 characters.")
        quit()
    key = '' 
    for i, u in enumerate(username):
        if i%2:
            key += str(ord(u.upper()))
        else:
            key += str(ord(u.lower()))
    return int(key[2*(len(username)-8):][0:8])

if __name__=="__main__":
    parser = argparse.ArgumentParser(
            description="keygen for adamziaja's crackme1")
    parser.add_argument('username')
    args = parser.parse_args()
    print(generate_key(args.username))

