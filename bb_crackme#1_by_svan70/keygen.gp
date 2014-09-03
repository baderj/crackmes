/* 
    1) Install Pari/GP with
            apt-get install pari-gp
    2) Run with
           gp -q keygen.gp
*/

rsa_decrypt(c, d, n) = {
    /* c is the cyphertext
       d is the private key
       n is the modulus 

       returns plaintext m */
    m = lift(Mod(c,n)^d);
    return(m);
}

rsa_private_key(e, n) = {
    /* e is the public key
       n is the modulus 
       
       returns: private key d */

    /* factor n */
    f = factorint(n);

    /* check if m has exactly two prime factors */
    nrfacs = sum(i=1,matsize(f)[1], f[i,2]);
    if(nrfacs != 2, return(Str("n has ", nrfacs, " factors (not 2)!")););

    /* get factors p*q = n */
    p = f[1,1];
    q = f[2,1];

    /* euler totient */
    phi_n = (p-1)*(q-1); 

    /* make sure 1 < e < phi_n */
    if(e >= phi_n, return(Str("e is larger than phi(n)")););

    /* determine private key d as d = e^-1 mod phi_n */
    d = (1/e) % phi_n;
    return(d);

}

e = 2^16+1;         /* public key */
n = 4073628529;     /* modulus n=p*q with two distinct primes p and q */

d = rsa_private_key(e, n);
m1 = rsa_decrypt(120076516, d, n);
m2 = rsa_decrypt(1841478100, d, n);
m3 = rsa_decrypt(987884830, d, n);


print(Str(m1,"-",m2,"-",m3););
quit()



