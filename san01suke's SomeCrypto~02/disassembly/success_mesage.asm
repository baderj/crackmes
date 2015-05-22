.text:00401475                 call    sub_4011E0
.text:0040147A                 add     esp, 8
.text:0040147D                 mov     byte_403270, al
.text:00401482                 test    al, al
.text:00401484                 jz      short loc_4014A2
.text:00401486                 mov     edx, [esp+0Ch]
.text:0040148A                 push    0
.text:0040148C                 push    offset aSuccess ; "Success"
.text:00401491                 push    edx
.text:00401492                 push    esi
.text:00401493                 call    ds:MessageBoxA
.text:00401499                 push    0
