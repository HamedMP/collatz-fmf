// budget_scan.c (track sunit; adapted from the never-run draft lemma-e/scripts/budget_scan.c)
// Records of T_k = H_k + s_k (k = 1,2,3) for the 3x+1 FMF hop map over odd 3 <= x0 < N.
// For every bit-length n of y0 = x0+1 (2^(n-1) < y0 <= 2^n): max T_k, smallest argmax, and the
// number of x0 with T_k > n (i.e. T_k > ceil(log2 y0)) and with T_k >= n+4, n+8.
// Exact unsigned 128-bit arithmetic with an overflow guard (aborts instead of wrapping).
// build: gcc -O2 -o budget_scan budget_scan.c -lm ; run: taskset -c 2 ./budget_scan 100000000
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
static inline int ctz128(u128 z) {
    uint64_t lo = (uint64_t)z;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((uint64_t)(z >> 64));
}
static u128 pow3[81];
int main(int argc, char **argv) {
    uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000ULL;
    pow3[0] = 1; for (int i = 1; i <= 80; i++) pow3[i] = pow3[i-1] * 3;
    static int best[4][70]; static uint64_t arg[4][70];
    static uint64_t cnt0[4][70], cnt4[4][70], cnt8[4][70], tot[70];
    // thresholds c: count and LAST (largest) x0 with T_k > c*log2(x0+1); float used only for this
    // exploratory tally (comparisons are far from ties except at exact powers of two, harmless here).
    static const double thr[8] = {1.2, 1.3, 1.4, 1.5, 1.75, 2.0, 2.5, 3.0};
    static uint64_t tc[4][8], tl[4][8];
    for (uint64_t x0 = 3; x0 < N; x0 += 2) {
        uint64_t y0 = x0 + 1;
        int n = 64 - __builtin_clzll(y0 - 1);        // 2^(n-1) < y0 <= 2^n
        tot[n]++;
        double L0 = log2((double)y0);
        u128 x = x0; int H = 0;
        for (int k = 1; k <= 3; k++) {
            u128 y = x + 1; int s = ctz128(y); u128 m = y >> s;
            if (s > 78 || m > (((u128)1 << 126) / pow3[s])) { fprintf(stderr, "overflow x0=%llu\n", (unsigned long long)x0); return 1; }
            u128 p = pow3[s] * m - 1; int v1 = ctz128(p);   // v-1
            x = p >> v1; H += s + v1;
            int T = H + ctz128(x + 1);
            if (T > best[k][n]) { best[k][n] = T; arg[k][n] = x0; }
            if (T > n) cnt0[k][n]++;
            if (T >= n + 4) cnt4[k][n]++;
            if (T >= n + 8) cnt8[k][n]++;
            if (T > 1.2 * L0) for (int j = 0; j < 8; j++) if (T > thr[j] * L0) { tc[k][j]++; tl[k][j] = x0; }
        }
    }
    printf("# k n maxT argmax_x0 maxT/log2(x0+1) maxT-n  #(T>n) #(T>=n+4) #(T>=n+8) #x0_in_band\n");
    for (int k = 1; k <= 3; k++)
        for (int n = 3; n < 70; n++) if (tot[n])
            printf("%d %d %d %llu %.4f %d %llu %llu %llu %llu\n", k, n, best[k][n], (unsigned long long)arg[k][n],
                   best[k][n] / log2((double)arg[k][n] + 1.0), best[k][n] - n,
                   (unsigned long long)cnt0[k][n], (unsigned long long)cnt4[k][n], (unsigned long long)cnt8[k][n],
                   (unsigned long long)tot[n]);
    printf("# exceptional sets Exc(k,delta) = {odd 3<=x0<N : T_k > (1+delta) log2(x0+1)}: k 1+delta count largest_x0\n");
    for (int k = 1; k <= 3; k++) for (int j = 0; j < 8; j++)
        printf("E %d %.2f %llu %llu\n", k, thr[j], (unsigned long long)tc[k][j], (unsigned long long)tl[k][j]);
    return 0;
}
