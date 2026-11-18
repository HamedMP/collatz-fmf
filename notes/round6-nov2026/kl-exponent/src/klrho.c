/* klrho.c -- single-thread power iteration for the Krasikov-Lagarias system
 * L_k^NT(lambda), lambda = 2^gamma  (KL 2003, (2.5)-(2.13) with the 3^(k-1) lifts).
 *
 * Index i in [0,N), N = 3^(k-1)  <->  residue m = 3i+2 (mod 3^k).  N3 = N/3.
 *   F(c)[3u]   = A c[(12u+2)%N]  + B min3(c, 4u % N3)        (m = 2 mod 9)
 *   F(c)[3u+1] = A c[(12u+6)%N]                              (m = 5 mod 9)
 *   F(c)[3u+2] = A c[(12u+10)%N] + C min3(c, (2u+1) % N3)    (m = 8 mod 9)
 * A = 4^-gamma, B = (3/4)^gamma, C = (3/2)^gamma, min3(c,t)=min(c[t],c[t+N3],c[t+2N3]).
 * lo = min F(c)/c, hi = max F(c)/c  (Collatz-Wielandt bounds for the growth factor).
 * Floating point: this program only SEARCHES; nothing it prints is a proof.
 *
 * usage: klrho K GAMMA MAXIT TOL IN OUT [STOPLO]
 *   iterate c <- F(c)/min F(c) at fixed gamma until hi/lo-1 < TOL, or (if STOPLO
 *   given) until lo >= STOPLO, or MAXIT.  IN = "-" (all ones), a raw REAL[N] file,
 *   or a raw REAL[N/3] file (level k-1, lifted).  OUT = "-" or file for the vector
 *   c whose ratios are the printed lo/hi.
 * compile: gcc -O3 -march=native [-DUSE_FLOAT] klrho.c -lm -o klrho
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifdef USE_FLOAT
typedef float real;
#else
typedef double real;
#endif

static long N, N3;

static inline real min3(const real *c, long t)
{
    real a = c[t], b = c[t + N3], d = c[t + 2 * N3];
    real m = a < b ? a : b;
    return m < d ? m : d;
}

static void step(const real *c, real *out, double gam, double *plo, double *phi, double *pmn)
{
    const real A = (real)pow(4.0, -gam), B = (real)pow(0.75, gam), C = (real)pow(1.5, gam);
    double lo = 1e300, hi = 0, mn = 1e300;
    long j0 = 2 % N, b0 = 0, b2 = 1 % N3;
    for (long u = 0; u < N3; u++) {
        long j1 = j0 + 4; if (j1 >= N) j1 -= N;
        long j2 = j1 + 4; if (j2 >= N) j2 -= N;
        real v0 = A * c[j0] + B * min3(c, b0);
        real v1 = A * c[j1];
        real v2 = A * c[j2] + C * min3(c, b2);
        long i0 = 3 * u;
        out[i0] = v0; out[i0 + 1] = v1; out[i0 + 2] = v2;
        double r0 = (double)v0 / c[i0], r1 = (double)v1 / c[i0 + 1], r2 = (double)v2 / c[i0 + 2];
        if (r0 < lo) lo = r0; if (r1 < lo) lo = r1; if (r2 < lo) lo = r2;
        if (r0 > hi) hi = r0; if (r1 > hi) hi = r1; if (r2 > hi) hi = r2;
        if (v0 < mn) mn = v0; if (v1 < mn) mn = v1; if (v2 < mn) mn = v2;
        j0 = j2 + 4; if (j0 >= N) j0 -= N;
        b0 += 4; if (b0 >= N3) b0 -= N3;
        b2 += 2; if (b2 >= N3) b2 -= N3;
    }
    *plo = lo; *phi = hi; *pmn = mn;
}

int main(int argc, char **argv)
{
    if (argc < 7) { fprintf(stderr, "usage: klrho K GAMMA MAXIT TOL IN OUT [STOPLO]\n"); return 1; }
    int K = atoi(argv[1]);
    double gam = atof(argv[2]);
    long maxit = atol(argv[3]);
    double tol = atof(argv[4]);
    const char *in = argv[5], *outf = argv[6];
    double stoplo = argc > 7 ? atof(argv[7]) : 0;
    if (K < 3) { fprintf(stderr, "K >= 3 required (use the Python reference for k=2)\n"); return 1; }
    N = 1; for (int j = 0; j < K - 1; j++) N *= 3;
    N3 = N / 3;
    real *c = malloc(N * sizeof(real)), *d = malloc(N * sizeof(real));
    if (!c || !d) { fprintf(stderr, "malloc failed\n"); return 1; }
    if (!strcmp(in, "-")) { for (long i = 0; i < N; i++) c[i] = 1; }
    else {
        FILE *f = fopen(in, "rb"); if (!f) { perror(in); return 1; }
        fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
        if (sz == (long)(N * sizeof(real))) {
            if (fread(c, sizeof(real), N, f) != (size_t)N) return 1;
        } else if (sz == (long)(N3 * sizeof(real))) {
            if (fread(c, sizeof(real), N3, f) != (size_t)N3) return 1;
            memcpy(c + N3, c, N3 * sizeof(real)); memcpy(c + 2 * N3, c, N3 * sizeof(real));
        } else { fprintf(stderr, "bad size %ld\n", sz); return 1; }
        fclose(f);
    }
    double lo = 0, hi = 0, mn = 1; long it; int why = 0;
    for (it = 1; it <= maxit; it++) {
        step(c, d, gam, &lo, &hi, &mn);
        if (stoplo > 0 ? (lo >= stoplo) : (hi / lo - 1 < tol)) { why = 1; break; }
        if (it == maxit) break;
        real s = (real)(1.0 / mn);
        for (long i = 0; i < N; i++) d[i] *= s;
        real *t = c; c = d; d = t;
    }
    double cmn = 1e300, cmx = 0;
    for (long i = 0; i < N; i++) { if (c[i] < cmn) cmn = c[i]; if (c[i] > cmx) cmx = c[i]; }
    printf("k=%d gamma=%.12f it=%ld conv=%d lo=%.12f hi=%.12f spread=%.7f\n",
           K, gam, it, why, lo, hi, cmx / cmn);
    if (strcmp(outf, "-")) {
        real s = (real)(1.0 / cmn);
        for (long i = 0; i < N; i++) c[i] *= s;
        FILE *f = fopen(outf, "wb"); if (!f) { perror(outf); return 1; }
        if (fwrite(c, sizeof(real), N, f) != (size_t)N) { perror("write"); return 1; }
        fclose(f);
    }
    return 0;
}
