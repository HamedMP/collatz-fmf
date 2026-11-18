// Brute force for the F_2[x] Collatz map in the Alon-Behajaina-Paran S_3 form:
// S_3(F) = (x+1)F with its leading term removed.  t(F) = #steps to reach 1.
// For each degree n: tau(n) = max t(F) over F of degree n with F(0)=1, argmax, count of maximisers, mean.
// (t_min(f) = 2 t(hat f) + deg f for odd f, so sigma(d) = 2 tau(d) + d.)
// usage: f2max nmin nmax
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc, char **argv) {
    int n0 = atoi(argv[1]), n1 = atoi(argv[2]);
    for (int n = n0; n <= n1; n++) {
        uint64_t top = 1ULL << n, best = 0, arg = 0, cnt = 0; double sum = 0;
        for (uint64_t mid = 0; mid < (n >= 1 ? top >> 1 : 1); mid++) {
            uint64_t F = n == 0 ? 1 : (top | (mid << 1) | 1);
            uint64_t t = 0;
            while (F != 1) {
                uint64_t G = F ^ (F << 1);
                int d = 63 - __builtin_clzll(G);
                F = G ^ (1ULL << d);
                t++;
            }
            sum += t;
            if (t > best) { best = t; arg = top | (mid << 1) | 1; cnt = 1; } else if (t == best) cnt++;
        }
        printf("n=%d tau=%llu tau/n=%.3f argmax=", n, (unsigned long long)best, (double)best / n);
        for (int i = n; i >= 0; i--) putchar(((arg >> i) & 1) ? '1' : '0');
        printf(" #max=%llu mean=%.3f mean/n=%.4f\n", (unsigned long long)cnt, sum / (n >= 1 ? (double)(top >> 1) : 1), sum / (n >= 1 ? (double)(top >> 1) : 1) / n);
        fflush(stdout);
    }
}
