# Referee script 3: Theorem A instances, (1.1), exponent arithmetic, B1/B3, A1, Prop D, litmus, vacuity.
import itertools, random, math, sys
from fractions import Fraction as F
random.seed(12345)

def mk(mult, sign):
    """generalised system: a: w -> (m^2 w + sign)/8 on gate (m^2 w + sign = 0 mod 8 ...) ; b: w -> m^3 w/16.
       gate for a: w = -sign (mod 8)  (for m odd, m^2 = 1 mod 8)."""
    m2, m3 = mult**2, mult**3
    ga = (-sign) % 8
    def step(w):
        if w % 8 == ga: return 'a', (m2*w + sign)//8
        if w % 16 == 0: return 'b', m3*w//16
        return None, None
    def class_of(P):
        r, B, p, W = 0, 0, 1, 0
        for ch in P:
            if ch == 'a':
                s = ((ga - W) * pow(p, -1, 8)) % 8
                r += s << B; W += p*s; B += 3; p *= m2; W = (m2*W+sign)//8
            else:
                s = ((-W) * pow(p, -1, 16)) % 16
                r += s << B; W += p*s; B += 4; p *= m3; W = m3*W//16
        return r, B
    return step, class_of
step, class_of = mk(3, 1)
def Bw(v): return 3*v.count('a') + 4*v.count('b')
def ew(v): return 2*v.count('a') + 3*v.count('b')
def orbit(w, P, st=step):
    o = [w]
    for ch in P:
        l, w = st(w)
        assert l == ch
        o.append(w)
    return o

# ---------- Theorem A: random words + all repetitions (overlapping included), exact integer form
cnt = viol = ovl = 0
for trial in range(3000):
    n = random.randint(2, 14)
    P = ''.join(random.choice('ab') for _ in range(n))
    if random.random() < .5:  # force repetitions
        h = P[:random.randint(1, n)]; P = (h*4)[:n+3]
    r, B = class_of(P)
    for w0 in {r if r > 0 else 1 << B, r + (1 << B), r + random.randint(1, 50)*(1 << B)}:
        o = orbit(w0, P)
        for i in range(len(P)):
            for ip in range(i+1, len(P)):
                L = 0
                while ip+L < len(P) and P[i+L] == P[ip+L]:
                    L += 1
                    u = P[i:i+L]; p = P[:ip]; cnt += 1
                    if i+L > ip: ovl += 1
                    c1 = (o[ip]-o[i]) % (1 << Bw(u)) == 0 and o[ip]-o[i] >= 1 << Bw(u)
                    c2 = 2**(Bw(u)+Bw(p)) < (w0+1) * 3**ew(p)
                    c3 = (o[ip]+1) * 2**Bw(p) <= (w0+1) * 3**ew(p)
                    if not (c1 and c2 and c3): viol += 1
print(f'ThmA: {cnt} repetition instances ({ovl} overlapping), violations {viol}')

# ---------- (1.1) and exponent arithmetic
L3 = math.log2(3); T0 = 4/(3*L3-4)
print('T0 =', T0, ' 3/log2(9/8) =', 3/math.log2(9/8), ' kappa =', 1-3/T0, (16-9*L3)/4,
      ' 3^9<2^16:', 3**9 < 2**16, ' 6.2988?', T0+1, ' A1 const 3/(3log2(3)-4) =', 3/(3*L3-4))
# exact form of (1.1): B >= T0*G  <=>  B(3L-4) >= 4(eL - B) <=> 3^(3B-4e)... i.e. 2^(3B)... check integer: 3^(4e) <= 3^(3B) * ... do it as
# B*(3L-4) >= 4eL-4B  <=>  3B*L >= 4e*L  <=> 3B >= 4e   (pure integers!)
okk = all(3*(3*x+4*y) >= 4*(2*x+3*y) for x in range(60) for y in range(60))
print('(1.1) is equivalent to 3B(v) >= 4e(v), i.e. 9x+12y >= 8x+12y : holds:', okk)
# chain: 2^B(u) < (w0+1) 3^e(p)/2^B(p), e(p) <= 3B(p)/4, B(p) <= 3B(u)  =>  2^(4B(u)) < (w0+1)^4 3^(4e(p)) / 2^(4B(p)) <= (w0+1)^4 (27/16)^(B(p)) <= (w0+1)^4 (27/16)^(3B(u))
# => (w0+1)^4 3^(9B(u)) > 2^(16B(u)).  monotone in B(u) since 2^16 > 3^9.
print('integer chain: (27/16)^3 = 3^9/2^12, so 2^(4B) < (w0+1)^4 3^(9B)/2^(12B)  <=> (w0+1)^4 3^(9B) > 2^(16B): OK')

# ---------- B1: fixed points of random non-erasing binary morphisms; test finite-form bound at level t with sigma
def fixedpoint(phi, n):
    y = 'c'
    while len(y) < n:
        y2 = ''.join(phi[ch] for ch in y)
        if y2 == y: break
        y = y2
    return y[:n]
def lemma_shape_prefix(y):
    """shortest prefix of block word y of form cc or c d^k c^j d (None if not within y)"""
    if y.startswith('cc'): return 'cc'
    k = 1
    while 1+k < len(y) and y[1+k] == 'd': k += 1
    if 1+k >= len(y): return None
    j = 0
    while 1+k+j < len(y) and y[1+k+j] == 'c': j += 1
    if 1+k+j >= len(y): return None
    return y[:2+k+j]
tested = viol = 0; minr = 9
for trial in range(400):
    phi = {'c': 'c' + ''.join(random.choice('cd') for _ in range(random.randint(1, 3))),
           'd': ''.join(random.choice('cd') for _ in range(random.randint(1, 3)))}
    sig = {'c': ''.join(random.choice('ab') for _ in range(random.randint(1, 3))),
           'd': ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))}
    y = fixedpoint(phi, 400)
    pc, pd = 'c', 'd'
    for t in range(0, 4):
        # check decomposition y = phi^t(y)
        dec = ''.join(pc if ch == 'c' else pd for ch in y)
        assert dec[:len(y)] == y[:len(dec)][:len(y)] or dec.startswith(y) or y.startswith(dec[:len(y)])
        sh = lemma_shape_prefix(y)
        if sh is not None:
            X = ''.join(sig[ch] for ch in pc); Y = ''.join(sig[ch] for ch in pd)
            P = ''.join(X if ch == 'c' else Y for ch in sh)
            if len(P) < 3000:
                r, B = class_of(P); w0 = r if r > 0 else 1 << B
                tested += 1
                if not (w0+1)**4 * 3**(9*Bw(X)) > 2**(16*Bw(X)): viol += 1; print('B1 VIOL', phi, sig, t)
                minr = min(minr, (w0+1).bit_length()/Bw(X))
        pc = ''.join(phi[ch] for ch in pc); pd = ''.join(phi[ch] for ch in pd)
print(f'B1: random morphisms x levels tested {tested}, violations {viol}, min bits(w0+1)/B(X_t) ~ {minr:.3f}')

# ---------- B3: palindromic closure computed directly (no Justin), check u_{n+1} = t u_n, t prefix of u_n
def palcl(w):
    for i in range(len(w)):
        s = w[i:]
        if s == s[::-1]: return w + w[:i][::-1]
    return w
chk = bad = 0; b3viol = 0; b3t = 0
for trial in range(600):
    alph = 'xyz' if trial % 2 else 'xyzt'
    d = ''.join(random.choice(alph) for _ in range(random.randint(3, 9)))
    u = ''; seen = set()
    sig = {ch: ''.join(random.choice('ab') for _ in range(random.randint(1, 2))) for ch in alph}
    for ch in d:
        un = palcl(u + ch)
        if ch in seen:
            chk += 1
            t = un[:len(un)-len(u)]
            if not (un.endswith(u) and un == t + u and u.startswith(t) and len(t) <= len(u)): bad += 1
            else:
                P = ''.join(sig[c] for c in un)
                if len(P) < 1500:
                    r, B = class_of(P); w0 = r if r > 0 else 1 << B; b3t += 1
                    Bu = Bw(''.join(sig[c] for c in u))
                    # w0+1 > 2^((1-1/T0) Bu), 1-1/T0 = (8-3L)/4 :  (w0+1)^4 3^(3Bu) > 2^(8Bu)
                    if not (w0+1)**4 * 3**(3*Bu) > 2**(8*Bu): b3viol += 1
        seen.add(ch); u = un
print(f'B3: Justin-shape instances {chk}, shape failures {bad}; numeric bound tests {b3t}, violations {b3viol}')

# ---------- Prop D
def orbits_mod(m):
    par = list(range(m))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    i8, i16 = pow(8, -1, m), pow(16, -1, m)
    for w in range(m):
        for v in ((9*w+1)*i8 % m, 27*w*i16 % m):
            a, b = f(w), f(v)
            if a != b: par[a] = b
    from collections import Counter
    return sorted(Counter(f(w) for w in range(m)).values()), {f(w) for w in range(m) if w % 11 == 10} if m % 11 == 0 else None
badD = 0; two = 0
for m in range(5, 500):
    if math.gcd(m, 6) != 1: continue
    sizes, cls = orbits_mod(m)
    if m % 11:
        if sizes != [m]: badD += 1; print('D FAIL', m, sizes)
    else:
        two += 1
        if sizes != [m//11, 10*m//11] or len(cls) != 1: badD += 1; print('D FAIL', m, sizes)
print('PropD: commutator ab-ba =', F(1, 8) - F(27, 128), '; m<500 coprime to 6: failures', badD, '; two-orbit moduli', two)

# ---------- Litmus
words = [''.join(t) for n in range(1, 5) for t in itertools.product('ab', repeat=n)]
def scan(mult, sign, shift):
    st, co = mk(mult, sign); v = 0; c = 0; minr = 9; grow_fail = None
    for X in words:
        for Y in words:
            shapes = [X+X] + [X + Y*k + X*j + Y for k in range(1, 5) for j in range(1, 5)]
            for P in shapes:
                r, B = co(P); w0 = r if r > 0 else 1 << B
                o = orbit(w0, P, st)
                if any(o[i+1] <= o[i] for i in range(len(P))) and grow_fail is None: grow_fail = (w0, P[:6])
                c += 1; BX = Bw(X)
                if not (w0+shift)**4 * 3**(9*BX) > 2**(16*BX): v += 1
                minr = min(minr, math.log2(w0+shift)/BX)
    return c, v, round(minr, 4), grow_fail
print('litmus (3,+1):', scan(3, 1, 1))
print('litmus (3,-1): (cases, violations of 3-type conclusion, min log2(w0+1)/B(X), first non-growth)', scan(3, -1, 1))
print('litmus (5,+1): same 3-type conclusion tested on 5-system:', scan(5, 1, 1))
print('   5-system: T_b = 4/(3log2 5-4) =', 4/(3*math.log2(5)-4), ' T_a =', 3/(2*math.log2(5)-3), ' 2^(16/9) =', 2**(16/9), ' 5^9<2^16:', 5**9 < 2**16)
# 3n-1 on v>=2: growth holds; the negative-integer mirror
st, co = mk(3, -1)
print('   (3,-1) fixed point: step(1) =', st(1), ' ; conclusion at w0=1, X=a:', (1+1)**4 * 3**27 > 2**48)
# x = (36w-19)/11 at w=-1 :
print('   w=-1 <-> x =', F(36*(-1)-19, 11), '(the -5 cycle of 3n+1)')

# ---------- vacuity: longest itineraries of positive integers below 2^LIM
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 64
best_len = (0,); best_ratio = (0,); nodes = 0
stack = [('', 0, 0, 1, 0)]
bound = 1 << LIM
while stack:
    u, r, B, p3, W = stack.pop(); nodes += 1
    if u and r > 0:
        # is u the FULL itinerary start of r (r realises u; true itinerary of r may be longer -> will be visited deeper with same r)
        if len(u) > best_len[0]: best_len = (len(u), r, u)
        q = B/math.log2(r+1)
        if q > best_ratio[0] and len(u) >= 6: best_ratio = (q, r, u, B)
    s = ((7 - W) * pow(p3, -1, 8)) % 8
    r2 = r + (s << B); W2 = W + p3*s
    if r2 < bound: stack.append((u+'a', r2, B+3, p3*9, (9*W2+1)//8))
    s = ((-W) * pow(p3, -1, 16)) % 16
    r2 = r + (s << B); W2 = W + p3*s
    if r2 < bound and (r2 > 0 or B < LIM): stack.append((u+'b', r2, B+4, p3*27, 27*W2//16))
print(f'vacuity: DFS nodes {nodes}; longest itinerary of a positive w0 < 2^{LIM}: len {best_len[0]}, w0={best_len[1]}, word {best_len[2]}')
print(f'   max B(prefix)/log2(w0+1) (len>=6): {best_ratio}')
print('   (Theorem B is non-trivial only when B(X) > 2.305 log2(w0+1), i.e. needs B(itinerary) >= 2B(X) > 4.6 log2(w0+1))')
