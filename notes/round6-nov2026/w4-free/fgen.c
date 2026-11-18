// F(x) = T^{floor(log2 x)}(x).  Generation counts of consecutive non-descending F-steps.
// N_k(L) = #{x in [2^L,2^(L+1)) : F^{j+1}(x) >= F^j(x) for all j<k}
// M_k(L) = independent-generations prediction: sum over x in bad_{k-1} of beta(level(F^{k-1}(x))),
//          beta(l) = P(Bin(l,1/2) >= amin(l)), amin(l) = least a with 3^a >= 2^l.
// usage: fgen Lmin Lmax
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
#define KMAX 16
#define LCAP 118
static double beta[LCAP+2];
static int lvl(u128 y){int l=0; while(y>>1){y>>=1;l++;} return l;}
int main(int argc,char**argv){
  int Lmin=atoi(argv[1]),Lmax=atoi(argv[2]);
  // beta via exact binomials in long double
  for(int l=0;l<=LCAP;l++){
    int amin=(int)ceill(l/log2l(3.0L)-1e-12L); // least a with a*log2(3) >= l
    long double s=0,c=1; // C(l,a)/2^l
    for(int a=0;a<=l;a++){ if(a>0) c=c*(l-a+1)/a; if(a>=amin) s+=c; }
    beta[l]=(double)(s/powl(2.0L,l));
  }
  for(int L=Lmin;L<=Lmax;L++){
    u64 N[KMAX+1]={0}; double M[KMAX+1]={0}; u64 over=0; int best=0; u64 bestx=0;
    u64 lo=1ULL<<L, hi=1ULL<<(L+1);
    #pragma omp parallel
    {
      u64 n[KMAX+1]={0}; double m[KMAX+1]={0}; u64 ov=0; int b=0; u64 bx=0;
      #pragma omp for schedule(static)
      for(u64 x=lo;x<hi;x++){
        u64 y=x; for(int i=0;i<L;i++) y=(y&1)?(3*y+1)>>1:y>>1;
        if(y<x) continue;
        n[1]++; int k=1; u128 z=y;
        while(k<KMAX){
          int l=lvl(z); if(l>LCAP){ov++;break;}
          m[k+1]+=beta[l];
          u128 w=z; for(int i=0;i<l;i++) w=(w&1)?(3*w+1)>>1:w>>1;
          if(w<z) break;
          k++; n[k]++; z=w;
        }
        if(k>b){b=k;bx=x;}
      }
      #pragma omp critical
      { for(int k=0;k<=KMAX;k++){N[k]+=n[k];M[k]+=m[k];} over+=ov; if(b>best||(b==best&&bx<bestx)){best=b;bestx=bx;} }
    }
    M[1]=beta[L]*(double)lo;
    printf("L=%d beta=%.6g maxstreak=%d at x=%llu overflow=%llu\n",L,beta[L],best,bestx,over);
    for(int k=1;k<=KMAX&&(N[k]||M[k]>0.5);k++) printf("  k=%d N=%llu model=%.1f ratio=%.4f log2N/L=%.4f\n",k,N[k],M[k],M[k]>0?N[k]/M[k]:0.0,N[k]?log2((double)N[k])/L:0.0);
    fflush(stdout);
  }
  return 0;
}
