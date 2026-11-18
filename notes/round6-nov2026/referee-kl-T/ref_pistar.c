// Referee brute force of pi*_a(x) from the definition. Generalised map T(n)=n/2 (even), (P n + D)/2 (odd).
// usage: ref_pistar P D X amin amax amod ares gamma1 gamma2 ...
// For each a in [amin,amax], a%amod==ares: enumerate all n with h(n)<=X where h(n)=max of orbit n..a (first hit of a).
// Output: a, N=pi*_a(X), then for each gamma: inf over x in [a,X] of pi*_a(x)/(x/a)^gamma and the x where it occurs
// (inf attained as left-limit at a jump point, or at x=X); also min over x at jump points (value AT jump).
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef unsigned long long u64;
static u64 *H; static size_t nH, capH;
static u64 *stn,*sth; static size_t sp, capS;
static void pushH(u64 h){ if(nH==capH){capH=capH?capH*2:1<<16; H=realloc(H,capH*8);} H[nH++]=h; }
static void pushS(u64 n,u64 h){ if(sp==capS){capS=capS?capS*2:1<<16; stn=realloc(stn,capS*8); sth=realloc(sth,capS*8);} stn[sp]=n; sth[sp]=h; sp++; }
static int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b; return x<y?-1:x>y;}
int main(int argc,char**argv){
  long P=atol(argv[1]), D=atol(argv[2]); u64 X=strtoull(argv[3],0,10);
  u64 amin=strtoull(argv[4],0,10), amax=strtoull(argv[5],0,10), amod=strtoull(argv[6],0,10), ares=strtoull(argv[7],0,10);
  double XF=getenv("XF")?atof(getenv("XF")):1.0; int ng=argc-8; double g[16]; for(int i=0;i<ng;i++) g[i]=atof(argv[8+i]);
  for(u64 a=amin;a<=amax;a++){ if(a%amod!=ares) continue;
    nH=0; sp=0; pushS(a,a);
    while(sp){ sp--; u64 n=stn[sp],h=sth[sp]; pushH(h);
      // predecessors p with T(p)=n, p!=a (first hit), h(p)=max(p,h)
      u64 p=2*n; if(p<=X && p!=a) pushS(p,p>h?p:h);
      // odd p with (P p + D)/2 = n  => p=(2n-D)/P
      long long num=(long long)(2*n)-D; if(num>0 && num%P==0){ p=num/P; if((p&1) && p<=X && p!=a) pushS(p,p>h?p:h); }
    }
    qsort(H,nH,8,cmp);
    printf("%llu %zu",a,nH);
    for(int gi=0;gi<ng;gi++){
      double best=1e300,bestj=1e300; u64 bx=0,bjx=0; 
      for(size_t i=0;i<nH;i++){
        if(i>0 && H[i]==H[i-1]) continue; if((double)H[i]<XF*a) continue;
        // just before jump at H[i]: count = i  (i>=1 unless H[i]==a)
        if(i>0){ double r=(double)i/pow((double)H[i]/a,g[gi]); if(r<best){best=r;bx=H[i];} }
        // at the jump: count = number <= H[i]
        size_t j=i; while(j+1<nH && H[j+1]==H[i]) j++;
        double r=(double)(j+1)/pow((double)H[i]/a,g[gi]); if(r<bestj){bestj=r;bjx=H[i];}
      }
      double r=(double)nH/pow((double)X/a,g[gi]); if(r<best){best=r;bx=X+1;}
      printf(" %.9g %llu %.9g %llu",best,bx,bestj,bjx);
    }
    printf("\n");
  }
  return 0;
}
