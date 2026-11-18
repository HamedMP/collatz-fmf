"""SAT encoder for matrix-interpretation termination certificates of SRSs.

Certificate families (see REPORT.md for the soundness statements):
  natural / full : N^d, [s](x) = M x + v, M[0][0] >= 1          (any rule removable)
  natural / top  : N^d, [s](x) = M x + v                        (marker rules only)
  arctic  / full : max-plus over N u {-inf}, linear, M[0][0] finite
  arctic  / top  : max-plus over Z u {-inf} ("below zero"), affine,
                   M[0][0] >= 0 or v[0] >= 0                    (marker rules only)

Interpretation convention: [s1 s2 ... sk] = [s1] o [s2] o ... o [sk]
(leftmost symbol outermost), so "top" rewriting is rewriting at the LEFT end.

Naturals are bit-blasted in binary with exact widths (no overflow cut-off, so
UNSAT answers are complete for the stated coefficient range); arctic/tropical
numbers use the order (unary) encoding.

This module shares no code with check.py.
"""
import time


class CNF:
    T, F = 1, -1

    def __init__(self):
        self.nv = 1
        self.cls = [[1]]
        self.cache = {}

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, lits):
        out = []
        for l in lits:
            if l == 1:
                return
            if l == -1:
                continue
            out.append(l)
        self.cls.append(out)

    def AND(self, a, b):
        if a == -1 or b == -1 or a == -b:
            return -1
        if a == 1:
            return b
        if b == 1 or a == b:
            return a
        key = ('&', a, b) if a < b else ('&', b, a)
        z = self.cache.get(key)
        if z is None:
            z = self.new()
            self.cls.append([-z, a])
            self.cls.append([-z, b])
            self.cls.append([z, -a, -b])
            self.cache[key] = z
        return z

    def OR(self, a, b):
        return -self.AND(-a, -b)

    def ORn(self, lits):
        s = set()
        for l in lits:
            if l == 1:
                return 1
            if l == -1:
                continue
            if -l in s:
                return 1
            s.add(l)
        if not s:
            return -1
        if len(s) == 1:
            return next(iter(s))
        key = ('|',) + tuple(sorted(s))
        z = self.cache.get(key)
        if z is None:
            z = self.new()
            self.cls.append([-z] + list(key[1:]))
            for l in key[1:]:
                self.cls.append([z, -l])
            self.cache[key] = z
        return z

    def XOR(self, a, b):
        if a == -1:
            return b
        if b == -1:
            return a
        if a == 1:
            return -b
        if b == 1:
            return -a
        if a == b:
            return -1
        if a == -b:
            return 1
        sign = 1
        if a < 0:
            a, sign = -a, -sign
        if b < 0:
            b, sign = -b, -sign
        key = ('^', a, b) if a < b else ('^', b, a)
        z = self.cache.get(key)
        if z is None:
            z = self.new()
            self.cls.append([-z, a, b])
            self.cls.append([-z, -a, -b])
            self.cls.append([z, -a, b])
            self.cls.append([z, a, -b])
            self.cache[key] = z
        return sign * z


# ------------------------------------------------------------------ naturals
class Nat:
    __slots__ = ('bits', 'ub')

    def __init__(self, bits, ub):
        n = ub.bit_length()
        self.bits = list(bits[:n])
        self.ub = ub


def nat_const(c):
    return Nat([1 if (c >> i) & 1 else -1 for i in range(c.bit_length())], c)


def nat_var(cnf, V):
    """fresh natural in [0, V-1]"""
    ub = V - 1
    x = Nat([cnf.new() for _ in range(ub.bit_length())], ub)
    if ub != (1 << ub.bit_length()) - 1:
        cnf.add([nat_ge_lit(cnf, nat_const(ub), x)])
    return x


def nat_add(cnf, x, y):
    if x.ub == 0:
        return y
    if y.ub == 0:
        return x
    ub = x.ub + y.ub
    n = ub.bit_length()
    out, c = [], -1
    for i in range(n):
        a = x.bits[i] if i < len(x.bits) else -1
        b = y.bits[i] if i < len(y.bits) else -1
        ab = cnf.XOR(a, b)
        out.append(cnf.XOR(ab, c))
        c = cnf.OR(cnf.AND(a, b), cnf.AND(ab, c))
    return Nat(out, ub)


def nat_sum(cnf, xs):
    xs = [x for x in xs if x.ub > 0]
    if not xs:
        return nat_const(0)
    while len(xs) > 1:
        xs.sort(key=lambda z: z.ub)
        xs = [nat_add(cnf, xs[0], xs[1])] + xs[2:]
    return xs[0]


def nat_mul(cnf, x, y):
    if x.ub == 0 or y.ub == 0:
        return nat_const(0)
    if len(x.bits) > len(y.bits):
        x, y = y, x
    rows = []
    for i, xb in enumerate(x.bits):
        if xb == -1:
            continue
        rows.append(Nat([-1] * i + [cnf.AND(xb, yb) for yb in y.bits], y.ub << i))
    r = nat_sum(cnf, rows)
    return Nat(r.bits, min(r.ub, x.ub * y.ub))


def nat_ge_lit(cnf, x, y, strict=False):
    """literal equivalent to x >= y (or x > y)"""
    n = max(len(x.bits), len(y.bits))
    g = -1 if strict else 1
    for i in range(n):
        a = x.bits[i] if i < len(x.bits) else -1
        b = y.bits[i] if i < len(y.bits) else -1
        g = cnf.OR(cnf.AND(a, -b), cnf.AND(-cnf.XOR(a, b), g))
    return g


# -------------------------------------------------------------------- arctic
class Arc:
    """order encoding: lits[i] <=> X >= lo+i ; no lits <=> X = -inf"""
    __slots__ = ('lo', 'lits')

    def __init__(self, lo, lits):
        lits = list(lits)
        while lits and lits[-1] == -1:
            lits.pop()
        self.lo, self.lits = lo, lits


ARC_NEG = Arc(0, [])


def arc_const(c):
    return ARC_NEG if c is None else Arc(c, [1])


def arc_var(cnf, lo, hi):
    lits = [cnf.new() for _ in range(hi - lo + 1)]
    for i in range(len(lits) - 1):
        cnf.add([-lits[i + 1], lits[i]])
    return Arc(lo, lits)


def arc_ge(x, t):
    if not x.lits:
        return -1
    if t <= x.lo:
        return x.lits[0]
    i = t - x.lo
    return x.lits[i] if i < len(x.lits) else -1


def arc_max(cnf, x, y):
    if not x.lits:
        return y
    if not y.lits:
        return x
    lo = min(x.lo, y.lo)
    hi = max(x.lo + len(x.lits), y.lo + len(y.lits)) - 1
    return Arc(lo, [cnf.OR(arc_ge(x, t), arc_ge(y, t)) for t in range(lo, hi + 1)])


def arc_plus(cnf, x, y):
    if not x.lits or not y.lits:
        return ARC_NEG
    n1, n2 = len(x.lits), len(y.lits)
    lits = []
    for k in range(n1 + n2 - 1):
        lits.append(cnf.ORn([cnf.AND(x.lits[i], y.lits[k - i])
                             for i in range(max(0, k - n2 + 1), min(k, n1 - 1) + 1)]))
    return Arc(x.lo + y.lo, lits)


def arc_cmp(cnf, cond, x, y, strict):
    """cond -> x >= y   (strict: cond -> x >> y, i.e. x > y or both -inf)"""
    d = 1 if strict else 0
    for i in range(len(y.lits)):
        t = y.lo + i
        cnf.add([-cond, -y.lits[i], arc_ge(x, t + d)])


# ------------------------------------------------------------------ problems
def build(rules, kind, mode, dim, V, lo, cand):
    """rules: oriented rules; cand: indices that may be strict.
    kind natural: coefficients in [0, V-1].
    kind arctic : finite coefficients in [lo, lo+V-2] plus -inf (lo=0 if full).
    returns cnf, strict-flag dict, decode(model)->interp"""
    cnf = CNF()
    syms = sorted({s for l, r in rules for s in l + r})
    d = dim
    I = {}
    if kind == 'natural':
        for s in syms:
            M = [[nat_var(cnf, V) for _ in range(d)] for _ in range(d)]
            v = [nat_var(cnf, V) for _ in range(d)]
            if mode == 'full':
                cnf.add([cnf.ORn(M[0][0].bits)])
            I[s] = (M, v)
        ident = ([[nat_const(1 if i == j else 0) for j in range(d)] for i in range(d)],
                 [nat_const(0)] * d)

        def compose(P, C):
            (Mp, vp), (Mc, vc) = P, C
            M = [[nat_sum(cnf, [nat_mul(cnf, Mp[i][k], Mc[k][j]) for k in range(d)])
                  for j in range(d)] for i in range(d)]
            v = [nat_sum(cnf, [nat_mul(cnf, Mp[i][k], vc[k]) for k in range(d)] + [vp[i]])
                 for i in range(d)]
            return M, v
    else:
        assert kind == 'arctic'
        if mode == 'full':
            vlo, vhi = 0, V - 2
        else:
            vlo, vhi = lo, lo + V - 2
        for s in syms:
            M = [[arc_var(cnf, vlo, vhi) for _ in range(d)] for _ in range(d)]
            if mode == 'full':
                v = [ARC_NEG] * d
                cnf.add([M[0][0].lits[0]])
            else:
                v = [arc_var(cnf, vlo, vhi) for _ in range(d)]
                cnf.add([arc_ge(M[0][0], 0), arc_ge(v[0], 0)])
            I[s] = (M, v)
        ident = ([[arc_const(0 if i == j else None) for j in range(d)] for i in range(d)],
                 [ARC_NEG] * d)

        def compose(P, C):
            (Mp, vp), (Mc, vc) = P, C
            M = [[None] * d for _ in range(d)]
            for i in range(d):
                for j in range(d):
                    acc = ARC_NEG
                    for k in range(d):
                        acc = arc_max(cnf, acc, arc_plus(cnf, Mp[i][k], Mc[k][j]))
                    M[i][j] = acc
            v = []
            for i in range(d):
                acc = vp[i]
                for k in range(d):
                    acc = arc_max(cnf, acc, arc_plus(cnf, Mp[i][k], vc[k]))
                v.append(acc)
            return M, v

    memo = {(): ident}

    def interp(s):
        if s not in memo:
            memo[s] = I[s[0]] if len(s) == 1 else compose(interp(s[:-1]), I[s[-1]])
        return memo[s]

    flags = {}
    for idx, (l, r) in enumerate(rules):
        (Ml, vl), (Mr, vr) = interp(tuple(l)), interp(tuple(r))
        sflag = cnf.new() if idx in cand else -1
        flags[idx] = sflag
        if kind == 'natural':
            for i in range(d):
                for j in range(d):
                    cnf.add([nat_ge_lit(cnf, Ml[i][j], Mr[i][j])])
                cnf.add([nat_ge_lit(cnf, vl[i], vr[i])])
            if sflag != -1:
                cnf.add([-sflag, nat_ge_lit(cnf, vl[0], vr[0], strict=True)])
        else:
            for i in range(d):
                for j in range(d):
                    a, b = Ml[i][j], Mr[i][j]
                    arc_cmp(cnf, 1, a, b, False)
                    if sflag != -1:
                        arc_cmp(cnf, sflag, a, b, True)
                arc_cmp(cnf, 1, vl[i], vr[i], False)
                if sflag != -1:
                    arc_cmp(cnf, sflag, vl[i], vr[i], True)
    cnf.add([f for f in flags.values() if f != -1])

    def decode(model):
        val = set(l for l in model if l > 0)

        def tv(l):
            return (l in val) if l > 0 else (-l not in val)

        out = {}
        for s in syms:
            M, v = I[s]
            if kind == 'natural':
                dn = lambda x: sum(1 << i for i, b in enumerate(x.bits) if tv(b))
            else:
                def dn(x):
                    c = sum(1 for b in x.lits if tv(b))
                    if c == 0:
                        return None
                    return x.lo + c - 1
            out[s] = {'M': [[dn(M[i][j]) for j in range(d)] for i in range(d)],
                      'v': [dn(v[i]) for i in range(d)]}
        return out

    return cnf, flags, decode


def solve(rules, kind, mode, dim, V, lo, cand, solver='cadical195', seed=None, negphase=False):
    """returns ('SAT', interp, stats) or ('UNSAT', None, stats).  No timeout
    here: prove.py runs this in a child process and kills it on timeout."""
    from pysat.solvers import Solver
    t0 = time.time()
    cnf, flags, decode = build(rules, kind, mode, dim, V, lo, cand)
    cls = cnf.cls
    if seed is not None:
        import random
        rnd = random.Random(seed)
        cls = cls[:]
        rnd.shuffle(cls)
    t1 = time.time()
    s = Solver(name=solver, bootstrap_with=cls)
    if negphase:
        s.set_phases([-v for v in range(2, cnf.nv + 1)])
    ok = s.solve()
    t2 = time.time()
    stats = dict(vars=cnf.nv, clauses=len(cls), t_enc=round(t1 - t0, 2), t_sat=round(t2 - t1, 2))
    if not ok:
        s.delete()
        return 'UNSAT', None, stats
    model = s.get_model()
    s.delete()
    interp = decode(model)
    strict = sorted(i for i, f in flags.items() if f != -1 and model[f - 1] > 0)
    stats['strict_flags'] = strict
    return 'SAT', interp, stats
