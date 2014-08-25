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
