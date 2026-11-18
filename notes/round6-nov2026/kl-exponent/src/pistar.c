/* pistar.c -- brute-force test of Theorem T (direct induction form of the
 * Krasikov-Lagarias bound) for the maps T(n) = n/2 (n even), (P n + D)/2 (n odd),
 * P in {3,5}, D in {+1,-1}.
 *
 * pistar_a(x) := #{ n <= x : T^j(n) = a for some j >= 0 and T^i(n) <= x for 0<=i<=j }
 *   (Krasikov-Lagarias 2003, section 2; j is taken minimal, which minimises the max).
 * Predecessors of v: 2v, and (2v - D)/P when P | 2v - D.  For each a the program
 * enumerates the whole predecessor tree with height h(n) = max of the orbit segment
 * n -> a, h <= XMAX, so that pistar_a(x) = #{n : h(n) <= x} for every real x <= XMAX.
 *
 * Tested inequality, for every a in the principal class (P | 2a - D) and EVERY real
 * x in [a, XMAX]:
 *      pistar_a(x) >= c[a mod P^k] * (x/a)^gamma / (2^(E gamma) * max c),
 * E = ord_P(2) (2 for P=3, 4 for P=5).  pistar is a right-continuous step function
 * and the bound is increasing, so it suffices to compare the count on [h_i, h_{i+1})
 * with the bound at h_{i+1} (and the last count with the bound at XMAX).
 * Output: for each weight file, min over (a, x) of count/bound, separately for a on a
 * cycle and a not on a cycle, with the minimiser.  Floating point (double) is used
 * for the bound; a result is only meaningful if the min ratio is not within 1e-9 of 1.
 *
 * usage: pistar P D AMIN AMAX ASTEP XFAC XCAP  WFILE1 [WFILE2 ...]
 *   a runs over AMIN <= a <= AMAX in the principal class, taking every ASTEP-th one;
 *   XMAX = min(XFAC*a, XCAP).
 *   WFILE: text; line 1 "k gamma"; then P^(k-1) lines "residue weight".
 * compile: gcc -O3 -march=native [-DH32] pistar.c -lm -o pistar   (H32: 32-bit heights, XCAP < 2^32)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

typedef unsigned long long u64;
#ifdef H32           /* heights stored in 32 bits: requires XCAP < 2^32 (checked) */
typedef uint32_t hval;
#else
typedef u64 hval;
#endif
static int P, D;

typedef struct { int k; double gamma; u64 M; double *c; double cmax;
                 double minr[2]; u64 mina[2]; double minx[2]; } wfile;

static hval *hs; static size_t nh, caph;
static void push_h(u64 h)
{
    if (nh == caph) { caph = caph ? 2 * caph : (1 << 20); hs = realloc(hs, caph * sizeof(hval));
                      if (!hs) { fprintf(stderr, "oom\n"); exit(2); } }
    hs[nh++] = (hval)h;
}
static int cmp(const void *a, const void *b)
{ hval x = *(const hval *)a, y = *(const hval *)b; return x < y ? -1 : x > y; }

typedef struct { u64 v, h; } node;
static node *st; static size_t capst;

/* returns 1 if a is on a cycle */
static int tree(u64 a, u64 xmax)
{
    size_t sp = 0; int cyc = 0;
    nh = 0;
    st[sp++] = (node){a, a};
    while (sp) {
        node t = st[--sp];
        push_h(t.h);
        if (sp + 2 >= capst) { capst *= 2; st = realloc(st, capst * sizeof(node)); }
        u64 w = 2 * t.v;
        if (w <= xmax) {
            if (w == a) cyc = 1; else st[sp++] = (node){w, w > t.h ? w : t.h};
        }
        long long num = 2 * (long long)t.v - D;
        if (num > 0 && num % P == 0) {
            u64 b = (u64)(num / P);
            /* b can exceed v only for D=-1, v=1 (b=1); in general h = max(h, b) */
            if (b == a) cyc = 1;
            else if (b <= xmax) st[sp++] = (node){b, b > t.h ? b : t.h};
        }
    }
    qsort(hs, nh, sizeof(hval), cmp);
    return cyc;
}

int main(int argc, char **argv)
{
    if (argc < 9) { fprintf(stderr, "usage: see source\n"); return 1; }
    P = atoi(argv[1]); D = atoi(argv[2]);
    u64 amin = strtoull(argv[3], 0, 10), amax = strtoull(argv[4], 0, 10), astep = strtoull(argv[5], 0, 10);
    double xfac = atof(argv[6]); u64 xcap = strtoull(argv[7], 0, 10);
    int nw = argc - 8, E = (P == 3) ? 2 : 4;
    if (sizeof(hval) == 4 && xcap >= 4294967296ULL) { fprintf(stderr, "XCAP too large for H32\n"); return 1; }
    wfile *W = calloc(nw, sizeof(wfile));
    for (int i = 0; i < nw; i++) {
        FILE *f = fopen(argv[8 + i], "r"); if (!f) { perror(argv[8 + i]); return 1; }
        if (fscanf(f, "%d %lf", &W[i].k, &W[i].gamma) != 2) return 1;
        W[i].M = 1; for (int j = 0; j < W[i].k; j++) W[i].M *= P;
        W[i].c = calloc(W[i].M, sizeof(double));
        u64 r; double v; size_t cnt = 0;
        while (fscanf(f, "%llu %lf", &r, &v) == 2) { W[i].c[r] = v; if (v > W[i].cmax) W[i].cmax = v; cnt++; }
        if (cnt != W[i].M / P) { fprintf(stderr, "bad weight count %zu\n", cnt); return 1; }
        fclose(f);
        W[i].minr[0] = W[i].minr[1] = 1e300;
    }
    capst = 1 << 16; st = malloc(capst * sizeof(node));
    /* principal residue r0: P | 2 r0 - D */
    int r0 = -1; for (int r = 0; r < P; r++) if (((2 * r - D) % P + P) % P == 0) r0 = r;
    u64 na = 0, ncyc = 0, tot = 0, cntp = 0;
    for (u64 a = amin; a <= amax; a++) {
        if ((int)(a % P) != r0) continue;
        if (cntp++ % astep) continue;
        double xm = xfac * (double)a; u64 xmax = xm > (double)xcap ? xcap : (u64)xm;
        if (xmax < a) continue;
        int cyc = tree(a, xmax);
        na++; ncyc += cyc; tot += nh;
        for (int i = 0; i < nw; i++) {
            double ca = W[i].c[a % W[i].M];
            if (ca <= 0) { fprintf(stderr, "no weight for a=%llu\n", a); return 1; }
            double Dc = ca / (pow(2.0, E * W[i].gamma) * W[i].cmax), g = W[i].gamma, ia = 1.0 / (double)a;
            double mr = 1e300, mx = 0;
            for (size_t j = 1; j <= nh; j++) {
                double xr = j < nh ? (double)hs[j] : (double)xmax;
                if (j < nh && hs[j] == hs[j - 1]) continue;       /* not a constancy interval */
                double q = (double)j / (Dc * pow(xr * ia, g));
                if (q < mr) { mr = q; mx = xr; }
            }
            if (mr < W[i].minr[cyc]) { W[i].minr[cyc] = mr; W[i].mina[cyc] = a; W[i].minx[cyc] = mx; }
        }
    }
    printf("map (%dn%+d)/2: tested %llu targets a in [%llu,%llu] (%llu on a cycle), xmax=min(%g a, %llu), %llu tree nodes\n",
           P, D, na, amin, amax, ncyc, xfac, xcap, tot);
    for (int i = 0; i < nw; i++) {
        printf("  k=%d gamma=%.7f M=%.6f :", W[i].k, W[i].gamma, W[i].cmax);
        if (W[i].minr[0] < 1e299) printf(" non-cycle min ratio %.6f (a=%llu, x->%.0f)", W[i].minr[0], W[i].mina[0], W[i].minx[0]);
        if (W[i].minr[1] < 1e299) printf(" ; cycle min ratio %.6f (a=%llu, x->%.0f)", W[i].minr[1], W[i].mina[1], W[i].minx[1]);
        printf("\n");
    }
    return 0;
}
