// referee: independent recomputation of M_B, P_B for B=2^LB (table 2^LA). Different structure from s5: per-term accumulation in long double.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
int main(int argc,char**argv){ int LA=atoi(argv[1]),LB=atoi(argv[2]); uint64_t A=1ULL<<LA,B=1ULL<<LB;
 double *F=malloc(A*sizeof(double)); uint16_t *C=malloc(A*2); F[1]=0;C[1]=0; // F excludes the term 1; C counts terms <B excluding 1
 double mF=0; uint64_t aF=0; unsigned mC=0; uint64_t aC=0; uint64_t maxsteps=0;
 for(uint64_t n=2;n<B;n++){ uint64_t lim = n<A?n:A; u128 x=n; long double f=0; unsigned c=0; uint64_t st=0;
   while(1){ if(x<B){ c++; if(x&1) f+=logl(1.0L+1.0L/(3.0L*(long double)(uint64_t)x)); }
     if(x&1) x=(3*x+1)>>1; else x>>=1; st++;
     if(x<lim) break; if(st>50000000){printf("FAIL n=%llu\n",(unsigned long long)n);return 2;} }
   if(st>maxsteps)maxsteps=st;
   double fn=(double)f+F[(uint64_t)x]; unsigned cn=c+C[(uint64_t)x];
   if(n<A){F[n]=fn;C[n]=cn;}
   if(fn>mF){mF=fn;aF=n;} if(cn>mC){mC=cn;aC=n;} }
 printf("B=2^%d table 2^%d: all reach 1. M_B=%.12f at n=%llu exp=%.9f ; P_B=%u at n=%llu ; maxsteps-to-table=%llu\n",LB,LA,mF,(unsigned long long)aF,exp(mF),mC,(unsigned long long)aC,(unsigned long long)maxsteps);
 return 0; }
