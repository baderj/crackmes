loc_401000:                             ; CODE XREF: DialogFunc+1CDp
.text:00401000                 push    ebp
.text:00401001                 mov     ebp, esp
.text:00401003                 mov     al, [ecx]
.text:00401005                 sub     esp, 20h
.text:00401008                 push    esi
.text:00401009                 xor     esi, esi
.text:0040100B                 test    al, al
.text:0040100D                 jz      loc_4010C6
.text:00401013                 lea     edx, [ebp-20h]
.text:00401016                 sub     edx, ecx
.text:00401018
.text:00401018 loc_401018:                             ; CODE XREF: .text:00401032j
.text:00401018                 cmp     al, 61h
.text:0040101A                 jl      loc_4010C6
.text:00401020                 cmp     al, 7Ah
.text:00401022                 jg      loc_4010C6
.text:00401028                 mov     [edx+ecx], al
.text:0040102B                 mov     al, [ecx+1]
.text:0040102E                 inc     ecx
.text:0040102F                 inc     esi
.text:00401030                 test    al, al
.text:00401032                 jnz     short loc_401018
.text:00401034                 cmp     esi, 1Ah
.text:00401037                 jnz     loc_4010C6
.text:0040103D                 xor     eax, eax
.text:0040103F                 nop
.text:00401040
.text:00401040 loc_401040:                             ; CODE XREF: .text:0040104Fj
.text:00401040                 mov     cl, byte_403010[eax]
.text:00401046                 mov     byte_403140[eax], cl
.text:0040104C                 inc     eax
.text:0040104D                 test    cl, cl
.text:0040104F                 jnz     short loc_401040
.text:00401051                 xor     ecx, ecx
.text:00401053                 cmp     byte_403140, cl
.text:00401059                 jz      short loc_401088
.text:0040105B                 jmp     short loc_401060
.text:0040105B ; ---------------------------------------------------------------------------
.text:0040105D                 align 10h
.text:00401060
.text:00401060 loc_401060:                             ; CODE XREF: .text:0040105Bj
.text:00401060                                         ; .text:00401086j
.text:00401060                 mov     al, byte_403140[ecx]
.text:00401066                 cmp     al, 61h
.text:00401068                 jl      short loc_40107E
.text:0040106A                 cmp     al, 7Ah
.text:0040106C                 jg      short loc_40107E
.text:0040106E
.text:0040106E loc_40106E:                             ; DATA XREF: start:loc_4012D5w
.text:0040106E                 push    cs
.text:0040106F                 mov     esi, 5948AC0h
.text:00401074
.text:00401074 loc_401074:                             ; CODE XREF: .text:loc_401074j
.text:00401074                 jg      short near ptr loc_401074+1
.text:00401074 ; ---------------------------------------------------------------------------
.text:00401076                 dw 0FFFFh
.text:00401078 ; ---------------------------------------------------------------------------
.text:00401078                 mov     byte_403140[ecx], dl
.text:0040107E
.text:0040107E loc_40107E:                             ; CODE XREF: .text:00401068j
.text:0040107E                                         ; .text:0040106Cj
.text:0040107E                 inc     ecx
.text:0040107F                 cmp     byte_403140[ecx], 0
.text:00401086                 jnz     short loc_401060
.text:00401088
.text:00401088 loc_401088:                             ; CODE XREF: .text:00401059j
.text:00401088                 or      eax, 0FFFFFFFFh
.text:0040108B                 mov     edx, offset byte_403140
.text:00401090                 test    ecx, ecx
.text:00401092                 jz      short loc_4010AD
.text:00401094
.text:00401094 loc_401094:                             ; CODE XREF: .text:004010ABj
.text:00401094                 movzx   esi, byte ptr [edx]
.text:00401097                 xor     esi, eax
.text:00401099                 and     esi, 0FFh
.text:0040109F                 shr     eax, 8
.text:004010A2                 xor     eax, ds:dword_402058[esi*4]
.text:004010A9                 inc     edx
.text:004010AA                 dec     ecx
.text:004010AB                 jnz     short loc_401094
.text:004010AD
.text:004010AD loc_4010AD:                             ; CODE XREF: .text:00401092j
.text:004010AD                 not     eax
.text:004010AF                 cmp     eax, 0F891B218h
.text:004010B4                 jnz     short loc_4010C6
.text:004010B6                 mov     eax, [ebp+8]
.text:004010B9                 mov     dword ptr [eax], offset byte_403140
.text:004010BF                 mov     al, 1
.text:004010C1                 pop     esi
.text:004010C2                 mov     esp, ebp
.text:004010C4                 pop     ebp
.text:004010C5                 retn
