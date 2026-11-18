"""Lemma F4 support: for every L<=LMAX, with a = largest a with 3^a < 2^L, check 2^L - 3^a > (3/2)^a - 1
(hence F(x) >= x  <=>  3^a(x) > 2^L for all x of level L).  Also Ellison-type margin statistics.
usage: python check_gap.py 20000 -> 'gap check ok up to L=20000' """
import sys
from fractions import Fraction
LMAX=int(sys.argv[1]); a=0; p3=1; worst=(9,0)
for L in range(1,LMAX+1):
    while p3*3 < (1<<L): p3*=3; a+=1
    gap=(1<<L)-p3
    assert gap*2**a > 3**a - 2**a, L          # gap > (3/2)^a - 1, exact
    # margin exponent: log2(gap)/L
    r=(gap.bit_length()-1)/L
    if L>=28 and r<worst[0]: worst=(r,L)
print("gap check ok up to L=%d; min floor(log2(2^L-3^a))/L for L>=28: %.4f at L=%d (needs > 0.369)"%(LMAX,worst[0],worst[1]))
