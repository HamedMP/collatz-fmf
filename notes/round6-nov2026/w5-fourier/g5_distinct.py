# are the rationals r = f_v(z) (parametrising E_K) distinct mod 1 ?  (needed for Parseval over zeta)
import sys
from fractions import Fraction as Fr
K = int(sys.argv[1]); st = [(0, 0, 0)]; rs = []
while st:
    P, Q, D = st.pop()
    if K - Q <= 3:
        for z in ([0] if K == Q else [0, -1]): rs.append(Fr(z*(1 << Q) - D, 3**P) % 1)
        continue
    st.append((P+2, Q+3, 9*D + (1 << Q))); st.append((P+3, Q+4, 27*D))
print("K=%d points=%d distinct mod 1=%d" % (K, len(rs), len(set(rs))))
