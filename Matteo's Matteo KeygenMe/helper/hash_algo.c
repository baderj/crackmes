#include <stdio.h>

inline int rand(int *seed) {
  *seed = *seed*0x343fd + 0x269EC3;
  return ((*seed) >> 0x10) & 0x7FFF;
}
 
long int main (long int argc, char *argv[]) {
    unsigned char hash[16];
    unsigned int i;
    unsigned int base = 0;
    unsigned int seed1 = 0x0110469A;
    unsigned int seed2 = 0x006C7972;
    unsigned int seed = seed1;
    unsigned int offset;
    unsigned int tmp;

    for(i = 0; i < 16; i++)
        hash[i] = 0;

    for(base = 0; base <= 2; base += 2) {
        for(i = 0; i < 4; i++)
        {
            do 
            {
                offset = rand(&seed) % 4;
            } while ( hash[base + offset*4] != 0 || hash[base + offset*4 + 1] != 0 );
            tmp = rand(&seed);
            hash[base + offset*4 + 1] += (tmp >> 8); 
            hash[base + offset*4] += (tmp & 0xFF); 
        }

        tmp = rand(&seed);
        for(i = 0; i < 4; i++) {
            hash[i*4 + 1] ^= (tmp >> 8);
            hash[i*4] ^= tmp & 0xFF;
        }

        if(base == 0) {
            seed2 ^= tmp;
            seed = seed2;
        }
    }

    tmp = rand(&seed);
    tmp = (tmp<<16) + tmp;
    for(base = 0; base < 4; base++) {
        for(i = 0; i < 4; i++) {
            hash[base*4 + i] ^= (tmp & 0xFF);
            tmp = (tmp >> 8) | ((tmp & 0xFF) << 24);
        }
    }

    printf("hash is:\n");
    for(i = 0; i < 16; i++)
        printf("%x ", hash[i]);
    printf("\n");
}
