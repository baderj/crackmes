#include <stdio.h>

inline int rand(int *seed)
{
  *seed = *seed*0x343fd + 0x269EC3;
  return ((*seed) >> 0x10) & 0x7FFF;
}
 
long int main (long int argc, char *argv[])
{
    unsigned char hash[16];
    unsigned char wanted_hash[] = {0xEB, 0x7D, 0x0E, 0x3C, 0x11, 0x16, 0xD1, 0x3A, 0x95, 0x01, 0x07, 0x0B, 0x26, 0x3E, 0x26, 0x36};
    unsigned int i;
    unsigned int base = 0;
    unsigned int hash1;
    unsigned int seed;
    unsigned int offset;
    unsigned int tmp;

    printf("starting to crack\n");
    int seed_end = 0;
    for( hash1 = 0; hash1 < 0xFFFFFFFF; hash1 += 1)
    {

        seed = hash1;
        if((hash1 & 0xFFFF) == 1) {
            printf("\r%x ", (hash1));
        }

        for(i = 0; i < 16; i++)
            hash[i] = 0;

        for(base = 0; base <= 2; base += 2) 
        {
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

            if(base == 0)
            {
                seed = 0x6f445a;                 
            }
        }

        tmp = rand(&seed);
        if (tmp != 0x36a)
            continue;


        tmp = (tmp<<16) + tmp;
        for(base = 0; base < 4; base++)
        {
            for(i = 0; i < 4; i++) {
                hash[base*4 + i] ^= (tmp & 0xFF);
                tmp = (tmp >> 8) | ((tmp & 0xFF) << 24);
            }
        }
        int mismatch = 0;
        for(i = 0; i < 16; i++) {
            if( hash[i] != wanted_hash[i] )
            {
                mismatch = 1;
                break;
            }
        }

        if (mismatch == 0 ) {
            printf("\nvalid hash1 is: %x\n", hash1);
        }
    }
}
