// referee-g2: brute force of (P): max of v2(rho+t*3^nu)/(log(2+max(|rho|,|t|))*log(nu+2)^2), |rho|,|t|<=B, 1<=nu<=NU
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
int main(int argc,char**argv){int B=argc>1?atoi(argv[1]):1024,NU=argc>2?atoi(argv[2]):200;
 double best=0,bestn=0;int br=0,bt=0,bn=0,bv=0; int maxv=0,mr=0,mt=0,mn=0; int nr=0,ntt=0,nn=0,nv=0;
 unsigned __int128 p=1; 
 for(int nu=1;nu<=NU;nu++){p*=3; /* mod 2^128 */
  double l2=log(nu+2.0)*log(nu+2.0);
  for(int t=-B;t<=B;t++){if(!t)continue;
   unsigned __int128 tp=(unsigned __int128)(__int128)t*p;
   for(int r=-B;r<=B;r++){if(!r)continue;
    unsigned __int128 x=tp+(unsigned __int128)(__int128)r;
    int v;
    if(x==0){ /* exact zero possible only if 3^nu<=B; otherwise v>=128: flag */
      if(nu<=6) continue; printf("FLAG v>=128 r=%d t=%d nu=%d\n",r,t,nu); continue;}
    uint64_t lo=(uint64_t)x; if(lo) v=__builtin_ctzll(lo); else v=64+__builtin_ctzll((uint64_t)(x>>64));
    int M=abs(r)>abs(t)?abs(r):abs(t);
    double q=v/(log(2.0+M)*l2);
    if(q>best){best=q;br=r;bt=t;bn=nu;bv=v;}
    double qn=v/log(2.0+M); /* without the log^2 nu factor */
    if(qn>bestn){bestn=qn;nr=r;ntt=t;nn=nu;nv=v;}
    if(v>maxv){maxv=v;mr=r;mt=t;mn=nu;}
   }}}
 printf("B=%d NU=%d\nmax ratio %.4f at rho=%d t=%d nu=%d v2=%d\n",B,NU,best,br,bt,bn,bv);
 printf("max v2/log(2+max) = %.4f at rho=%d t=%d nu=%d v2=%d\n",bestn,nr,ntt,nn,nv);
 printf("max v2 = %d at rho=%d t=%d nu=%d\n",maxv,mr,mt,mn);return 0;}
