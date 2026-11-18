"""w2-alpha core: enumerate E mod 2^Q (2-adic Cantor set of infinite a/b itineraries),
check mirror identities, hull fullness, extension statistics, Frostman projection test.
Systems: '3n+1': a: w->(9w+1)/8 (w=7 mod 8), b: w->27w/16 (16|w)
         '5n+1': a: w->(25w+1)/8 (w=7 mod 8), b: w->125w/16
         '3n-1': a: w->(9w-1)/8 (w=1 mod 8), b: w->27w/16
Exact integer arithmetic throughout."""
import sys, math
from collections import Counter
SYS = {'3n+1': (9, 1, 27, 2, 3), '5n+1': (25, 1, 125, 2, 3), '3n-1': (9, -1, 27, 2, 3)}

def step(w, al, be, bm):
    if w % 2 == 0:
        return (bm * w // 16, 4) if w % 16 == 0 else None
    return ((al * w + be) // 8, 3) if (al * w + be) % 8 == 0 else None

def leaves(Q, name):
    """yield (r, Qu, Mu, wp, na, nb): class r mod 2^Qu (first Qu>=Q), multiplier Mu (=3^P for a=3),
    wp = image of r under the word (the mirror residue)."""
    al, be, bm, _, _ = SYS[name]
    st = [(0, 0, 1, 0, 0, 0)]
    while st:
        r, q, M, wp, na, nb = st.pop()
        if q >= Q:
            yield r, q, M, wp, na, nb
            continue
        # a: need al*(wp+M t)+be = 0 mod 8
        for t in range(8):
            v = wp + M * t
            if (al * v + be) % 8 == 0 and v % 2 == 1:
                st.append((r + (t << q), q + 3, M * al, (al * v + be) // 8, na + 1, nb))
        for t in range(16):
            v = wp + M * t
            if v % 16 == 0:
                st.append((r + (t << q), q + 4, M * bm, bm * v // 16, na, nb + 1))

def life(w, name, cap=10**6):
    al, be, bm, _, _ = SYS[name]
    L = 0
    while L < cap:
        s = step(w, al, be, bm)
        if s is None: return L
        w, d = s; L += d
    return L

if __name__ == '__main__':
    name = sys.argv[1]; Q = int(sys.argv[2])
    s = -math.log2(0.8191725133961643)  # x^3+x^4=1
    lv = list(leaves(Q, name))
    print(f"system {name}  Q={Q}  #leaves={len(lv)}  2^(sQ)={2**(s*Q):.1f}  s={s:.6f}")
    # mirror check (only meaningful when M > 2^q i.e. expanding): r = floor(2^q wp / M) for 3n+1,5n+1
    bad = 0
    for r, q, M, wp, na, nb in lv:
        assert 0 <= r < (1 << q)
        if name != '3n-1':
            assert 0 <= wp < M
            if (wp << q) // M != r: bad += 1
    print("mirror identity r = floor(2^q w'/M) failures:", bad)
    # integers below 2^Q that are seeds to depth Q; extension statistics
    seeds = sorted(set(r for r, q, M, wp, na, nb in lv if r < (1 << Q)))
    ext = Counter()
    longest = []
    for w in seeds:
        L = life(w, name)
        if L >= 10**6: longest.append((w, 'INF')); continue
        ext[L - Q] += 1
        longest.append((L - Q, w))
    tot = sum(ext.values())
    print(f"seeds w<2^Q with life>=Q: {len(seeds)} (finite-life {tot}); infinite-life (cap 1e6 bits):",
          [w if w < 10**6 else f'2^{Q}-{(1<<Q)-w}' for w, t in longest if t == 'INF'])
    cum = 0; rows = []
    mx = max(ext) if ext else 0
    for m in range(mx, -1, -1):
        cum += ext.get(m, 0)
        if m % 4 == 0: rows.append((m, cum))
    for m, c in rows[::-1]:
        if c: print(f"  extra bits >= {m:3d}: {c:8d}  frac {c/tot:.5f}   heuristic 2^(-(1-s)m) = {2**(-(1-s)*m):.5f}")
