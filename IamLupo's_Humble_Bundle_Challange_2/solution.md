# Finding Master Keys

I`m using Python to decrypt the challenge, you can find the script with all steps in ``./scripts/crack.py``.


## Bytes 0-3: Local File Header Signature

These are the first few bytes of the ciphertext:

     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
    2f 45 4e 43 ad 62 1e 10 94 a0 17 ad 81 64 2e 7f
    /  E  N  C  ?  b  ?  ?  ?  ?  ?  ?  ?  d  .  ?

    16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
    b9 cc 59 77 0f 50 e6 29 1e 33 4f 31 e9 09 40 b1
    ?  ?  Y  w  ?  P  ?  )  ?  3  O  1  ?  ?  @  ?

    32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47
    e9 19 c1 94 b8 4d d0 7a 4e f4 12 dd ac c4 b4 f5
    ?  ?  ?  ?  ?  M  ?  z  N  ?  ?  ?  ?  ?  ?  ?

The first four bytes ``/ENC`` are constant magic number written by this line: 

    fwrite("/ENC", sizeof(char), 4, output_file);

The remaining bytes are the encrypted data. When I'm referring to the ciphertext I'm speaking of the bytes *without*  ``/ENC``, i.e.:

     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 
    ad 62 1e 10 94 a0 17 ad 81 64 2e 7f b9 cc 59 77 
    ?  b  ?  ?  ?  ?  ?  ?  ?  d  .  ?  ?  ?  Y  w 

    16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 
    0f 50 e6 29 1e 33 4f 31 e9 09 40 b1 e9 19 c1 94 
    ?  P  ?  )  ?  3  O  1  ?  ?  @  ?  ?  ?  ?  ? 

    32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 
    b8 4d d0 7a 4e f4 12 dd ac c4 b4 f5 7a b9 72 19 
    ?  M  ?  z  N  ?  ?  ?  ?  ?  ?  ?  z  ?  r  ? 

From the name of the encrypted file ``crackme.zip.enc`` we can guess that the ciphertext is a ZIP file. We know that the first four Bytes of a ZIP file are always ``50 4B 03 05``according to the ZIP format specification https://www.pkware.com/documents/APPNOTE/APPNOTE-6.3.0.TXT. Let's see how the encryption routine turns this known plaintext into ciphertext:

    for(unsigned int i = 0; i < 16; i++) {
        data[i] ^= generate_key[i];
    }

The encryption is a simple synchronous stream cipher with a blocksize of 16 bytes. For instance, for the first four bytes of the ciphertext we have: 

                        0  1  2  3
        plaintext:     50 4b 03 04
    XOR generate_key:  ?? ?? ?? ??
    --------------------------------
        ciphertext     ad 62 1e 10 

The unknown ``generate_key`` for the first block of 16 bytes is therefore:

                        0  1  2  3
        plaintext:     50 4b 03 04
    XOR ciphertext     ad 62 1e 10 
    --------------------------------
        generate_key:  fd 29 1d 14 

The ``generate_key`` is modified after each block of 16 Bytes by calling ``GenerateKey``. The result is based on a ``master_key``. How do we get this master key? The steps that lead to the ``generate_key`` of the first block are:

	for(unsigned int i = 0; i < 16; i++) {
        ...
		generate_key[i] = 0x00;
	}
	GenerateKey(master_key, generate_key);
	GenerateKey(master_key, generate_key);
   
To get to the ``master_key`` we need to reverse ``GenerateKey``:

    void GenerateKey(unsigned char* master_key, unsigned char* generate_key) {
        char shuffle[16] = { 0x8, 0xA, 0x0, 0x1, 0x9, 0xC, 0xF, 0x3, 0x6, 0x2, 0xD, 0xE, 0x4, 0x2, 0x5, 0x7 };
        
        for(unsigned int i = 0; i < 5; i++) {
            for(unsigned int j = 0; j < 16; j++) {
                unsigned int nr = (unsigned int)generate_key[j];
                generate_key[j] = (shuffle[(nr / 16)] * 0x10) + shuffle[(nr % 16)];
            }
            
            for(unsigned int j = 0; j < 16; j++) {
                generate_key[j] = (((unsigned int)generate_key[j]) + (unsigned int)master_key[j]) & 0xFF;
            }
        }
    }

This function does a lot of shuffling around and it would be tedious to write a routine that reverses the function. Fortunately, the function operates one character at a time: the value ``generate_key[i]`` depends only on the initial value of ``generate_key[i]`` and ``master_key[i]`` - the other elements of ``generate_key`` and ``master_key`` have no influence on ``generate_key[i]``. Also, the transformation is the same for all elements of ``generate_key``. Let's rewrite the function as:

    unsigned char TransformByte(unsigned char mc, unsigned char gc) {
        char shuffle[16] = { 0x8, 0xA, 0x0, 0x1, 0x9, 0xC, 0xF, 0x3, 0x6, 0x2, 0xD, 0xE, 0x4, 0x2, 0x5, 0x7 };
        unsigned int nr = (unsigned int)gc
        gc = (shuffle[(nr / 16)] * 0x10) + shuffle[(nr % 16)];
        gc = (((unsigned int)gc) + (unsigned int)mc) & 0xFF;
        return gc;
    }

    void GenerateKey(unsigned char* master_key, unsigned char* generate_key) {
        
        for(unsigned int i = 0; i < 5; i++) {
            for(unsigned int j = 0; j < 16; j++) {
                generate_key[i] = TransformByte(master_key[i], generate_key[i]);
            }
        }
    }

To reverse ``TransformByte`` we only need to calculate the result for all 256 potential values of the master key character given the initial ``generate_key``, then compare the result to the desired ``generate_key`` result and see if they match. Of course we can easily reverse multiple iterations of ``GenerateKey`` too. The following ``PotentialMasterKeys`` generates all master keys for a given plaintext-ciphertext-pair and the nr of iteration (the number of times ``GenerateKey`` was called to generate the ``generate_key`` used to encrypt the plaintext):

    def reverseTransformByte(gc_before, gc_after, nr_iterations):
        valid_mc = []
        gc = gc_before 
        for m in range(256):
            gc = gc_before 
            gc = TransformByte(gc, m, nr_iterations)
            if gc == gc_after:
                valid_mc.append(m)
        return valid_mc

    def TransformByte(g, m, nr_iterations):
        shuffle = [0x8, 0xA, 0x0, 0x1, 0x9, 0xC, 0xF, 0x3, 0x6, 0x2, 0xD, 0xE, 
                                                            0x4, 0x2, 0x5, 0x7]
        for i in range(nr_iterations*5):
            nr = g
            g = (shuffle[(nr // 16)] * 0x10) + shuffle[(nr % 16)]
            g = (g + m) & 0xFF
        return g


    def PotentialMasterKeys(plaintext, ciphertext, nr_iterations):
        generate_key = [a ^ b for a,b in zip(plaintext, ciphertext)] 
        keys = []
        for gc in generate_key:
            r = reverseTransformByte(0x0, gc, nr_iterations)
            keys.append(r)
        return keys

Let's run ``PotentialMasterKeys`` on our known plaintext (the four bytes from the ZIP header signature) and the corresponding ciphertext: 

    keys = []

    p = [0x50, 0x4B, 0x03, 0x04]     # ZIP local file header signature
    c = [0xad, 0x62, 0x1e, 0x10]     # First four bytes of ciphertext

    keys += PotentialMasterKeys(p, c, 2)
    print_key_combinations(keys)

The routine calculates multiple choices for all four bytes of the master key::

    {73,7f,93,eb}  {17,b7}  {1b,cf,d3,db}  {12,e2} 

All 4*2*4*2 master key combinations turn our four byte plaintext into the ciphertext of the challenge. 

## Bytes 4-5: Version Needed to Extract 
The next two bytes of a ZIP represent the version needed to extract. Ignoring all versions that indicate encryption leaves us with the following versions:

    1.0 - Default value
    1.1 - File is a volume label
    2.0 - File is a folder (directory)
    2.0 - File is compressed using Deflate compression
    2.1 - File is compressed using Deflate64(tm)
    2.5 - File is compressed using PKWARE DCL Implode 
    2.7 - File is a patch data set 
    4.5 - File uses ZIP64 format extensions
    4.6 - File is compressed using BZIP2 compression*
    6.3 - File is compressed using LZMA
    6.3 - File is compressed using PPMd+
    6.3 - File is encrypted using Blowfish
    6.3 - File is encrypted using Twofish

At this point I'm taking an educated guess by assuming the ZIP has been compressed using the same settings used to compress the challenge folder. The challenge zip folder has bytes ``0x14 0x00`` as the version (meaning Version 2.0). Using the same code as before gives:

    p = [0x14, 0x00]     # Version Needed to Extract 
    c = [0x94, 0xa0]     # 5th and 6th byte of the ciphertext 
    keys += PotentialMasterKeys(p, c, 2)
    print_key_combinations(keys)

    # OUTPUT:
    # ...  {54,e4}  {08,10,74,88,90}

Again we end up with multiple values for our masterkey.


## Bytes 6-7: General Purpose Bit Flag   

The next two bytes of a ZIP file are the *general purpose bit flag*. Again I'm assuming the ZIP was created with the same tool and setting as ``Humble_Bundle_Challenge_2.zip``. If it was, then the general Purpose bit flags are all zero: ``0x00 0x00`` - most ZIP files don't have any flags set, so making this assumption isn't far fetched:

    p = [0x00, 0x00]     # 
    c = [0x17, 0xad]     # First four bytes of ciphertext
    keys += PotentialMasterKeys(p, c, 2)
    print_key_combinations(keys)

    PotentialMasterKeys(p, c)

    # OUTPUT:
    # ... 56 {3f,4f}


## Bytes 32-39 - File Name (from second character on)

So far we managed to get candidates for the first 8 bytes of the master key. The problem is, we are already at 1280 combinations. Before moving on to the second half of the master key, let's try to narrow down the number of combinations we got so far. The first 8 bytes of the master key can be used to generate the next ``generate_key``, which in turn can be used to decrypt bytes 16:23. These bytes fall into the ``CRC-32`` field,  the compressed size field and the uncompressed size field of the ZIP header. While we could definitely rule out some master keys resulting in implausible sizes, let's move on the next block at bytes 32:39 where we find an even better header value:

    Offset
    30	n	File name

Since the file name is probably longer than 2 character it should span to the bytes 32+. Let's decrypt bytes 32 to 37 for all 1280 master key combinations and see which result looks like it is part of a filename. I make the assumption that the filename has an extension, and all characters are ASCII. Therefore we have two valid plaintext types:

1. The plaintext contains the "." character and all characters up to "." plus one extra character (for the extension) are ASCII.
2. The plaintext does not contain the "." character. This would mean the extension comes after byte 37 and all decrypted characters are part of the filename and must be ASCII. 

The following routine checks those two cases:

    def is_part_of_ascii_filename(s):
        """ two cases:
            - there is a dot in s -> all chars upto to dot plus one (extension)
            are ASCII chars
            - there is no dot in s -> all chars must be ASCII
        """
        if not '.' in s:
            dot_index = len(s)
        else:
            dot_index = s.index('.')
        return all(32 <= ord(c) <= 126 for c in s[:dot_index+2]) 

The next code snippet iterates over all master key combinations, decrypts the ciphertext and then checks if the result is valid according to ``is_part_of_ascii_filename``:

    def decrypt(c, m, nr_iterations):
        g = []
        for mc in m: 
            g.append(TransformByte(0x00, mc, nr_iterations))
        return [gg ^ cc for gg, cc in zip(g, c)]

    c = [0xb8, 0x4d, 0xd0, 0x7a, 0x4e, 0xf4, 0x12, 0xdd] # Bytes 32-37 of ciphertext
    valid_names = set()
    for m in itertools.product(*keys):
        p = decrypt(c, m, 4)
        fn = "".join(chr(pp) for pp in p[0:8])
        if is_part_of_ascii_filename(fn):
            valid_names.add(fn)

    for valid_name in valid_names:
        print("__{}".format(valid_name))

The output of the above script is::

    __BDMe.txt
    __BDjE.txΣ
    __BDje.txΣ
    __BDjE.txt
    __ADME.txt
    __BDMe.txΣ
    __bDjE.txΣ
    __ADME.txΣ
    __bDje.txt
    __bDjE.txt
    __ADje.txt
    __ADMe.txt
    __BDME.txt
    __bDME.txΣ
    __ADje.txΣ
    __ADMe.txΣ
    __bDME.txt
    __bDje.txΣ
    __ADjE.txt
    __BDME.txΣ
    __bDMe.txΣ
    __ADjE.txΣ
    __bDMe.txt
    __BDje.txt

The two underscores at the beginning represent the yet unknown plaintext bytes 30 and 31. The result ``__ADME.txt`` stands out because it nicely extends to:

    README.txt

Let's go with that result and see which master keys lead to ``ADME.txt``. By taking the intersection with the key combinations we already have this gives us a much reduced list of master keys:

    p = [ord(f) for f in "ADME.txt"]   # filename[2:] 
    c = [0xb8, 0x4d, 0xd0, 0x7a, 0x4e, 0xf4, 0x12, 0xdd] # Bytes 32-37 of ciphertxt
    keys2 = PotentialMasterKeys(p, c, 4)                 # These master keys produce "ADME.txt"
    keys_intersection = []

    """ ``keys`` at this point still contains the 1280 master key combinations
        derived from the first 8 bytes of the ZIP header """
    for k1, k2 in zip(keys, keys2):
        keys_intersection.append(set(k1) & set(k2))

    print_key_combinations(keys_intersection)

The output is:

    7f  17  1b  12  54  {08,10}  56  3f

So we know all but the fifth byte of the first 8 master key bytes. 


## Bytes 30-31: Start of Filename - "RE" 

From the previous section we learned that bytes 30 and 31 of the plaintext are "RE". Those bytes are generated based on bytes 14 and 15 of the master key, for which we get 16 different combinations:

    p = [ord(f) for f in "RE"]   # filename[:2]
    c = [0xc1, 0x94] # Bytes 30-31 of ciphertxt
    keys = PotentialMasterKeys(p, c, 3)
    print_key_combinations(keys)

    # OUTPUT:
    # {20,50,56,70}  {39,8f,af,f9}


## Bytes 12-13: File Last Modification Date

Bytes 12 and 13 represent the *file last modification date*. The crackme gives the hint **One important hint you need to crack this challange is that this challange originally started at 16 September 2014 - 07:20 AM.**, so we can assume that the ZIP content was created Sept. 16th 2014. The MS-DOS time for this date - in little endian order - is ``30 45``:

    def time_and_date(d):
        t = d.timetuple()
        time = (t.tm_hour << 11) + (t.tm_min << 5) + (t.tm_sec/2)
        date = ((t.tm_year-1980) << 9) + (t.tm_mon << 5) + (t.tm_mday)
        return [ time&0xFF, (time&0xFF00) >> 8, date&0xFF, (date&0xFF00) >> 8]

    d = datetime.strptime( "2014-09-16 07:20:00", "%Y-%m-%d %H:%M:%S")
    print(["{:02x}".format(h) for h in time_and_date(d)[2:]])  # only output date

    # OUTPUT:
    # ['30', '45']

This leads to the following bytes 12 and 13 of the master key:

    p = [0x30, 0x45] # Bytes 12-13: file last modification date
    c = [0xb9, 0xcc] # Bytes 12-13 of ciphertxt
    keys = PotentialMasterKeys(p, c, 2)
    print_key_combinations(keys)

    # OUTPUT:
    # {07,57}  {07,57}


## Bytes 28-29: Extra field length (m)

The previous section left us with 4 master key combinations. We can eliminate 3 of those by looking at the next block: Bytes 28 and 29 represent the length of the extra field. Given the four master key combinations from the previous section we get these potential values of the extra field:

    p = [0x30, 0x45] # Bytes 12-13: file last modification date
    c = [0xb9, 0xcc] # Bytes 12-13 of ciphertxt
    keys = PotentialMasterKeys(p, c, 2)
    c = [0xe9, 0x19] # Bytes 28-29 of ciphertext (extra field length)
    for m in itertools.product(*keys):
        p = decrypt(c, m, 3)
        print([hex(mm) for mm in m], (p[0] << 8) + p[1])

    # Output
    (['0x7', '0x7'], 61440)
    (['0x7', '0x57'], 61680)
    (['0x57', '0x7'], 0)
    (['0x57', '0x57'], 240)

The ``Humble_Bundle_Challange_2.zip`` doesn't have an extra field and the length is set to zero. Setting the master key bytes 12 and 13 to ``57 07`` also results in an extra field length of 0. Although 240 also seems like a valid extra field length, it would be a huge coincidence that one of our four potential master key combos gives a master key length of 0 by chance. This fixes the master key bytes 12 an 13 to:

    57 07


## Bytes 8-9: Compression method

Bytes 8 and 9 represent the compression method. Removing the reserved choices gives the following potential values:

    0 - The file is stored (no compression)
    1 - The file is Shrunk
    2 - The file is Reduced with compression factor 1
    3 - The file is Reduced with compression factor 2
    4 - The file is Reduced with compression factor 3
    5 - The file is Reduced with compression factor 4
    6 - The file is Imploded
    7 - Reserved for Tokenizing compression algorithm
    8 - The file is Deflated
    9 - Enhanced Deflating using Deflate64(tm)
    10 - PKWARE Data Compression Library Imploding (old IBM TERSE)
    12 - File is compressed using BZIP2 algorithm
    14 - LZMA (EFS)
    18 - File is compressed using IBM TERSE (new)
    19 - IBM LZ77 z Architecture (PFS)
    97 - WavPack compressed data
    98 - PPMd version I, Rev 1

This code snippet generates the master key for all of the compression methods:

    for cm in list(range(11)) + [12, 14, 18, 19, 97, 98]:
        p = [cm, 0x00] # Bytes 8-9: compression method 
        c = [0x81, 0x64] # Bytes 8-9 of ciphertxt
        keys = PotentialMasterKeys(p, c, 2)
        print("compression method {}".format(cm))
        print_key_combinations(keys)

    # OUTPUT:
    compression method 0
    XX  {42,52,92}
    compression method 1
    {54,e4}  {42,52,92}
    compression method 2
    XX  {42,52,92}
    compression method 3
    {5c,d5}  {42,52,92}
    compression method 4
    {1d,fd}  {42,52,92}
    compression method 5
    XX  {42,52,92}
    compression method 6
    b6  {42,52,92}
    compression method 7
    XX  {42,52,92}
    compression method 8
    {07,57}  {42,52,92}
    compression method 9
    XX  {42,52,92}
    compression method 10
    XX  {42,52,92}
    compression method 12
    {1f,5b,63,9b,ff}  {42,52,92}
    compression method 14
    XX  {42,52,92}
    compression method 18
    {5a,6a}  {42,52,92}
    compression method 19
    4c  {42,52,92}
    compression method 97
    XX  {42,52,92}
    compression method 98
    aa  {42,52,92}

For many compression method there isn't a master key that generates the ciphertext. Only these method remain:

    1 - The file is Shrunk
    3 - The file is Reduced with compression factor 2
    4 - The file is Reduced with compression factor 3
    6 - The file is Imploded
    8 - The file is Deflated
    12 - File is compressed using BZIP2 algorithm
    18 - File is compressed using IBM TERSE (new)
    19 - IBM LZ77 z Architecture (PFS)
    98 - PPMd version I, Rev 1

Still, many combinations remain for bytes 8 and 9. The next section allows us to filter the potential candidates.


## Bytes 22-25: Uncompressed Size

The previous section gave many combinations for bytes 8 and 9 of the master key. We can reduce the number a little by looking at the next block, i.e., bytes 24 and 25. These two are the two most significant bytes of the four byte value ``uncompressed size``. Let's calculate the sizes that result from the master key combinations: 

for cm in list(range(11)) + [12, 14, 18, 19, 97, 98]:
    p = [cm, 0x00] # Bytes 8-9: compression method 
    c = [0x81, 0x64] # Bytes 8-9 of ciphertxt
    keys = PotentialMasterKeys(p, c, 2)
    # print("compression method {}".format(cm))
    # print_key_combinations(keys)

    keys = [[0x56],[0x3f,0x4f]] + keys # prepend masterkey bytes 6-7
    c = [0x4f, 0x31, 0xe9, 0x09] # ciphertext bytes 22-25
    for m in itertools.product(*keys):
        p = decrypt(c, m, 3)
        size = (p[3]<<24) + (p[2]<<16) + (p[1]<<8) + p[3]
        print("Compression {}, Key {}: {} Mega Bytes".format(cm, m, size/1024/1024.0))

The output is:

    Compression 1, Key (86, 63, 84, 66): 15.4375 Mega Bytes
    Compression 1, Key (86, 63, 84, 82): 1807.4375 Mega Bytes
    Compression 1, Key (86, 63, 84, 146): 2575.4375 Mega Bytes
    Compression 1, Key (86, 63, 228, 66): 14.4375 Mega Bytes
    Compression 1, Key (86, 63, 228, 82): 1806.4375 Mega Bytes
    Compression 1, Key (86, 63, 228, 146): 2574.4375 Mega Bytes
    ....


Many sizes are unreasonable, e.g., 2575 MB is way to large. Let's assume the compression rate was at most 90%, which gives a maximum uncompressed size of 360745*10. Adding the check:

    if size < 360745*10:
        print("Compression {}, Key {}: {} Mega Bytes".format(cm, m, size/1024/1024.0))

leaves the following potential master keys (the numbers in brackets are the master key values for bytes 6 to 9 in decimal notation):

    Compression 3, Key (86, 63, 213, 66): 2.0 Mega Bytes
    Compression 3, Key (86, 79, 213, 66): 2.05859375 Mega Bytes
    Compression 8, Key (86, 63, 87, 66): 0.0 Mega Bytes
    Compression 8, Key (86, 79, 87, 66): 0.05859375 Mega Bytes
    Compression 12, Key (86, 63, 91, 66): 0.25 Mega Bytes
    Compression 12, Key (86, 63, 99, 66): 2.125 Mega Bytes
    Compression 12, Key (86, 79, 91, 66): 0.30859375 Mega Bytes
    Compression 12, Key (86, 79, 99, 66): 2.18359375 Mega Bytes
    Compression 98, Key (86, 63, 170, 66): 2.1875 Mega Bytes
    Compression 98, Key (86, 79, 170, 66): 2.24609375 Mega Bytes

For now I'm not considering compression 98: ``PPMd version I, Rev 1``, and compression 18 ``IBM TERSE (new)`` - these seems like a rare choice. If in the end we don't have a master key that successfully decrypts the ZIP we can still come back and loosen the assumptions. For now, the choices for bytes 8 and 9 of the master key are:

    213, 66 
    87, 66
    91, 66
    99, 66
    170, 66

Or in Hex and using the set notation:

    {d5, 57, 5b, 63, aa} 42


## Bytes 26-27: File Name Length (n)

So far we have information for all masterkey positions except bytes 10 and 11. Those two master key bytes affect byte 10,11 of the ciphertext, which represents the *file last modification time*. The crackme says when the challenge started, but we can't assume the ZIP was created at exactly that time. So let's have a look at the next block. Bytes 26 and 27 represent the *file name length (n)*. We already know the filename is probably ``README.TXT`` which has a length of 10 Bytes, or in little endian hex ``0x0A 0x00``. This gives the following combinations for the master key bytes 10 and 11:

    p = [len("README.TXT"), 0x0] # Bytes 26-27: file name length 
    c = [0x40, 0xb1] # Bytes 26-27 of ciphertxt
    keys = PotentialMasterKeys(p, c, 3)
    print_key_combinations(keys)

    # OUTPUT
    # 3a  19

Neat! Only one combination leads to the file name length 10. Let's check if this also gives a valid time stamp:

    from datetime import datetime
    def dos_time_to_datetime(date, time):
        # little endian to big endian
        date = (date[1] << 8) + date[0]
        time = (time[1] << 8) + time[0]
        year = ((date & 0xFE00) >> 9) + 1980
        month = (date & 0x1E0) >> 5
        day = date & 0x1F
        hours = (time & 0xF800) >> 11
        mins = (time & 0x7E0) >> 5
        secs = (time & 0x1F) << 1

        return datetime(year, month, day, hours, mins, secs)

    c = [0x2e, 0x7f] # Bytes 10,11 of cipher
    for m in itertools.product(*keys): # should only be one combo
        time = decrypt(c, m, 2)
        print(dos_time_to_datetime([0x30, 0x45], time))

    # OUTPUT:
    # 2014-09-16 06:40:58

Good! The time stamp is valid and *before* 07:20. We now got information about all master key bytes and can start to brute force the combinations 


# Testing Potential Master Keys

## Summary of What we Know about the Master Key

For the first half of the master key we have the following two combinations:

    7f  17  1b  12  54  {08,10}  56  3f

For bytes 8 and 9 we have 5 choices:

    {d5, 57, 5b, 63, aa} 42

For bytes 10 and 11 we know:

    3a  19

Bytes 12 and 13 are:

    57 07

And the last two bytes 14 and 15 are one of the following 16 combinations:

    {20,50,56,70} {39,8f,af,f9}

So in total we got 2*5*4*4 = 160 different master keys.


## Brute Forcing all 160 Combinations

Which one of the 160 combinations is the correct one? I used a small (and very slow) Python script to decrypt the ``crackme.zip.enc`` for all master keys and checked with ziplib if the resulting file was a valid ZIP:

    def DecryptFile(data, master_key):
        def GenerateKey(master_key, generate_key):
            for i, mc in enumerate(master_key):
                generate_key[i] = TransformByte(generate_key[i], mc, 1)

        g = 16*[0]
        GenerateKey(master_key, g)
        GenerateKey(master_key, g)
        plaintext = []
        for i in range(0, len(data), 16):
            for j in range(16):
                if i+j < len(data):
                    plaintext.append(data[i+j] ^ g[j])
            GenerateKey(master_key, g)
        return plaintext

    keys = [[0x7f],[0x17],[0x1b],[0x12],[0x54],[0x08,0x10],[0x56],[0x3f],
            [0xd5,0x57,0x5b,0x63,0xaa],[0x42],[0x3a],[0x19],[0x57],[0x07],
            [0x20,0x50,0x56,0x70],[0x39,0x8f,0xaf,0xf9]]


    data = read_file('../ciphertext/crackme.zip.enc')[4:]
    for i, m in enumerate(itertools.product(*keys)):
        print "testing key {}...".format(i),
        plaintext = DecryptFile(data, m)
        write_file('tmp.zip', plaintext)
        try:
            zip_file = zipfile.ZipFile('tmp.zip')
        except Exception as e: 
            print("no")
            continue

        if zip_file.testzip():
            print("no")
        else:
            print("yes! Got it.")
            print("Master Key is: {}".format(" ".join(["{:02x}".format(mc) for mc in m])))
            print("You should be able to unzip tmp.zip now")

After a while I got:

    ...
    testing key 100... no
    testing key 101... no
    testing key 102... no
    testing key 103... no
    testing key 104... yes! Got it.
    Master Key is: 7f 17 1b 12 54 10 56 3f 57 42 3a 19 57 07 56 39
    You should be able to unzip tmp.zip now

The content of the ZIP is an Image and a README:

    If you read this you cracked the challange! :D
    Great job! And have fun with the humble bundle book!

    Link: https://www.humblebundle.com/?gift=m67EUEYdnfZpXY4A
    Youtube: https://www.youtube.com/watch?v=dE-sN5MUUKs&hd=1
