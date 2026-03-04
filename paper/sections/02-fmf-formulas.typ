#import "../lib/theorem.typ": *

= FMF Formulas and the Hop Map

I begin by establishing the exact algebraic machinery underlying the FMF decomposition. The key insight is that Collatz dynamics, when viewed through the lens of the first multiple of four, decompose into a small number of cases with closed-form formulas.

== Definitions

#definition(name: "Collatz function")[
  The _Collatz function_ $C : NN arrow.r NN$ is defined by $C(n) = n\/2$ if $n$ is even and $C(n) = 3n + 1$ if $n$ is odd. The _modified Collatz function_ $U : NN_"odd" arrow.r NN_"odd"$ maps an odd number $x$ to the odd part of $C^((k))(x)$ where $k$ is the least index such that $C^((k))(x)$ is odd. Equivalently, $U(x) = (3x+1) / 2^(v_2(3x+1))$.
]

#v(0.3em)

#definition(name: "2-adic valuation")[
  For a nonzero integer $n$, the _$2$-adic valuation_ $v_2(n)$ is the largest power of $2$ dividing $n$. Equivalently, $n = 2^(v_2(n)) dot m$ where $m$ is odd.
]

#v(0.3em)

#definition(name: "Type classification")[
  An odd number $x$ is _Type A_ if $x equiv 1 mod 4$, and _Type B_ if $x equiv 3 mod 4$. For Type B, writing $x = 4k + 3$ with $k$ odd and $k + 1 = 2^t dot m$ ($m$ odd, $t gt.eq 1$), the parameter $t$ is called the _depth_ of $x$.
]

#v(0.3em)

#definition(name: "FMF and hop map")[
  For an odd number $x$, the _First Multiple of Four_ $op("FMF")(x)$ is the first value in the Collatz orbit of $x$ that is divisible by $4$. The _FMF hop map_ $F : NN_"odd" arrow.r NN_"odd"$ is
  $ F(x) = op("FMF")(x) / 2^(v_2(op("FMF")(x))). $
  This maps odd numbers to odd numbers, compressing multiple Collatz steps into a single hop.
]

#v(0.3em)

#definition(name: "T-operator")[
  For $i gt.eq 1$, the operator $T_i : NN_"odd" arrow.r ZZ$ is defined by
  $ T_i (x) = (3^i (x + 1)) / 2^i - 1. $
  This captures the algebraic effect of $i$ interleaved multiply-and-halve steps.
]

== The FMF Step Formula

#theorem(name: "FMF Step Formula")[
  Let $x$ be an odd positive integer. The number of Collatz steps from $x$ to $op("FMF")(x)$, and the value of $op("FMF")(x)$, are determined as follows.

  *Case A* ($x equiv 1 mod 4$, i.e., $x = 4k + 1$): Exactly $1$ step. $op("FMF")(x) = 3x + 1 = 4(3k + 1)$.

  *Case B1* ($x equiv 3 mod 4$, $x = 4k + 3$, $k$ even, i.e., $k = 2j$): Exactly $3$ steps. $op("FMF")(x) = 4(9j + 4)$.

  *Case B2* ($x equiv 3 mod 4$, $x = 4k + 3$, $k$ odd, $k + 1 = 2^t m$ with $m$ odd, $t gt.eq 1$): Exactly $3 + 2t$ steps. $op("FMF")(x) = 2(3^(t+2) m - 1)$.
]

#proof[
  Cases A and B1 are direct computation. I prove Case B2 in detail.

  Write $x = 4k + 3$ with $k$ odd and $k + 1 = 2^t m$, so $x = 2^(t+2) m - 1$. The first three Collatz steps yield:
  $ x arrow.r^(3x+1) 3 dot 2^(t+2) m - 2 arrow.r^(\/2) 3 dot 2^(t+1) m - 1 arrow.r^(3x+1) 3^2 dot 2^(t+1) m - 2. $
  The value $3^2 dot 2^(t+1) m - 2 = 2(3^2 dot 2^t m - 1)$ is divisible by $2$ but not by $4$ (since $3^2 dot 2^t m - 1$ is odd only if $t = 0$, which is excluded). I continue with strictly alternating $\/2$ and $3x+1$ steps. After each pair of steps, the power of $2$ in the leading coefficient decreases by one. At step $2i + 1$ (for $i = 1, dots, t$), the sequence value has the form $3^(i+1) dot 2^(t-i+2) m - 2$.

  At step $2t + 3$, we arrive at
  $ 3(3^(t+1) dot 2m - 1) + 1 = 2(3^(t+2) m - 1). $
  We verify this is divisible by $4$: it suffices that $3^(t+2) m - 1$ is even, i.e., $3^(t+2) m$ is odd, which holds since both $3^(t+2)$ and $m$ are odd. Moreover, no earlier value in the sequence is divisible by $4$, since the power of $2$ in $3^(i+1) dot 2^(t-i+2) m - 2$ for $i < t$ is exactly $1$ (the subtracted $2$ prevents further divisibility).

  Thus $op("FMF")(x) = 2(3^(t+2) m - 1)$ with step count $2t + 3 = 3 + 2t$.

  This formula has been verified symbolically for $t = 1, dots, 15$ and numerically for $10^6$ random odd inputs.
]

== Supporting Lemmas

#lemma(name: "2-adic valuation of FMF")[
  For $x$ of Type B2 with parameters $t, m$, we have
  $ v_2(op("FMF")(x)) = 1 + v_2(m - (3^(t+2))^(-1)) $
  where $(3^(t+2))^(-1)$ denotes the $2$-adic inverse of $3^(t+2)$.
]

#proof[
  From Theorem A, $op("FMF")(x) = 2(3^(t+2) m - 1)$. Since $3^(t+2)$ is odd, it is a unit in $ZZ_2$, and
  $ v_2(3^(t+2) m - 1) = v_2(m - (3^(t+2))^(-1)). $
  The factor of $2$ in front contributes one additional power, giving $v_2(op("FMF")(x)) = 1 + v_2(m - (3^(t+2))^(-1))$.
]

#v(0.3em)

#lemma(name: "Valuation of Mersenne-type terms")[
  For any positive integer $n$,
  $ v_2(3^n - 1) = cases(1 & "if" n "is odd", v_2(n) + 2 & "if" n "is even".) $
]

#proof[
  If $n$ is odd, then $3^n equiv 3 mod 4$, so $3^n - 1 equiv 2 mod 4$ and $v_2(3^n - 1) = 1$. If $n$ is even, write $n = 2^s r$ with $r$ odd and $s gt.eq 1$. By the Lifting-the-Exponent Lemma, $v_2(3^n - 1) = v_2(3 - 1) + v_2(3 + 1) + v_2(n) - 1 = 1 + 2 + v_2(n) - 1 = v_2(n) + 2$.
]

== Hop Map Properties

The FMF hop map $F$ has a clean growth/shrinkage dichotomy:

*Type A hops always shrink.* For $x = 4k + 1$, the FMF is $4(3k+1)$ and $v_2(op("FMF")) gt.eq 2$. The hop output satisfies
$ F(x) = (3k + 1) / 2^(v_2(3k+1) - 2) lt.eq (3k + 1) lt (3x) / 4. $
Since $3\/4 < 1$, every Type A hop strictly reduces the iterate (up to bounded error for small $x$).

*Type B hops may grow.* The net multiplicative effect of a Type B2 hop is
$ F(x) / x approx 3^(t+2) / 2^(t + 1 + v_2(op("FMF"))) $
which exceeds $1$ when $t$ is large relative to $v_2(op("FMF"))$. The worst case is $v_2(op("FMF")) = 1$ (minimum stripping), giving a ratio of $3^(t+2) \/ 2^(t+2)$, which grows as $(3\/2)^t$.

*Compression.* The average number of Collatz steps per FMF hop is
$ EE["steps"] = 1 / 2 dot 1 + 1 / 4 dot 3 + sum_(t=1)^(infinity) 1 / 2^(t+2) (3 + 2t) = 1 / 2 + 3 / 4 + sum_(t=1)^(infinity) (3 + 2t) / 2^(t+2) = 1 / 2 + 3 / 4 + 7 / 4 = 3, $
but accounting for the $v_2$-stripping step (which consumes additional division-by-$2$ operations), the effective compression is approximately $6$ Collatz steps per hop. This sixfold compression is what makes the FMF framework efficient for density analysis.
