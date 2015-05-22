.text:004011E0 ; =============== S U B R O U T I N E =======================================
.text:004011E0
.text:004011E0 ; Attributes: bp-based frame
.text:004011E0
.text:004011E0 sub_4011E0      proc near               ; CODE XREF: .text:00401475p
.text:004011E0
.text:004011E0 var_1C          = byte ptr -1Ch
.text:004011E0 arg_0           = dword ptr  8
.text:004011E0 arg_4           = dword ptr  0Ch
.text:004011E0
.text:004011E0                 push    ebp
.text:004011E1                 mov     ebp, esp
.text:004011E3                 xor     eax, eax
.text:004011E5                 sub     esp, 1Ch
.text:004011E8                 cmp     [edi], al
.text:004011EA                 jz      loc_401296
.text:004011F0
.text:004011F0 loc_4011F0:                             ; CODE XREF: sub_4011E0+15j
.text:004011F0                 inc     eax
.text:004011F1                 cmp     byte ptr [eax+edi], 0
.text:004011F5                 jnz     short loc_4011F0
.text:004011F7                 cmp     eax, 7
.text:004011FA                 jnz     loc_401296
.text:00401200                 mov     edx, [ebp+arg_0]
.text:00401203                 lea     eax, [ebp+var_1C]
.text:00401206                 call    sub_401000
.text:0040120B                 xor     eax, eax
.text:0040120D                 lea     ecx, [ecx+0]
.text:00401210
.text:00401210 loc_401210:                             ; CODE XREF: sub_4011E0+3Fj
.text:00401210                 mov     cl, byte_403010[eax]
.text:00401216                 mov     byte_403140[eax], cl
.text:0040121C                 inc     eax
.text:0040121D                 test    cl, cl
.text:0040121F                 jnz     short loc_401210
.text:00401221                 push    esi
.text:00401222                 xor     esi, esi
.text:00401224                 cmp     byte_403140, 0
.text:0040122B                 jz      short loc_40123A
.text:0040122D                 lea     ecx, [ecx+0]
.text:00401230
.text:00401230 loc_401230:                             ; CODE XREF: sub_4011E0+58j
.text:00401230                 inc     esi
.text:00401231                 cmp     byte_403140[esi], 0
.text:00401238                 jnz     short loc_401230
.text:0040123A
.text:0040123A loc_40123A:                             ; CODE XREF: sub_4011E0+4Bj
.text:0040123A                 push    esi
.text:0040123B                 lea     eax, [ebp+var_1C]
.text:0040123E                 call    sub_401110
.text:00401243                 mov     ecx, edi
.text:00401245                 lea     eax, [ebp+var_1C]
.text:00401248                 call    sub_401090
.text:0040124D                 push    esi
.text:0040124E                 lea     eax, [ebp+var_1C]
.text:00401251                 call    sub_401110
.text:00401256                 or      eax, 0FFFFFFFFh
.text:00401259                 mov     ecx, esi
.text:0040125B                 mov     edx, offset byte_403140
.text:00401260                 test    esi, esi
.text:00401262                 jz      short loc_40127D
.text:00401264
.text:00401264 loc_401264:                             ; CODE XREF: sub_4011E0+9Bj
.text:00401264                 movzx   esi, byte ptr [edx]
.text:00401267                 xor     esi, eax
.text:00401269                 and     esi, 0FFh
.text:0040126F                 shr     eax, 8
.text:00401272                 xor     eax, ds:dword_402058[esi*4]
.text:00401279                 inc     edx
.text:0040127A                 dec     ecx
.text:0040127B                 jnz     short loc_401264
.text:0040127D
.text:0040127D loc_40127D:                             ; CODE XREF: sub_4011E0+82j
.text:0040127D                 not     eax
.text:0040127F                 pop     esi
.text:00401280                 cmp     eax, 0B45D7873h
.text:00401285                 jnz     short loc_401296
.text:00401287                 mov     eax, [ebp+arg_4]
.text:0040128A                 mov     dword ptr [eax], offset byte_403140
.text:00401290                 mov     al, 1
.text:00401292                 mov     esp, ebp
.text:00401294                 pop     ebp
.text:00401295                 retn
.text:00401296 ; ---------------------------------------------------------------------------
.text:00401296
.text:00401296 loc_401296:                             ; CODE XREF: sub_4011E0+Aj
.text:00401296                                         ; sub_4011E0+1Aj ...
.text:00401296                 xor     al, al
.text:00401298                 mov     esp, ebp
.text:0040129A                 pop     ebp
.text:0040129B                 retn
.text:0040129B sub_4011E0      endp
