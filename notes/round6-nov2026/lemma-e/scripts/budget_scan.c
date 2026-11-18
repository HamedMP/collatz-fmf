// Brute-force records of T_k = H_k + s_k (k = 1,2,3) for the 3x+1 FMF hop map.
// For each bit-length n of y0 = x0+1 (2^(n-1) < y0 <= 2^n) prints max T_k and the
// smallest argmax x0.  Exact 128-bit integer arithmetic; aborts on overflow risk.
// build: gcc -O2 -o budget_scan budget_scan.c ; run: ./budget_scan 32
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static inline int ctz128(u128 z) {
    uint64_t lo = (uint64_t)z;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((uint64_t)(z >> 64));
}
static u128 pow3[81];
int main(int argc, char **argv) {
    int nb = argc > 1 ? atoi(argv[1]) : 28;
    pow3[0] = 1; for (int i = 1; i <= 80; i++) pow3[i] = pow3[i-1] * 3;
    static int best[4][70]; static uint64_t arg[4][70];
    uint64_t N = 1ULL << nb;
    for (uint64_t x0 = 3; x0 < N; x0 += 2) {
        int n = 64 - __builtin_clzll(x0);            // 2^(n-1) <= x0 < 2^n, y0=x0+1 in (2^(n-1),2^n]
        u128 x = x0; int H = 0;
        for (int k = 1; k <= 3; k++) {
            u128 y = x + 1; int s = ctz128(y); u128 m = y >> s;
            if (s > 80 || (m >> 1) > (((u128)1 << 126) / pow3[s])) { fprintf(stderr, "overflow x0=%llu\n", (unsigned long long)x0); return 1; }
            u128 p = pow3[s] * m - 1; int v1 = ctz128(p);   // v-1
            x = p >> v1; H += s + v1;
            int T = H + ctz128(x + 1);
            if (T > best[k][n]) { best[k][n] = T; arg[k][n] = x0; }
        }
    }
    for (int k = 1; k <= 3; k++)
        for (int n = 2; n <= nb; n++)
            printf("%d %d %d %llu\n", k, n, best[k][n], (unsigned long long)arg[k][n]);
    return 0;
}
