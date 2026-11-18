// w2-delta s3: exact DP over all n < B = 2^LB.
//  Flog(n) = sum of log(1+1/(3x)) over ODD elements x < B of the trajectory n, T(n), ... (stopped at 1, 1 excluded)
//  Hall(n) = sum of 1/x over ALL elements x < B (1 excluded),  cnt(n) = number of elements < B (1 excluded)
//  Res(n)  = full residue log: sum over all odd elements (also those >= B), i.e. log( 2^K / (3^d n) )
// Also verifies that every 2 <= n < B has a finite stopping time (hence reaches 1).
// Build: gcc -O2 -o s3_small s3_small.c -lm ; Run: taskset -c 5 ./s3_small 26
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    int LB = argc > 1 ? atoi(argv[1]) : 24;
    uint64_t B = 1ULL << LB;
    double *Flog = malloc(B * sizeof(double));
    float *Hall = malloc(B * sizeof(float));
    float *Res = malloc(B * sizeof(float));
    uint16_t *cnt = malloc(B * sizeof(uint16_t));
    if (!Flog || !Hall || !Res || !cnt) { puts("alloc fail"); return 1; }
    Flog[1] = 0; Hall[1] = 0; Res[1] = 0; cnt[1] = 0; Flog[0]=Hall[0]=Res[0]=0; cnt[0]=0;
    double mF = 0, mH = 0, mR = 0; uint64_t aF = 0, aH = 0, aR = 0, aC = 0; unsigned mC = 0;
    for (uint64_t n = 2; n < B; n++) {
        u128 x = n; double f = 0, h = 0, r = 0; unsigned c = 0; unsigned long steps = 0;
        do {
            if (x & 1) { double w = log1p(1.0 / (3.0 * (double)x)); r += w; if (x < B) f += w; }
            if (x < B) { h += 1.0 / (double)x; c++; }
            x = (x & 1) ? (3 * x + 1) / 2 : x / 2;
            if (++steps > 100000000UL) { printf("no stopping time found for %lu\n", (unsigned long)n); return 2; }
        } while (x >= n);
        uint64_t y = (uint64_t)x;
        Flog[n] = f + Flog[y]; Hall[n] = (float)(h + Hall[y]); Res[n] = (float)(r + Res[y]); cnt[n] = c + cnt[y];
        if (Flog[n] > mF) { mF = Flog[n]; aF = n; }
        if (Hall[n] > mH) { mH = Hall[n]; aH = n; }
        if (Res[n] > mR) { mR = Res[n]; aR = n; }
        if (cnt[n] > mC) { mC = cnt[n]; aC = n; }
    }
    printf("B=2^%d: all 2<=n<B have finite stopping time (reach 1)\n", LB);
    printf("M_B   = max Flog = %.12f at n=%lu  (exp = %.9f)\n", mF, (unsigned long)aF, exp(mF));
    printf("max full log-residue = %.12f at n=%lu (Res = %.9f)\n", mR, (unsigned long)aR, exp(mR));
    printf("max harmonic sum over elements <B (float32 DP) = %.6f at n=%lu\n", mH, (unsigned long)aH);
    printf("P_B   = max #elements <B on one trajectory = %u at n=%lu\n", mC, (unsigned long)aC);
    return 0;
}
