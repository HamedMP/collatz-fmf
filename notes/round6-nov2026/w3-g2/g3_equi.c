// g3_equi.c -- equidistribution of z_v = T^L(y_v) = 3^a + tau_v modulo 2^m over all v of length L, weight a (w3-g2)
// usage: g3_equi L alo ahi M     prints, for each a in [alo,ahi] and m<=M: N, chi2, dof, z-score, TV, noise-TV
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int L, alo, ahi, M; static u64 **H;
static void dfs(int j,int a,u128 t,u128 p){
    if(a>ahi || a+(L-j)<alo) return;
    if(j==L){ u128 z=t+p; H[a-alo][(u64)z & ((1ULL<<M)-1)]++; return; }
    u128 t0=t,t1=t+p;
    if(t0&1){ dfs(j+1,a+1,(3*t0+1)>>1,3*p); dfs(j+1,a,t1>>1,p);} 
    else    { dfs(j+1,a,t0>>1,p); dfs(j+1,a+1,(3*t1+1)>>1,3*p);} 
}
int main(int c,char**v){
    L=atoi(v[1]);alo=atoi(v[2]);ahi=atoi(v[3]);M=atoi(v[4]);
    H=malloc((ahi-alo+1)*sizeof(u64*));
    for(int i=0;i<=ahi-alo;i++) H[i]=calloc(1ULL<<M,sizeof(u64));
    dfs(0,0,0,1);
    printf("# L a m N chi2 dof z TV noiseTV maxdev/sd\n");
    for(int i=0;i<=ahi-alo;i++){
        for(int m=M;m>=1;m--){
            u64 n=1ULL<<m; double N=0; for(u64 k=0;k<n;k++) N+=H[i][k];
            double e=N/n, chi=0, tv=0, mx=0;
            for(u64 k=0;k<n;k++){ double d=H[i][k]-e; chi+=d*d/e; tv+=fabs(d); if(fabs(d)/sqrt(e)>mx) mx=fabs(d)/sqrt(e);} 
            tv/=2*N; double dof=n-1;
            printf("%d %d %d %.0f %.1f %.0f %.2f %.3e %.3e %.2f\n",L,i+alo,m,N,chi,dof,(chi-dof)/sqrt(2*dof),tv,sqrt(n/(2*M_PI*N)),mx);
            // fold to m-1
            for(u64 k=0;k<n/2;k++) H[i][k]+=H[i][k+n/2];
        }
    }
    return 0;
}
