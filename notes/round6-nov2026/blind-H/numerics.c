// numerics: max harmonic sum and max #{x_k<=X}/X^eta over distinct stretches from n<=N
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int cmp(const void*a,const void*b){uint64_t x=*(uint64_t*)a,y=*(uint64_t*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){
  uint64_t N=argc>1?strtoull(argv[1],0,10):10000000ULL;
  int sgn=argc>2?atoi(argv[2]):1; // +1: 3x+1, -1: 3x-1
  double eta; {double t=log(2)/log(3); eta=-(t*log2(t)+(1-t)*log2(1-t));}
  double *H=malloc((N+1)*sizeof(double));
  double bestH=0; uint64_t argH=0; double bestR=0; uint64_t argR=0, argX=0; int maxlen=0;
  uint64_t CAP=1ULL<<20; static uint64_t buf[100000]; static uint64_t all[100000];
  for(uint64_t n=1;n<=N;n++){
    // harmonic sum of the distinct stretch (until first repeat). For 3x+1 we rely on convergence to 1 (verified by run),
    // for 3x-1 we detect cycles by Brent.
    u128 x=n; double s=0; int len=0,m=0;
    if(sgn==1){
      // stretch: n,...,1 then (if n==1) 2 ; if n==2: 2,1
      if(n==1){s=1.5;len=2;buf[m++]=1;buf[m++]=2;}
      else{
        int memo=0;
        while(1){
          if(x<n && !memo){ /* for count ratio we still need full list of small terms; continue explicitly */ }
          s+=1.0/(double)x; len++;
          if(x<=CAP) buf[m++]=(uint64_t)x;
          if(x==1) break;
          x=(x&1)?(3*x+1)/2:x/2;
        }
      }
    } else {
      // 3x-1: collect full stretch until repeat (cycles: 1 ; 5,7,10 ; 17-cycle). stop when hitting a cycle element twice
      int k=0;
      while(1){
        // check repeat among known cycle minima: detect by x in {1,5,17} seen before
        all[k++]=(uint64_t)x; s+=1.0/(double)x; len++;
        if(x<=CAP) buf[m++]=(uint64_t)x;
        u128 y=(x&1)?(3*x-1)/2:x/2;
        int rep=0;
        { for(int i=0;i<k;i++) if(all[i]==(uint64_t)y){rep=1;break;} }
        if(rep) break;
        x=y;
        if(k>=99999){fprintf(stderr,"too long %llu\n",(unsigned long long)n);return 1;}
      }
    }
    if(len>maxlen)maxlen=len;
    if(s>bestH){bestH=s;argH=n;}
    qsort(buf,m,sizeof(uint64_t),cmp);
    for(int i=0;i<m;i++){
      if(i+1<m && buf[i+1]==buf[i]) {fprintf(stderr,"dup at n=%llu\n",(unsigned long long)n);return 1;}
      double r=(i+1)/pow((double)buf[i],eta);
      if(r>bestR){bestR=r;argR=n;argX=buf[i];}
    }
  }
  printf("sgn=%d N=%llu eta=%.6f\n",sgn,(unsigned long long)N,eta);
  printf("max harmonic sum = %.9f at n=%llu\n",bestH,(unsigned long long)argH);
  printf("max count ratio (X<=2^20) = %.6f at n=%llu X=%llu\n",bestR,(unsigned long long)argR,(unsigned long long)argX);
  printf("max stretch length = %d ; for X>2^20 ratio <= len/2^(20 eta) = %.5f\n",maxlen,maxlen/pow(2,20*eta));
  return 0;}
