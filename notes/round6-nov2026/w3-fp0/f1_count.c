// f1_count.c -- exact N(Q,m) = #{c in E_{Q+m} : c < 2^Q} for the system
//   a: w->(M2*w+d)/8 on w = -d mod 8 ,  b: w->M3*w/16 on 16|w,   (M2,M3)=(9,27) or (25,125), d=+1/-1
// Enumerates E_Q top-down (exact, mod 2^Q, Q<=120), then runs the exact integer forward
// (256-bit) and histograms lambda(c)-Q, lambda(c)=max{K : c in E_K}.
// usage: f1_count Q [mult=3|5] [d=1|-1]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef unsigned __int128 u128;
static int Q; static u128 MASK; static u128 inv2, inv3; static unsigned M2, M3; static int dsg;
#define MAXM 400
typedef struct { uint64_t h[MAXM]; uint64_t n; int maxpos_life; u128 maxpos_w; } acc_t;
// 256-bit little helper
typedef struct { u128 lo, hi; } u256;
static inline int life(u128 c){ // returns lambda(c) (capped at 250); c exact integer
  if(c==0) return 100000;
  if(dsg<0 && c==1) return 100000; // fixed point of a for 3n-1 system
  u256 w; w.lo=c; w.hi=0; int bits=0;
  for(;;){
    unsigned low=(unsigned)(w.lo&15);
    int isa = dsg>0 ? ((low&7)==7) : ((low&7)==1);
    unsigned mul; int sh; unsigned add;
    if(isa){ mul=M2; sh=3; add=1; }
    else if(low==0){ mul=M3; sh=4; add=0; }
    else {
      int rem;
      if(low&1){ // odd: compare with -d mod 2^r
        unsigned t = dsg>0 ? (low+1) : (low-1); // t = w + d ; need 2^r | t
        rem = (t&1)?0:((t&2)?1:((t&4)?2:3)); if(rem>3) rem=3;
        // also w=0 mod 2^r impossible for odd except r=0
      } else { rem = (low&2)?1:((low&4)?2:3); 
        // even w could also be = -d mod 2^r only for r=0
      }
      return bits+rem;
    }
    // w = (mul*w + add*d) >> sh   (for d=-1: (mul*w-1)/8)
    u128 l0 = (uint64_t)w.lo, l1 = (uint64_t)(w.lo>>64), l2=(uint64_t)w.hi, l3=(uint64_t)(w.hi>>64);
    u128 t0 = l0*mul; u128 t1 = l1*mul + (t0>>64); u128 t2 = l2*mul + (t1>>64); u128 t3 = l3*mul + (t2>>64);
    if(t3>>62){ return -1; } // overflow guard
    w.lo = ((u128)(uint64_t)t1<<64) | (uint64_t)t0; w.hi = ((u128)(uint64_t)t3<<64)|(uint64_t)t2;
    if(add){ if(dsg>0){ w.lo+=1; if(w.lo==0) w.hi+=1; } else { if(w.lo==0) w.hi-=1; w.lo-=1; } }
    w.lo = (w.lo>>sh) | (w.hi<<(128-sh)); w.hi >>= sh;
    bits+=sh;
  }
}
static void emit(u128 c, acc_t*A){
  A->n++;
  int L=life(c);
  if(L<0){ fprintf(stderr,"overflow\n"); exit(1); }
  int m = L>=100000 ? MAXM-1 : L-Q;
  if(m<0){ fprintf(stderr,"BUG life<Q: m=%d\n",m); exit(1);} 
  if(m>=MAXM-1) m = (L>=100000)?MAXM-1:MAXM-2;
  A->h[m]++;
  if(L<100000 && L>A->maxpos_life){ A->maxpos_life=L; A->maxpos_w=c; }
}
// node: c = add + mult*z mod 2^Q for z in E_rem, rem = Q-used
static void rec(int used, u128 mult, u128 add, acc_t*A){
  int rem=Q-used;
  if(rem<4){
    emit(add&MASK,A);
    if(rem>0){ // z = -d mod 2^rem  (2^rem-1 for d=1 ; 1 for d=-1)
      u128 z = dsg>0 ? (((u128)1<<rem)-1) : 1;
      if(!(dsg<0 && rem==1)) ; 
      emit((add+mult*z)&MASK,A);
    }
    return;
  }
  // letter a: z -> (8z-d)/M2 ; letter b: z -> 16z/M3
  rec(used+3,(mult*8*inv2)&MASK,(dsg>0?(add-mult*inv2):(add+mult*inv2))&MASK,A);
  rec(used+4,(mult*16*inv3)&MASK,add,A);
}
static u128 inv_odd(u128 a){ u128 x=a; for(int i=0;i<8;i++) x*=2-a*x; return x; }
typedef struct { int used; u128 mult, add; } node_t;
static node_t *nodes; static int nn=0;
static void pre(int used,u128 mult,u128 add,int depthbits){
  if(used>=depthbits || Q-used<4){ nodes[nn++] = (node_t){used,mult,add}; return; }
  pre(used+3,(mult*8*inv2)&MASK,(dsg>0?(add-mult*inv2):(add+mult*inv2))&MASK,depthbits);
  pre(used+4,(mult*16*inv3)&MASK,add,depthbits);
}
int main(int argc,char**argv){
  Q=atoi(argv[1]); int mm = argc>2?atoi(argv[2]):3; dsg = argc>3?atoi(argv[3]):1;
  M2=mm*mm; M3=mm*mm*mm;
  MASK = Q>=128 ? ~(u128)0 : (((u128)1<<Q)-1);
  inv2=inv_odd(M2)&MASK; inv3=inv_odd(M3)&MASK;
  nodes=malloc(sizeof(node_t)*200000);
  pre(0,1,0, Q<40?Q/2:36);
  int T=omp_get_max_threads(); acc_t *accs=calloc(T,sizeof(acc_t));
  #pragma omp parallel for schedule(dynamic,1)
  for(int i=0;i<nn;i++){ rec(nodes[i].used,nodes[i].mult,nodes[i].add,&accs[omp_get_thread_num()]); }
  acc_t tot; memset(&tot,0,sizeof tot);
  for(int t=0;t<T;t++){ tot.n+=accs[t].n; for(int m=0;m<MAXM;m++) tot.h[m]+=accs[t].h[m];
    if(accs[t].maxpos_life>tot.maxpos_life){tot.maxpos_life=accs[t].maxpos_life; tot.maxpos_w=accs[t].maxpos_w;} }
  printf("# system mult=%d d=%d Q=%d  N_Q=%llu  infinite=%llu  max finite life=%d at w=0x%016llx%016llx\n",mm,dsg,Q,(unsigned long long)tot.n,
     (unsigned long long)tot.h[MAXM-1], tot.maxpos_life,(unsigned long long)(tot.maxpos_w>>64),(unsigned long long)tot.maxpos_w);
  // cumulative: N(Q,m) = #{life >= Q+m}
  uint64_t cum=0; uint64_t N[MAXM]; for(int m=MAXM-1;m>=0;m--){ cum+=tot.h[m]; N[m]=cum; }
  for(int m=0;m<MAXM-1;m++){ printf("%d %d %llu\n",Q,m,(unsigned long long)N[m]); if(N[m]==tot.h[MAXM-1]) break; }
  return 0;
}
