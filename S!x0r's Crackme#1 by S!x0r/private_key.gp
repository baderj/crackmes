/* 
    1) Install Pari/GP with
            apt-get install pari-gp
    2) Run with
           gp -q private_key.gp
*/

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

/* AD08D0361CC7FE8D1D3EAC5A68394C95 as decimal */
n = 230002204674084418548395124071717227669; /* modulus n=p*q with two distinct primes p and q */
d = rsa_private_key(e, n);
print("private key is: ", d)
quit()


