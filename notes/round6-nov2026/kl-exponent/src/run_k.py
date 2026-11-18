#!/usr/bin/env python3
"""Search driver (floating point, NOT a proof): locate gamma_k = log2(lambda_k) for
L_k^NT by a secant iteration on the Collatz-Wielandt growth factor rho(gamma), then
write two integer certificates

  cert/k{K}_lower : weights w with  w <= F_gamma(w)   at gamma_lo  (feasible point)
  cert/k{K}_upper : weights w with  F_gamma(w) < w    at gamma_hi  (no feasible point)

for src/check_cert.py to verify in exact integer arithmetic.  gamma = num / 2^40.

usage: run_k.py K GAMMA_GUESS [--float] [--margin M] [--warm FILE]
"""
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
T = 40


def F_small(c, gam):
    """reference map for k = 2 only (N = 3, residues 2, 5, 8 mod 9)."""
    A, B, C = 4.0 ** -gam, 0.75 ** gam, 1.5 ** gam
    cb = min(c)
    # m=2: 4m=8 -> idx 2 ; m=5: 4m=20=2 -> idx 0 ; m=8: 4m=32=5 -> idx 1
    return [A * c[2] + B * cb, A * c[0], A * c[1] + C * cb]


def rho_k2(gam, tol):
    c = [1.0, 1.0, 1.0]
    for _ in range(200000):
        f = F_small(c, gam)
        r = [x / y for x, y in zip(f, c)]
        if max(r) / min(r) - 1 < tol:
            break
        mn = min(f)
        c = [x / mn for x in f]
    mn = min(c)
    return min(r), max(r), np.array([x / mn for x in c])


class Runner:
    def __init__(self, K, use_float):
        self.K = K
        self.exe = os.path.join(HERE, "klrho_f" if use_float else "klrho_d")
        self.dtype = np.float32 if use_float else np.float64
        self.tol = 4e-6 if use_float else 1e-12
        self.vec = os.path.join(ROOT, "cert", f"work_k{K}.bin")
        self.have = False

    def rho(self, gam, warm=None, tol=None, maxit=20000):
        tol = tol or self.tol
        if self.K == 2:
            lo, hi, c = rho_k2(gam, tol)
            c.astype(self.dtype).tofile(self.vec)
            return lo, hi
        src = self.vec if self.have else (warm or "-")
        out = subprocess.run([self.exe, str(self.K), f"{gam:.15f}", str(maxit), str(tol), src, self.vec],
                             capture_output=True, text=True, check=True).stdout.strip()
        print("   ", out, flush=True)
        self.have = True
        d = dict(tok.split("=") for tok in out.split())
        return float(d["lo"]), float(d["hi"])


def quantize(vec_file, dtype, out_file, small):
    mm = np.memmap(vec_file, dtype=dtype, mode="r")
    n = mm.shape[0]
    CH = 1 << 24
    cmin = min(float(mm[s0:s0 + CH].min()) for s0 in range(0, n, CH))
    spread = max(float(mm[s0:s0 + CH].max()) for s0 in range(0, n, CH)) / cmin
    if small:
        bits = 52 - max(0, math.ceil(math.log2(spread)))   # exact doubles -> exact ints
        w = np.rint(np.asarray(mm, dtype=np.float64) / cmin * float(1 << bits)).astype(np.uint64)
        w.astype("<u8").tofile(out_file)
        return "<u8", spread
    bits = 31 - math.ceil(math.log2(spread))
    with open(out_file, "wb") as f:
        for s0 in range(0, n, CH):
            w = np.rint(mm[s0:s0 + CH].astype(np.float64) * (float(1 << bits) / cmin))
            assert w.max() < 2 ** 32 and w.min() >= 1
            w.astype("<u4").tofile(f)
    return "<u4", spread


def main():
    K = int(sys.argv[1])
    g0 = float(sys.argv[2])
    use_float = "--float" in sys.argv
    margin = float(sys.argv[sys.argv.index("--margin") + 1]) if "--margin" in sys.argv else None
    warm = sys.argv[sys.argv.index("--warm") + 1] if "--warm" in sys.argv else None
    small = K <= 16
    if margin is None:
        margin = 2e-8 if small else 1e-5
    os.makedirs(os.path.join(ROOT, "cert"), exist_ok=True)
    R = Runner(K, use_float)
    # secant on f(g) = log(rho(g))
    ga = g0
    lo, hi = R.rho(ga, warm)
    fa = math.log(math.sqrt(lo * hi))
    gb = ga + fa / 0.45
    for _ in range(12):
        lo, hi = R.rho(gb)
        fb = math.log(math.sqrt(lo * hi))
        if abs(fb) < (2e-7 if use_float else 1e-11) or fb == fa:
            break
        ga, fa, gb = gb, fb, gb - fb * (gb - ga) / (fb - fa)
    gstar = gb - fb / 0.45
    print(f"k={K} gamma* ~ {gstar:.9f}  lambda* ~ {2 ** gstar:.8f}", flush=True)
    res = {"k": K, "gamma_star_float": gstar, "lambda_star_float": 2 ** gstar}
    for mode, g in (("lower", gstar - margin), ("upper", gstar + margin)):
        num = math.floor(g * 2 ** T) if mode == "lower" else math.ceil(g * 2 ** T)
        gq = num / 2 ** T
        lo, hi = R.rho(gq)
        d = os.path.join(ROOT, "cert", f"k{K}_{mode}")
        os.makedirs(d, exist_ok=True)
        dt, spread = quantize(R.vec, R.dtype, os.path.join(d, "weights.bin"), small)
        json.dump({"k": K, "gamma_num": num, "gamma_log2den": T, "mode": mode,
                   "weights": "weights.bin", "dtype": dt}, open(os.path.join(d, "cert.json"), "w"))
        res[mode] = {"gamma": gq, "lambda": 2 ** gq, "float_lo": lo, "float_hi": hi, "spread": spread}
        print(f"  wrote {d}: gamma={gq:.10f} float ratios [{lo:.10f},{hi:.10f}] spread={spread:.6f}", flush=True)
    json.dump(res, open(os.path.join(ROOT, "cert", f"k{K}_search.json"), "w"), indent=1)
    if K >= 14:
        os.remove(R.vec)


if __name__ == "__main__":
    main()
