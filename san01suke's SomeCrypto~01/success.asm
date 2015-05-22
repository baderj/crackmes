.text:0040129D                 call    loc_401000
.text:004012A2                 add     esp, 4
.text:004012A5                 mov     byte_403270, al
.text:004012AA                 test    al, al
.text:004012AC                 jz      short loc_4012CA
.text:004012AE                 mov     ecx, [esp+100h+lpText]
.text:004012B2                 push    0               ; uType
.text:004012B4                 push    offset Caption  ; "Success"
