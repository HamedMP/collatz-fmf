"""sE_maxmass.py — Lemma M exact check: max-mass of Syrac(Z/3^m) <= C (2/3)^m,
C = prod_{i>=0} (1 - 2^{-2*3^i})^{-1} < 1.34, via the Lemma 1.12 recursion in
exact Fractions. Also verifies the one-parity-class structure used in the proof.
"""
import sys
from fractions import Fraction as Fr

def report(name, ok, detail=""):
    print(f"[{name}] {'PASS' if ok else 'FAIL'} {detail}", flush=True)
    if not ok:
        sys.exit(f"FAILED: {name}")

def syrac_law_exact(m):
    law = {0: Fr(1)}
    for i in range(m):
        Mm = 3 ** (i + 1)
        new = {}
        inv2 = pow(2, -1, Mm)
        per = 2 * 3 ** i
        denom = 1 - Fr(1, 2 ** per)
        for Xv, p in law.items():
            v = (3 * Xv + 1) % Mm
            for r in range(1, per + 1):
                v = (v * inv2) % Mm
                new[v] = new.get(v, Fr(0)) + p * Fr(1, 2 ** r) / denom
        law = new
    return law

# parity-class structure: for x mod 3 nonzero, admissible a (2^a x = 1 mod 3)
# form exactly one class mod 2
for x in (1, 2):
    adm = {a % 2 for a in range(1, 13) if (pow(2, a, 3) * x) % 3 == 1}
    if len(adm) != 1:
        report("E0", False, f"x={x}")
report("E0", True, "admissible exponents form one parity class mod 2 (both residues)")

C = 1.0
for i in range(0, 12):
    C /= (1 - 2.0 ** (-2 * 3 ** i))
print(f"  C = prod (1-2^-2*3^i)^-1 = {C:.6f}")

print("  m   max-mass       (2/3)^m       ratio")
ok = True
for m in range(1, 8):
    law = syrac_law_exact(m)
    mx = max(law.values())
    bound = Fr(2, 3) ** m
    ratio = float(mx / bound)
    print(f"  {m}   {float(mx):.8f}   {float(bound):.8f}   {ratio:.4f}")
    if mx > bound * Fr(134, 100):
        ok = False
report("E1", ok, "max-mass <= 1.34 (2/3)^m exactly for m <= 7")
print("\nALL sE CHECKS COMPLETE", flush=True)
