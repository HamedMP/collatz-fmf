"""litmus_scan.py -- records of T_k = H_k + s_k for the litmus maps (exact ints).
Run: taskset -c 2 /home/matrix/home/projects/collatz/venv/bin/python litmus_scan.py > ../data/litmus_scan.txt
Maps: (a,d,sign): 3n+1 (control), 5n+1 (y = 3x+1), 3n-1 (negative x under 3n+1; y = x+1 < 0),
3n+5 (y = x+5).  Per bit-length n of |y0|: max T_k, argmax x0, max T_k - n.  Orbits hitting y = 0
(only possible for 3n-1: x -> -1) are counted separately (T = infinity; excluded from the theorem).
"""
import sys
def v2(x):
    x = abs(x); return (x & -x).bit_length() - 1
def run(name, a, d, xs):
    best = {}; inf = {1: 0, 2: 0, 3: 0}
    for x0 in xs:
        y0 = (a - 2) * x0 + d
        if y0 == 0: continue
        n = (abs(y0) - 1).bit_length()
        y = y0; H = 0
        for k in (1, 2, 3):
            s = v2(y); m = y >> s
            p = a ** s * m - d; v1 = v2(p)
            y = (p >> v1) + d; H += s + v1
            if y == 0:
                for kk in range(k, 4): inf[kk] += 1
                break
            T = H + v2(y)
            if T > best.get((k, n), (0, 0))[0]: best[(k, n)] = (T, x0)
    print(f"## {name}: orbits reaching y=0 within k hops: {inf}")
    for k in (1, 2, 3):
        row = []
        for n in range(8, 24):
            if (k, n) in best:
                T, x0 = best[(k, n)]
                row.append(f"n={n}:T={T}(+{T-n})@{x0}")
        print(f"k={k}: " + "  ".join(row))
N = 1_000_000
run("3n+1", 3, 1, range(3, N, 2))
run("5n+1 (y=3x+1)", 5, 1, range(1, N // 3, 2))
run("3n-1 (negative x)", 3, 1, range(-3, -N, -2))
run("3n+5 (y=x+5)", 3, 5, range(1, N, 2))
