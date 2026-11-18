// visits.c -- d_X(a) = #{n<=X : orbit of n (3n+1 map) passes through a}/X for a<=A.  usage: visits X A
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
int main(int c,char**v){ long X=atol(v[1]),A=atol(v[2]); long *V=calloc(A+1,sizeof(long)), *V2=calloc(A+1,sizeof(long));
  for(long n=1;n<=X;n++){ u128 x=n; for(;;){ if(x<=(u128)A){ V[(long)x]++; if(n<=X/10)V2[(long)x]++; } if(x==1)break; if(x&1)x=(3*x+1)>>1; else x>>=1; } }
  printf("# a  a%%9  d_X(a)  a*d_X(a)  a*d_{X/10}(a)\n");
  double mn=1e9,mx=0; long amn=0,amx=0;
  for(long a=1;a<=A;a++){ double w=(double)a*V[a]/X, w2=(double)a*V2[a]/(X/10);
    if(a%3 && a>4){ if(w<mn){mn=w;amn=a;} if(w>mx){mx=w;amx=a;} }
    if(a<=64 || a>A-8) printf("%ld %ld %.6f %.4f %.4f\n",a,a%9,(double)V[a]/X,w,w2); }
  printf("over a in (4,%ld], 3 !| a: min a*d(a) = %.4f at a=%ld ; max = %.4f at a=%ld\n",A,mn,amn,mx,amx);
  double s[9]={0}; long k[9]={0}; for(long a=A/2;a<=A;a++){ s[a%9]+=(double)a*V[a]/X; k[a%9]++; }
  printf("mean of a*d(a) over a in [A/2,A] by a mod 9:"); for(int r=0;r<9;r++) printf(" %.4f",s[r]/k[r]); printf("\n");
  return 0; }
