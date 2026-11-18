# Referee check of Lemma 6 and Proposition F (own implementation).
import numpy as np, math, sys
from collections import Counter

s = 0.2877607871

def v2(x):
    return (x & -x).bit_length() - 1 if x else 10 ** 9

# ---- E_k from the forward definition (r in E_k iff a compatible step leads into E_{k-3}/E_{k-4})
def E_forward(kmax):
    E = {0: {0}}
    for k in range(1, kmax + 1):
        S = set()
        for r in range(1 << k):
            ok = False
            if k < 3:
                ok = (r % (1 << k) == 7 % (1 << k)) or (r == 0)
            else:
                if r % 8 == 7:
                    # a(w) = (9w+1)/8, determined mod 2^(k-3)
                    if ((9 * r + 1) // 8) % (1 << (k - 3)) in E[k - 3]: ok = True
                if not ok:
                    if k < 4:
                        ok = (r % (1 << k) == 0)
                    elif r % 16 == 0 and ((27 * r) // 16) % (1 << (k - 4)) in E[k - 4]:
                        ok = True
            if ok: S.add(r)
        E[k] = S
    return E

def E_inverse(kmax):
    E = {0: [0], 1: [0, 1], 2: [0, 3], 3: [0, 7]}
    for k in range(4, kmax + 1):
        m = 1 << k
        i9 = pow(9, -1, m); i27 = pow(27, -1, m)
        A = [((8 * z - 1) * i9) % m for z in E[k - 3]]
        B = [(16 * z * i27) % m for z in E[k - 4]]
        E[k] = sorted(A + B)
        assert len(set(E[k])) == len(E[k])
    return E

KMAX = 40
E = E_inverse(KMAX)
Ef = E_forward(16)
for k in range(17):
    assert set(E[k]) == Ef[k], k
print("E_k inverse-branch construction == forward definition for k<=16")
N = [len(E[k]) for k in range(KMAX + 1)]
for k in range(4, KMAX + 1): assert N[k] == N[k - 3] + N[k - 4]
# projection consistency E_k mod 2^(k-1) == E_{k-1}
for k in range(1, KMAX + 1):
    assert {c % (1 << (k - 1)) for c in E[k]} == set(E[k - 1])
rat = [N[j] / 2 ** (s * j) for j in range(KMAX + 1)]
print("N_j 2^-sj range: min %.4f (j=%d) max %.4f (j=%d)" % (min(rat), rat.index(min(rat)), max(rat), rat.index(max(rat))))
# long range by recursion
NN = [1, 2, 2, 2]
for j in range(4, 5000): NN.append(NN[j - 3] + NN[j - 4])
import fractions
lo = min(math.log2(NN[j]) - s * j for j in range(5000)); hi = max(math.log2(NN[j]) - s * j for j in range(5000))
print("N_j 2^-sj over j<5000: [%.4f, %.4f]" % (2 ** lo, 2 ** hi))
assert all(NN[j + 3] <= 2 * NN[j] for j in range(4990))
assert all(NN[j + 1] >= NN[j] for j in range(4990))

# ---- Lemma 6
worst = 0
for k in range(0, KMAX + 1):
    for n in range(0, k + 1):
        c = Counter(x % (1 << n) for x in E[k])
        phi = max(c.values())
        assert phi <= 2 * N[k - n], (k, n, phi)
        worst = max(worst, phi / N[k - n])
        pairs = sum(v * v for v in c.values())
        assert pairs <= 2 * N[k - n] * N[k]
print("LEMMA6 OK for all n<=k<=%d; max fibre/N_{k-n} = %.3f" % (KMAX, worst))

# ---- Proposition F
class Direct:
    def __init__(self, kappa):
        self.k = kappa; self.E = np.array(E[kappa], dtype=np.int64)
    def __getitem__(self, idx):
        idx = np.asarray(idx, dtype=np.int64); out = np.empty(len(idx))
        for a in range(0, len(idx), 4096):
            ph = (idx[a:a+4096, None] * self.E[None, :]) % (1 << self.k)
            z = np.exp(2j * np.pi * ph / (1 << self.k)).sum(axis=1)
            out[a:a+4096] = z.real ** 2 + z.imag ** 2
        return out

def T_vals(kappa):
    """|T_kappa(xi)|^2 for all xi mod 2^kappa via FFT (direct sums for kappa>22)."""
    if kappa > 22: return Direct(kappa)
    ind = np.zeros(1 << kappa)
    ind[E[kappa]] = 1
    F = np.fft.fft(ind)
    return (F.real ** 2 + F.imag ** 2)

def lemma5(j): return j * 2 ** ((j + 1) / 2)

rng = np.random.default_rng(12345)
ncase = 0; worstF = 0; worstClosed = 0
for kappa in list(range(4, 23)) + [24, 26]:
    T2 = T_vals(kappa)
    mod = 1 << kappa
    tau = 1 << max(kappa - 2, 0)
    reps = 400 if kappa <= 20 else 120
    for rep in range(reps):
        e = int(rng.integers(0, kappa + 2)) if rep % 3 else 0
        hodd = int(2 * rng.integers(0, 1 << 20) + 1) * (1 if rng.random() < .5 else -1)
        h = hodd << e
        lam0 = int(2 * rng.integers(0, mod // 2) + 1)
        # unimodal M: several shapes
        shape = rep % 6
        L = int(rng.integers(1, 6 * tau + 2)) if shape < 3 else int(rng.integers(1, 60))
        L = min(L, 5000)
        if shape in (0, 3):
            M = np.ones(L)
        elif shape in (1, 4):
            pk = rng.integers(0, L)
            up = np.sort(rng.random(pk)); dn = np.sort(rng.random(L - pk))[::-1]
            M = np.concatenate([up, dn]) * rng.integers(1, 50)
        else:
            x = np.arange(L) - L / 2
            M = np.exp(-x * x / (2 * (L / 6 + 1) ** 2))
        i0 = int(rng.integers(-3 * tau, 3 * tau + 1))
        idx = np.array([(h * lam0 * pow(3, i0 + t, mod)) % mod for t in range(L)])
        lhs = float((M * T2[idx]).sum())
        W = float(M.sum()); Ms = float(M.max())
        rhs1 = 2 * N[kappa] * (W * N[min(e + 3, kappa)] + Ms * sum(N[j + e] * lemma5(j) for j in range(4, kappa - e + 1)))
        rhs2 = N[kappa] ** 2 * (6 * 2 ** (s * e - s * kappa) * W + 11.1 * kappa * 2 ** ((kappa - e) / 2) * Ms)
        assert lhs <= rhs1 * (1 + 1e-9), (kappa, h, lam0, shape, lhs, rhs1)
        assert rhs1 <= rhs2 * (1 + 1e-9), (kappa, e, rhs1, rhs2)
        worstF = max(worstF, lhs / rhs1); worstClosed = max(worstClosed, rhs1 / rhs2)
        ncase += 1
    # adversarial: for h=1 and h=2^e, the interval (window) maximizing the sum, all window lengths up to 64, over full orbit
    for e in (0, 1, 3):
        if e >= kappa: continue
        for sign in (1, -1):
            orb = np.array([(sign * (1 << e) * pow(3, i, mod)) % mod for i in range(min(tau, 200000) + 64)])
            v = T2[orb]
            cs = np.concatenate([[0], np.cumsum(v)])
            for L in (1, 2, 3, 5, 8, 16, 32, 64):
                lhs = float((cs[L:] - cs[:-L]).max())
                rhs1 = 2 * N[kappa] * (L * N[min(e + 3, kappa)] + sum(N[j + e] * lemma5(j) for j in range(4, kappa - e + 1)))
                assert lhs <= rhs1
                worstF = max(worstF, lhs / rhs1); ncase += 1
print("PROP F: %d instances OK; max LHS/RHS1 = %.4f ; max RHS1/RHS2 = %.4f" % (ncase, worstF, worstClosed))

# exact pair-count decomposition check (the proof's intermediate claims), kappa<=16
for kappa in range(4, 17):
    Ek = np.array(E[kappa])
    d = (Ek[:, None] - Ek[None, :])
    vv = np.where(d == 0, 99, np.log2((d & -d).astype(float) + (d == 0))).astype(int)
    for n in range(0, kappa + 1):
        exact = int((vv == n).sum()); atleast = int((vv >= n).sum())
        assert exact <= atleast <= 2 * N[kappa - n] * N[kappa]
print("pair counts by valuation OK (kappa<=16)")

# closed-form constants
g = 1 / (1 - 2 ** (-(s + 0.5)))
print("geometric factor %.4f (claimed 2.377); 2*1.64*2^(3s)=%.4f (<=6); 2*sqrt2*1.64*%.4f=%.4f (<=11.1); *6.5=%.3f (claimed 72)"
      % (g, 2 * 1.64 * 2 ** (3 * s), g, 2 * math.sqrt(2) * 1.64 * g, 2 * math.sqrt(2) * 1.64 * g * 6.5))
print("ALL OK")
