// w2-delta s4: "generation" counts.  E_m(L) = #{ y in [2^L, 2^(L+1)) : T^j(y) >= 2^(L-1) for all 0<=j<=m*L/2 } , m/2 = 1,1.5,2,3,4,8
// (value-based: trajectory stays above X/2 for lambda*L steps, X = 2^L).  lambda=1 is the Terras/Lagarias range.
// Build: gcc -O2 -o s4_generations s4_generations.c ; Run: taskset -c 5 ./s4_generations 12 30
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    int L1 = atoi(argv[1]), L2 = atoi(argv[2]);
    int q = argc > 3 ? atoi(argv[3]) : 3;
    static const int mult2[6] = {2, 3, 4, 6, 8, 16};      // lambda = mult2/2
    printf("# q=%d   L  log2(E_lambda)/L for lambda=1,1.5,2,3,4,8   (raw counts follow)\n", q);
    for (int L = L1; L <= L2; L++) {
        uint64_t X = 1ULL << L, lo = X >> 1, E[6] = {0};
        for (uint64_t y = X; y < 2 * X; y++) {
            u128 x = y; int j = 0, lim = 8 * L, ok = 1;
            while (j < lim) {
                x = (x & 1) ? ((u128)q * x + 1) / 2 : x / 2; j++;
                if (x < lo) { ok = 0; break; }
                if (x >> 120) { j = lim; break; }          // escaped far above: counts as surviving
            }
            int surv = ok ? lim : j - 1;                    // survived all steps <= surv
            for (int i = 0; i < 6; i++) if (surv * 2 >= mult2[i] * L) E[i]++;
        }
        printf("%2d ", L);
        for (int i = 0; i < 6; i++) printf(" %.4f", E[i] ? log2((double)E[i]) / L : 0.0);
        printf("   ");
        for (int i = 0; i < 6; i++) printf(" %lu", (unsigned long)E[i]);
        printf("\n"); fflush(stdout);
    }
    return 0;
}
