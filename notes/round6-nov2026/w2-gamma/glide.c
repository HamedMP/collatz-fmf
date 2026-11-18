// glide.c : stopping time sigma(n) = least k with T^k(n) < n, T(n)=n/2 or (3n+1)/2.
// mode 1: exhaustive records for n < 2^NMAX (odd n = 3 mod 4 only; others have sigma<=2... sigma(1 mod 4)=2, even=1)
// mode 2: hybrid structured search: n = 2^(N-M) u - 1, u < 2^M  (all-ones low part), report best sigma
// mode 3: pseudo-random N-bit odd numbers, 2^M samples, report best sigma
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static inline int sigma(u128 n, int cap){
    u128 x=n; int k=0;
    while(k<cap){
        if(x&1){ if(x > (((u128)1)<<125)) return -1; x=(3*x+1)>>1; } else x>>=1;
        k++;
        if(x<n) return k;
    }
    return cap;
}
static uint64_t s=88172645463325252ULL;
static inline uint64_t rnd(){ s^=s<<13; s^=s>>7; s^=s<<17; return s; }
int main(int argc,char**argv){
    int mode=atoi(argv[1]);
    if(mode==1){
        int NMAX=atoi(argv[2]); int best=0; int nb=3;
        uint64_t lim=1ULL<<NMAX;
        int rec_at_bits[70]={0}; uint64_t arg_at_bits[70]={0};
        for(uint64_t n=3;n<lim;n+=4){
            // quick 2-step filter: n=3 mod 4 ; further cheap filter none
            int k=sigma(n,100000);
            if(k>best){ best=k; int b=64-__builtin_clzll(n); rec_at_bits[b]=k; arg_at_bits[b]=n; }
        }
        int run=0; uint64_t a=0;
        for(int b=2;b<=NMAX;b++){ if(rec_at_bits[b]>run){run=rec_at_bits[b];a=arg_at_bits[b];} printf("N=%d max_sigma(n<2^N)=%d at n=%llu\n",b,run,(unsigned long long)a); }
    } else if(mode==2){
        int N=atoi(argv[2]), M=atoi(argv[3]); int best=0; uint64_t bu=0;
        for(uint64_t u=1;u<(1ULL<<M);u++){
            u128 n=(((u128)u)<<(N-M))-1;
            int k=sigma(n,100000); if(k>best){best=k;bu=u;}
        }
        u128 n0=(((u128)1)<<N)-1;
        printf("hybrid N=%d M=%d best sigma=%d at u=%llu ; sigma(2^N-1)=%d\n",N,M,best,(unsigned long long)bu,sigma(n0,100000));
    } else {
        int N=atoi(argv[2]), M=atoi(argv[3]); int best=0; u128 bn=0;
        for(uint64_t i=0;i<(1ULL<<M);i++){
            u128 n=(((u128)rnd())<<64|rnd()); n>>=(128-N); n|=3; n|=((u128)1)<<(N-1);
            int k=sigma(n,100000); if(k>best){best=k;bn=n;}
        }
        printf("random N=%d samples=2^%d best sigma=%d at n=%llu*2^64+%llu\n",N,M,best,(unsigned long long)(bn>>64),(unsigned long long)bn);
    }
    return 0;
}
