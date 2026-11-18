"""Independent certificate checker for the srs-termination track.

Shares NO code with encoder.py / prove.py / systems.py: it reads a JSON
certificate (or a chain of them) and re-verifies everything with exact Python
integer arithmetic.  -infinity is JSON null.

Certificate (one rule-removal step):
  rules    : [[lhs, rhs], ...]   lists of symbol names, ORIGINAL orientation
  reversed : bool                if true every lhs and rhs is reversed first
  kind     : "natural" | "arctic"
  mode     : "full" | "top"
  dim      : d
  strict   : indices of the rules claimed strictly decreasing (to be removed)
  interp   : {symbol: {"M": d x d, "v": d}}

Semantics: [s1 s2 ... sk] = [s1] o [s2] o ... o [sk]   (leftmost outermost).

What is checked (soundness proofs: REPORT.md section B.1):
 natural/full : entries in N; M[0][0] >= 1 for every symbol;
                every rule  M_l >= M_r, v_l >= v_r entrywise;
                strict rules additionally v_l[0] > v_r[0].
 natural/top  : entries in N; same inequalities, no M[0][0] condition;
                + MARKER CONDITION below.
 arctic/full  : entries in N u {-inf}; all v = -inf; M[0][0] finite;
                every rule M_l >= M_r; strict rules M_l >> M_r entrywise
                (a >> b  iff  a > b or a = b = -inf).
 arctic/top   : entries in Z u {-inf}; for every symbol M[0][0] >= 0 or
                v[0] >= 0; every rule M_l >= M_r, v_l >= v_r; strict rules
                M_l >> M_r and v_l >> v_r;  + MARKER CONDITION.
 MARKER CONDITION (top modes; after orientation): let K be the smallest set
   that contains the first symbol of the lhs of every strict rule and is closed
   under: if a rule has lhs[0] in K or rhs[0] in K then both are in K.  Every
   rule of the system either contains no symbol of K at all, or has a symbol of
   K as the first symbol of both sides and no symbol of K anywhere else.
"""
import json
import sys


def fail(msg):
    raise SystemExit('CHECK FAILED: ' + msg)


def ge(a, b):                      # arctic/natural >= with None = -inf
    if b is None:
        return True
    if a is None:
        return False
    return a >= b


def gg(a, b):                      # arctic strict
    if b is None:
        return True
    if a is None:
        return False
    return a > b


def a_plus(a, b):
    return None if a is None or b is None else a + b


def a_max(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b


def compose_nat(P, C, d):
    Mp, vp = P
    Mc, vc = C
    M = [[sum(Mp[i][k] * Mc[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
    v = [sum(Mp[i][k] * vc[k] for k in range(d)) + vp[i] for i in range(d)]
    return M, v


def compose_arc(P, C, d):
    Mp, vp = P
    Mc, vc = C
    M = [[None] * d for _ in range(d)]
    v = [None] * d
    for i in range(d):
        for j in range(d):
            acc = None
            for k in range(d):
                acc = a_max(acc, a_plus(Mp[i][k], Mc[k][j]))
            M[i][j] = acc
        acc = vp[i]
        for k in range(d):
            acc = a_max(acc, a_plus(Mp[i][k], vc[k]))
        v[i] = acc
    return M, v


def check_step(c, quiet=False):
    kind, mode, d = c['kind'], c['mode'], c['dim']
    if kind not in ('natural', 'arctic') or mode not in ('full', 'top'):
        fail('unknown kind/mode')
    rules = [(list(l), list(r)) for l, r in c['rules']]
    if c.get('reversed'):
        rules = [(l[::-1], r[::-1]) for l, r in rules]
    strict = sorted(set(c['strict']))
    if not strict:
        fail('no strict rule')
    if any(not (0 <= i < len(rules)) for i in strict):
        fail('strict index out of range')
    syms = sorted({s for l, r in rules for s in l + r})
    I = {}
    for s in syms:
        if s not in c['interp']:
            fail('no interpretation for symbol %r' % s)
        M = c['interp'][s]['M']
        v = c['interp'][s]['v']
        if len(M) != d or any(len(row) != d for row in M) or len(v) != d:
            fail('bad shape for %r' % s)
        for x in [e for row in M for e in row] + list(v):
            if x is None:
                if kind == 'natural':
                    fail('-inf in natural interpretation')
            elif type(x) is not int:
                fail('non-integer coefficient')
            elif x < 0 and not (kind == 'arctic' and mode == 'top'):
                fail('negative coefficient')
        if kind == 'natural' and mode == 'full' and M[0][0] < 1:
            fail('M[0][0] < 1 for %r' % s)
        if kind == 'arctic' and mode == 'full':
            if any(x is not None for x in v):
                fail('arctic/full needs v = -inf')
            if M[0][0] is None:
                fail('M[0][0] = -inf for %r' % s)
        if kind == 'arctic' and mode == 'top':
            if not ((M[0][0] is not None and M[0][0] >= 0) or (v[0] is not None and v[0] >= 0)):
                fail('neither M[0][0] >= 0 nor v[0] >= 0 for %r' % s)
        I[s] = (M, v)
    if mode == 'top':
        for i in strict:
            if not rules[i][0]:
                fail('strict rule with empty lhs')
        K = {rules[i][0][0] for i in strict}
        grown = True
        while grown:                       # close K under "marker l[0] is rewritten to marker r[0]"
            grown = False
            for l, r in rules:
                if l and r and (l[0] in K) != (r[0] in K):
                    K |= {l[0], r[0]}
                    grown = True
        for idx, (l, r) in enumerate(rules):
            nl = sum(1 for s in l if s in K)
            nr = sum(1 for s in r if s in K)
            if nl == 0 and nr == 0:
                continue
            if not (nl == 1 and nr == 1 and l[0] in K and r[0] in K):
                fail('marker condition violated by rule %d' % idx)
    if kind == 'natural':
        ident = ([[1 if i == j else 0 for j in range(d)] for i in range(d)], [0] * d)
        comp = compose_nat
    else:
        ident = ([[0 if i == j else None for j in range(d)] for i in range(d)], [None] * d)
        comp = compose_arc

    def interp(word):
        acc = ident
        for s in word:
            acc = comp(acc, I[s], d)
        return acc

    for idx, (l, r) in enumerate(rules):
        (Ml, vl), (Mr, vr) = interp(l), interp(r)
        for i in range(d):
            for j in range(d):
                if not ge(Ml[i][j], Mr[i][j]):
                    fail('rule %d not weakly decreasing (M[%d][%d])' % (idx, i, j))
            if not ge(vl[i], vr[i]):
                fail('rule %d not weakly decreasing (v[%d])' % (idx, i))
        if idx in strict:
            if kind == 'natural':
                if not vl[0] > vr[0]:
                    fail('rule %d not strict' % idx)
            else:
                for i in range(d):
                    for j in range(d):
                        if not gg(Ml[i][j], Mr[i][j]):
                            fail('rule %d not strict (M[%d][%d])' % (idx, i, j))
                    if not gg(vl[i], vr[i]):
                        fail('rule %d not strict (v[%d])' % (idx, i))
    if not quiet:
        print('  step OK: %s/%s d=%d%s removes rules %s' % (
            kind, mode, d, ' reversed' if c.get('reversed') else '', strict))
    return strict


def check_chain(ch):
    """chain: {"system": name, "rules": [...], "steps": [cert, ...]}.
    Verifies each step against the rules that remain, returns remaining rules."""
    cur = [(tuple(l), tuple(r)) for l, r in ch['rules']]
    for n, c in enumerate(ch['steps']):
        got = [(tuple(l), tuple(r)) for l, r in c['rules']]
        if got != cur:
            fail('step %d: rule list differs from the remaining rules' % n)
        strict = check_step(c)
        cur = [x for i, x in enumerate(cur) if i not in set(strict)]
    return cur


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        ch = json.load(open(fn))
        print('%s: system %s, %d rules' % (fn, ch.get('system'), len(ch['rules'])))
        for i, (l, r) in enumerate(ch['rules']):
            print('   %2d: %s -> %s' % (i, ' '.join(l), ' '.join(r)))
        rem = check_chain(ch)
        if rem:
            print('  PARTIAL: %d rules remain:' % len(rem))
            for l, r in rem:
                print('      %s -> %s' % (' '.join(l), ' '.join(r)))
        else:
            print('  TERMINATION PROOF VERIFIED (all rules removed)')
