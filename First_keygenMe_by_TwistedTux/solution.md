<h2>Key's First Character</h2>
If the length of <tt>clef</tt> is 6 we continue here:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080484C1                 mov     edi, [esp+4]    ; edi = pseudo
.text:080484C5                 push    edi             ; s
.text:080484C6                 call    _strlen         ; strlen(pseudo)
.text:080484CB                 add     esp, 4          ; caller cleanup
.text:080484D1                 mov     [esp], eax      ; pseudo_length --> [esp]
.text:080484D4                 push    eax
.text:080484D5                 call    func_1          ; func_1(pseudo_length)
.text:080484DA                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:080484DF                 add     ebx, eax        ; ebx = &hardcoded_str[func_1_rv]
.text:080484E1                 mov     dl, [ebx]       ; dl = hardcoded_str[func_1_rv]
.text:080484E3                 mov     edi, [esp+8]    ; edi = clef
.text:080484E7                 mov     dh, [edi]       ; dh = clef[0]
.text:080484E9                 cmp     dl, dh          ; clef[0] == hardcoded_str[func_1_rv]
.text:080484EB                 jnz     short exit      ; if not equal then exit
</pre>

The snippet translates to: 
<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
char hardcoded[] = "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU+4mjW6fxqZeF3Qa1rPhdKIouk";
char* pseudo = argv[1];
char* clef = argv[2];
int pseudo_length = strlen(pseudo);
int func_1_rv = func_1(pseudo_length);
if( clef[0] != hardcoded_str[func_1_rv] )
    exit(1); // we failed
</pre>

So the we know that <strong>the first character of <tt>clef</tt> needs to be at position <tt>func_1_rv</tt> into <tt>hardcoded_str</tt>, where <tt>func_1_rv</tt> is the return value of <tt>func_1</tt></strong>:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080485CD func_1          proc near               ; CODE XREF: main+85p
.text:080485CD
.text:080485CD pseudo_length   = dword ptr  8
.text:080485CD
.text:080485CD                 push    ebp
.text:080485CE                 mov     ebp, esp
.text:080485D0                 mov     eax, [ebp+pseudo_length]
.text:080485D3                 and     eax, 0FFh
.text:080485D8                 xor     al, 3Bh
.text:080485DA                 and     eax, 3Fh
.text:080485DF                 leave
.text:080485E0                 retn    4
.text:080485E0 func_1          endp
</pre>

This short function boils down to:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_1(int pseudo_length) 
{
    return (pseudo_length ^ 0x3B) & 0x3F;
}
</pre>


<h2>Key's Second Character</h2>
Next follows disassembly that looks almost the same as the one from the previous section: 

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080484ED                 mov     edi, [esp]      ; edi = pseudo_length
.text:080484F0                 push    edi             ; arg1 = pseudo_length
.text:080484F1                 mov     edi, [esp+8]    ; edi = pseudo
.text:080484F5                 push    edi             ; arg0 = pseudo
.text:080484F6                 call    func_2
.text:080484FB                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:08048500                 add     ebx, eax        ; ebx = &hardcoded_str[func_2_rv]
.text:08048502                 mov     dl, [ebx]       ; dl = hardcoded_str[func_2_rv]
.text:08048504                 mov     edi, [esp+8]    ; edi = clef
.text:08048508                 inc     edi             ; edi = &clef[1]
.text:08048509                 mov     dh, [edi]       ; dh = clef[1]
.text:0804850B                 cmp     dl, dh          ; clef[1] == hardcoded_str[func_2_rv]
.text:0804850D                 jnz     exit            ; if not equal then exit
</pre>

The only differences are:
<ul>
<li>a different subroutine gets called, I renamed it as <tt>func_2</tt>. The first parameter to <tt>func_2</tt> is <tt>pseudo</tt>, the second parameter is the <tt>pseudo_length = strlen(pseudo)</tt>.</li>
<li>the instruction <tt>inc edi</tt> makes <tt>edi</tt> reference <tt>clef[1]</tt>.</li>
</ul>

<strong>There's one pitfall:</strong>  Because of the preceeding <tt>push edi</tt> in the second line, <tt>[esp+8]</tt> points to <tt>pseudo</tt>, and not <tt>clef</tt> as you might expect. Be careful when interpreting stack references based on <tt>esp</tt> rather than <tt>ebp</tt>. 

This is the C code for the snippet:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_2_rv = func_2(pseudo, pseudo_length);
if( clef[1] != hardcoded_str[func_2_rv] )
    exit(1); // we failed
</pre>

The subroutine <tt>func_2</tt> looks as follows:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080485E3 func_2          proc near               ; CODE XREF: main+A6p
.text:080485E3
.text:080485E3 pseudo          = dword ptr  8
.text:080485E3 pseudo_length   = dword ptr  0Ch
.text:080485E3
.text:080485E3                 push    ebp
.text:080485E4                 mov     ebp, esp
.text:080485E6                 sub     esp, 8
.text:080485EC                 mov     ecx, [ebp+pseudo_length]
.text:080485EF                 mov     esi, [ebp+pseudo]
.text:080485F2                 add     esi, ecx
.text:080485F4                 xor     eax, eax
.text:080485F6                 jmp     loc_8048606
.text:080485FB ; ---------------------------------------------------------------------------
.text:080485FB
.text:080485FB loc_80485FB:                            ; CODE XREF: func_2+2Aj
.text:080485FB                 dec     esi
.text:080485FC                 mov     dl, [esi]
.text:080485FE                 and     edx, 0FFh
.text:08048604                 add     eax, edx
.text:08048606
.text:08048606 loc_8048606:                            ; CODE XREF: func_2+13j
.text:08048606                 dec     ecx
.text:08048607                 cmp     ecx, 0FFFFFFFFh
.text:0804860D                 jnz     short loc_80485FB
.text:0804860F                 xor     al, 4Fh
.text:08048611                 and     eax, 3Fh
.text:08048616                 leave
.text:08048617                 retn    8
.text:08048617 func_2          endp
</pre>

Which represents the following loop:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_2(char* pseudo, int pseudo_length)
{
    int res = 0;
    for(int i = 0; i < pseudo_length; i++)
        res += pseudo[i];
    return (res ^ 0x4F) & 0x3F;
}
</pre>

<h2>Key's Third Character</h2>
The next lines again look almost like the checks in for the first two characters of <tt>clef</tt>: 

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:08048513                 mov     edi, [esp]
.text:08048516                 push    edi
.text:08048517                 mov     edi, [esp+8]
.text:0804851B                 push    edi
.text:0804851C                 call    func_3
.text:08048521                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:08048526                 add     ebx, eax
.text:08048528                 mov     dl, [ebx]
.text:0804852A                 mov     edi, [esp+8]
.text:0804852E                 add     edi, 2
.text:08048534                 mov     dh, [edi]
.text:08048536                 cmp     dl, dh          ; clef[2] == hardcoded_str[func_3_rv]
.text:08048538                 jnz     exit
</pre>
The only difference being the new subroutine <tt>func_3</tt> and the reference to the third character of <tt>clef</tt>:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_3_rv = func_3(pseudo, pseudo_length);
if( clef[2] != hardcoded_str[func_3_rv] )
    exit(1); // we failed
</pre>

This is <tt>func_3</tt>:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:0804861A func_3          proc near               ; CODE XREF: main+CCp
.text:0804861A
.text:0804861A pseudo          = dword ptr  8
.text:0804861A pseudo_length   = dword ptr  0Ch
.text:0804861A
.text:0804861A                 push    ebp
.text:0804861B                 mov     ebp, esp
.text:0804861D                 mov     eax, 1
.text:08048622                 mov     esi, [ebp+pseudo]
.text:08048625                 mov     ecx, [ebp+pseudo_length]
.text:08048628                 jmp     loc_804863C
.text:0804862D ; ---------------------------------------------------------------------------
.text:0804862D
.text:0804862D loc_804862D:                            ; CODE XREF: func_3+29j
.text:0804862D                 xor     ebx, ebx
.text:0804862F                 mov     bl, [esi]
.text:08048631                 and     bl, 0FFh
.text:08048634                 mul     ebx
.text:08048636                 and     eax, 0FFh
.text:0804863B                 inc     esi
.text:0804863C
.text:0804863C loc_804863C:                            ; CODE XREF: func_3+Ej
.text:0804863C                 dec     ecx
.text:0804863D                 cmp     ecx, 0FFFFFFFFh
.text:08048643                 jnz     short loc_804862D
.text:08048645                 xor     al, 55h
.text:08048647                 and     eax, 3Fh
.text:0804864C                 leave
.text:0804864D                 retn    8
.text:0804864D func_3          endp
</pre>

Again we loop over all characters in <tt>pseudo</tt>, this time multiplying the ASCII codes rather than adding them up as in <tt>func_2</tt>:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_3(char* pseudo, int pseudo_length)
{
    int res = 1;
    for(int i = 0; i < pseudo_length; i++)
        res *= pseudo[i];
    return (res ^ 0x55) & 0x3F;
}
</pre>


<h2>Key's Fourth Character</h2>
Next in our <tt>main</tt> routine follows more of the same:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:0804853E                 mov     edi, [esp]
.text:08048541                 push    edi
.text:08048542                 mov     edi, [esp+8]
.text:08048546                 push    edi
.text:08048547                 call    func_4
.text:0804854C                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:08048551                 add     ebx, eax
.text:08048553                 mov     dl, [ebx]
.text:08048555                 mov     edi, [esp+8]
.text:08048559                 add     edi, 3
.text:0804855F                 mov     dh, [edi]
.text:08048561                 cmp     dl, dh          ; clef[3] == hardcoded_str[func_4_rv]
.text:08048563                 jnz     exit
</pre>

or in C:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_4_rv = func_4(pseudo, pseudo_length);
if( clef[3] != hardcoded_str[func_4_rv] )
    exit(1); // we failed
</pre>

The subroutine <tt>func_4</tt> is: 

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:08048650 func_4          proc near               ; CODE XREF: main+F7p
.text:08048650
.text:08048650 pseudo          = dword ptr  8
.text:08048650 pseudo_length   = dword ptr  0Ch
.text:08048650
.text:08048650                 push    ebp
.text:08048651                 mov     ebp, esp
.text:08048653                 sub     esp, 4
.text:08048659                 mov     esi, [ebp+pseudo]
.text:0804865C                 mov     al, [esi]
.text:0804865E                 mov     ecx, [ebp+pseudo_length]
.text:08048661                 jmp     loc_804866F
.text:08048666 ; ---------------------------------------------------------------------------
.text:08048666
.text:08048666 loc_8048666:                            ; CODE XREF: func_4+26j
.text:08048666                 inc     esi
.text:08048667                 mov     bl, [esi]
.text:08048669                 cmp     bl, al
.text:0804866B                 jbe     short loc_804866F
.text:0804866D                 mov     al, bl
.text:0804866F
.text:0804866F loc_804866F:                            ; CODE XREF: func_4+11j
.text:0804866F                                         ; func_4+1Bj
.text:0804866F                 dec     ecx
.text:08048670                 cmp     ecx, 0FFFFFFFFh
.text:08048676                 jnz     short loc_8048666
.text:08048678                 xor     al, 0Eh
.text:0804867A                 push    eax             ; seed
.text:0804867B                 call    _srand
.text:08048680                 call    _rand
.text:08048685                 and     eax, 3Fh
.text:0804868A                 leave
.text:0804868B                 retn    8
.text:0804868B func_4          endp
</pre>

It contains two library calls that IDA identifies as <tt>_srand</tt> and <tt>_rand</tt>. The former <a href="http://www.cplusplus.com/reference/cstdlib/srand/">initializes the random number generator</a>, the latter <a href="http://www.cplusplus.com/reference/cstdlib/rand/">generates a random integer between 0 and <tt>RAND_MAX</tt></a>. This is the <tt>func_4</tt> in C++:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
#include <stdlib.h>  /* for srand and rand */
int func_4(char* pseudo, int pseudo_length)
{
    int res = pseudo[0];
    for(int i = 0; i < pseudo_length; i++)
        if(pseudo[i] > res)
            res = pseudo[i];
    srand(res ^0xE);
    return rand() & 0x3F;
}
</pre>

<h2>Key's Fifth Character</h2>
The next block still offers nothing new:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:08048569                 mov     edi, [esp]
.text:0804856C                 push    edi
.text:0804856D                 mov     edi, [esp+8]
.text:08048571                 push    edi
.text:08048572                 call    func_5
.text:08048577                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:0804857C                 add     ebx, eax
.text:0804857E                 mov     dl, [ebx]
.text:08048580                 mov     edi, [esp+8]
.text:08048584                 add     edi, 4
.text:0804858A                 mov     dh, [edi]
.text:0804858C                 cmp     dl, dh
.text:0804858E                 jnz     exit
</pre>

It's yet another one of our checks:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_5_rv = func_5(pseudo, pseudo_length);
if( clef[4] != hardcoded_str[func_5_rv] )
    exit(1); // we failed
</pre>

The routine <tt>func_5</tt> is:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:0804868E func_5          proc near               ; CODE XREF: main+122p
.text:0804868E
.text:0804868E pseudo          = dword ptr  8
.text:0804868E pseudo_length   = dword ptr  0Ch
.text:0804868E
.text:0804868E                 push    ebp
.text:0804868F                 mov     ebp, esp
.text:08048691                 xor     ebx, ebx
.text:08048693                 mov     esi, [ebp+pseudo]
.text:08048696                 mov     ecx, [ebp+pseudo_length]
.text:08048699                 dec     ecx
.text:0804869A                 jmp     loc_80486BC
.text:0804869F ; ---------------------------------------------------------------------------
.text:0804869F
.text:0804869F loc_804869F:                            ; CODE XREF: func_5+34j
.text:0804869F                 xor     edx, edx
.text:080486A1                 mov     dl, [esi]
.text:080486A3                 push    ecx
.text:080486A4                 push    ebx
.text:080486A5                 push    2
.text:080486AA                 push    edx
.text:080486AB                 call    sub_8048708
.text:080486B0                 pop     ebx
.text:080486B1                 pop     ecx
.text:080486B2                 add     ebx, eax
.text:080486B4                 and     ebx, 0FFh
.text:080486BA                 inc     esi
.text:080486BB                 dec     ecx
.text:080486BC
.text:080486BC loc_80486BC:                            ; CODE XREF: func_5+Cj
.text:080486BC                 cmp     ecx, 0FFFFFFFFh
.text:080486C2                 jnz     short loc_804869F
.text:080486C4                 mov     eax, ebx
.text:080486C6                 xor     al, 0EFh
.text:080486C8                 and     eax, 3Fh
.text:080486CD                 leave
.text:080486CE                 retn    8
.text:080486CE func_5          endp
</pre>

With another call to a subroutine <tt>sub_8048708</tt>:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:08048708 sub_8048708     proc near               ; CODE XREF: func_5+1Dp
.text:08048708
.text:08048708 arg_0           = dword ptr  8
.text:08048708 arg_4           = dword ptr  0Ch
.text:08048708
.text:08048708                 push    ebp
.text:08048709                 mov     ebp, esp
.text:0804870B                 mov     ecx, [ebp+arg_4]
.text:0804870E                 mov     eax, 1
.text:08048713                 cmp     ecx, 0
.text:08048719                 jz      short locret_804872A
.text:0804871B                 mov     ebx, [ebp+arg_0]
.text:0804871E                 mul     ebx
.text:08048720                 jmp     loc_8048727
.text:08048725 ; ---------------------------------------------------------------------------
.text:08048725
.text:08048725 loc_8048725:                            ; CODE XREF: sub_8048708+20j
.text:08048725                 mul     ebx
.text:08048727
.text:08048727 loc_8048727:                            ; CODE XREF: sub_8048708+18j
.text:08048727                 dec     ecx
.text:08048728                 jnz     short loc_8048725
.text:0804872A
.text:0804872A locret_804872A:                         ; CODE XREF: sub_8048708+11j
.text:0804872A                 leave
.text:0804872B                 retn    8
.text:0804872B sub_8048708     endp
</pre>

This second subroutine returns <tt>arg_0</tt> raised to the power of <tt>arg_4</tt>:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
sub_8048708(arg_0, arg_4) = pow(arg_0, arg_4); // arg_0 ** arg_4
</pre>

So <tt>func_5</tt> translates to the following C code:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_5(char* pseudo, int pseudo_length)
{
    int res = 0;
    for(int i = 0; i < pseudo_length; i++) 
    {
        res += pseudo[i]*pseudo[i]; // sub_8048708(pseudo[i], 2)
    }
    return (res ^ 0xEF) & 0x3F;
}
</pre>


<h2>Key's Sixth Character</h2>
Finally we get a snippet that looks slightly different:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:08048594                 mov     edi, [esp+4]    ; edi = pseudo
.text:08048598                 xor     edx, edx        ; edx = 0
.text:0804859A                 mov     dl, [edi]       ; dl = pseudo[0]
.text:0804859C                 push    edx             ; arg0 = pseudo[0]
.text:0804859D                 call    func_6
.text:080485A2                 mov     ebx, offset hardcoded_str ; "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU"...
.text:080485A7                 add     ebx, eax
.text:080485A9                 mov     dl, [ebx]
.text:080485AB                 mov     edi, [esp+8]
.text:080485AF                 add     edi, 5
.text:080485B5                 mov     dh, [edi]
.text:080485B7                 cmp     dl, dh          ; clef[5] == hardcoded_str[func_6_rv]
.text:080485B9                 jnz     exit
</pre>

This time the subroutine <tt>func_6</tt> takes the first character of <tt>pseudo</tt> as the only parameter:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_6_rv = func_6(pseudo[0]);
if( clef[5] != hardcoded_str[func_6_rv] )
    exit(1); // we failed
</pre>

Here's <tt>func_6</tt>:

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080486D1 func_6          proc near               ; CODE XREF: main+14Dp
.text:080486D1
.text:080486D1 pseudo_0        = dword ptr  8
.text:080486D1
.text:080486D1                 push    ebp
.text:080486D2                 mov     ebp, esp
.text:080486D4                 xor     eax, eax
.text:080486D6                 mov     esi, [ebp+pseudo_0]
.text:080486D9                 cmp     esi, 0
.text:080486DF                 jz      short loc_80486FF
.text:080486E1                 call    _rand
.text:080486E6                 mov     ecx, [ebp+pseudo_0]
.text:080486E9                 jmp     loc_80486F5
.text:080486EE ; ---------------------------------------------------------------------------
.text:080486EE
.text:080486EE loc_80486EE:                            ; CODE XREF: func_6+25j
.text:080486EE                 push    ecx
.text:080486EF                 call    _rand
.text:080486F4                 pop     ecx
.text:080486F5
.text:080486F5 loc_80486F5:                            ; CODE XREF: func_6+18j
.text:080486F5                 dec     ecx
.text:080486F6                 jnz     short loc_80486EE
.text:080486F8                 and     eax, 0FFh
.text:080486FD                 xor     al, 0E5h
.text:080486FF
.text:080486FF loc_80486FF:                            ; CODE XREF: func_6+Ej
.text:080486FF                 and     eax, 3Fh
.text:08048704                 leave
.text:08048705                 retn    4
.text:08048705 func_6          endp
</pre>

The snippet just takes <tt>n</tt> random numbers and returns the last one, where <tt>n</tt> is the ASCII code of our letter <tt>pseudo[0]</tt>:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
int func_6(char pseudo0)
{
    int res = 0;
    for(int i = 0; i < pseudo0; i++)
        res = rand();
    return (res ^ 0xE5) & 0x3F;
}
</pre>

<h2>The Goodboy Message</h2>
If we passed all 6 tests for the characters in <tt>clef</tt> we get to this snippet: 

<pre class="nums:false nums-toggle:false lang:asm highlight:0 decode:true " >
.text:080485BF                 push    offset aBravo   ; "Bravo !!\n"
.text:080485C4                 call    _printf
.text:080485C9                 xor     eax, eax
.text:080485CB                 leave
.text:080485CC                 retn
.text:080485CC main            endp ; sp-analysis failed
</pre>

Which is prints the <tt>Bravo !!\n</tt> goodboy message before returning 0:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
printf("Bravo !!\n")
return 0;
</pre>

<h2>The Keygen</h2>
Putting together all six tests we obtain our keygenerator:

<pre class="nums:false nums-toggle:false lang:c++ decode:true highlight:0 " >
#include <stdio.h>
#include <cstring>
#include <stdlib.h> 

int func_1(int pseudo_length) 
{
    return (pseudo_length ^ 0x3B) & 0x3F;
}

int func_2(char* pseudo, int pseudo_length)
{
    int res = 0;
    for(int i = 0; i < pseudo_length; i++)
        res += pseudo[i];
    return (res ^ 0x4F) & 0x3F;
}

int func_3(char* pseudo, int pseudo_length)
{
    int res = 1;
    for(int i = 0; i < pseudo_length; i++)
        res *= pseudo[i];
    return (res ^ 0x55) & 0x3F;
}

int func_4(char* pseudo, int pseudo_length)
{
    int res = pseudo[0];
    for(int i = 0; i < pseudo_length; i++)
        if(pseudo[i] > res)
            res = pseudo[i];
    srand(res ^0xE);
    return rand() & 0x3F;
}

int func_5(char* pseudo, int pseudo_length)
{
    int res = 0;
    for(int i = 0; i < pseudo_length; i++) 
    {
        res += pseudo[i]*pseudo[i];
    }
    return (res ^ 0xEF) & 0x3F;
}

int func_6(char pseudo0)
{
    int res = 0;
    for(int i = 0; i < pseudo0; i++)
        res = rand();
    return (res ^ 0xE5) & 0x3F;
}

int main(int argc, char *argv[])
{
    if( argc != 2 ) 
        printf("usage: keygen <pseudo>\n");
    char hardcoded[] = "A-CHRDw87lNS0E9B2TibgpnMVys5XzvtOGJcYLU+4mjW6fxqZeF3Qa1rPhdKIouk";
    char* pseudo = argv[1];
    char clef[7];
    int pseudo_length = strlen(pseudo);
    clef[0] = hardcoded[func_1(pseudo_length)];
    clef[1] = hardcoded[func_2(pseudo, pseudo_length)]; 
    clef[2] = hardcoded[func_3(pseudo, pseudo_length)]; 
    clef[3] = hardcoded[func_4(pseudo, pseudo_length)]; 
    clef[4] = hardcoded[func_5(pseudo, pseudo_length)]; 
    clef[5] = hardcoded[func_6(pseudo[0])];
    clef[6] = 0;
    printf("pseudo: %s\n", pseudo);
    printf("clef: %s\n", clef);
}
</pre>
