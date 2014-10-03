def sub_4014EA(hexx):
    ecx = 0xFFFFFFFF 
    cl = 0xFF
    ch = 0xFF
    edx = 0xFFFFFFFF
    dl = 0xFF
    dh = 0xFF
    for i in range(2):
        bx = 0
        if i == 0:
            al = (hexx & 0xFF00) >> 8 
        else:
            al = (hexx & 0xFF)
        al = al ^ cl
        ax = al
        cl,ch,dl,dh = ch,dl,dh,0
        for j in range(8):
            cf = bx % 2
            bx = (bx >> 1)
            cf2 = ax % 2
            ax = (ax >> 1) + (cf << 15)
            if cf2:
                ax = ax ^ 0x8320
                bx = bx ^ 0xEDB8
        ch = ch & 0xFF
        cl = cl & 0xFF
        dl = dl & 0xFF
        dh = dh & 0xFF
        bx = bx & 0xFFFF
        ecx = (ecx & 0xFFFF0000) + (ch << 8) + cl
        eax = ax
        ecx = eax ^ ecx
        edx = (edx & 0xFFFF0000) + (dh << 8) + dl
        edx = edx ^ bx
        cl = ecx & 0xFF
        ch = (ecx >> 8) & 0xFF
        dl = edx & 0xFF
        dh = (edx >> 8) & 0xFF


    edx = (1<<32) - edx - 1
    ecx = (1<<32) - ecx - 1
    eax = edx
    eax = (edx << 16)
    eax = (eax & 0xFFFF0000) + (ecx & 0xFFFF)
    return eax

f = sub_4014EA(0x07D0)
print(hex(f))
