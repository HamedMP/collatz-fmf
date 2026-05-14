#v(0.8em)
#text(size: 1.45em, weight: "bold")[Notation Guide]

The paper uses three levels of notation: the original Collatz map, the FMF
hop map, and the reduced return/gap obstruction maps. This table collects the
symbols most often used later.

#table(
  columns: (1.05fr, 2.8fr),
  inset: 5pt,
  [*Symbol*], [*Meaning*],
  [$C(n)$], [The ordinary Collatz map: $n\/2$ for even $n$, and $3n+1$ for odd $n$.],
  [$op("FMF")(x)$], [The first value divisible by $4$ reached from an odd input $x$ before stripping all powers of $2$.],
  [$F(x)$], [The odd-to-odd FMF hop obtained from $op("FMF")(x)$ by dividing by its full $2$-adic valuation.],
  [Type A], [Odd inputs $x equiv 1 mod 4$; this is the pointwise shrinking FMF channel except for $x=1$.],
  [Type B], [Odd inputs $x equiv 3 mod 4$, written $x=2^(t+2)m-1$ with $m$ odd and $t>=0$.],
  [$R=F(x)\/x$], [The FMF hop ratio used in the fractional-moment contraction theorem.],
  [growth-B hop], [A Type B hop with minimal FMF valuation $v_2(op("FMF"))=2$; this is the strict growth mechanism counted by the Quartering Law.],
  [$r=(r_0,dots,r_(L-1))$], [A binary return word; $r_i$ is a return length in the reduced binary-depth return map.],
  [$R_w,Q_w$], [For a finite return word $w$, the least prefix residue and dyadic modulus of the corresponding return-code congruence.],
  [$N_R(B,L)$], [The number of length-$L$ return words with least prefix residue at most $B$.],
  [$k=(k_0,dots,k_(L-1))$], [A reduced ${0,1}$ gap word; $k_i$ is a zero-gap length between length-$1$ returns.],
  [$S_w,H_w$], [For a finite gap word $w$, the least prefix residue and dyadic modulus of the corresponding gap-code congruence.],
  [$N_G(B,L)$], [The number of length-$L$ gap words with least prefix residue at most $B$.],
  [$W_R(B,L), W_G(B,L)$], [Terminal-window versions of the same finite-height counts. The missing rank theorem asks for sharp unweighted bounds on these quantities.],
)

#v(0.4em)

The letters $R_w$ and $S_w$ always denote least prefix residues, while $R$
without a subscript denotes the hop ratio. The return and gap systems are not
new Collatz maps; they are reduced partial maps for the first bounded-depth
pointwise obstruction classes isolated in Sections 6--8.
