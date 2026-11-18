// referee: harmonic sums and sojourn counts for T(x)=x/2, (3x+d)/2, distinct stretch from n to first repeat
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
typedef unsigned long long u64;
static long d; static u64 N; static double *S; static unsigned char *fl; static double Xw; static int mode;
static inline u64 T(u64 x){ if(x&1){ if(x>(1ULL<<61)){fprintf(stderr,"overflow\n");exit(1);} return (3*x+d)/2;} return x/2;}
static inline double w(u64 x){ return mode? (x<=Xw?1.0:0.0) : 1.0/(double)x; }
static double direct(u64 n, int reg){ // Floyd
  u64 a=n,b=n; do{a=T(a);b=T(T(b));}while(a!=b);
  // find mu
  u64 p=n,q=a; double s=0; while(p!=q){ s+=w(p); p=T(p); q=T(q);} 
  double c=0; u64 r=p; u64 mn=p; int len=0; do{ c+=w(r); if(r<mn)mn=r; r=T(r); len++; }while(r!=p);
  if(reg){ r=p; int newc=0; do{ if(r<=N && !fl[r]){fl[r]=1;S[r]=c;newc=1;} r=T(r);}while(r!=p);
    if(newc && mode==0) printf("  d=%ld cycle min=%llu len=%d harmonic=%.6f\n",d,mn,len,c); }
  return s+c;
}
static void run(double *best,u64 *arg){
  *best=0;*arg=0;
  for(u64 n=1;n<=N;n++){ fl[n]=0; }
  for(u64 n=1;n<=N;n++){
    if(!fl[n]){
      u64 x=n; double s=0; int steps=0; int done=0;
      while(1){ s+=w(x); x=T(x); steps++; if(x<n){ S[n]=s+S[x]; done=1; break;} if(steps>3000) break; }
      if(!done){ double v=direct(n,1); if(!fl[n]) S[n]=v; }
    }
    if(S[n]>*best){*best=S[n];*arg=n;}
  }
}
int main(int argc,char**argv){
  d=atol(argv[1]); u64 Nh=strtoull(argv[2],0,10); int Lmax=atoi(argv[3]);
  u64 M = Nh > (1ULL<<Lmax)? Nh : (1ULL<<Lmax);
  S=malloc((M+1)*sizeof(double)); fl=malloc(M+1);
  double best; u64 arg;
  mode=0; N=Nh; run(&best,&arg);
  printf("d=%ld N=%llu max harmonic sum=%.6f at n=%llu\n",d,N,best,arg);
  mode=1; double worst=0;
  for(int L=6;L<=Lmax;L++){ N=1ULL<<L; Xw=(double)N; run(&best,&arg);
    double r=best/pow(Xw,0.94996); if(r>worst)worst=r;
    printf("d=%ld X=2^%d max#terms<=X = %.0f at m=%llu ratio=%.5f (count/X=%.5f)\n",d,L,best,arg,r,best/Xw); }
  printf("d=%ld worst sojourn ratio=%.5f\n",d,worst);
  return 0;
}
