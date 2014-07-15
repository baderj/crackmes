.text:00401000 ; =============== S U B R O U T I N E =======================================
.text:00401000
.text:00401000
.text:00401000 sub_401000      proc near               ; CODE XREF: sub_4011E0+26p
.text:00401000                                         ; DATA XREF: .text:004014DAo
.text:00401000                 mov     dword ptr [eax], 0
.text:00401006                 mov     dword ptr [eax+4], 1
.text:0040100D                 mov     dword ptr [eax+8], 2
.text:00401014                 mov     dword ptr [eax+0Ch], 3
.text:0040101B                 mov     dword ptr [eax+10h], 4
.text:00401022                 mov     dword ptr [eax+14h], 5
.text:00401029                 mov     dword ptr [eax+18h], 6
.text:00401030                 mov     cl, [edx]
.text:00401032                 test    cl, cl
.text:00401034                 jz      short locret_40108C
.text:00401036                 push    esi
.text:00401037                 jmp     short loc_401040
.text:00401037 ; ---------------------------------------------------------------------------
.text:00401039                 align 10h
.text:00401040
.text:00401040 loc_401040:                             ; CODE XREF: sub_401000+37j
.text:00401040                                         ; sub_401000+89j
.text:00401040                 movsx   ecx, cl
.text:00401043                 and     ecx, 80000001h
.text:00401049                 jns     short loc_401050
.text:0040104B                 dec     ecx
.text:0040104C                 or      ecx, 0FFFFFFFEh
.text:0040104F                 inc     ecx
.text:00401050
.text:00401050 loc_401050:                             ; CODE XREF: sub_401000+49j
.text:00401050                 jz      short loc_40105C
.text:00401052                 mov     esi, [eax+4]
.text:00401055                 mov     ecx, [eax]
.text:00401057                 mov     [eax], esi
.text:00401059                 mov     [eax+4], ecx
.text:0040105C
.text:0040105C loc_40105C:                             ; CODE XREF: sub_401000:loc_401050j
.text:0040105C                 mov     ecx, [eax]
.text:0040105E                 mov     esi, [eax+4]
.text:00401061                 mov     [eax], esi
.text:00401063                 mov     esi, [eax+8]
.text:00401066                 mov     [eax+4], esi
.text:00401069                 mov     esi, [eax+0Ch]
.text:0040106C                 mov     [eax+8], esi
.text:0040106F                 mov     esi, [eax+10h]
.text:00401072                 mov     [eax+0Ch], esi
.text:00401075                 mov     esi, [eax+14h]
.text:00401078                 mov     [eax+10h], esi
.text:0040107B                 mov     esi, [eax+18h]
.text:0040107E                 mov     [eax+14h], esi
.text:00401081                 inc     edx
.text:00401082                 mov     [eax+18h], ecx
.text:00401085                 mov     cl, [edx]
.text:00401087                 test    cl, cl
.text:00401089                 jnz     short loc_401040
.text:0040108B                 pop     esi
.text:0040108C
.text:0040108C locret_40108C:                          ; CODE XREF: sub_401000+34j
.text:0040108C                 retn
.text:0040108C sub_401000      endp
