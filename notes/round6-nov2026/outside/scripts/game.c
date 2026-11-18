// Energy-game solver for the "3-adic lookahead game" on the pruned inverse 3x+1 tree.
//
// State: r = n mod 3^j, r not divisible by 3.
// Moves of the path-builder ("Max"):
//   E: n -> 2n            (edge label 0), new state 2r mod 3^j, weight -p
//   O: n -> (2n-1)/3      (edge label 1), allowed iff r mod 9 in {2,8}; the new residue is
//        known only mod 3^(j-1); the adversary ("Min") chooses the top ternary digit t.
//        weight q-p
// Max wants the running sum of weights bounded below, i.e. ones-ratio >= p/q up to O(1).
//
// g(r) = least initial credit c >= 0 from which Max can keep (credit + partial sums) >= 0
// forever.  Least fixed point of
//   g(r) = max(0, min( g(2r) + p ,  max_t g((2r-1)/3 + t*3^(j-1)) - (q-p) ))
// computed by chaotic (Gauss-Seidel) iteration from g = 0 along the reverse doubling cycle.
// If g exceeds CAP we declare failure ("no certificate at this j for this p/q").
//
// usage: game j p q [cap] [dumpfile]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef int32_t val_t;

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: game j p q [cap] [dumpfile]\n"); return 2; }
    int j = atoi(argv[1]);
    long p = atol(argv[2]), q = atol(argv[3]);
    long cap = argc > 4 ? atol(argv[4]) : 2000000;
    const char *dump = argc > 5 ? argv[5] : NULL;
    uint64_t N = 1; for (int i = 0; i < j; i++) N *= 3;
    uint64_t N3 = N / 3;
    uint64_t inv2 = (N + 1) / 2;
    val_t *g = calloc(N, sizeof(val_t));
    if (!g) { fprintf(stderr, "alloc fail\n"); return 2; }
    uint64_t nstates = 2 * N3;
    int sweep = 0; int failed = 0;
    clock_t t0 = clock();
    for (;;) {
        uint64_t changed = 0; val_t mx = 0;
        uint64_t r = 1;               // we update g[r/2] using g[r]
        val_t gr = g[1];
        for (uint64_t it = 0; it < nstates; it++) {
            uint64_t s = (r * inv2) % N;   // s = r/2, so 2s = r
            long best = (long)gr + p;      // E move
            unsigned m9 = s % 9;
            if (m9 == 2 || m9 == 8) {
                uint64_t b = (2 * s - 1) / 3;   // < N3*... reduce mod N3
                b %= N3;
                val_t a0 = g[b], a1 = g[b + N3], a2 = g[b + 2 * N3];
                val_t am = a0 > a1 ? a0 : a1; if (a2 > am) am = a2;
                long alt = (long)am - (q - p);
                if (alt < best) best = alt;
            }
            if (best < 0) best = 0;
            if (best > g[s]) { g[s] = (val_t)best; changed++; }
            if (g[s] > mx) mx = g[s];
            gr = g[s]; r = s;
        }
        sweep++;
        if (mx > cap) { failed = 1; break; }
        if (!changed) break;
        if (sweep % 50 == 0) { fprintf(stderr, "  sweep %d changed %llu max %d\n", sweep, (unsigned long long)changed, mx); }
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    val_t mx = 0; for (uint64_t r = 0; r < N; r++) if (r % 3 && g[r] > mx) mx = g[r];
    printf("j=%d p/q=%ld/%ld=%.6f %s sweeps=%d maxcredit=%d time=%.1fs\n", j, p, q, (double)p / q,
           failed ? "FAIL(cap)" : "OK", sweep, mx, secs);
    if (!failed && dump) {
        FILE *f = fopen(dump, "wb");
        fwrite(g, sizeof(val_t), N, f); fclose(f);
    }
    free(g);
    return failed ? 1 : 0;
}
