// w2-delta s5: exact small-part constants for B2 = 2^LB2 using a table for n < 2^LA and streaming above.
//  F(n)  = sum of log(1+1/(3x)) over ODD elements x < B2 of the trajectory of n stopped at 1 (1 excluded)
//  H(n)  = sum of 1/x over ALL elements x < B2 (1 excluded);  C(n) = number of elements < B2 (1 excluded)
// Output: M = max F, Hmax = max H, P = max C over 2 <= n < B2; also verifies every n < B2 reaches 1.
// Build: gcc -O2 -o s5_small_stream s5_small_stream.c -lm ; Run: taskset -c 5 ./s5_small_stream 26 30
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    int LA = atoi(argv[1]), LB2 = atoi(argv[2]);
    uint64_t A = 1ULL << LA, B2 = 1ULL << LB2;
    double *F = malloc(A * sizeof(double)), *H = malloc(A * sizeof(double));
    uint16_t *C = malloc(A * sizeof(uint16_t));
    if (!F || !H || !C) { puts("alloc fail"); return 1; }
    F[0] = F[1] = 0; H[0] = H[1] = 0; C[0] = C[1] = 0;
    double mF = 0, mH = 0; unsigned mC = 0; uint64_t aF = 0, aH = 0, aC = 0;
    for (uint64_t n = 2; n < B2; n++) {
        uint64_t lim = n < A ? n : A;           // stop when x < lim (then table lookup)
        u128 x = n; double f = 0, h = 0; unsigned c = 0; unsigned long steps = 0;
        do {
            if (x < B2) { double xd = (double)(uint64_t)x; h += 1.0 / xd; c++; if (x & 1) f += log1p(1.0 / (3.0 * xd)); }
            x = (x & 1) ? (3 * x + 1) / 2 : x / 2;
            if (++steps > 100000000UL) { printf("no descent found for %lu\n", (unsigned long)n); return 2; }
        } while (x >= lim);
        uint64_t y = (uint64_t)x;
        double fn = f + F[y], hn = h + H[y]; unsigned cn = c + C[y];
        if (n < A) { F[n] = fn; H[n] = hn; C[n] = (uint16_t)cn; }
        if (fn > mF) { mF = fn; aF = n; }
        if (hn > mH) { mH = hn; aH = n; }
        if (cn > mC) { mC = cn; aC = n; }
        if ((n & ((1ULL << 28) - 1)) == 0) { fprintf(stderr, "n=2^28*%lu\n", (unsigned long)(n >> 28)); }
    }
    printf("B2=2^%d (table 2^%d): every 2<=n<B2 reaches 1\n", LB2, LA);
    printf("M_B   = max F = %.12f at n=%lu  (exp = %.9f)\n", mF, (unsigned long)aF, exp(mF));
    printf("H_B   = max H = %.9f at n=%lu\n", mH, (unsigned long)aH);
    printf("P_B   = max C = %u at n=%lu\n", mC, (unsigned long)aC);
    return 0;
}
