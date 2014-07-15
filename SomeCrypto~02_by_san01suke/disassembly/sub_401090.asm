.text:00401090 ; =============== S U B R O U T I N E =======================================
.text:00401090
.text:00401090
.text:00401090 sub_401090      proc near               ; CODE XREF: sub_4011E0+68p
.text:00401090                 movsx   edx, byte ptr [ecx]
.text:00401093                 add     edx, 0FFFFFFD0h
.text:00401096                 push    esi
.text:00401097                 xor     esi, esi
.text:00401099                 mov     [eax], edx
.text:0040109B                 cmp     edx, 7
.text:0040109E                 jb      short loc_4010A2
.text:004010A0                 mov     [eax], esi
.text:004010A2
.text:004010A2 loc_4010A2:                             ; CODE XREF: sub_401090+Ej
.text:004010A2                 movsx   edx, byte ptr [ecx+1]
.text:004010A6                 add     edx, 0FFFFFFD0h
.text:004010A9                 mov     [eax+4], edx
.text:004010AC                 cmp     edx, 7
.text:004010AF                 jb      short loc_4010B4
.text:004010B1                 mov     [eax+4], esi
.text:004010B4
.text:004010B4 loc_4010B4:                             ; CODE XREF: sub_401090+1Fj
.text:004010B4                 movsx   edx, byte ptr [ecx+2]
.text:004010B8                 add     edx, 0FFFFFFD0h
.text:004010BB                 mov     [eax+8], edx
.text:004010BE                 cmp     edx, 7
.text:004010C1                 jb      short loc_4010C6
.text:004010C3                 mov     [eax+8], esi
.text:004010C6
.text:004010C6 loc_4010C6:                             ; CODE XREF: sub_401090+31j
.text:004010C6                 movsx   edx, byte ptr [ecx+3]
.text:004010CA                 add     edx, 0FFFFFFD0h
.text:004010CD                 mov     [eax+0Ch], edx
.text:004010D0                 cmp     edx, 7
.text:004010D3                 jb      short loc_4010D8
.text:004010D5                 mov     [eax+0Ch], esi
.text:004010D8
.text:004010D8 loc_4010D8:                             ; CODE XREF: sub_401090+43j
.text:004010D8                 movsx   edx, byte ptr [ecx+4]
.text:004010DC                 add     edx, 0FFFFFFD0h
.text:004010DF                 mov     [eax+10h], edx
.text:004010E2                 cmp     edx, 7
.text:004010E5                 jb      short loc_4010EA
.text:004010E7                 mov     [eax+10h], esi
.text:004010EA
.text:004010EA loc_4010EA:                             ; CODE XREF: sub_401090+55j
.text:004010EA                 movsx   edx, byte ptr [ecx+5]
.text:004010EE                 add     edx, 0FFFFFFD0h
.text:004010F1                 mov     [eax+14h], edx
.text:004010F4                 cmp     edx, 7
.text:004010F7                 jb      short loc_4010FC
.text:004010F9                 mov     [eax+14h], esi
.text:004010FC
.text:004010FC loc_4010FC:                             ; CODE XREF: sub_401090+67j
.text:004010FC                 movsx   ecx, byte ptr [ecx+6]
.text:00401100                 add     ecx, 0FFFFFFD0h
.text:00401103                 mov     [eax+18h], ecx
.text:00401106                 cmp     ecx, 7
.text:00401109                 jb      short loc_40110E
.text:0040110B                 mov     [eax+18h], esi
.text:0040110E
.text:0040110E loc_40110E:                             ; CODE XREF: sub_401090+79j
.text:0040110E                 pop     esi
.text:0040110F                 retn
.text:0040110F sub_401090      endp
