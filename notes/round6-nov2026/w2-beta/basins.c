// basins.c -- generalized qn+d map T(n)=n/2 (even), (q n + d)/2 (odd), on positive integers.
// Labels every n<=N by (mode 0) the cycle it falls into [label = index of cycle, by cycle minimum],
// or (mode C>0) by its first-passage point Pass_C(n) = first orbit element <= C  (label = that element).
// Label 0xFFFF = orbit exceeded 2^120 (treated as "escape").
// Output: counts per label at checkpoints, max gap of each label per checkpoint window,
//         residue profile mod 9 and mod 8 at N.
// usage: basins q d N C
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef int64_t i64;
#define ESC 0xFFFF
int main(int argc,char**argv){
  i64 q=atoll(argv[1]), d=atoll(argv[2]), N=atoll(argv[3]), C=atoll(argv[4]);
  uint16_t *lab=malloc((N+1)*sizeof(uint16_t));
  i64 cycmin[4096]; int ncyc=0;
  u128 cap=((u128)1)<<120;
  int nlab;
  if(C>0){ nlab=C+1; }
  for(i64 n=1;n<=N;n++){
    if(C>0 && n<=C){ lab[n]=(uint16_t)n; continue; }
    u128 x=n; uint16_t L=ESC; 
    u128 tort=x; i64 power=1, lam=0;   /* Brent cycle detection: cycles whose minimum exceeds n are possible for 3n+d */
    for(;;){
      if(x&1) x=(q*x+d)>>1; else x>>=1;
      if(x<(u128)n){ L=lab[(i64)x]; break; }
      if(x>cap){ L=ESC; break; }
      lam++;
      if(x==tort){ /* on a cycle: find its minimum */
        u128 mn=x, z=x; do{ if(z&1) z=(q*z+d)>>1; else z>>=1; if(z<mn)mn=z; }while(z!=x);
        if(C>0){fprintf(stderr,"cycle above C at %lld\n",(long long)n); L=ESC-1;}
        else { int f=-1; for(int i=0;i<ncyc;i++) if(cycmin[i]==(i64)mn) f=i; if(f<0){ cycmin[ncyc]=(i64)mn; f=ncyc++; } L=f; }
        break; }
      if(lam==power){ tort=x; power*=2; lam=0; }
    }
    lab[n]=L;
  }
  if(C==0){ nlab=ncyc; printf("# cycles (by minimum):"); for(int i=0;i<ncyc;i++) printf(" [%d]=%lld",i,(long long)cycmin[i]); printf("\n"); }
  // checkpoints
  i64 *cnt=calloc(nlab+2,sizeof(i64)), *last=calloc(nlab+2,sizeof(i64)), *gap=calloc(nlab+2,sizeof(i64)), *gappos=calloc(nlab+2,sizeof(i64));
  i64 esc=0; static i64 hist[70000][40]; memset(hist,0,sizeof(hist));
  i64 cps[64]; int ncp=0; for(i64 p=1000;p<=N;p*=10){ cps[ncp++]=p; if(2*p<=N)cps[ncp++]=2*p; if(5*p<=N)cps[ncp++]=5*p; }
  int ci=0;
  int show = (C==0)? nlab : 0;
  for(i64 n=1;n<=N;n++){
    uint16_t L=lab[n];
    if(L>=ESC-1){esc++;}
    else { cnt[L]++; { i64 g=n-last[L]-1; if(g>0 && L<70000){int b=0; while((g>>b)>1)b++; hist[L][b]++;} } if(n-last[L]-1>gap[L]){gap[L]=n-last[L]-1; gappos[L]=last[L]+1;} last[L]=n; }
    if(ci<ncp && n==cps[ci]){
      if(C==0){
        printf("X=%lld esc=%lld(%.6f)",(long long)n,(long long)esc,(double)esc/n);
        for(int i=0;i<show;i++) printf(" | c%d: dens=%.6f maxgap=%lld@%lld",i,(double)cnt[i]/n,(long long)gap[i],(long long)gappos[i]);
        printf("\n");
      }
      ci++;
    }
  }
  { int lo=(C==0)?0:(int)(C/2+1), hi=(C==0)?(nlab<8?nlab:8):(C<=64?(int)C+1:lo);
    for(int i=lo;i<hi;i++){ printf("gaphist label %d (bin b = gaps in [2^b,2^(b+1))):",(C==0)?i:i); for(int b=0;b<40;b++){ if(b>30)break; printf(" %lld",(long long)hist[i][b]);} printf("\n"); } }
  if(C==0){
    // residue profiles, normalised: (count in class)/(count of label) * modulus  (==1 means equidistributed)
    int mods[4]={3,9,27,8};
    for(int mi=0;mi<4;mi++){ int m=mods[mi];
      for(int i=0;i<show && i<8;i++){
        i64 *rc=calloc(m,sizeof(i64)); i64 tot=0;
        for(i64 n=1;n<=N;n++) if(lab[n]==i){rc[n%m]++;tot++;}
        if(tot<1000){free(rc);continue;}
        printf("profile c%d mod %d:",i,m); double mx=0,mn=1e9;
        for(int r=0;r<m;r++){ double v=(double)rc[r]*m/tot; if(m<=9)printf(" %.5f",v); if(v>mx)mx=v; if(v<mn)mn=v; }
        printf("  [min %.5f max %.5f]\n",mn,mx); free(rc);
      }
    }
  } else {
    // first-passage distribution pi_C(m), m in (C/2, C]; restricted to n in (C, N]
    double tot=(double)(N-C);
    printf("# first passage: m  m%%3  m%%9  pi_C(m)*C/2  maxgap\n");
    double s[3]={0,0,0}; double hmax=0; i64 hm=0; double s9[9]={0};
    for(i64 m=1;m<=C;m++){ i64 c=cnt[m]-1; double w=c/tot*(C/2.0);
      if(m<=C/2){ if(c!=0) printf("UNEXPECTED mass at m=%lld\n",(long long)m); continue; }
      s[m%3]+=c/tot; s9[m%9]+=c/tot; if(w>hmax){hmax=w;hm=m;}
      if(C<=64 || m>C-12) printf("%lld %lld %lld %.6f %lld\n",(long long)m,(long long)(m%3),(long long)(m%9),w,(long long)gap[m]);
    }
    printf("mass by m mod 3: %.6f %.6f %.6f ; esc=%.3g\n",s[0],s[1],s[2],esc/tot);
    printf("mass by m mod 9:"); for(int r=0;r<9;r++)printf(" %.6f",s9[r]); printf("\n");
    printf("H = max_m pi_C(m)*C/2 = %.6f at m=%lld\n",hmax,(long long)hm);
    // dump all for later analysis
    FILE*f=fopen(argv[5]?argv[5]:"pass.tsv","w"); for(i64 m=C/2+1;m<=C;m++) fprintf(f,"%lld\t%lld\t%lld\n",(long long)m,(long long)(cnt[m]-1),(long long)gap[m]); fclose(f);
  }
  return 0;
}
