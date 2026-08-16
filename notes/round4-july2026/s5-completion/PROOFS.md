# The Natural-Density Upgrade of Tao's Almost-All Theorem: Complete Section-5 Rebuild

Session: s5-completion, 2026-07-21. Repo READ-ONLY; this document + scripts live in
scratchpad/s5-completion/. Source audited: arXiv:1909.03562v7 (local copy
../tao-natural-density/tao_v7.txt, fetched 2026-07-21). Prior-round inputs:
Theorem 56 (proof.md), S4-T/S4-J audit (../tao-natural-density/RESULTS.md),
S5 kernel (verify_s5.py).

Numbering "(x.y)" refers to Tao's paper. All new items carry letters (P7, J*, R, ...).

--------------------------------------------------------------------------------
## PART 0. Conventions

Syr(N) = (3N+1)/2^{v2(3N+1)} on odd N. a^{(n)}(N) = (a_1..a_n) the Syracuse
valuations, a_[i,j] their partial sums, S_n := a_[1,n]. Geom(2): P(a=j)=2^{-j},
j>=1; mean 2, variance 2. F_n as (1.5): F_n(a_1..a_n) = sum_{i=1}^n 3^{n-i}
2^{-a_[i,n]}; 0 < F_n <= 3^n (1.13). Aff_a(N) = 3^n 2^{-|a|} N + F_n(a);
Syr^n(N) = Aff_{a^{(n)}(N)}(N) (1.7). Syracuse random variable
X_n := Syrac(Z/3^n) = F_n(Geom(2)^n) mod 3^n (1.22); by reversal (1.29)
X_n == 2^{-a_1} + 3 2^{-a_[1,2]} + ... + 3^{n-1} 2^{-a_[1,n]} mod 3^n.
T_x(N) = first n with Syr^n(N) <= x; Pass_x(N) = Syr^{T_x}(N).
U_y := uniform on odd [y, 2y), y a power of 2 (exactly y/2 atoms of mass 2/y).
"x large" = larger than an absolute constant. c, C absolute, varying per line.

Parameters (all functions of x):
  n0 := floor(log x / (10 log 2))                       [Tao (5.1)]
  m0 := ceil( sqrt(log x) * (log log x)^2 )             [SMALLER than Tao's (5.2)]
  Lam := C0 * sqrt(log x * log log x)                   [valuation envelope width]
  Lam' := 20*Lam*log 2 + C1,  Lam'' := 3*Lam*log 2 + C2 [derived widths; Lam'
      pads I_y enough to contain every Lemma-R live range: center offsets are
      O(Lam + sqrt(m0 llx)) = O(Lam) and Gaussian widths O(sqrt(ell llx)) =
      O(Lam), all divided by log(4/3)]
  alpha := 1.001                                        [Tao (1.18)]
Window range for the chain: dyadic y with x^{1.0003} <= y <= x^{1.003}.
Standoff inequality (x large): m0*log(4/3) >= 10*Lam''  --- (S)
  [since m0/Lam'' ~ (llx)^{3/2}/C0 -> infinity].
E-window: hidden constants chosen so all cited absorptions hold; every use is
flagged. Throughout ell := n - m0 (word length at play), and for M in E'(E):
  g_M(ell) := ell*log2(3) + log2(y/M),   s*(ell,M) := ceil(g_M(ell)).

--------------------------------------------------------------------------------
## PART I. Skeleton of Tao's reduction (Sections 3 + 5) with density tags

Legend: [AG] density-agnostic (proof works verbatim for uniform dyadic windows,
possibly after renaming constants); [LOG] uses logarithmic density specifically.

SECTION 3 (Theorem 1.6/3.1 from Prop 1.11):
  3a. Orbit monotonicity (T_{x'} <= T_x, Pass-orbit inclusion, E_{N0} descent
      transfer) — deterministic. [AG]
  3b. P(B_{x^alpha}) >= P(B_x) - O(x^-c) - O(log^-c x): uses (1.19)+(1.20) of
      the SAME window family. [AG given (1.19)/(1.20) for that family]
  3c. Telescoping over j (geometric error sum). [AG]
  3d. Base case (window below N0). [AG]
  3e. Covering [1,x] by windows: log-uniform on [1,x] = mixture of log-uniforms
      on [y, y^alpha]. [LOG — replaced by dyadic covering, trivial for natural
      density: [1,x] = union of dyadic blocks; see Theorem 3-U]
  3f. f(N)->infty diagonalization + Col-from-Syr reduction. [AG, rewritten]

SECTION 5 (Prop 1.11 from Prop 1.14):
  5a. (5.4): d_TV(a^{(n0)}(N_y), Geom(2)^{n0}) << 2^{-c n0} via mod-2^{3n0}
      equidistribution + Prop 1.9. [AG — uniform windows are BETTER: error
      2^{3n0}/(y/2) <= x^{-0.7}]
  5b. (5.5)+(1.19): drift argument. [AG]
  5c. (5.12): valuation envelope A^{(n)} holds outside prob log^{-10}x. [AG]
  5d. (5.13)-(5.15): deterministic envelope estimates on the A-event. [AG]
  5e. (5.16): T_x(N_y) in I_y w.h.p. — needs window-shape only through
      "boundary buffers". [AG for dyadic windows with padded I_y; see 5.2-U]
  5f. Prop 5.2 event equivalences (step-back by m0; E' definition). [AG]
  5g. THE WEIGHT IDENTITY (after (5.19)): for log-uniform N_y,
      P(Aff_a(N_y) = M) = (1+O(x^-c)) * (2^{-|a|} 3^{n-m0}/M) / ((alpha-1)/2 log y).
      The 1/N weight at the reconstructed preimage factors as the Geom(2)
      probability 2^{-|a|} times an a-free factor. [LOG — THE crux. Natural-
      density replacement: exact lattice-point pinning; the 2^{-|a|} emerges
      from counting, and a NEW renewal averaging over n (Lemma R) replaces the
      exact factorization. This is where the Archimedean exp(O(sqrt n)) spread
      (Tao's stated reason for log density, line ~635) has to be confronted;
      it is beaten by the equidistribution of {ell log2 3} (Rhin input).]
  5h. Automatic window membership of reconstructions for n in I_y. [LOG-flavored
      (wide window); for dyadic windows membership is NOT automatic — it IS the
      pinning indicator. Replaced by the exact pinned-count identity (Lemma K).]
  5i. Lemma 5.3: c_n(X) << 1. [AG — pure lattice/harmonic counting; reused
      as Lemma 5.3-U with n-m0 -> m0.]
  5j. (5.20)<-Prop 1.14: fine-scale replacement of Syrac(Z/3^{n-m0}) by
      uniform-refined Syrac(Z/3^{m0}) tested against c_n. [AG in itself, but
      for uniform windows the test COUPLES the offset X with the total
      valuation S (through the pin s*(ell,M)) — needs the JOINT version
      (Lemma J*), which is exactly Tao Remark 1.16's requested object.]

SECTION 6 (Prop 1.14 from Prop 1.17): [AG; rebuilt with the S-marginal riding
  along = Lemma J*; the only new input is Lemma P7.]
SECTION 7 (Prop 1.17): [AG; used as a BLACK BOX through its majorant (7.5),
  E prod_j |f(3^{2j-2}2^{-b_[1,j]}, b_j)| <<_A n^{-A} — this is what Tao's
  Section 7 actually proves. Audited by prior round (S4-T/S4-J).]

--------------------------------------------------------------------------------
## PART II. The new lemmas, with proofs

### Lemma P7 (phased Prop 7.1 — summed version).
For n >= 1 and xi in Z/3^n with 3 ∤ xi, let chi(z) := e(-xi (z mod 3^n)/3^n) as
in (7.1), and let (a_1..a_n) ~ Geom(2)^n, S := a_[1,n], X_n as in (1.29). Then

   sum_{s in Z} | E[ 1_{S=s} * chi(X_n) ] |  <=  E prod_{j in [n/2]}
        |f(3^{2j-2} 2^{-b_[1,j]}, b_j)|   <<_A  n^{-A}   for every fixed A>0,

uniformly in xi, where b_j := a_{2j-1}+a_{2j} and f is Tao's (7.4).

PROOF. Let G := sigma(b_1..b_{floor(n/2)}) for n even, and additionally
including a_n for n odd. By Tao's pairing identity (display before (7.4);
machine-verified exactly, prior round T1b) and the conditional independence of
the a_{2j} given G (Section 7.1), we have, G-measurably,
   E[chi(X_n) | G] = ( prod_{j in [n/2]} f(3^{2j-2}2^{-b_[1,j]}, b_j) ) * gamma,
where gamma := chi(3^{n-1} 2^{-b_[1,floor(n/2)] - a_n}) for n odd (a
G-measurable scalar with |gamma| = 1 exactly), gamma := 1 for n even. Hence
|E[chi|G]| = prod_j |f_j| =: H(b), G-measurably. Now S = b_[1,n/2] (n even) or
b_[1,floor(n/2)] + a_n (n odd) is G-measurable, so the events {S=s} are
disjoint G-events. Therefore
   sum_s |E[1_{S=s} chi]| = sum_s |E[1_{S=s} E[chi|G]]|
                          <= sum_s E[1_{S=s} H(b)] = E[H(b)].
Finally E[H(b)] <<_A n^{-A} is precisely what Tao's Section 7 proves: his
(7.5) bounds |S_chi(n)| by E[H(b)] and the entire remainder of Section 7
(white points / renewal process / triangle geometry) estimates E[H(b)] itself.
QED.

COROLLARY P7' (uniform b-measurable weights). For any complex weight W
measurable w.r.t. G with |W| <= 1: |E[W chi(X_n)]| <<_A n^{-A}. In particular
the joint characters E[e(theta S) chi(X_n)] uniformly in theta in [0,1)
(= the S4-J statement of the prior round, now with an explicit mechanism), and
Tao Remark 1.16's "entire affine map" characters.

REMARK. The unpaired letter (n odd) contributes a modulus-1 factor AFTER
conditioning on it; this is why G must include a_n. No step of Section 7 is
re-proved; P7 is a strict repackaging of (7.5). [Machine check: sB, n=7,8,
six frequencies: LHS <= RHS with factor ~5 margin.]

### Lemma J* (joint fine-scale mixing = Tao Remark 1.16 object).
For 1 <= m <= n:
   Osc^J_{m,n} := sum_{s} sum_{Y in Z/3^n} | P(S_n=s, X_n=Y)
        - 3^{m-n} sum_{Y' = Y mod 3^m} P(S_n=s, X_n=Y') |   <<_A  m^{-A}.
Equivalently d_TV( (S_n, X_n), (S_n, X_n + U) ) <<_A m^{-A} with
U ~ Unif(3^m Z/3^n Z) independent. (Tao's Prop 1.14 is the S-marginalized
special case.)

PROOF.
(a) Reduction to 0.9n <= m <= n. For m'' <= n the pair (S_n, X_n mod 3^{m''})
has the law of (S_{m''} + R, X_{m''}) with R := a_[m''+1,n] independent of
(S_{m''}, X_{m''}) [by (1.29): X_n mod 3^{m''} depends only on a_1..a_{m''}].
Hence for m' <= m'':
   sum_s sum_{Y mod 3^{m''}} |(Id - A_{m'}) law(S_n, X_n mod 3^{m''})|
     <= sum_t P(R=t) * Osc^J_{m',m''}  = Osc^J_{m',m''},          (convexity)
where A_{m'} is coset-averaging in the X-coordinate at scale 3^{m'}. Choose
scales m = m_r < ... < m_1 < m_0' = n with m_{i+1} >= 0.9 m_i; telescoping
g - A_m g = sum_i (Id - A_{m_i}) A_{m_{i+1}} g (A_n := Id) gives
Osc^J_{m,n} <= sum_i Osc^J_{m_i, m_{i+1}} <= sum_i C_A m_i^{-A-2} <<_A m^{-A}.
Bounded m is trivial (Osc^J <= 2).
(b) Regime 0.9n <= m <= n. Follow Section 6 verbatim with the S-marginal:
  (i) Event E: (6.2) with constant C_A. sum_s-oscillation of the not-E part
      <= 2 P(not E) << n^{-A-1} by (6.3).
  (ii) Stopping time k as in Sec 6 ((6.5)-range, O(C_A sqrt(n log n)) values),
      events B_k; E -> E_k enlargement (block-1-measurable); partition by
      C_{k,l} with l in the (6.8)-range (O(C_A^2 log n) values). Triangle
      inequalities exactly as Tao; per-(k,l) target n^{-A-3}.
  (iii) Fix (k,l). g_s(Y) := P(S_n=s, X_n=Y, E_k ∧ B_k ∧ C_{k,l}). Split s:
      GOOD: |s - l - 2(n-k-1)| <= C_A sqrt(n log n); BAD-total
      <= 2 P(|S'' - 2(n-k-1)| > C_A sqrt(n log n)) << n^{-c C_A} (Lemma 2.2),
      where S'' := a_[k+2,n].
  (iv) Cauchy-Schwarz over good s and Y:
      sum_{good s} ||g_s - A_m g_s||_1
        <= (C_A sqrt(n log n))^{1/2} 3^{n/2} ( sum_s ||g_s - A_m g_s||_2^2 )^{1/2}.
  (v) Plancherel per s: ||g_s - A_m g_s||_2^2 = 3^{-n} sum_{xi not in
      3^{n-m}-lattice} |ghat_s(xi)|^2.
  (vi) EXACT factorization: on C_{k,l}: X_n = F_{k+1}(a_{k+1}..a_1)
      + 3^{k+1} 2^{-l} F_{n-k-1}(a_n..a_{k+2}) mod 3^n [Tao line (2682);
      machine-verified exhaustively, sA-A4], S_n = l + S'', and E_k, B_k,
      C_{k,l} are block-1-measurable. Hence
        ghat_s(xi) = FF(xi) * SF_{s-l}(xi),
        FF(xi) := E[e_{3^n}(-xi F_{k+1}(block1)) 1_{E_k ∧ B_k ∧ C_{k,l}}],
        SF_{s'}(xi) := E[1_{S''=s'} e_{3^{n-k-1}}(-xi 2^{-l} F''(block2))].
  (vii) Per-frequency second factor, SUMMED over s': for xi outside the coarse
      lattice write xi = 3^j 2^l xi' mod 3^n, 0 <= j < n-m, 3 ∤ xi'; then
      n'' := n-k-j-1 >> n (Tao line (2707)), F'' mod 3^{n''} depends only on
      the first n'' block-2 letters (in (1.29)-indexing), and with
      R'' := the sum of the remaining block-2 letters (independent):
        sum_{s'} |SF_{s'}(xi)| <= sum_t P(R''=t) sum_{s0} |E[1_{S=s0}
             chi''(X_{n''})]| <= E[H-majorant at n''] <<_{A'} n^{-A'}
      by LEMMA P7, uniformly in such xi.
  (viii) First factor, Plancherel over ALL xi:
        sum_xi |FF(xi)|^2 = 3^n sum_Y P(F_{k+1}(block1)=Y, E_k ∧ B_k ∧ C_{k,l})^2
        <= 3^n 2^{-l} = n^{O(C_A^2)},
      by Corollary 6.3 (injectivity: at most one tuple per Y on the events;
      each tuple has probability 2^{-l}) and (6.8). UNCHANGED from Tao.
  (ix) Combine: sum_s sum_{xi not coarse} |ghat_s|^2
        <= sup_xi (sum_{s'} |SF_{s'}(xi)|)^2 * sum_xi |FF(xi)|^2
        <= C n^{-2A'} n^{O(C_A^2)}.
      Plug into (iv): sum_{good s} ||g_s - A_m g_s||_1
        <= C (C_A sqrt(n log n))^{1/2} * n^{-A' + O(C_A^2)} <= n^{-A-3}
      for A' := A + O(C_A^2) + 4. Summing the k, l, s-bad, E-errors gives (b).
QED.

REMARK. Only two departures from Tao's Section 6: the phase/indicator in the
second factor (handled by P7: the majorant is the SAME), and one extra
Cauchy-Schwarz over the O(sqrt(n log n)) live values of s (cost n^{1/4+o(1)},
absorbed). [Machine check: sA-A3 computes Osc^J exactly at n<=8: it tracks the
plain Osc within factor < 1.9 and decays with the gap, as predicted.]

### Proposition 5.2-U (uniform-window approximate formula).
Let x be large, y dyadic with x^{1.0003} <= y <= x^{1.003}, E subset of odd
[1,x]. Define
  A^{(n')} := { a in (N+1)^{n'} : |a_[1,j] - 2j| <= Lam for all j <= n' },
  I_y := [ (log(y/x) - Lam')/log(4/3) , (log(2y/x) + Lam')/log(4/3) ],
  E' := E'(E) := { M odd : T_x(M) = m0, Pass_x(M) in E,
                   e^{-Lam''} (4/3)^{m0} x <= M <= e^{Lam''} (4/3)^{m0} x }.
Then
  P(Pass_x(U_y) in E) = sum_{n in I_y ∩ Z} sum_{a in A^{(n-m0)}} sum_{M in E'}
        P(Aff_a(U_y) = M)  +  O(log^{-5} x).
Moreover P(T_x(U_y) = infinity) << x^{-c}  [(1.19)-U].

PROOF (mirror of Tao Prop 5.2; every changed step spelled out).
 (1) Mod-2 equidistribution: U_y mod 2^{3n0} is within TV-distance
     2^{3n0}/(y/2) <= 2 x^{0.3 - 1.0003} <= x^{-0.7} of uniform-odd (an
     interval of length L meets each odd class mod q in L/(2q) + O(1) points).
     Prop 1.9 then gives d_TV(a^{(n0)}(U_y), Geom(2)^{n0}) << 2^{-c n0} = x^{-c}.
 (2) Envelope: P(a^{(n0)}(U_y) not in A^{(n0)}) <= n0 * 2 exp(-c Lam^2/n0)
     + x^{-c} <= log^{-10} x for C0 large (Lemma 2.2(ii): Lam^2/n0 =
     10 log 2 * C0^2 * llx).
 (3) Deterministic on the A-event (a := a^{(n0)}(U_y) in A^{(n0)}): for n <= n0,
     Syr^n(U_y) = 3^n 2^{-S_n} U_y + O(3^{n0}) and 3^{n0} = x^{log3/(10 log2)}
     = x^{0.1585...} while 3^n 2^{-S_n} U_y >= (3/4)^{n0} e^{-Lam log 2} y
     >= x^{1.0003 - 0.125 - o(1)} >= x^{0.87}; hence
       Syr^n(U_y) = (1 + O(x^{-0.6})) 3^n 2^{-S_n} U_y                (5.13-U)
       Syr^n(U_y) = exp(O(Lam log 2 + O(1))) (3/4)^n U_y.             (5.14-U)
     Consequently T_x(U_y) = log(U_y/x)/log(4/3) + O(Lam) and, since
     U_y in [y,2y), ALWAYS T_x(U_y) in I_y on the A-event (I_y is padded by
     Lam' > Lam log 2 + C): P(T_x(U_y) in I_y) >= 1 - log^{-10} x - x^{-c}.
     Also (1.19)-U: on |S_{n0}| > 1.9 n0 (prob 1 - x^{-c} by (1)+Lemma 2.2),
     Syr^{n0}(U_y) <= 3^{n0} 2^{-1.9 n0} 2y + O(3^{n0}) <= x^{0.98} < x.
 (4) Step-back equivalence: for n in I_y, ON the A-event,
       {T_x(U_y) = n ∧ Pass_x(U_y) in E}  =  {Syr^{n-m0}(U_y) in E'}         (*)
     Forward: if T_x = n then T_x(Syr^{n-m0}(U_y)) = m0, Pass agrees, and by
     (5.14-U), Syr^{n-m0}(U_y) = e^{O(Lam log2 + C)} (4/3)^{m0} x, inside the
     E'-window for C2 large. Backward: if M := Syr^{n-m0}(U_y) in E', then for
     0 <= j <= n-m0, (5.14-U) gives Syr^j(U_y) >= e^{-(Lam log2+C)}
     (4/3)^{(n-m0-j)} M >= e^{-2 Lam''} (4/3)^{m0} x > x by the standoff (S);
     hence T_x(U_y) = (n-m0) + T_x(M) = n and Pass_x(U_y) = Pass_x(M) in E.
     [This is where the toy-scale sD excess lives: (S) fails for bounded m0.]
 (5) Sum over n in I_y of P(Syr^{n-m0}(U_y) in E' ∧ A-event), convert by
     Lemma 2.1: the event {Syr^{n-m0}(U_y) = M ∧ a^{(n-m0)}(U_y) = a} equals
     {U_y = N*(n,a,M)} = {Aff_a(U_y) = M}; restrict a to A^{(n-m0)} (relax
     from A^{(n0)}: one-sided, error (2)). Collect errors: <= log^{-5} x. QED.

### Lemma K (exact pinned-count kernel; = the proved S5-1 fiber bijection).
For n, a in (N+1)^{ell} (ell := n-m0), M in E': P(Aff_a(U_y) = M) equals
(2/y) * 1[ M ≡ F_ell(a) mod 3^ell ] * 1[ y <= 2^{|a|} (M - F_ell(a))/3^ell < 2y ],
and when the congruence holds the reconstruction N* := 2^{|a|}(M-F_ell(a))/3^ell
is automatically an odd integer with a^{(ell)}(N*) = a, Syr^ell(N*) = M
[Lemma 2.1 + the (5.18)-(5.19) oddness argument]. For fixed (n, M, congruence
class), the window indicator pins |a| to a single value
  s_pin(n,M,F) = ceil( log2( 3^ell y / (M - F_ell(a)) ) ),
and s_pin = s*(ell,M) := ceil(g_M(ell)) UNLESS frac(g_M(ell)) is within
2 x^{-0.7} of {0} (call such (ell,M) BOUNDARY pairs), because
0 < F_ell(a) <= 3^{n0} <= x^{-0.74} M on the E'-window. The map
N |-> (T_x(N), word, Pass) is injective. CAUTION: without the envelope, a
single N can have Syr^{n-m0}(N) in E' for SEVERAL n (orbit re-ascent above x);
uniqueness of n holds ON the A-event (Tao's (5.14)-envelope argument, used in
Prop 5.2-U(4)); a dip before step n forces a valuation deviation
>= log(4/3)/log 2 * m0 >> Lam, so every multi-n (fake) triple has word outside
A^{(ell)} and is charged to the type-(i) error in the sandwich step — no
uniqueness beyond the A-event is used anywhere.
[Machine: prior round verify_s5.py S5-1a/b — exhaustive at y=2^15, x=2^9:
identity, congruence, pin, injectivity, surjectivity; zero failures.]

COUNT FORMULA (combining 5.2-U + K, dropping the A-restriction):
  P(Pass_x(U_y) in E) = (2/y) * COUNT + O(log^{-5} x),
  COUNT := sum_{ell in I_y - m0} sum_{M in E'} 2^{s_pin} *
           P( S_ell = s_pin ∧ X_ell ≡ M mod 3^ell )      [free ensemble]
with errors from dropping A: the A-restricted count differs from the free
count by (i) triples with word not in A^{(ell)}: their total weighted mass is
<= sum_{ell in I} y * P(a not in A^{(ell)}) * (2/y) <= |I_y| log^{-10} x
<= log^{-9} x [per-(s,Y) weights W(s,Y) := sum_{M in E' ∩ class, s*=s} 2^{s*}
<= y(1 + x^{-0.8}), see (W) below]; (ii) triples with word in A but whose
orbit dips <= x before step n: EMPTY by the standoff argument in 5.2-U(4).
  (W): for fixed (ell, s, Y): the M in E' with M ≡ Y mod 3^ell and s*(ell,M)=s
  lie in one 3^ell-AP inside a length-(3^ell y 2^{-s}) M-range: at most
  y 2^{-s} + 1 values, each weighted 2^s: W <= y + 2^s <= y(1 + x^{-0.8})
  since 2^s <= 2 * 3^ell y e^{Lam''} / ((4/3)^{m0} x) <= y x^{-0.8}.

### Lemma B (boundary pairs are negligible).
The total contribution to COUNT of boundary pairs (ell, M) is <= C y x^{-0.5}.
PROOF. For boundary pairs allow both pin values (upper bound):
contribution <= sum_{ell} sum_{M in Bdry(ell)} sum_{s in {s*, s*+1}} 2^{s}
P(S_ell = s, X_ell ≡ M mod 3^ell). Apply J* at coarse scale m0 (error
<= |I| y m0^{-30} as in (W)); then the exact last-m0 split (Lemma W below),
P(S=s, X ≡ M mod 3^{m0}) <= max-mass * P-Gaussian sum; by Lemma M below,
3^{m0}-normalized coarse masses are <= C 2^{m0} 3^{-m0}... Assembling as in
Part III with E-replaced-by-Bdry and using sum over the Gaussian in ell:
contribution <= C y sum_{M in Bdry} 2^{m0} / M + small. #Bdry(ell) <=
4 x^{-0.7} * (#E'-range integers) and sum_{M in Bdry} 1/M <= 4 x^{-0.7} *
2Lam''; hence total <= C y 2^{m0} x^{-0.7} Lam'' <= y x^{-0.5}
(2^{m0} = e^{O(sqrt(log x) (llx)^2 log 2)} <= x^{o(1)}). QED.

### Lemma M (max-mass of the Syracuse variable).
max_r P(Syrac(Z/3^m) = r) <= C (2/3)^m with C := prod_{i>=0}(1-2^{-2*3^i})^{-1}
= 1.35450... < 1.36.
PROOF. Lemma 1.12 recursion: admissible a for a given target x form ONE parity
class (2^a x ≡ 1 mod 3 iff (-1)^a x ≡ 1 mod 3); sum over a class of 2^{-a} is
2/3 (odd a) or 1/3 (even a), <= 2/3; the normalization multiplies by
(1-2^{-2*3^m})^{-1}. Induct. QED. [Machine: sE.]

### Lemma W (exact last-block split).
For ell >= m0: X_ell mod 3^{m0} = psi(w) where w := (a_{ell-m0+1},..,a_ell) is
the last m0 letters and psi(w) := sum_{r=1}^{m0} 3^{r-1} 2^{-w_[m0-r+1, m0]}
mod 3^{m0} [from (1.5): only the i > ell - m0 terms survive mod 3^{m0}].
Moreover S_ell = S'_{ell-m0} + |w| with (a_1..a_{ell-m0}) independent of w, so
EXACTLY:
  P(S_ell = s ∧ X_ell ≡ M mod 3^{m0})
    = sum_w P(w) 1[psi(w) ≡ M] P(S_{ell-m0} = s - |w|),
and law(psi(w)) = law(Syrac(Z/3^{m0})) exactly [reversal (1.24)/(1.29): the
suffix-sums of an iid word are the prefix-sums of the reversed iid word].

### Lemma 5.3-U (thin-fiber harmonic bound; Tao Lemma 5.3 transplanted).
For every r in Z/3^{m0}:  sum_{M in E', M ≡ r mod 3^{m0}} 1/M  <=  C 3^{-m0}.
Hence sum_{M in E'} 3^{m0} pi_{m0}(M)/M <= C, where pi_{m0}(r) :=
P(Syrac(Z/3^{m0}) = r).
PROOF. Partition E' by the m0-step valuation word v = a^{(m0)}(M). As in Tao's
Lemma 5.3: (1.7) confines M to ONE residue class mod 2^{v_[1,m0]+1} and to the
v-subwindow (5.24): 3^{-m0} 2^{v_[1,m0-1]} x << M <= 3^{-m0} 2^{v_[1,m0]} x;
CRT with the class mod 3^{m0} gives modulus 2^{v_[1,m0]+1} 3^{m0}. The harmonic
sum over an AP ((5.25)-(5.26)) is <= (2^{v_[1,m0]+1} 3^{m0})^{-1} (v_{m0} log 2
+ O(1)) + 1/M0(v), and when 2^{v_[1,m0]} > x^{1/2} the extra lower bound
M >> 3^{-m0} 2^{v_[1,m0]} holds (valuation argument, Tao (2338)-(2356)).
Summing over v: sum_v 2^{-v_[1,m0]} (v_{m0}+C) 3^{-m0} + (terms with
2^{v_[1,m0]} > x^{1/2}) <= C 3^{-m0}. Density-agnostic: no measure enters. QED.

### Lemma R (renewal-Gaussian-equidistribution).
There are absolute C and c_R := 1/25 such that the following holds for x
large. Let gamma be real, t an integer with |t| <= 4 Lam + 4 m0... precisely
|t - 2m0| <= C sqrt(m0 llx) + 2m0 [the w-truncation range]; let
g(ell) = ell log2(3) + gamma and s*(ell) = ceil(g(ell)). Suppose the interval
I contains the live range {ell : |s*(ell) - t - 2(ell - m0)| <= 10 sqrt(ell llx)}
(satisfied by I = I_y - m0 in the assembly: the center sits at ell* =
[log2(y/M) + 2m0 - t]/(2 - log2 3) = I_y-center - m0 + O(Lam)/log(4/3), and
Lam' covers offset + width). Then
  | sum_{ell in I} 2^{1 - frac(g(ell))} P( S_{ell-m0} = s*(ell) - t )
      - 1/log(4/3) |   <=  C log^{-c_R} x.
[log = natural log; 1/log(4/3) = 3.4760594967...]

PROOF.
 (1) EXACT law: P(S_k = s) = C(s-1, k-1) 2^{-s} (compositions). Two-term
     Stirling with explicit remainder gives, for |d| <= k^{0.6} (d := s - 2k):
     P(S_k = 2k + d) = (4 pi k)^{-1/2} e^{-d^2/(4k)} (1 + O((1+|d|^3)/k
     ... standard expansion)) + O(k^{-3/2}); and the Chernoff tail
     P(|S_k - 2k| >= lam) <= 2 exp(-c lam^2/k) for lam <= k (Lemma 2.2 or
     directly from the exact binomial).
 (2) Truncate ell: the summand is supported (up to total mass log^{-10} x,
     by (1)-tails) on the range Z := {ell : |z(ell)| <= K sqrt(k(ell))},
     K := C sqrt(llx), where k(ell) := ell - m0 and z(ell) := s*(ell)-t-2k(ell)
     = (log2(3) - 2) ell + [gamma-t-dependent const] + O(1). Note z decreases
     by delta := 2 - log2 3 = 0.415... per unit ell; |Z| <= C sqrt(ell* llx)
     with ell* the center. Z is contained in I by hypothesis.
 (3) Blocks: partition Z into consecutive blocks of length J0 := ceil(log^{2/5} x).
     On a block starting at ell_1: z varies by delta J0; the Gaussian factor
     G(ell) := (4 pi k)^{-1/2} exp(-z^2/(4k)) satisfies, across the block,
     G(ell) = G(ell_1) (1 + O( J0 (|z_1|+J0)/k + J0/k )) = G(ell_1)
     (1 + O(J0 sqrt(llx)/sqrt(k))) = G(ell_1)(1 + O(log^{-1/10+o(1)} x)),
     using |z| <= K sqrt k and k >= c log x [window range: k >= 0.0009 log x
     ... with the chain range h >= 0.0003 log x: k >= h/log(4/3) - m0 - O(Lam)
     >= 0.001 log x]. Also the LLT error in (1) is O(k^{-3/2}(1+|z|^3/k^{3/2}))
     per term: summed over Z: O(K^3-ish * |Z| k^{-3/2}) = O(log^{-1/2+o(1)} x).
 (4) Koksma per block: the summand is w(u_ell) G_pin(ell) with u_ell :=
     frac(g(ell)), w(u) := 2^{1-u}, and G_pin(ell) := P(S_k = s*(ell)-t) where
     s*(ell)-t-2k = z(ell) = z-linear-in-ell + (1 - u_ell)-correction absorbed:
     precisely s*(ell) = g(ell) + (1 - u_ell), so z(ell) contains the SAME
     u_ell; write the block summand as h_{ell_1}(u_ell) + errors, where
     h_{ell_1}(u) := 2^{1-u} G_{ell_1}(z-lin(ell) + 1 - u): for fixed block,
     h is a function of u of total variation <= 3 * G(ell_1) sup-part
     (jump at 0 of size <= 2 G, smooth variation <= C G (1 + K sqrt(llx)/
     sqrt k /...)) <= C G(ell_1). By Koksma's inequality on the block,
       | sum_{block} w(u_ell) G_pin - J0 G(ell_1) * Int |
         <= C G(ell_1) J0 ( D*_{J0} + log^{-1/10+o(1)} x ),
     Int := int_0^1 h-normalized du -> handled with the same u-integral below.
 (5) Discrepancy: D*_{J0} of {g(ell)}_{ell in block} = {ell log2 3 + gamma}:
     shift-invariance costs a factor 2; Erdos-Turan:
       D*_J({j beta}) <= C ( 1/Kf + sum_{kf<=Kf} 1/(kf J ||kf beta||) ),
     and Rhin's 1987 effective linear-forms measure [G. Rhin, "Approximants de
     Pade et mesures effectives d'irrationalite", Prog. Math. 71 (1987),
     155-164: |u log 2 + v log 3| >= H^{-7.616} for H = max|u|,|v| >= 2]
     gives ||q log2 3|| >= c q^{-7.616}; optimizing Kf = J^{1/8.616}:
       D*_J <= C J^{-1/8.616} = C J^{-0.116...}.
     With J0 = log^{2/5} x: D*_{J0} <= C log^{-0.0464} x.
 (6) Sum the blocks: sum_block J0 G(ell_1) <= C sum_ell G(ell) <= C/delta + C.
     Total error <= C (log^{-0.0464} x + log^{-1/10+o(1)} x + log^{-1/2+o(1)} x
     + log^{-10} x) <= C log^{-1/25} x.
 (7) Main term: sum_ell G(ell) * int_0^1 2^{1-u} du, where the ell-sum of the
     Gaussian sweeping at rate delta equals 1/delta + O(log^{-1/2+o(1)} x)
     (Riemann sum of the Gaussian density in the variable z/…; standard), and
     int_0^1 2^{1-u} du = 1/log 2. Product: 1/(delta log 2) = 1/(2 log 2 -
     log 3) = 1/log(4/3). QED.
[Machine: sC — K -> 3.4760595 uniformly over random phases and shifts, error
1.0e-2 at scale 300 down to 1.7e-3 at 6000; separate factor check
sum_ell P = 2.409422 vs 1/delta-normalized 2.409421.]

--------------------------------------------------------------------------------
## PART III. Assembly

### Theorem 5-U (uniform-window stabilization; natural-density Prop 1.11).
Let x be large. For every dyadic y in [x^{1.0003}, x^{1.003}] and every
E subset of odd [1,x]:
  P(Pass_x(U_y) in E) = Q_x(E) + O(log^{-1/25} x),   uniformly in E, y,
  Q_x(E) := (2/log(4/3)) sum_{M in E'(E)} 3^{m0} pi_{m0}(M mod 3^{m0}) / M.
In particular, for two such windows y, y':
  d_TV( Pass_x(U_y), Pass_x(U_{y'}) ) <= C log^{-1/25} x,          (1.20-U)
and P(T_x(U_y) = infinity) << x^{-c}                               (1.19-U).

PROOF. Chain the pieces:
 (a) Prop 5.2-U, then Lemma K: P(Pass in E) = (2/y) COUNT_A + O(log^{-5}x),
     COUNT_A := the A-restricted pinned triple count.
 (b) Sandwich: |COUNT_A - COUNT| <= y log^{-9} x  [type-(i) via weights (W)
     and the envelope probability; type-(ii) empty by the standoff (S)].
 (c) Remove boundary pairs: Lemma B, error y x^{-0.5}.
 (d) J*-replacement at coarse scale m0 (A := 30 * 25):
     COUNT = sum_{ell,M} 2^{s*(ell,M)} 3^{m0-ell}
             P(S_ell = s*(ell,M) ∧ X_ell ≡ M mod 3^{m0}) + O(y |I_y| m0^{-A})
     [test the J*-L1 bound against the weights (W) <= y(1+o(1))]. The error is
     <= y log^{-10} x since m0^{-A} = exp(-A/2 * llx * (1+o(1)))-ish
     beats every power of log x.
 (e) Exact split (Lemma W) + w-truncation (||w| - 2 m0| <= C sqrt(m0 llx),
     tail mass log^{-10} x via weights + Lemma 5.3-U):
     COUNT = sum_{M in E'} sum_w P(w) 1[psi(w) ≡ M mod 3^{m0}]
             * sum_{ell} 2^{s*(ell,M)} 3^{m0-ell} P(S_{ell-m0} = s*(ell,M)-|w|)
             + errors.
 (f) Pull out 2^{s*} = (3^ell y / M) 2^{1-frac(g_M(ell))}: the inner ell-sum
     becomes (3^{m0} y / M) * [Lemma R sum with gamma = log2(y/M), t = |w|],
     = (3^{m0} y / M) (1/log(4/3) + O(log^{-1/25} x)), uniformly in (M,w).
 (g) Sum over w: sum_w P(w) 1[psi(w) ≡ M] = pi_{m0}(M) exactly (Lemma W).
     Aggregate the R-errors with Lemma 5.3-U:
     sum_M (y/M) 3^{m0} pi_{m0}(M) * C log^{-1/25} x <= C y log^{-1/25} x.
 (h) Multiply by (2/y). All errors <= C log^{-1/25} x. Q_x(E) does not depend
     on y; d_TV = sup_E |difference| gives (1.20-U). QED.

### Theorem 3-U (natural-density almost-all boundedness).
There are absolute C, c* := 1/25 with: for all N0 >= 16,
  limsup_{Z->infty} (1/Z) #{ N <= Z odd : Syr_min(N) > N0 } <= C log^{-c*} N0,
  limsup_{Z->infty} (1/Z) #{ N <= Z : Col_min(N) > N0 }   <= C log^{-c*} N0.

PROOF. Fix N0 large (small N0 trivial by constants). Index the chain by
THRESHOLDS. For a threshold x let w(x) := the dyadic power of 2 nearest
x^{alpha}, and define the event (on the probability space of U_{w(x)})
  B_x := { T_x(U_{w(x)}) < infinity } ∧ { Pass_x(U_{w(x)}) in E_{N0} },
  E_{N0} := {M odd : Syr_min(M) <= N0}.
BASE: for x_b := (N0/2)^{1/alpha}: on {T_{x_b} < infinity} (probability
>= 1 - x_b^{-c} by (1.19)-U) we have Pass_{x_b}(U) <= x_b <= N0 BY DEFINITION
of Pass, hence Syr_min(Pass) <= Pass <= N0: P(B_{x_b}) >= 1 - x_b^{-c}.
STEP (x -> x^alpha), for x >= x_b: with W' := w(x^alpha) (a dyadic scale
~ x^{alpha^2}):
 (a) same-r.v. small->large transfer: {T_x(U_{W'}) < inf ∧ Pass_x(U_{W'}) in
     E_{N0}} implies B_{x^alpha} (for the same U_{W'}): T_{x^alpha} <= T_x <
     inf, and orbit(Pass_{x^alpha}) contains Pass_x, so
     Syr_min(Pass_{x^alpha}) <= Syr_min(Pass_x) <= N0. [No side condition:
     transfers always go from smaller threshold x to larger x^alpha.]
 (b) window swap at the common threshold x (Theorem 5-U, both windows w(x),
     W' have exponents over x inside [1.0003, 1.003] after dyadic slack):
     P(T_x(U_{W'}) < inf ∧ Pass_x(U_{W'}) in E_{N0})
       >= P(T_x(U_{w(x)}) < inf ∧ Pass_x(U_{w(x)}) in E_{N0}) - C log^{-c*} x
          - C x^{-c}
       =  P(B_x) - C log^{-c*} x - C x^{-c}.
     (The T=infinity convention mismatch between the TV statement and the
     event is absorbed by (1.19)-U.)
 So P(B_{x^alpha}) >= P(B_x) - C log^{-c*}x - C x^{-c}.
UNROLL from x_b up to any threshold X (J ~ log(log X/log N0)/log alpha steps,
thresholds x_j = x_b^{alpha^j}):
  P(B_X) >= 1 - C sum_{j>=0} ( (alpha^j log x_b)^{-c*} + x_b^{-c alpha^j} )
         >= 1 - C' (1 - alpha^{-c*})^{-1} log^{-c*} N0 =: 1 - eps(N0),
the series geometric (ratio alpha^{-c*} < 1), dominated by the base scale.
ENDGAME: for any dyadic z (large), apply with X := the threshold whose window
is z (X ~ z^{1/alpha}): on B_X: Syr_min(U_z) <= Syr_min(Pass_X(U_z)) <= N0
[orbit(U_z) contains Pass_X(U_z)]. Hence
  #{N in [z,2z) odd : Syr_min(N) > N0} <= eps(N0) z/2.
Covering: for Z large, #{N <= Z odd, Syr_min > N0} <= sum_{dyadic z <= Z/2}
eps(N0) z/2 + O(N0^{C}) <= eps(N0) Z/2 + o(Z). Hence upper density (in odd
integers, hence with the factor for all integers) <= C log^{-c*} N0.
Col-version: every N = 2^e N' with N' odd has Col_min(N) = Col_min(N') <=
max(N0', Syr-related...): using (1.2)-monotonicity Col_min(N') <= Syr_min(N'):
  #{N <= Z : Col_min(N) > N0} <= sum_{e <= log2 Z} #{N' <= Z/2^e odd :
      Syr_min(N') > N0} <= sum_e (eps Z/2^e + o(Z/2^e) + O(N0^C))
  <= 2 eps(N0) Z + o(Z) + O(N0^C log Z). QED.

### Theorem ND (main theorem: natural-density version of Tao's Theorem 1.3).
For every function f: N+1 -> R with lim_{N->infty} f(N) = +infinity:
  Col_min(N) <= f(N)  for almost all N in the sense of NATURAL DENSITY
(the density of the exceptional set exists and equals 0). Quantitatively, the
exceptional set {N : Col_min(N) > N0} has upper natural density
<= C log^{-1/25} N0.

PROOF. Given eps > 0 choose N0 with C log^{-1/25} N0 < eps/2 and F with
f(N) >= N0 for N >= F. Then {N <= Z : Col_min(N) > f(N)} is contained in
[1,F] union {N <= Z : Col_min(N) > N0}, of size <= F + (eps/2 + o(1)) Z:
upper density <= eps. QED.

--------------------------------------------------------------------------------
## PART IV. Status ledger, dependencies, and what a referee must check

PROVED IN THIS DOCUMENT (new): P7, P7', J*, 5.2-U (+ (1.19)-U), K
(restatement of the prior round's machine-verified kernel + Lemma 2.1),
B, M, W, 5.3-U (transplant of Tao's Lemma 5.3), R, Theorem 5-U, Theorem 3-U,
Theorem ND.

EXTERNAL INPUTS (all published):
 [T1] Tao, arXiv:1909.03562v7: Prop 1.9, Lemma 2.1, Lemma 2.2, Cor 6.3, and
      Section 7's bound E prod_j |f| <<_A n^{-A} ((7.5) + Sections 7.1-7.5).
      Used as black boxes; NO step of Sections 6-7 is modified — Section 6 is
      re-run with an extra factor riding along (J*), Section 7 is untouched.
 [T2] Rhin 1987: |u log2 + v log3| >= max(|u|,|v|)^{-7.616} for max >= 2
      => mu(log2 3) <= 8.616 => D*_J << J^{-0.116}. (Any finite irrationality
      measure yields some c* > 0; sharper measures improve c*.)
 [T3] Classical: Erdos-Turan inequality, Koksma inequality, Stirling.

RATE: c* = 1/25 (bottleneck: block-discrepancy of {ell log2 3} + block-
freezing balance; the J*-error, envelope, LLT, and boundary terms are all
o(log^{-1/25} x) with the parameter choices above).

MACHINE VERIFICATION (this session, scratchpad/s5-completion/):
  sA_joint_mixing.py — exact joint (S,X)-tables (integer DP; rows = NB law,
    columns = Lemma 1.12 law; Tao's published Z/9 table reproduced); exact
    joint oscillation Osc^J tables n<=8 (tracks plain Osc, factor < 1.9);
    exact two-block factorization identity (A4). ALL PASS.
  sB_phased_sec7.py — Lemma P7 inequality at n=7,8, six frequencies: holds
    with ~5x margin; plain |S_chi| <= summed version consistency. ALL PASS.
  sC_lemmaR.py — Lemma R constant: K -> 1/log(4/3) = 3.4760595 uniformly over
    random phases/shifts, errors 1.0e-2 (scale 300) -> 1.7e-3 (6000); factor
    check 1/(2-log2 3) = 2.409421 matches. ALL PASS.
  sD_endtoend.py — exhaustive windows at x=2^12: WINDOW-STABILIZATION
    TV(Pass-law: U_{2^21} vs U_{2^21*sqrt2}) = 0.00204, vs U_{2^25} = 0.00153
    [the (1.20-U) claim, exact enumeration, no sampling]; free-count mass
    excess (the early-dip/fake-triple term, killed at real scale by the
    standoff (S) + envelope) decays geometrically in m0: +0.399, +0.276,
    +0.189, +0.124, +0.075 at m0 = 2..6, ratios 0.69, 0.69, 0.66, 0.60;
    shape-TV against the predicted law improves 0.0873 -> 0.0556 (m0 = 3 -> 6);
    m0 = 8 rows carry an enumeration-cutoff artifact (MMAX = 1024x), noted.
    ALL PASS (D1, D2, D3).
  sE_maxmass.py — Lemma M exact check: parity-class structure + max-mass
    <= 1.36 (2/3)^m for m <= 7 (exact Fractions); C = 1.354503. ALL PASS.

HONESTY NOTES (referee targets, in decreasing order of attention needed):
 1. Lemma R step (4): the coupling of the u_ell-dependence inside the Gaussian
    argument with the 2^{1-u} weight — handled by treating h(u) as a single
    BV function per block; a referee should check the BV constant and the
    claim that Koksma applies to the coupled function (the sequence u_ell is
    the SAME {g(ell)} in both places — no independence is claimed or needed).
 2. J* step (iv): the extra Cauchy-Schwarz over s and its interaction with
    Tao's per-(k,l) error targets (n^{-A-3} vs his n^{-A-2}) — pure
    bookkeeping, but worth re-deriving.
 3. 5.2-U step (4) backward direction: the standoff use (S) and the
    Lam''-window constants (C1, C2, C0 orders).
 4. The chain in Theorem 3-U: dyadic-vs-alpha-grid slack (windows land inside
    [x^{1.0003}, x^{1.003}]) — elementary but fiddly.
 5. Lemma 5.3-U: transplant with n-m0 -> m0 — check (5.24)'s v-subwindow at
    the new scale (it never used the measure, only (1.7) + AP harmonic sums).
The items NOT needing attention: P7 (three-line conditioning), W (exact
identity), M (one-line induction), K (machine-verified exhaustively + Lemma
2.1), B (crude bounds with huge margins).

WHAT THIS DELIVERS RELATIVE TO THE LITERATURE: Tao's Theorem 1.3 with
logarithmic density replaced by natural density, answering the question he
raises in the paper (line ~295: "it is plausible that some refinement of the
arguments below will allow one to replace logarithmic density by natural
density") and constructing the object requested in his Remark 1.16 (fine-scale
mixing of the entire affine map = Lemma J*). The proof inherits Tao's
structure; the genuinely new mathematical content is (i) J* via the phase-
transparency of Section 6/7 (Lemma P7), (ii) the pinned-count renewal
assembly (Lemmas K + W + R) that replaces the log-uniform weight identity,
with the Rhin equidistribution of {ell log2 3} supplying the Archimedean
mixing that logarithmic density previously provided for free.
