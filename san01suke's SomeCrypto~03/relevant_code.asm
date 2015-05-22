.text:00401258 ; ---------------------------------------------------------------------------
.text:00401259                 align 10h
.text:00401260
.text:00401260 ; =============== S U B R O U T I N E =======================================
.text:00401260
.text:00401260 ; Attributes: bp-based frame
.text:00401260
.text:00401260 sub_401260      proc near               ; CODE XREF: DialogFunc+1DDp
.text:00401260
.text:00401260 permutation     = byte ptr -2Ch
.text:00401260 arg_0           = dword ptr  8
.text:00401260
.text:00401260 name_length = eax
.text:00401260 serial = esi
.text:00401260                 push    ebp
.text:00401261                 mov     ebp, esp
.text:00401263                 sub     esp, 30h
.text:00401266                 push    serial
.text:00401267                 mov     serial, name_length
.text:00401269                 xor     name_length, name_length
.text:0040126B                 cmp     [edx], al
.text:0040126D                 jz      failed          ; if name empty jump
.text:00401273
.text:00401273 loc_401273:                             ; CODE XREF: sub_401260+18j
.text:00401273                 inc     name_length
.text:00401274                 cmp     byte ptr [name_length+edx], 0 ; name[index] == '\0'
.text:00401278                 jnz     short loc_401273
.text:0040127A                 cmp     name_length, 4  ; -> name length needs to >= 4
.text:0040127D                 jl      failed
.text:00401283                 xor     eax, eax
.text:00401285                 cmp     [serial], al    ; if empty serial jump
.text:00401287                 jz      failed
.text:0040128D                 lea     ecx, [ecx+0]    ; ecx = 7743008E
.text:00401290
.text:00401290 loc_401290:                             ; CODE XREF: sub_401260+35j
.text:00401290                 inc     eax
.text:00401291                 cmp     byte ptr [eax+serial+0], 0
.text:00401295                 jnz     short loc_401290
.text:00401297                 cmp     eax, 10         ; serial length needs to be 10
.text:0040129A                 jnz     failed
.text:004012A0                 lea     eax, [ebp+permutation] ; eax will hold permutation
.text:004012A3                 call    permutation_name ; generate permutation based on name
.text:004012A8                 mov     al, byte_403010
.text:004012AD                 mov     byte_403080, al
.text:004012B2                 mov     edx, 17
.text:004012B7                 jmp     short loc_4012C0
.text:004012B7 ; ---------------------------------------------------------------------------
.text:004012B9                 align 10h
.text:004012C0
.text:004012C0 loc_4012C0:                             ; CODE XREF: sub_401260+57j
.text:004012C0                                         ; sub_401260+79j
.text:004012C0                 mov     cl, byte_403010[edx]
.text:004012C6                 mov     byte_403080[edx], cl
.text:004012CC                 lea     eax, [edx+17]
.text:004012CF                 cdq
.text:004012D0                 mov     ecx, 103
.text:004012D5                 idiv    ecx             ; eax = edx/103, edx = edx % 103
.text:004012D7                 test    edx, edx
.text:004012D9                 jnz     short loc_4012C0 ; loop while edx != 0
.text:004012DB                 mov     edx, offset byte_403080
.text:004012E0                 lea     eax, [ebp+permutation]
.text:004012E3                 call    map_rotate
.text:004012E8                 mov     ecx, serial
.text:004012EA                 lea     eax, [ebp+permutation]
.text:004012ED                 call    mapping_is_serial
.text:004012F2                 mov     edx, offset byte_403080
.text:004012F7                 lea     eax, [ebp+permutation]
.text:004012FA                 call    map_rotate
.text:004012FF encrypted_msg = edx
.text:004012FF                 mov     ecx, 67h
.text:00401304                 mov     encrypted_msg, offset byte_403080
.text:00401309                 or      eax, 0FFFFFFFFh
.text:0040130C                 lea     esp, [esp+0]
.text:00401310
.text:00401310 loc_401310:                             ; CODE XREF: sub_401260+C7j
.text:00401310                 movzx   esi, byte ptr [encrypted_msg]
.text:00401313                 xor     esi, eax
.text:00401315                 and     esi, 0FFh
.text:0040131B                 shr     eax, 8
.text:0040131E                 xor     eax, ds:dword_402060[esi*4]
.text:00401325                 inc     encrypted_msg
.text:00401326                 dec     ecx
.text:00401327                 jnz     short loc_401310
.text:00401329                 not     eax
.text:0040132B                 cmp     eax, 72DD193Dh
.text:00401330                 jnz     short failed
.text:00401332                 mov     encrypted_msg, [ebp+arg_0]
.text:00401335                 mov     eax, ds:MessageBoxA
.text:0040133A                 push    encrypted_msg
.text:0040133B                 push    offset aSuccess ; "Success"
.text:00401340                 push    eax
.text:00401341                 mov     ecx, offset byte_403080
.text:00401346                 mov     byte ptr unk_403078, 1
.text:0040134D                 call    ecx ; byte_403080
.text:0040134F                 add     esp, 0Ch
.text:00401352                 mov     al, 1
.text:00401354                 pop     esi
.text:00401355                 mov     esp, ebp
.text:00401357                 pop     ebp
.text:00401358                 retn
.text:00401359 ; ---------------------------------------------------------------------------
