# Referee script 2: Lemma L brute force (exact integer / Fraction arithmetic).
import itertools, sys
from fractions import Fraction as F
import numpy as np

def reps(word):
    """all (pc,pd,uc,ud) for factor u at i<i' inside word (overlap allowed), p=word[:i']"""
    n = len(word); out = set()
    for i in range(n):
        for ip in range(i+1, n):
            L = 0
            while ip+L < n and word[i+L] == word[ip+L]: L += 1
            if L == 0: continue
            p = word[:ip]; pc, pd = p.count('c'), p.count('d')
            # longer u is better for ratio and for l(u)>=l_c ; only need maximal L
            u = word[i:i+L]
            out.add((pc, pd, u.count('c'), u.count('d')))
    return np.array(sorted(out), dtype=np.int64)

DEN = 40
grid = np.arange(1, 50*DEN, dtype=np.int64)       # rho = n/40 in (0,50)
# extra adversarial rationals near case thresholds: rho = 2/k (+-eps), 3j-5 (+-eps), (1+j)/2
extra = set()
for k in range(1, 22):
    for e in (F(0), F(1, 10**6), F(-1, 10**6)):
        extra.add(F(2, k)+e)
for j in range(1, 22):
    for e in (F(0), F(1, 10**6), F(-1, 10**6)):
        for base in (F(3*j-5), F(1+j, 2), F(2)):
            if base+e > 0: extra.add(base+e)
extra = sorted(extra)

def best_ratio_grid(word):
    R = reps(word)
    if len(R) == 0: return None
    pc, pd, uc, ud = [R[:, t][:, None] for t in range(4)]
    lp = pc*DEN + pd*grid[None, :]; lu = uc*DEN + ud*grid[None, :]
    ok = (lu >= DEN) & (lp <= 3*lu)
    good = ok.any(axis=0)
    # worst ratio over grid (float, exploratory only)
    ratio = np.where(lu >= DEN, lp/np.maximum(lu, 1), np.inf).min(axis=0)
    return good, ratio, R

def check_extra(R, word):
    bad = []
    for rho in extra:
        ok = False
        for pc, pd, uc, ud in R.tolist():
            lu = uc + ud*rho
            if lu >= 1 and pc + pd*rho <= 3*lu: ok = True; break
        if not ok: bad.append(rho)
    return bad

# --- (A) the shapes the lemma / finite form uses
N = 22
shapes = ['cc'] + ['c' + 'd'*k + 'c'*j + 'd' for k in range(1, N) for j in range(1, N) if k+j+2 <= N]
nbad = 0; worst = 0; warg = None
for w in shapes:
    good, ratio, R = best_ratio_grid(w)
    if not good.all():
        nbad += 1; print('FAIL shape', w, 'rho=', grid[~good][:5]/DEN)
    b = check_extra(R, w)
    if b: nbad += 1; print('FAIL shape (extra rho)', w, b[:5])
    m = ratio.max()
    if m > worst: worst, warg = m, (w, grid[ratio.argmax()]/DEN)
print('(A) shapes of length<=22:', len(shapes), 'failures:', nbad, 'worst min-ratio on grid:', worst, warg)

# --- (B) literal witness of the lemma's case analysis, exact Fractions
def literal(k, j, rho):
    """word c d^k c^j d ; returns (i, i', u) as the proof prescribes"""
    if k*rho <= 2: return 0, k+1, 'c'
    if k >= 2: return 1, 2, 'd'*(k-1)
    # k == 1, rho > 2
    if j >= 2 and rho <= 3*j-5: return 2, 3, 'c'*(j-1)
    return 1, j+2, 'd'
nb = 0; cnt = 0
rhos = [F(n, DEN) for n in range(1, 50*DEN, 7)] + extra
for k in range(1, 21):
    for j in range(1, 21):
        if k+j+2 > N: continue
        word = 'c' + 'd'*k + 'c'*j + 'd'
        for rho in rhos:
            i, ip, u = literal(k, j, rho); cnt += 1
            okocc = i < ip and word[i:i+len(u)] == u and word[ip:ip+len(u)] == u and ip+len(u) <= len(word)
            l = lambda s: s.count('c') + rho*s.count('d')
            if not (okocc and l(word[:ip]) <= 3*l(u) and l(u) >= 1):
                nb += 1
                if nb < 10: print('LITERAL FAIL', k, j, rho, i, ip, u, okocc)
print('(B) literal case-analysis witnesses checked:', cnt, 'failures:', nb)

# --- (C) completeness: ALL words of length M starting with c. which fail on some rho?
M = int(sys.argv[1]) if len(sys.argv) > 1 else 14
fails = []
for t in itertools.product('cd', repeat=M-1):
    w = 'c' + ''.join(t)
    res = best_ratio_grid(w)
    good = res[0] if res else np.zeros(1, bool)
    if not good.all(): fails.append(w)
import re
unexpected = [w for w in fails if not re.fullmatch(r'cd+c*', w)]
print('(C) all', 2**(M-1), 'words of length', M, ': words failing for some grid rho:', len(fails),
      '; of these NOT of the incomplete form c d^k c^j (no closing d):', len(unexpected), unexpected[:5])
# infinite cases k=inf, j=inf : c d^n and c d c^n for large n
for w in ['c' + 'd'*200, 'cd' + 'c'*200]:
    good, ratio, R = best_ratio_grid(w)
    print('    limit case', w[:6]+'...', 'all grid rho ok:', bool(good.all()), 'extra bad:', check_extra(R, w)[:3])
