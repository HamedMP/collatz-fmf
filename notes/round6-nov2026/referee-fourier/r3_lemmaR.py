# Step 6: Lemma R with exact integers.
import sys
from fractions import Fraction as Fr
KM = 400
MM = 1 << KM
def run(h, epsn, epsd, KM=KM, verbose=True):
    # bad iff |m| * epsd < epsn * 2^k   (eps = epsn/epsd)
    PM = (3*KM)//4 + 12
    inv = [pow(3, -(P+5), MM) for P in range(PM+8)]
    def m(P, k):
        M = 1 << k; r = (11*h*inv[P]) % M
        return r - M if 2*r > M else r        # symmetric residue (r = M/2 -> +M/2; never bad)
    nb = 0; pairs = 0; viol = 0; cong = 0
    bad = set()
    for k in range(8, KM+1):
        for P in range(0, PM):
            if abs(m(P, k))*epsd < epsn << k: bad.add((P, k))
    for (P, k) in bad:
        for dP, dQ in ((4, 6), (5, 7), (6, 8)):
            ch = (P+dP, k-dQ)
            if k-dQ >= 8 and ch in bad:
                pairs += 1
                if m(P, k) != 3**dP*m(*ch): viol += 1
                if (m(P, k) - 3**dP*m(*ch)) % (1 << (k-dQ)): cong += 1
    # also the congruence for ALL parent/child pairs on a subsample
    c2 = 0
    for k in range(16, KM+1, 7):
        for P in range(0, PM-8, 5):
            for dP, dQ in ((4, 6), (5, 7), (6, 8)):
                if (m(P, k) - 3**dP*m(P+dP, k-dQ)) % (1 << (k-dQ)): c2 += 1
    # runs: longest chain of bad nodes, and check the consequence for every chain (DP over bad nodes: all maximal-from-start chains)
    sys.setrecursionlimit(10000)
    memo = {}
    def longest(n):
        if n in memo: return memo[n]
        P, k = n; best = 1
        for dP, dQ in ((4, 6), (5, 7), (6, 8)):
            c = (P+dP, k-dQ)
            if c in bad: best = max(best, 1+longest(c))
        memo[n] = best; return best
    L = max((longest(n) for n in bad), default=0)
    # consequence check: enumerate chains by DFS from each bad node (cap total)
    cons_viol = 0; chains = 0
    def dfs(start, node, J):
        nonlocal cons_viol, chains
        P0, k0 = start; PJ, kJ = node
        chains += 1
        M0 = 1 << k0; r = (11*h*inv[PJ]) % M0; d = min(r, M0-r)
        # ||.|| <= eps*3^-(PJ-P0) <= eps*3^-4J
        if not (d*epsd*3**(PJ-P0) < epsn*M0 and PJ-P0 >= 4*J): cons_viol += 1
        if chains > 300000: return
        for dP, dQ in ((4, 6), (5, 7), (6, 8)):
            c = (PJ+dP, kJ-dQ)
            if c in bad: dfs(start, c, J+1)
    for n in sorted(bad):
        if chains > 300000: break
        dfs(n, n, 0)
    if verbose: print("h=%s eps=%d/%d: bad nodes %d of %d, bad parent-child pairs %d, exactness violations %d (congruence failures %d, all-pairs congruence failures %d), longest run %d, chains checked %d, consequence violations %d" % (h if abs(h) < 10**9 else "~3^%d" % round(len(str(h))/0.477), epsn, epsd, len(bad), (KM-7)*PM, pairs, viol, cong, c2, L, chains, cons_viol))
    return viol
for h in (1, 5, 3**20, 3**150, 7*3**60, -3**90):
    run(h, 1, 1000)
print("-- threshold: eps*(2^8+3^6)<1 <=> eps<1/985; test larger eps for sharpness")
for h in (1, 5, 3**20, 3**150):
    for en, ed in ((1, 985), (1, 500), (1, 100), (1, 20), (1, 5)):
        run(h, en, ed)
