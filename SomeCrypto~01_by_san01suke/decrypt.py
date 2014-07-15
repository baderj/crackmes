import string
 
crypt = """Ix lzctusdzetgc, ex n-fsb (nvfnujuvujsx-fsb) jn e fenjl lsatsxrxu sw
ncaaruzjl qrc ehdszjugan pgjlg trzwszan nvfnujuvujsx. Ix fhslq ljtgrzn, ugrc
ezr uctjlehhc vnrm us sfnlvzr ugr zrheujsxngjt fruprrx ugr qrc exm ugr
ljtgrzurbu.""".replace('\n', '')
 
key = 'EFLMRWDGJIQHAXSTOZNUVYPBCK'.lower()
mapping = {}
for k, c in zip(key, string.lowercase):
    mapping[k] = c
 
msg = ""
for c in crypt:
    msg += mapping.get(c, c)
 
print("the key is: {}".format(''.join([mapping[x] for x in string.lowercase])))
print("the plaintext is: {}".format(msg))
