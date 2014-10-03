serial = "07D0-05EA-0A26-"
for i in range(256):
    print('{}{:02x}{:02x}'.format(serial, i, i ^ 0x35))

