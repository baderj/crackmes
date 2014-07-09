"""Reverse key generator for GordonBM's Reverse Keygenme
   see http://www.crackmes.de/users/gordonbm/reverse_keygenme/ 
   (simple mode)
   """

import argparse
import re


def crack(key):
    """generate msg for key"""
    res = ""
    for code in re.findall(r'([2-9]\d|1\d{2})', key):
        res += chr(int(code))
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Reverse Keygen")
    parser.add_argument("encrypted")
    args = parser.parse_args()
    print(crack(args.encrypted))
