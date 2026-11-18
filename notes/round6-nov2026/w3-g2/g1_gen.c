// g1_gen.c  -- generation counts by DFS over the Terras tree (w3-g2).
// E_lambda(X) = #{ y in [X,2X) : T^j(y) >= X/2 for all 0<=j<=lambda*L },  X = 2^L.
// Enumerates residues y mod 2^j bit by bit; state t = T^j(y mod 2^j), a = #odd steps, p = 3^a.
// For the true y in [2^L,2^(L+1)):  T^j(y) = t + p*((y - r_j)>>j) < t + p*2^(L-j+1), which gives the pruning.
// Leaves are re-checked by direct iteration (exact, 128-bit), recording the death time
// D(y) = min{ j : T^j(y) < X/2 }.  Output: histogram of D over the range [0, LMAXMUL*L].
// usage: g1_gen L part nparts   (splits on the low 6 bits of y: class c handled iff c % nparts == part)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
typedef uint64_t u64;
static int L; static u64 thr; static int JMAX;
static u64 *hist; static u64 nodes=0, leaves=0;
static int part, nparts;
static void leaf(u64 y){
    leaves++;
    u128 x=y; int j;
    for(j=0;j<=JMAX;j++){
        if(x<thr){ hist[j]++; return; }
        x = (x&1) ? (3*x+1)>>1 : x>>1;
    }
    hist[JMAX+1]++;   // survived all j<=JMAX
}
static void dfs(int j, u64 r, u128 t, u128 p){
    // invariant: t = T^j(r), r = y mod 2^j, p = 3^a
    nodes++;
    if(j==6 && (int)(r % (u64)nparts)!=part) return;
    // upper bound for T^j(y)
    u128 ub = t + p*((((u128)1)<<(L-j+1))-1);
    if(ub<thr) return;
    if(j==L){ leaf(r + (((u64)1)<<L)); return; }
    // child with bit j = 0: value t ; bit j = 1: value t+p
    u128 t0=t, t1=t+p;
    u128 n0 = (t0&1)? (3*t0+1)>>1 : t0>>1;
    u128 n1 = (t1&1)? (3*t1+1)>>1 : t1>>1;
    dfs(j+1, r, n0, (t0&1)? 3*p : p);
    dfs(j+1, r | (((u64)1)<<j), n1, (t1&1)? 3*p : p);
}
int main(int argc,char**argv){
    L=atoi(argv[1]); part=argc>2?atoi(argv[2]):0; nparts=argc>3?atoi(argv[3]):1;
    int mul = argc>4?atoi(argv[4]):8;
    thr=((u64)1)<<(L-1); JMAX=mul*L;
    hist=calloc(JMAX+2,sizeof(u64));
    dfs(0,0,0,1);
    printf("L %d part %d/%d nodes %llu leaves %llu\n",L,part,nparts,(unsigned long long)nodes,(unsigned long long)leaves);
    for(int j=0;j<=JMAX+1;j++) if(hist[j]) printf("D %d %llu\n",j,(unsigned long long)hist[j]);
    return 0;
}
