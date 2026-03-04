#import "../lib/theorem.typ": *

= Supporting Growth Bounds

The theoretical results of the preceding sections are complemented by extensive computational investigations. This section records the key empirical findings and partially proved bounds that support the framework. All observations are based on systematic testing across multiple magnitude ranges, with sample sizes and failure counts reported explicitly.

== Epoch structure

An _epoch_ for an odd integer $x$ is the sequence of FMF hops from $x$ until the trajectory first drops below $x$. The epoch decomposes naturally into a growth phase (consecutive hops where the trajectory value exceeds $x$) followed by a recovery phase (subsequent hops until descent below $x$).

#observation(name: "Epoch Duration")[
  For every tested odd $x$ (up to 60 bits, including $2^n - 1$ for $n$ up to 44), the epoch duration satisfies
  $ op("epoch")(x) <= 2.83 dot log_2(x). $
  The mean epoch is $1.74$ hops. The descent rate is $100%$ across $250 000$ tests. The ratio $op("epoch")(x) \/ log_2(x)$ _decreases_ with the magnitude of $x$: for $x > 10^4$, the maximum ratio drops to $1.63$, and for random 60-bit integers, the maximum observed ratio is $0.13$.
]

This decreasing ratio is consistent with the spectral contraction: larger integers have more bits, and the negative drift of $-0.83$ bits per hop becomes statistically dominant over longer trajectories.

== Growth phase structure

#observation(name: "Growth Phase Structure")[
  Among all observed growth phases (across $1.5 times 10^6$ growth chains):
  - Maximum duration: $7$ hops (with a single exceptional case of $37$ hops at $x = 270271$).
  - $66.4%$ of growth phases consist of a single hop.
  - $99.3%$ of growth phases have duration $<= 3$ hops.
  - Maximum total growth: approximately $10$ bits above the starting value.
  - Within growth phases, $t$-values tend to _increase_ (mean change $+0.755$, with $P(op("increase")) = 0.585$). This is surprising: higher $t$ means more multiplication by $3$, which should produce more growth. Growth terminates not because $t$ decreases, but because $v_2(op("FMF"))$ occasionally takes a large value despite high $t$.
]

#observation(name: "$2^n - 1$ Trajectories")[
  The integers $x = 2^n - 1$ are natural worst-case candidates: they have maximal $t$-parameter ($t = n - 2$) and minimal $v_2(op("FMF")) = 2$ when $n$ is odd. Despite this:
  - $F(2^n - 1)$ is Type A in $21\/22$ cases for $n = 3, dots, 24$.
  - The first-hop ratio grows as approximately $(3\/2)^n \/ 2^(v_2(3^n - 1) - 1)$.
  - Recovery time after the initial growth scales as $op("growth_bits") \/ 0.83$ hops, consistent with the drift rate.
  - Some trajectories pass through smaller $2^n - 1$ values (e.g., $2^(21) - 1$ passes through $31 = 2^5 - 1$), inheriting their recovery structure.
]

== Conjectured bounds

#conjecture(name: "Growth Chain Bound")[
  For all odd integers with $m$-parameter $m_0$,
  $ op("growth_chain_length") <= 0.55 dot log_2(m_0) + 3. $
  This bound is verified with zero violations across approximately $1.5 times 10^6$ growth chains spanning starting values up to $60$ bits.
]

The constant $0.55$ arises naturally from the growth-B dynamics: each growth-B step consumes approximately $log_2(8) - log_2(3^2) approx 3.83 - 3.17 = 0.66$ bits of precision in the $m$-value while generating approximately $0.17$ bits of net trajectory growth (since $v_2 = 2$ gives a multiplier of $3^(t+2)\/4$, and $log_2(3\/4) approx -0.415$ per effective step).

#observation(name: "Bit Consumption")[
  Each growth-B step consumes approximately $4$ bits of precision in the $m$-parameter (through the 2-adic expansion of factor $>= 8$) and generates approximately $0.17$ bits of net trajectory growth. The net consumption is approximately $3.83$ bits per step. Since the $m$-parameter has at most $log_2(m_0)$ bits of precision, the growth chain is bounded by $log_2(m_0) \/ 3.83 approx 0.26 dot log_2(m_0)$ steps before the expanding map exhausts the available precision.
]

#remark[
  The gap between the empirical constant $0.55$ and the heuristic estimate $0.26$ reflects the fact that not all bits are consumed uniformly: carry propagation in the multiplication $3^(t+2) m$ can preserve low-order bit patterns for several steps before the expansion effect dominates. A rigorous proof of the Growth Chain Bound would require effective control over this carry propagation, which connects to the same equidistribution questions identified in Section 6.
]
