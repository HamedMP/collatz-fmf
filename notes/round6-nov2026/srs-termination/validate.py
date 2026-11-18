"""Brute-force validation of the rewriting semantics of the new systems.

For every system and every input value up to N (default 10^6):
  * the canonical string  L <binary digits> <marker>  is built,
  * the dynamic rules whose lhs is a suffix are collected (must be <= 1),
  * the result is compared with the arithmetic partial map (defined below,
    independently of systems.py): a rule matches  ==>  the map is defined and,
    after applying the rule and normalising with the auxiliary rules (each step
    is a genuine application of a rule looked up in the system's rule list),
    the string is  L <binary> <marker'>  with value = map(value),
  * inputs where the map is defined but no rule matches ("exceptions", caused
    by the leading-1 convention) are listed; they must be a finite explicit set
    and each must have a FINITE arithmetic orbit.
Then the arithmetic maps are cross-checked against the repository's own
definitions (return map T(n) of paper section 6; real Collatz/FMF iteration).

usage: validate.py [N]
"""
import sys
from fractions import Fraction

import systems

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
BIN = {'f': 0, 't': 1}
TER = {'0': 0, '1': 1, '2': 2}
MARK = {'R': (1, 0), 'R0': (1, 0), 'R1': (1, 0), 'O': (2, 1)}     # value -> mul*value+add


# ----------------------------------------------------------- arithmetic maps
def F_W(z, st):
    if z % 16 == 0:
        return 27 * z // 16, st
    if z % 8 == 7:
        return (9 * z + 1) // 8, st
    return None


def F_RET(n, st):
    if st == 'R0':
        if n % 8 == 7:
            return (9 * n + 1) // 8, 'R0'
        if n % 16 == 0:
            return 9 * n // 16, 'R1'
    else:
        if n % 8 == 3:
            return (27 * n + 7) // 8, 'R0'
        if n % 16 == 14:
            return (27 * n + 6) // 16, 'R1'
    return None


def F_G(x, st):
    if x % 8 == 7:
        return (3 * x + 1) // 2, st
    if x % 16 == 11:
        return (9 * x + 5) // 8, st
    return None


def F_P(m, st):
    return ((27 * m + 1) // 16, st) if m % 16 == 13 else None


def F_W01(z, st):
    if z % 8 == 7:
        return (9 * z + 1) // 8, st
    if z % 128 == 80:
        return (243 * z + 16) // 128, st
    return None


SPEC = {'W01': (F_W01, ['R']), 'W': (F_W, ['R']), 'RET': (F_RET, ['R0', 'R1']), 'G': (F_G, ['O']), 'P': (F_P, ['R'])}


# ----------------------------------------------------------- string side
def value(s):
    """functional semantics: L=1, f/t binary digit, 0/1/2 ternary digit, marker"""
    assert s[0] == 'L'
    v = 1
    for c in s[1:-1]:
        if c in BIN:
            v = 2 * v + BIN[c]
        else:
            v = 3 * v + TER[c]
    mul, add = MARK[s[-1]]
    return mul * v + add


def canon(val, marker):
    mul, add = MARK[marker]
    if (val - add) % mul:
        return None
    b = (val - add) // mul
    if b < 1:
        return None
    return ['L'] + ['t' if c == '1' else 'f' for c in bin(b)[3:]] + [marker]


def affine(word):
    """composite affine map (a, b): x -> a x + b of a word without L"""
    a, b = 1, 0
    for c in word:
        if c in BIN:
            a, b = 2 * a, 2 * b + BIN[c]
        elif c in TER:
            a, b = 3 * a, 3 * b + TER[c]
        else:
            m, d = MARK[c]
            a, b = m * a, m * b + d
    return a, b


def check_system(name):
    F, markers = SPEC[name]
    rules = systems.SYSTEMS[name]['rules']
    dyn = [(l, r) for l, r in rules if l[-1] in MARK]
    aux = {l: r for l, r in rules if l[-1] not in MARK}
    assert len(aux) == 9 and len(dyn) + 9 == len(rules)
    # symbolic checks -------------------------------------------------------
    for l, r in aux.items():
        if l[0] == 'L':
            assert affine(l[1:])[0] * 1 + affine(l[1:])[1] == affine(r[1:])[0] * 1 + affine(r[1:])[1], (l, r)
        else:
            assert affine(l) == affine(r), (l, r)
    for l, r in dyn:
        (a, b), (c, e) = affine(l), affine(r)
        for x in range(0, 200):            # affine identity  F(a x + b) = c x + e  for ALL x >= 0
            out = F(a * x + b, l[-1])
            assert out == (c * x + e, r[-1]), (name, l, r, x)
    # brute force -----------------------------------------------------------
    exceptions = []
    nmatch = 0
    for marker in markers:
        for val in range(1, N + 1):
            s = canon(val, marker)
            if s is None:
                continue
            m = [(l, r) for l, r in dyn if len(s) > len(l) and tuple(s[-len(l):]) == l]
            assert len(m) <= 1
            out = F(val, marker)
            if not m:
                if out is not None:
                    exceptions.append((val, marker))
                continue
            assert out is not None, (name, val, marker)
            nmatch += 1
            l, r = m[0]
            body = s[:-len(l)]             # L + binary digits (normal form)
            for c in r[:-1]:               # push the rhs digits one by one, normalising
                body.append(c)
                i = len(body) - 1
                while body[i] in TER:
                    key = (body[i - 1], body[i])
                    rhs = aux[key]         # genuine rule application  key -> rhs
                    if key[0] == 'L':
                        body[i - 1:i + 1] = rhs
                        break
                    body[i - 1:i + 1] = rhs
                    i -= 1
            t = body + [r[-1]]
            assert all(c in BIN for c in t[1:-1])
            assert (value(t), t[-1]) == out, (name, val, marker, t, out)
            assert t == canon(out[0], out[1])
    # exceptions must have finite arithmetic orbits
    for val, marker in exceptions:
        cur, steps = (val, marker), 0
        while cur is not None:
            cur = F(*cur)
            steps += 1
            assert steps < 1000
    print('%-4s: %d dynamic rules; inputs 1..%d x %s: %d rule applications validated; '
          'exceptions (map defined, no rule matches; all have finite orbits): %s'
          % (name, len(dyn), N, markers, nmatch, exceptions))


# ----------------------------------------------------------- repo cross-checks
def v2(n):
    return (n & -n).bit_length() - 1


def T_paper(n):
    """binary return partial map, paper section 6: 33n+32 = 16^r w, gate
    w = eps_r mod 8 (eps = 7 for even r, 5 for odd r), T(n) = (3*27^r*w - 85)/88"""
    Wv = 33 * n + 32
    k = v2(Wv)
    if k % 4:
        return None
    r = k // 4
    w = Wv >> k
    if w % 8 != (7 if r % 2 == 0 else 5):
        return None
    num = 3 * 27 ** r * w - 85
    assert num % 88 == 0
    return num // 88, r


def fmf_hop(x):
    """real Collatz iteration: first multiple of 4 strictly after x on the orbit of odd x"""
    y = 3 * x + 1
    while y % 4:
        y = y // 2 if y % 2 == 0 else 3 * y + 1
    return y


def cross_checks():
    # (i) two-state map composed over a block 0,1^r,0  ==  T_paper ; (iv) W-form on 33n+32
    cnt = 0
    for n in range(0, N + 1):
        cur = F_RET(n, 'R0')
        r = 0
        while cur is not None and cur[1] == 'R1':
            r += 1
            cur = F_RET(*cur)
        tp = T_paper(n)
        if cur is None:
            assert tp is None, n
        else:
            assert tp == (cur[0], r), (n, tp, cur, r)
            cnt += 1
        # W-form: run from z = 33n+32 until one (9z+1)/8 step has been made
        z = 33 * n + 32
        ok = True
        while z % 16 == 0:
            z = 27 * z // 16
        if z % 8 == 7:
            z = (9 * z + 1) // 8
        else:
            ok = False
        assert ok == (tp is not None), n
        if ok:
            assert z == 33 * tp[0] + 32, n
    print('cross (i)+(iv): two-state block map == paper T(n) == W-form block on z=33n+32 for all 0<=n<=%d '
          '(%d defined)' % (N, cnt))
    # (ii) two-state map == real FMF growth-B hop to a Type-B state of depth t2 in {0,1}
    #      which is itself a continuing state (its own hop is growth-B with Type-B output;
    #      equivalently m2 = 23 mod 24 (t2=0) / 13 mod 24 (t2=1): the "normal form")
    cnt = 0
    for st, (c, depth) in (('R0', (23, 0)), ('R1', (13, 1))):
        for n in range(0, N + 1):
            m = 24 * n + c
            x = (1 << (depth + 2)) * m - 1
            y = fmf_hop(x)
            nxt = None
            if v2(y) == 2:                       # growth-B hop
                x2 = y // 4
                if x2 % 4 == 3:                  # Type-B output
                    t2 = v2(x2 + 1) - 2
                    if t2 <= 1:
                        m2 = (x2 + 1) >> (t2 + 2)
                        c2 = 23 if t2 == 0 else 13
                        y2 = fmf_hop(x2)
                        continuing = (v2(y2) == 2 and (y2 // 4) % 4 == 3)
                        assert continuing == ((m2 - c2) % 24 == 0), (n, st)
                        if continuing:
                            nxt = ((m2 - c2) // 24, 'R0' if t2 == 0 else 'R1')
            assert nxt == F_RET(n, st), (n, st, nxt)
            cnt += nxt is not None
    print('cross (ii): two-state map == real Collatz FMF growth-B hop onto a continuing Type-B state of '
          'depth in {0,1}, all 0<=n<=%d, both states (%d defined)' % (N, cnt))
    # (iii) G-run == real growth-B hop
    cnt = 0
    for x in range(3, N + 1, 2):
        y = fmf_hop(x)
        growthB = (x % 4 == 3 and v2(y) == 2)
        cur, done = x, False
        while True:
            if cur % 8 == 7:
                cur = (3 * cur + 1) // 2
            elif cur % 16 == 11:
                cur = (9 * cur + 5) // 8
                done = True
                break
            else:
                break
        assert done == growthB, x
        if done:
            assert cur == y // 4, x
            cnt += 1
    print('cross (iii): G-run (rule-1 steps then one rule-2 step) == real growth-B hop for all odd 3<=x<=%d '
          '(%d growth-B hops)' % (N, cnt))
    # calibration identities
    for m in range(13, 5000, 16):
        m2 = (27 * m + 1) // 16
        assert 16 * (11 * m2 + 1) == 27 * (11 * m + 1)
    for n in range(14, 5000, 16):
        n2 = (27 * n + 6) // 16
        assert 16 * (11 * n2 + 6) == 27 * (11 * n + 6)
    for n in range(0, 5000 * 128, 16):
        a = F_RET(n, 'R0')
        b = F_RET(*a)
        if b and b[1] == 'R0':
            assert 128 * (115 * b[0] + 112) == 243 * (115 * n + 112)
    print('identities: 16(11m\'+1)=27(11m+1); 16(11n\'+6)=27(11n+6); 128(115n\'\'+112)=243(115n+112) OK')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        for nm in sys.argv[2:]:
            check_system(nm)
    else:
        for nm in ('W', 'RET', 'G', 'P'):
            check_system(nm)
        cross_checks()
