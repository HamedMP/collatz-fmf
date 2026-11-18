"""String rewriting systems for the srs-termination track.

Conventions (identical to Yolcu-Aaronson-Heule, arXiv:2105.14697):
  a string s_1 s_2 ... s_k denotes the function  s_k o ... o s_1  (leftmost
  symbol is applied FIRST, i.e. is the most significant digit).

Symbols and their functional view  x -> mul*x + add :
  f : 2x      t : 2x+1                     (binary digits)
  0 : 3x      1 : 3x+1     2 : 3x+2        (ternary digits)
  a..e : 5x+0 .. 5x+4                      (quinary digits, litmus 5n+1)
  L : constant 1  (left end marker, most significant digit 1)
  R, R0, R1 : x   (right end markers; R0/R1 carry a state)
  O : 2x+1        (right end marker of an odd number)

Each system is a list of rules (lhs, rhs), lhs/rhs tuples of symbols.
"""

SEM = {
    'f': (2, 0), 't': (2, 1),
    '0': (3, 0), '1': (3, 1), '2': (3, 2),
    'a': (5, 0), 'b': (5, 1), 'c': (5, 2), 'd': (5, 3), 'e': (5, 4),
    'R': (1, 0), 'R0': (1, 0), 'R1': (1, 0), 'O': (2, 1),
}
BIN = ['f', 't']
DIG = {3: ['0', '1', '2'], 5: ['a', 'b', 'c', 'd', 'e']}


def rule(l, r):
    return (tuple(l.split()), tuple(r.split()))


def aux_rules(base):
    """Value-preserving base-swap rules A_base (binary digit moves right past a
    base-`base` digit) and B_base (leading 1 followed by a base-`base` digit is
    rewritten into binary)."""
    A, B = [], []
    dg = DIG[base]
    for beta in (0, 1):
        for q in range(base):
            tot = base * beta + q          # (2x+beta)*base + q = 2*(base*x+q') + beta'
            A.append(((BIN[beta], dg[q]), (dg[tot // 2], BIN[tot % 2])))
    for q in range(base):
        v = base * 1 + q                   # value of  L q
        bits = bin(v)[3:]                  # drop '0b1'
        B.append((('L', dg[q]), ('L',) + tuple(BIN[int(c)] for c in bits)))
    return A, B


A3, B3 = aux_rules(3)
X3 = A3 + B3
A5, B5 = aux_rules(5)
X5 = A5 + B5

# sanity: these are exactly the paper's rules
assert A3 == [rule('f 0', '0 f'), rule('f 1', '0 t'), rule('f 2', '1 f'),
              rule('t 0', '1 t'), rule('t 1', '2 f'), rule('t 2', '2 t')]
assert B3 == [rule('L 0', 'L t'), rule('L 1', 'L f f'), rule('L 2', 'L f t')]

SYSTEMS = {}
# name -> dict(rules=[...], dyn=number of leading dynamic rules, doc=...)


def add(name, dyn, aux, doc):
    SYSTEMS[name] = dict(rules=list(dyn) + list(aux), ndyn=len(dyn), doc=doc)


# ---------------------------------------------------------------- published
DT = [rule('f R', 'R'), rule('t R', '2 R')]
add('T', DT, X3, 'YAH Collatz system T (11 rules); SN(T) <=> Collatz')
for i in range(11):
    full = DT + X3
    sub = full[:i] + full[i + 1:]
    SYSTEMS['T-%d' % i] = dict(rules=sub, ndyn=None,
                               doc='YAH T minus rule %d (%s -> %s); published terminating'
                               % (i, ' '.join(full[i][0]), ' '.join(full[i][1])))
add('Farkas', [rule('1 R', 'R'), rule('0 f R', '0 R'), rule('1 f R', '1 R'),
               rule('1 t R', '1 2 R'), rule('2 t R', '2 2 R')], X3,
    'YAH Farkas variant F; published terminating (arctic)')
add('Wp', [rule('f R', '0 R')], X3, "YAH simple example W': n -> 3n/2; published terminating")
DS = [rule('f f O', '0 O'), rule('t f O', 'O'), rule('t O', '2 O')]
add('S', DS, X3, 'YAH odd system S; SN(S) <=> Collatz')
add('S1', [DS[1], DS[2]], X3, 'YAH S minus ffO->0O; OPEN in the paper (class 1 mod 8)')
add('S2', [DS[0], DS[2]], X3, 'YAH S minus tfO->O; OPEN in the paper (class 5 mod 8)')
add('S3', [DS[0], DS[1]], X3, 'YAH S minus tO->2O; published terminating')
DC4 = [rule('f f R', 'f R'), rule('t f R', 't R'), rule('t R', '2 f R')]
DT4 = [rule('f R', 'R'), rule('f t R', '1 f R'), rule('t t R', '2 t R')]
add('C4-0', [DC4[1], DC4[2]], X3, 'YAH C^{Even/4} minus ffR->fR; published terminating')
add('C4-2', [DC4[0], DC4[2]], X3, 'YAH C^{Even/4} minus tfR->tR; published terminating')
add('T4-1', [DT4[0], DT4[2]], X3, 'YAH T^{Odd/4} minus ftR->1fR; published terminating')
add('T4-3', [DT4[0], DT4[1]], X3, 'YAH T^{Odd/4} minus ttR->2tR; published terminating')

# ---------------------------------------------------------------- new systems
# (a) binary return map, two-state n-coordinates (m = 24n+23 at depth 0,
#     m = 24n+13 at depth 1; paper Prop. "Binary-Depth Affine Normal Form")
RET = [rule('t t t R0', '2 2 R0'),       # 0->0 : n=8k+7   -> 9k+8   = (9n+1)/8
       rule('f f f f R0', '0 0 R1'),     # 0->1 : n=16k    -> 9k     = 9n/16
       rule('f t t R1', '1 0 2 R0'),     # 1->0 : n=8k+3   -> 27k+11 = (27n+7)/8
       rule('t t t f R1', '2 2 0 R1')]   # 1->1 : n=16k+14 -> 27k+24 = (27n+6)/16
add('RET', RET, X3, 'binary return system (two-state); SN <=> H1')
add('RET-r0', [RET[0]], X3, 'CALIBRATION return letter r=0 only: n -> (9n+1)/8')
add('RET-r1', [RET[1], RET[2]], X3, 'CALIBRATION return letter r=1 only (0->1->0 forever)')
add('RET-11', [RET[3]], X3, 'CALIBRATION depth-1 self loop n -> (27n+6)/16 (Lemma P, n-coordinates)')
add('RET-r01', [RET[0], RET[1], RET[2]], X3, 'return letters r in {0,1} (= RET minus 1->1); OPEN')
add('RET-no00', [RET[1], RET[2], RET[3]], X3, 'return letters r >= 1 (= RET minus 0->0); OPEN')
add('RET-no01', [RET[0], RET[2], RET[3]], X3, 'RET minus 0->1 (provable: r=0 chain or Lemma P)')
add('RET-no10', [RET[0], RET[1], RET[3]], X3, 'RET minus 1->0 (provable: r=0 chain or Lemma P)')
# Lemma P in m-coordinates: m=16k+13 -> 27k+22 = (27m+1)/16
add('P', [rule('t t f t R', '2 1 1 R')], X3, 'CALIBRATION Lemma P system m -> (27m+1)/16')
# (b) single-coordinate W-form  z -> 27z/16 (z=0 mod 16),  z -> (9z+1)/8 (z=7 mod 8)
WD = [rule('f f f f R', '0 0 0 R'), rule('t t t R', '2 2 R')]
add('W', WD, X3, 'single-coordinate W-form; SN <=> H1+ (all positive z), which implies H1')
add('W-r0', [WD[1]], X3, 'CALIBRATION W-form r=0 only: z -> (9z+1)/8')
add('W-16', [WD[0]], X3, 'CALIBRATION W-form z -> 27z/16 only (trivial)')
# r=1 only in W-coordinates as ONE composite rule: z=128k+80 -> 243k+152 = (243z+16)/128
add('W-r1', [rule('t f t f f f f R', '1 2 1 2 2 R')], X3,
    'CALIBRATION W-form r=1 only (block 16w -> 27w -> (243w+1)/8); invariant 115z+16')
add('W01', [WD[1], rule('t f t f f f f R', '1 2 1 2 2 R')], X3,
    'W-form with return letters r in {0,1} as composite rules; SN <=> no infinite {0,1}-letter orbit (all z); OPEN')
# (c) growth-B chain system
GD = [rule('t t O', '2 t O'),      # x=8j+7   -> 12j+11 = (3x+1)/2  (depth t -> t-1)
      rule('t f t O', '2 0 O')]    # x=16i+11 -> 18i+13 = (9x+5)/8  (depth-0 growth-B hop)
add('G', GD, X3, 'growth-B system; SN <=> every growth-B chain is finite')
add('G-0', [GD[1]], X3, 'G minus ttO->2tO: x -> (9x+5)/8 only (provable)')
add('G-1', [GD[0]], X3, 'G minus tftO->20O: x -> (3x+1)/2 only (provable)')
# G-0 in the adapted coordinate y = x+5 (fixed point moved to 0): y=16k -> 18k = 9y/8
add('G0y', [rule('f f f f R', 'f 0 0 R')], X3,
    'CALIBRATION G-0 in the coordinate y=x+5: y -> 9y/8 on y = 0 mod 16')
# FMF-native odd-to-odd system (extra)
add('FMF', [rule('f O', '1 R'),        # x=4k+1  -> 3k+1
            rule('f t O', '1 1 R'),    # x=8j+3  -> 9j+4
            rule('t t O', '2 t O'),    # x=8j+7  -> 12j+11
            rule('f R', 'R'),
            rule('t R', 'O')],
    X3, 'FMF-native system; SN <=> Collatz')

# ---------------------------------------------------------------- negative controls
# every one of these has an explicit rewriting LOOP (found and replayed by loops.py)
add('C5', [rule('f R', 'R'), rule('t R', 'd R')], X5,
    'NEG 5n+1 analogue of T: 2k+1 -> 5k+3; cycle 13,33,83')
add('C3m', [rule('f R', 'R'), rule('t R', '1 R')], X3,
    'NEG 3n-1 analogue of T: 2k+1 -> 3k+1; cycles through 5 and 17')
add('FMF3m', [rule('t O', '2 R'),      # y=4k+3 -> 3k+2 = (3y-1)/4
              rule('f O', '0 O'),      # y=4k+1 -> 6k+1 = (3y-1)/2
              rule('f R', 'R'), rule('t R', 'O')], X3,
    'NEG odd-to-odd system for 3n-1; cycles 5,7 and 17')
add('FMF5', [rule('t O', 'e R'),       # x=4k+3 -> 5k+4 = (5x+1)/4
             rule('f O', 'b O'),       # x=4k+1 -> 10k+3 = (5x+1)/2
             rule('f R', 'R'), rule('t R', 'O')], X5,
    'NEG odd-to-odd system for 5n+1; cycle 13,33,83')
add('S3m', [rule('f O', '0 O'),        # y=4k+1 -> 6k+1 = (3y-1)/2
            rule('t t O', '2 O'),      # y=8k+7 -> 6k+5 = (3y-1)/4
            rule('f t O', 'O')],       # y=8k+3 -> 2k+1 (same 3n-1 trajectory)
    X3, 'NEG 3n-1 analogue of YAH S (odd marker); cycle 17,25,37,55,41,61,91,23')
add('G5', [rule('f O', 'b O'),               # x=4k+1   -> 10k+3 = (5x+1)/2
           rule('f t f f t O', 'b O')],      # x=64k+19 -> 10k+3 = (5x+1)/32
    X5, 'NEG two-rule growth-style system for 5n+1; cycle 13,33,83')


def subsystems(name):
    """systems obtained from `name` by deleting one rule; returns list of names"""
    base = SYSTEMS[name]
    out = []
    for i, (l, r) in enumerate(base['rules']):
        nm = '%s~%d' % (name, i)
        if nm not in SYSTEMS:
            SYSTEMS[nm] = dict(rules=base['rules'][:i] + base['rules'][i + 1:], ndyn=None,
                               doc='%s minus rule %d (%s -> %s)' % (name, i, ' '.join(l), ' '.join(r)))
        out.append(nm)
    return out


for _n in ('RET', 'W', 'G'):
    subsystems(_n)


def show(name):
    s = SYSTEMS[name]
    return '\n'.join('%2d: %s -> %s' % (i, ' '.join(l), ' '.join(r))
                     for i, (l, r) in enumerate(s['rules']))


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or SYSTEMS):
        print('==', n, '--', SYSTEMS[n]['doc'])
        print(show(n))
