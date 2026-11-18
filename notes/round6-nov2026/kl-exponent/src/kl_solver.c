/* kl_solver.c -- monotone (Jacobi) iteration for the Krasikov-Lagarias
 * system L_k^{NT}(lambda)  (Krasikov-Lagarias 2003, eqs (2.5)-(2.13)).
 *
 * Unknowns c[i], i in [0,N), N = 3^(k-1); c[i] <-> residue m = 3i+2 mod 3^k.
 * cb[t], t in [0,N3), N3 = 3^(k-2):  cb[t] = min(c[t], c[t+N3], c[t+2N3]).
 * F(c)[i] = A*c[(4i+2) mod N] + ( i=3u   : B*cb[4u mod N3]       (m=2 mod 9)
 *                                i=3u+1 : 0                     (m=5 mod 9)
 *                                i=3u+2 : C*cb[(2u+1) mod N3] ) (m=8 mod 9)
 * with A = lambda^-2, B = lambda^(alpha-2), C = lambda^(alpha-1), alpha=log2(3).
 * Feasible  <=>  exists c>0 with c <= F(c).
 * For any c>0:  lo = min_i F(c)_i/c_i,  hi = max_i F(c)_i/c_i.
 *   lo >= 1  ==> c is feasible at lambda            (lambda_k >= lambda)
 *   hi <  1  ==> no feasible vector at lambda       (lambda_k <  lambda)
 * (floating point here is only a search; the certificate is checked elsewhere
 *  in exact integer arithmetic.)
 *
 * modes:
 *   kl_solver bisect k lam_lo lam_hi tol maxit [in.bin]  [out_prefix]
 *   kl_solver fixed  k lam maxit target_lo [in.bin|-] out.bin
 *       iterate at fixed lambda until lo >= target_lo (or maxit); write vector.
 * Vector files: raw REAL[N] (native endian), no header.
 * Compile: gcc -O3 -march=native -fopenmp [-DUSE_FLOAT] kl_solver.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>

#ifdef USE_FLOAT
typedef float real;
#else
typedef double real;
#endif

static long N, N3;
static int K;

static inline real min3(real a, real b, real c) {
    real m = a < b ? a : b;
    return m < c ? m : c;
}

/* out = F(c); returns lo,hi of F(c)/c, and min,max of out */
static void step(const real *c, real *cb, real *out, double lam,
                 double *plo, double *phi, double *pmn, double *pmx)
{
    const double alpha = log2(3.0);
    const real A = (real)pow(lam, -2.0), B = (real)pow(lam, alpha - 2.0),
               C = (real)pow(lam, alpha - 1.0);
    long t;
#pragma omp parallel for schedule(static)
    for (t = 0; t < N3; t++) cb[t] = min3(c[t], c[t + N3], c[t + 2 * N3]);

    double lo = 1e300, hi = 0, mn = 1e300, mx = 0;
#pragma omp parallel
    {
        double llo = 1e300, lhi = 0, lmn = 1e300, lmx = 0;
        long u;
#pragma omp for schedule(static) nowait
        for (u = 0; u < N3; u++) {
            long i0 = 3 * u;
            long j0 = (4 * i0 + 2) % N;      /* index of 4m for i0   */
            long j1 = j0 + 4; if (j1 >= N) j1 -= N;
            long j2 = j1 + 4; if (j2 >= N) j2 -= N;
            long b0 = (4 * u) % N3;
            long b2 = (2 * u + 1) % N3;
            real v0 = A * c[j0] + B * cb[b0];
            real v1 = A * c[j1];
            real v2 = A * c[j2] + C * cb[b2];
            out[i0] = v0; out[i0 + 1] = v1; out[i0 + 2] = v2;
            double r0 = (double)v0 / c[i0], r1 = (double)v1 / c[i0 + 1],
                   r2 = (double)v2 / c[i0 + 2];
            if (r0 < llo) llo = r0; if (r1 < llo) llo = r1; if (r2 < llo) llo = r2;
            if (r0 > lhi) lhi = r0; if (r1 > lhi) lhi = r1; if (r2 > lhi) lhi = r2;
            if (v1 < lmn) lmn = v1;   /* v1 = A*c[..] is always the candidate min? no: track all */
            if (v0 < lmn) lmn = v0; if (v2 < lmn) lmn = v2;
            if (v0 > lmx) lmx = v0; if (v1 > lmx) lmx = v1; if (v2 > lmx) lmx = v2;
        }
#pragma omp critical
        {
            if (llo < lo) lo = llo; if (lhi > hi) hi = lhi;
            if (lmn < mn) mn = lmn; if (lmx > mx) mx = lmx;
        }
    }
    *plo = lo; *phi = hi; *pmn = mn; *pmx = mx;
}

static void scale(real *c, double s)
{
    long i;
#pragma omp parallel for schedule(static)
    for (i = 0; i < N; i++) c[i] = (real)(c[i] * s);
}

/* iterate at fixed lam from *pc (uses *pd as scratch, swaps pointers).
 * stops when lo >= stop_lo  (returns +1), hi < stop_hi (returns -1),
 * or maxit reached (returns 0).  The vector in *pc on exit is the INPUT of the
 * last step (i.e. the vector whose ratios are lo/hi). */
static int iterate(real **pc, real **pd, real *cb, double lam, long maxit,
                   double stop_lo, double stop_hi, double *plo, double *phi,
                   double *pmx, long *pit, int verbose)
{
    real *c = *pc, *d = *pd;
    double lo = 0, hi = 0, mn = 1, mx = 1;
    long it;
    int res = 0;
    for (it = 1; it <= maxit; it++) {
        step(c, cb, d, lam, &lo, &hi, &mn, &mx);
        if (verbose && (it % verbose == 0))
            fprintf(stderr, "    it %ld lo-1=%.3e hi-1=%.3e\n", it, lo - 1, hi - 1);
        if (lo >= stop_lo) { res = 1; break; }
        if (hi < stop_hi) { res = -1; break; }
        /* accept d as new iterate, normalised to min = 1 */
        scale(d, 1.0 / mn);
        real *tmp = c; c = d; d = tmp;
    }
    if (it > maxit) it = maxit;
    *pc = c; *pd = d; *plo = lo; *phi = hi; *pit = it;
    /* max/min of current c */
    {
        double cmn = 1e300, cmx = 0; long i;
#pragma omp parallel for reduction(min:cmn) reduction(max:cmx)
        for (i = 0; i < N; i++) { if (c[i] < cmn) cmn = c[i]; if (c[i] > cmx) cmx = c[i]; }
        *pmx = cmx / cmn;
    }
    return res;
}

static void load(const char *fn, real *c)
{
    FILE *f = fopen(fn, "rb");
    if (!f) { perror(fn); exit(1); }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (sz == (long)(N * sizeof(real))) {
        if (fread(c, sizeof(real), N, f) != (size_t)N) { perror("read"); exit(1); }
    } else if (sz == (long)(N3 * sizeof(real))) {
        /* level k-1 vector: lift c_k[i + j*N3] = c_{k-1}[i] */
        if (fread(c, sizeof(real), N3, f) != (size_t)N3) { perror("read"); exit(1); }
        memcpy(c + N3, c, N3 * sizeof(real));
        memcpy(c + 2 * N3, c, N3 * sizeof(real));
        fprintf(stderr, "  (lifted level k-1 vector)\n");
    } else { fprintf(stderr, "bad size %ld for %s\n", sz, fn); exit(1); }
    fclose(f);
}

static void save(const char *fn, const real *c)
{
    FILE *f = fopen(fn, "wb");
    if (!f) { perror(fn); exit(1); }
    if (fwrite(c, sizeof(real), N, f) != (size_t)N) { perror("write"); exit(1); }
    fclose(f);
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: see source\n"); return 1; }
    const char *mode = argv[1];
    K = atoi(argv[2]);
    N = 1; for (int j = 0; j < K - 1; j++) N *= 3;
    N3 = N / 3;
    real *c = malloc(N * sizeof(real)), *d = malloc(N * sizeof(real)),
         *cb = malloc(N3 * sizeof(real));
    if (!c || !d || !cb) { fprintf(stderr, "malloc failed\n"); return 1; }
    long i;
    double lo, hi, mx; long it;

    if (!strcmp(mode, "bisect")) {
        double a = atof(argv[3]), b = atof(argv[4]), tol = atof(argv[5]);
        long maxit = atol(argv[6]);
        const char *in = argc > 7 ? argv[7] : "-";
        const char *outp = argc > 8 ? argv[8] : NULL;
        if (strcmp(in, "-")) load(in, c);
        else for (i = 0; i < N; i++) c[i] = 1;
        real *best = NULL; double bestlam = 0, bestmx = 0;
        if (outp) best = malloc(N * sizeof(real));
        while (b - a > tol) {
            double lam = 0.5 * (a + b);
            int r = iterate(&c, &d, cb, lam, maxit, 1.0, 1.0, &lo, &hi, &mx, &it, 0);
            printf("k=%d lam=%.10f res=%+d it=%ld lo-1=%.3e hi-1=%.3e spread=%.7f\n",
                   K, lam, r, it, lo - 1, hi - 1, mx);
            fflush(stdout);
            if (r > 0) { a = lam; if (best) { memcpy(best, c, N * sizeof(real)); bestlam = lam; bestmx = mx; } }
            else if (r < 0) b = lam;
            else { fprintf(stderr, "undecided at lam=%.10f; stopping\n", lam); break; }
        }
        printf("RESULT k=%d lam_feasible=%.10f lam_infeasible=%.10f gamma_lo=%.8f gamma_hi=%.8f\n",
               K, a, b, log2(a), log2(b));
        if (best && bestlam > 0) {
            char fn[512]; snprintf(fn, sizeof fn, "%s", outp);
            save(fn, best);
            printf("SAVED %s lam=%.10f spread=%.7f\n", fn, bestlam, bestmx);
        }
    } else if (!strcmp(mode, "fixed")) {
        double lam = atof(argv[3]);
        long maxit = atol(argv[4]);
        double target = atof(argv[5]);
        const char *in = argv[6], *out = argv[7];
        if (strcmp(in, "-")) load(in, c);
        else for (i = 0; i < N; i++) c[i] = 1;
        int r = iterate(&c, &d, cb, lam, maxit, target, 0.0, &lo, &hi, &mx, &it, 10);
        printf("k=%d lam=%.10f res=%+d it=%ld lo-1=%.3e hi-1=%.3e spread=%.7f\n",
               K, lam, r, it, lo - 1, hi - 1, mx);
        save(out, c);
    } else { fprintf(stderr, "unknown mode\n"); return 1; }
    return 0;
}
