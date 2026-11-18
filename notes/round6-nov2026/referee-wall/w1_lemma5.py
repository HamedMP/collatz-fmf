# Referee check of Lemma 5: |sum_{i in I} e(a 3^i / 2^j)| <= j 2^((j+1)/2), j>=4, a odd, every interval I.
import numpy as np, math, sys

def v2(x):
    return (x & -x).bit_length() - 1

worst_ratio = 0
for j in range(4, 15):
    mod = 1 << j
    tau = 1 << (j - 2)
    # structure checks
    pw = [pow(3, i, mod) for i in range(2 * tau)]
    assert len(set(pw[:tau])) == tau and pw[tau] == 1, "period"
    assert set(pw[:tau]) == {x for x in range(mod) if x % 8 in (1, 3)}, "image set"
    # v2(3^d-1)
    for d in range(1, min(tau, 2000)):
        v = v2(3 ** d - 1)
        assert v == (1 if d % 2 else v2(d) + 2)
    # surviving d (mod tau) with v2(3^d - 1) >= j-3  (d=0 always survives)
    surv = [d for d in range(tau) if d == 0 or v2(pow(3, d, mod * 16) - 1) >= j - 3]
    # all odd a for j<=10, else representatives + random
    if j <= 10:
        alist = list(range(1, mod, 2))
    else:
        rng = np.random.default_rng(j)
        alist = [1, mod - 1, 5, mod - 5, 7, 3] + [int(2 * x + 1) for x in rng.integers(0, mod // 2, 6)]
    pwa = np.array(pw, dtype=np.int64)
    mx = 0.0
    mxS = 0.0
    maxcomplete = 0.0
    for a in alist:
        ph = np.exp(2j * np.pi * ((a * pwa) % mod) / mod)
        maxcomplete = max(maxcomplete, abs(ph[:tau].sum()))
        P = np.concatenate([[0], np.cumsum(ph)])  # 2tau+1 prefix sums
        # max over all intervals within two periods = diameter of prefix set
        m = 0.0
        if len(P) <= 1100:
            m = np.abs(P[:, None] - P[None, :]).max()
        else:
            for u in range(len(P)):
                t = np.abs(P[u + 1:] - P[u]).max() if u + 1 < len(P) else 0
                if t > m: m = t
        mx = max(mx, m)
        # twisted complete sums S(a,b) for all b via FFT
        S = np.fft.fft(ph[:tau])
        mxS = max(mxS, np.abs(S).max())
    bound = j * 2 ** ((j + 1) / 2)
    print(f"j={j:2d} tau={tau:5d} #a={len(alist):5d} surv_d={len(surv)} max_complete={maxcomplete:.1e} "
          f"max_I={mx:9.3f} (/2^(j/2)={mx/2**(j/2):.3f}) bound={bound:9.2f} ratio={mx/bound:.3f} "
          f"max_b|S|/2^(j/2)={mxS/2**(j/2):.4f} (limit sqrt2)")
    assert len(surv) <= 8
    assert mx <= bound and mxS <= 2 ** ((j + 1) / 2) + 1e-6 and maxcomplete < 1e-6
    worst_ratio = max(worst_ratio, mx / bound)
    # completion constant: (1/tau) sum_b |c_b| for worst interval length
    worstc = 0
    for L in range(1, tau):
        b = np.arange(1, tau)
        c = np.abs(np.sin(np.pi * b * L / tau) / np.sin(np.pi * b / tau)).sum() / tau + L / tau
        worstc = max(worstc, c)
        if tau > 600 and L > 5 and L % 97: continue
    assert worstc <= 2 + math.log(tau / 2) + 1e-9 <= j
    print(f"      completion L1 const max_L={worstc:.3f} <= 2+ln(tau/2)={2+math.log(tau/2):.3f} <= j")
print("LEMMA5 OK worst ratio", worst_ratio)
