/* Referee brute force for Theorem ND (independent of sD).  gcc -O2 -o brute brute.c -lm
   Part A: 3n+1, all n <= NMAX: every n>1 has an iterate < n (hence Col_min = 1 by induction):
           count failures; natural-density proportion with Col_min(n) <= f is then exactly 1.
   Part B: timed version: odd n in [N/2,N): fraction reaching <= f(N) within t*ln(n) Syracuse steps.
   Part C: litmus maps q n + d : 5n+1 and 3n-1; fraction of odd n <= N whose orbit is seen to go
           <= B before exceeding 2^100 or 5000 odd steps.
   Part D: first-passage law Pass_x(U) for uniform odd windows [y,2y) and other shapes; total
           variation between windows (exhaustive enumeration, no sampling).                       */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef unsigned long long u64;

static inline u64 syr(u64 n){ n = 3*n+1; return n >> __builtin_ctzll(n); }

static void partA(u64 NMAX){
    u64 fail=0, maxsteps=0, arg=0;
    for(u64 n=3;n<=NMAX;n+=2){            /* even n drop immediately */
        u128 m=n; u64 st=0;
        while(m>=n){ if(m&1) m=3*m+1; else m>>=1; st++; if(st>100000){fail++;break;} }
        if(st>maxsteps){maxsteps=st;arg=n;}
    }
    printf("[A] 3n+1, n<=%llu: numbers with no iterate below themselves: %llu ; longest stopping time %llu at n=%llu\n",
           NMAX,fail,maxsteps,arg);
    printf("    => Col_min(n)=1 for every n<=%llu, so #{n<=N: Col_min(n)>f}/N = 0 for any f>=1 at these scales.\n",NMAX);
}

static void partB(void){
    double ts[4]={1.0,1.1,1.25,1.5};
    printf("[B] odd n in [N/2,N): fraction with Syr^m(n) <= f(N) for some m <= t*ln(n)/ln(4/3)\n");
    printf("    N        f(N)            t=1.0     t=1.1     t=1.25    t=1.5\n");
    for(int e=4;e<=8;e++){
        u64 N=1; for(int i=0;i<e;i++) N*=10;
        double fs[3]={log(log((double)N)), log((double)N), pow(log((double)N),2)};
        const char* nm[3]={"lnln N","ln N","(ln N)^2"};
        for(int fi=0;fi<3;fi++){
            u64 cnt[4]={0,0,0,0}, tot=0; double f=fs[fi];
            for(u64 n=(N/2)|1;n<N;n+=2){
                tot++; u64 m=n; int st=0; double L=log((double)n)/log(4.0/3.0);
                while((double)m>f && st<= (int)(1.5*L)+1){ m=syr(m); st++; }
                if((double)m<=f) for(int k=0;k<4;k++) if(st<=ts[k]*L) cnt[k]++;
            }
            printf("    1e%d  %-9s=%7.2f  %.5f   %.5f   %.5f   %.5f\n",e,nm[fi],f,
                   (double)cnt[0]/tot,(double)cnt[1]/tot,(double)cnt[2]/tot,(double)cnt[3]/tot);
        }
    }
}

static void partC(void){
    printf("[C] litmus maps n -> (q n + d)/2^v on odd n; fraction of odd n<=N whose orbit reaches <= B\n");
    printf("    (orbit abandoned as 'escaped' on exceeding 2^100 or after 5000 odd steps)\n");
    int qs[3]={3,3,5}; int ds[3]={1,-1,1}; u64 Bs[2]={20,1000};
    for(int k=0;k<3;k++) for(int bi=0;bi<2;bi++) for(int e=3;e<=7;e++){
        u64 N=1; for(int i=0;i<e;i++) N*=10;
        if(k<2 && e<7 && e>3) continue;
        u64 ok=0,tot=0,esc=0; u128 LIM=((u128)1)<<100;
        for(u64 n=1;n<=N;n+=2){
            tot++; u128 m=n; int st=0; int good=0;
            while(st<5000){
                if(m<=Bs[bi]){good=1;break;}
                if(m>LIM) break;
                m = (u128)qs[k]*m + ds[k];
                while(!(m&1)) m>>=1;
                st++;
            }
            if(good) ok++; else esc++;
        }
        printf("    %dn%+d  B=%-5llu N=1e%d   reached<=B: %.6f   escaped/undecided: %.6f\n",qs[k],ds[k],Bs[bi],e,(double)ok/tot,(double)esc/tot);
    }
}

/* Part D */
static double *hist; static u64 X;
static double passhist(u64 lo, u64 hi, int logw, double *h){  /* odd N in [lo,hi); weight 1 or 1/N */
    memset(h,0,sizeof(double)*(X+2)); double tot=0;
    for(u64 n=lo|1;n<hi;n+=2){
        u64 m=n; while(m>X) m=syr(m);
        double w = logw? 1.0/(double)n : 1.0;
        h[m]+=w; tot+=w;
    }
    for(u64 i=0;i<=X;i++) h[i]/=tot;
    return tot;
}
static double tv(double*a,double*b){ double s=0; for(u64 i=0;i<=X;i++) s+=fabs(a[i]-b[i]); return s/2; }

static void partD(int lx,int ly){
    X=1ULL<<lx; u64 y=1ULL<<ly;
    double *h0=malloc(sizeof(double)*(X+2)),*h1=malloc(sizeof(double)*(X+2));
    printf("[D] x=2^%d: TV( Pass_x(U_[y,2y)) with y=2^%d , Pass_x(other window) )\n",lx,ly);
    passhist(y,2*y,0,h0);
    struct {const char*nm; u64 lo,hi; int lw;} W[]={
        {"uniform [2y,4y)",2*y,4*y,0},
        {"uniform [4y,8y)",4*y,8*y,0},
        {"uniform [1.5y,3y) (non-dyadic start)",y+y/2,3*y,0},
        {"uniform [y,1.25y)  (quarter-octave: NOT covered by Thm 5-U)",y,y+y/4,0},
        {"uniform [1.75y,2y) (top eighth: NOT covered)",y+3*(y/4),2*y,0},
        {"log-uniform [y,2y)",y,2*y,1},
        {"log-uniform [y,8y)  (Tao-type measure)",y,8*y,1},
    };
    for(int i=0;i<7;i++){ passhist(W[i].lo,W[i].hi,W[i].lw,h1); printf("    vs %-58s TV = %.5f\n",W[i].nm,tv(h0,h1)); }
    /* coarse feature: law of Pass_x/x in 8 equal bins, for the reference window and the log-uniform one */
    passhist(y,8*y,1,h1);
    printf("    P(Pass_x <= x*j/8), j=1..8  uniform[y,2y): ");
    double c=0; for(int j=1;j<=8;j++){ for(u64 i=(X*(j-1))/8+1;i<=(X*j)/8;i++) c+=h0[i]; printf("%.4f ",c);} printf("\n");
    printf("                                 log-unif[y,8y): ");
    c=0; for(int j=1;j<=8;j++){ for(u64 i=(X*(j-1))/8+1;i<=(X*j)/8;i++) c+=h1[i]; printf("%.4f ",c);} printf("\n");
    free(h0);free(h1);
}

int main(int argc,char**argv){
    u64 NMAX = argc>1? strtoull(argv[1],0,10):100000000ULL;
    partA(NMAX); fflush(stdout);
    partB(); fflush(stdout);
    partC(); fflush(stdout);
    partD(10,20); partD(12,22); partD(14,24); partD(16,24); fflush(stdout);
    return 0;
}
