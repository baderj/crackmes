import hashlib
import argparse

def keygen(username):
    """ private key, see private_key.gp """
    d = 35066939730281390814817536468479435777

    """ modulus """
    n = 0xAD08D0361CC7FE8D1D3EAC5A68394C95 

    def rsa_decrypt(c, d, n):
        """
            c: ciphertext
            d: private key
            n: modulus
        """
        return pow(c, d, n)

    def rotm1(p):
        c = "".join([chr(ord(x)-1) for x in p])
        return c

    shifted = rotm1(username)
    md5 = hashlib.md5(shifted).hexdigest()
    md5 = "5321783072" + md5[10:]
    c = int(md5,16)
    m = rsa_decrypt(c, d, n)
    code = hex(m).rstrip("L").lstrip("0x")
    return code

if __name__=="__main__":
    desc = "Keygen for S!x0r's Crackme#1"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("username")
    args = parser.parse_args()
    code = keygen(args.username)
    print("""your credentials are:
    username: {}
    code:     {}""".format(args.username, code))

