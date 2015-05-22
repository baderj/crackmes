import socket, uuid
import sys

def keygen(name):
    hostname = socket.gethostname() 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = s.getsockname()[0]
    mac =  ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

    print("hostname: {}".format(hostname))
    print("ip:       {}".format(ip))
    print("mac:      {}".format(mac))

    hex_name = ''.join(["{:02x}".format(ord(x)) for x in name])
    calc = 0

    i_str = ""
    for x in hex_name:
        try:
            int(x)
            i_str += x
        except ValueError:
            break
    a = int(i_str) & 0xFFFFFFFF
    try:
        b = int(mac[3]) 
    except ValueError:
        b = 0
    s1 = (a + 171) & 0xFFFFFFFF
    s2 = (a + 15658734) & 0xFFFFFFFF
    s3 = a // s1 
    s4 = b + s3 
    s5 = (s4 ^ 35) + s2*(s4 ^ b) & 0xFFFFFFFF
    s6 = (s1 ^ b) + ((b + s2) ^ 0x33838D) & 0xFFFFFFFF
    s7 = 978670 * b & 0xFFFFFFFF
    s8 = s6 + s7 + a & 0xFFFFFFFF
    serial = "{}{}{}{}".format(mac[3], ip[1], s8, hostname[0])

    print("name:     {}".format(name))
    print("serial:   {}".format(serial))


keygen(sys.argv[1])
