.text:00401110 sub_401110      proc near               ; CODE XREF: sub_4011E0+5Ep
.text:00401110                                         ; sub_4011E0+71p
.text:00401110
.text:00401110 var_1C          = dword ptr -1Ch
.text:00401110 var_18          = word ptr -18h
.text:00401110 var_16          = byte ptr -16h
.text:00401110 var_14          = dword ptr -14h
.text:00401110 var_10          = dword ptr -10h
.text:00401110 var_C           = dword ptr -0Ch
.text:00401110 var_8           = dword ptr -8
.text:00401110 var_4           = dword ptr -4
.text:00401110 arg_0           = dword ptr  8
.text:00401110
.text:00401110                 push    ebp
.text:00401111                 mov     ebp, esp
.text:00401113                 mov     ecx, 7
.text:00401118                 sub     esp, 1Ch
.text:0040111B                 cmp     [ebp+arg_0], ecx
.text:0040111E                 jle     loc_4011CB
.text:00401124                 mov     edx, [eax+8]
.text:00401127                 lea     edx, [ebp+edx+var_1C]
.text:0040112B                 mov     [ebp+var_4], edx
.text:0040112E                 mov     edx, [eax+0Ch]
.text:00401131                 lea     edx, [ebp+edx+var_1C]
.text:00401135                 mov     [ebp+var_8], edx
.text:00401138                 mov     edx, [eax+10h]
.text:0040113B                 lea     edx, [ebp+edx+var_1C]
.text:0040113F                 push    ebx
.text:00401140                 push    esi
.text:00401141                 mov     esi, [eax]
.text:00401143                 mov     [ebp+var_C], edx
.text:00401146                 mov     edx, [eax+14h]
.text:00401149                 push    edi
.text:0040114A                 mov     edi, [eax+4]
.text:0040114D                 mov     eax, [eax+18h]
.text:00401150                 lea     edx, [ebp+edx+var_1C]
.text:00401154                 mov     [ebp+var_10], edx
.text:00401157                 lea     edx, [ebp+eax+var_1C]
.text:0040115B                 mov     eax, offset unk_403142
.text:00401160                 lea     esi, [ebp+esi+var_1C]
.text:00401164                 lea     edi, [ebp+edi+var_1C]
.text:00401168                 mov     [ebp+var_14], edx
.text:0040116B                 sub     ecx, eax
.text:0040116D                 lea     ecx, [ecx+0]
.text:00401170
.text:00401170 loc_401170:                             ; CODE XREF: sub_401110+B6j
.text:00401170                 movzx   edx, byte ptr [eax-2]
.text:00401174                 mov     ebx, [ebp+var_4]
.text:00401177                 mov     [esi], dl
.text:00401179                 movzx   edx, byte ptr [eax-1]
.text:0040117D                 mov     [edi], dl
.text:0040117F                 movzx   edx, byte ptr [eax]
.text:00401182                 mov     [ebx], dl
.text:00401184                 movzx   edx, byte ptr [eax+1]
.text:00401188                 mov     ebx, [ebp+var_8]
.text:0040118B                 mov     [ebx], dl
.text:0040118D                 movzx   edx, byte ptr [eax+2]
.text:00401191                 mov     ebx, [ebp+var_C]
.text:00401194                 mov     [ebx], dl
.text:00401196                 movzx   edx, byte ptr [eax+3]
.text:0040119A                 mov     ebx, [ebp+var_10]
.text:0040119D                 mov     [ebx], dl
.text:0040119F                 movzx   edx, byte ptr [eax+4]
.text:004011A3                 mov     ebx, [ebp+var_14]
.text:004011A6                 mov     [ebx], dl
.text:004011A8                 mov     edx, [ebp+var_1C]
.text:004011AB                 mov     [eax-2], edx
.text:004011AE                 mov     dx, [ebp+var_18]
.text:004011B2                 mov     [eax+2], dx
.text:004011B6                 movzx   edx, [ebp+var_16]
.text:004011BA                 mov     [eax+4], dl
.text:004011BD                 add     eax, 7
.text:004011C0                 lea     edx, [ecx+eax]
.text:004011C3                 cmp     edx, [ebp+arg_0]
.text:004011C6                 jl      short loc_401170
.text:004011C8                 pop     edi
.text:004011C9                 pop     esi
.text:004011CA                 pop     ebx
.text:004011CB
.text:004011CB loc_4011CB:                             ; CODE XREF: sub_401110+Ej
.text:004011CB                 mov     esp, ebp
.text:004011CD                 pop     ebp
.text:004011CE                 retn    4
.text:004011CE sub_401110      endp
