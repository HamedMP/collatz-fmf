# Exact-rational cross-check of every numerical constant certified in
# lean/CollatzFMF/Const{Count,H,Cycle,Odd,Refine}.lean.  Run:
#   /home/matrix/home/projects/collatz/venv/bin/python crosscheck.py
from fractions import Fraction as F
from math import comb, exp

S = 3

def bad(s, L, a):                      # Lean: Const.BadA
    return 2**(L+a) < 3**a*(2**a+1)*2**s

def bcount(s, L):                      # Lean: Const.bcount
    return sum(comb(L, a) for a in range(L+1) if bad(s, L, a))

def bcount_odd(s, L):                  # Lean: Const.bcountOdd  (= bo_{L+1})
    return sum(comb(L, a) for a in range(L+1) if bad(s, L+1, a+1))

W = [5005, 4004, 3276, 2730, 2310, 1980, 1716]
def chunk_num(c, b):                   # Lean: Const.chunkNum
    return 24024*b + sum(W[j]*min(b, (j+1)*c) for j in range(7))

def run(s, f, M):                      # Lean: run s f M (prow M) 0
    return sum(2**(M+f-L)*bcount(s, L) for L in range(M, M+f))
def run_odd(s, f, M):                  # Lean: runOdd s f M (prow M) 0
    return sum(2**(M+f)*F(bcount_odd(s, M+i), 2**(M+i+1)) for i in range(f))
def run_c(s, f, m):                    # Lean: runC s f m (prow (m+3)) 0
    return sum(2**(m+f)*F(chunk_num(2**(m+i), bcount(s, m+i+3)), 2**(m+i+1)) for i in range(f))

def T(x): return x//2 if x % 2 == 0 else (3*x+1)//2
def oc(L, x):
    c = 0
    for _ in range(L):
        c += x % 2; x = T(x)
    return c

if __name__ == "__main__":
    # brute-force guards for the count identities (levels up to 13)
    for L in range(0, 14):
        blk = range(2**L, 2**(L+1))
        assert sum(1 for n in blk if bad(S, L, oc(L, n))) == bcount(S, L)
        if L >= 1:
            assert sum(1 for n in blk if n % 2 == 1 and bad(S, L, oc(L, n))) == bcount_odd(S, L-1)
    assert bcount(S, 9) == 382 and bcount(S, 4) == 15 and bcount_odd(S, 2) == 4
    # chunk bound dominates the true maximum
    for l in range(0, 6):
        c = 2**l
        for b in range(0, 8*c+1):
            assert sum(F(1, 8*c+i) for i in range(b)) <= F(chunk_num(c, b), 360360*c)
    # kernel-evaluated inequalities
    r0, r32, r71 = run(S, 300, 0), run(S, 268, 32), run(S, 229, 71)
    assert 22499*2**300 <= r0*1000 <= 22500*2**300
    assert r32*1000 <= 5027*2**300
    assert 1029*2**300 <= r71*1000 <= 1030*2**300
    ro = run_odd(S, 268, 31)
    assert 3143*2**299 <= ro*1000 <= 3144*2**299
    rc = run_c(S, 297, 0)
    assert 169425*360360*2**297 <= rc*2*10000 <= 169426*360360*2**297
    assert run(S, 3, 0) == 3*8
    assert 120*29**300*5000 <= 23*30**300
    tail = F(46, 10000)
    q = F(3, 4)                        # 1 - 2/2^3
    # constants
    print("exact masses:", float(F(r0, 2**300)), float(F(r32, 2**300)), float(F(r71, 2**300)),
          "odd32:", float(F(ro, 2**299)), "chunk0:", float(rc*2/(360360*2**297)))
    H0 = (F(225046, 10000) + 1)/q;          assert H0 <= F(1567, 50);  print("theoremH_3134:", float(H0))
    H71 = (F(10346, 10000) + F(72, 2**71))/q; assert H71 <= F(69, 50); print("harmonic_ge_71:", float(H71))
    H32 = (F(50316, 10000) + F(33, 2**32))/q; assert H32 <= F(671, 100); print("harmonic_ge_32:", float(H32))
    Href = (F(199472, 10000) + 1)/q;        assert Href <= F(2793, 100); print("theoremH_2793:", float(Href))
    assert 3 + F(169426, 10000) + tail <= F(199472, 10000)
    eps = F(33, 2**32) + 497*F(2, 2**32)
    U = (F(50316, 10000) + eps)/q;          assert U/3 <= F(5591, 2500); print("U32:", float(U))
    Wo = F(31486, 10000) + eps + F(1, 4)*U; assert Wo/3 <= F(16087, 10000); print("Wodd32:", float(Wo))
    MB = 0.2256541127
    print("residue_split_32      : exp(5591/2500) =", exp(5591/2500),
          " x exp(M_B) =", exp(MB+5591/2500), " x 4/3 =", 4/3*exp(MB+5591/2500))
    print("residue_split_32_odd  : exp(16087/10000) =", exp(1.6087),
          " x exp(M_B) =", exp(MB+1.6087), " x 4/3 =", 4/3*exp(MB+1.6087))
    print("exp(23/50) =", exp(0.46), " exp(1567/150) =", exp(1567/150), " exp(931/100) =", exp(9.31))
    print("ALL CHECKS PASSED")
