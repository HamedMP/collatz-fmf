// Energy-game solver, generic in the map n -> n/2 | (a n + c)/2  (a in {3,5}, c = +-1).
// Backward moves on the pruned inverse tree (nodes not divisible by a):
//   E: n -> 2n                         weight -p
//   O: n -> (2n-c)/a, allowed iff a | 2n-c and a^2 does not divide 2n-c (child not divisible by a);
//      child known only mod a^(j-1); adversary picks top digit t in {0..a-1}.   weight q-p
// g = least fixed point of g(r) = max(0, min(g(2r)+p, max_t g(b+t a^(j-1)) - (q-p))).
// Finite g  <=>  (j,p,q)-certificate exists.  Divergence declared when max g > cap
// (rigorous iff cap >= nstates*q; otherwise heuristic).
// usage: game2 a c j p q cap [dumpfile]     (quiet; prints one line; exit 0 = OK, 1 = FAIL)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef int32_t val_t;
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: game2 a c j p q cap [dumpfile]\n"); return 2; }
    int a = atoi(argv[1]), c = atoi(argv[2]), j = atoi(argv[3]);
    long p = atol(argv[4]), q = atol(argv[5]), cap = atol(argv[6]);
    const char *dump = argc > 7 ? argv[7] : NULL;
    int64_t N = 1; for (int i = 0; i < j; i++) N *= a;
    int64_t N1 = N / a, inv2 = (N + 1) / 2, a2 = (int64_t)a * a;
    int64_t nstates = N - N1;
    val_t *g = calloc(N, sizeof(val_t));
    if (!g) return 2;
    long sweep = 0; int failed = 0; val_t mx = 0;
    for (;;) {
        int64_t changed = 0; int64_t r = 1; val_t gr = g[1];
        for (int64_t it = 0; it < nstates; it++) {
            int64_t s = (r * inv2) % N;            // s = r/2 mod N
            long best = (long)gr + p;
            int64_t u = ((2 * s - c) % a2 + a2) % a2;
            if (u % a == 0 && u != 0) {
                int64_t b = (((2 * s - c) / a) % N1 + N1) % N1;   // exact division: 2s-c = u mod a^2, a | u
                val_t am = g[b];
                for (int t = 1; t < a; t++) if (g[b + t * N1] > am) am = g[b + t * N1];
                long alt = (long)am - (q - p);
                if (alt < best) best = alt;
            }
            if (best < 0) best = 0;
            if (best > g[s]) { g[s] = (val_t)best; changed++; if (best > mx) mx = (val_t)best; }
            gr = g[s]; r = s;
        }
        sweep++;
        if (mx > cap) { failed = 1; break; }
        if (!changed) break;
    }
    printf("a=%d c=%d j=%d p/q=%ld/%ld %s sweeps=%ld maxcredit=%d\n", a, c, j, p, q, failed ? "FAIL" : "OK", sweep, mx);
    if (!failed && dump) { FILE *f = fopen(dump, "wb"); fwrite(g, sizeof(val_t), N, f); fclose(f); }
    return failed;
}
