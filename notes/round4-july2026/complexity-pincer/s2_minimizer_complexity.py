"""
s2_minimizer_complexity.py  (complexity-pincer, task 2: empirical falsification)

(a) Re-runs the exact {0,1} minima (explore70 logic) to length 20 and the beam
    search (explore72 logic) to length 120, beam width 4000.
(b) For each minimizer word: exact factor complexity profile p(m), p(m)/m,
    ones density; compares against the refereed thresholds
    T_R in (3.1493,3.1494), T_G in (6.2390,6.2391) and the new sharpened
    constants 3/(5log2(3)-7) = 3.243907, 7/(7log2(3)-10) = 6.394220.
(c) Per-word Lemma-U certificate: for every repeated factor pair (i<i', len m,
    ones k) the seed must satisfy
        M >= 2^(3m+4k) * 8^i' * 16^{S_i'} / (9^i' * 27^{S_i'}) - 1  (return)
        A >= 2^(7m+3k) * 2^{7i'+3K_i'} / 3^{5i'+2K_i'}              (gap)
    Computes the max forced bound over all pairs and compares with the ACTUAL
    least residue (must hold -- exact self-test of the counting relation),
    and reports the tightness (bits forced / bits actual).
"""

import sys
from math import log2
sys.path.insert(0, "/Users/hamed/dev/playgrounds/collatz/explorations")

from explore53_gap_minima import EMPTY as GAP_EMPTY, extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY, extend as extend_return

B0 = log2(9 / 8)            # 0.169925...
B1 = log2(27 / 16)          # 0.754888...
G0 = log2(243 / 128)        # 0.924813...
G1 = log2(9 / 8)

T_R_REF, T_G_REF = 3.1493, 6.2390
T_R_NEW = 3 / (5 * log2(3) - 7)
T_G_NEW = 7 / (7 * log2(3) - 10)


def complexity_profile(word, mmax=None):
    L = len(word)
    mmax = mmax or L
    prof = []
    for m in range(1, mmax + 1):
        if m > L:
            break
        prof.append(len({word[s:s + m] for s in range(L - m + 1)}))
    return prof


def forced_seed_return(word):
    """max over repeated-factor pairs of the exact forced lower bound on M (ceil)."""
    L = len(word)
    S = [0]
    for x in word:
        S.append(S[-1] + x)
    best = 0
    best_info = None
    for m in range(1, L):
        occ = {}
        for s in range(L - m + 1):
            occ.setdefault(word[s:s + m], []).append(s)
        for fac, pos in occ.items():
            if len(pos) < 2:
                continue
            k = sum(fac)
            Q = 1 << (3 * m + 4 * k)
            ip = pos[1]  # earliest second occurrence gives the strongest bound
            # M+1 >= Q * 8^ip * 16^{S_ip} / (9^ip 27^{S_ip})
            num = Q * 8**ip * 16**S[ip]
            den = 9**ip * 27**S[ip]
            bound = -(-num // den) - 1  # ceil(num/den) - 1
            if bound > best:
                best = bound
                best_info = (m, k, pos[0], ip)
    return best, best_info


def forced_seed_gap(word):
    L = len(word)
    K = [0]
    for x in word:
        K.append(K[-1] + x)
    best = 0
    best_info = None
    for m in range(1, L):
        occ = {}
        for s in range(L - m + 1):
            occ.setdefault(word[s:s + m], []).append(s)
        for fac, pos in occ.items():
            if len(pos) < 2:
                continue
            k = sum(fac)
            Q = 1 << (7 * m + 3 * k)
            ip = pos[1]
            num = Q * 2**(7 * ip + 3 * K[ip])
            den = 3**(5 * ip + 2 * K[ip])
            bound = -(-num // den)  # A >= ceil(...)  (envelope has no +1 slack)
            if bound > best:
                best = bound
                best_info = (m, k, pos[0], ip)
    return best, best_info


def describe_word(tag, word, residue):
    L = len(word)
    ones = sum(word)
    prof = complexity_profile(word, mmax=min(L - 1, 60))
    ratios = [(p / m) for m, p in enumerate(prof, start=1)]
    mx = max(ratios)
    mxm = ratios.index(mx) + 1
    # p(m)/m at a few marks
    marks = {m: prof[m - 1] for m in (2, 4, 8, 16, 32) if m <= len(prof)}
    print(f"  {tag} L={L} ones={ones} density={ones/L:.4f} residue_bits={residue.bit_length()}")
    print(f"    p(m): {prof[:20]}{'...' if len(prof) > 20 else ''}")
    print(f"    max p(m)/m = {mx:.4f} at m={mxm}; p(m)/m at marks: " +
          ", ".join(f"m={m}:{p}/{m}={p/m:.3f}" for m, p in marks.items()))
    return prof


def run_exact_minima():
    print("=" * 78)
    print("EXACT {0,1} MINIMA (length <= 20), complexity profiles vs thresholds")
    print(f"refereed: T_R in (3.1493,3.1494), T_G in (6.2390,6.2391); "
          f"new: T_R'={T_R_NEW:.6f}, T_G'={T_G_NEW:.6f}")
    print("=" * 78)
    states = [RETURN_EMPTY]
    for level in range(1, 21):
        states = [extend_return(s, d) for s in states for d in (0, 1)]
        best = min(states, key=lambda s: s.residue)
        if level in (10, 16, 20):
            prof = describe_word(f"RETURN exact-min", best.word, best.residue)
            fb, info = forced_seed_return(best.word)
            ok = best.residue >= fb
            print(f"    certificate: forced M >= 2^{fb.bit_length()-1 if fb>0 else 0} "
                  f"({fb.bit_length()} bits) from pair {info}; actual {best.residue.bit_length()} bits; "
                  f"holds={ok}  tightness={fb.bit_length()/best.residue.bit_length():.3f}")
            assert ok, "LEMMA U VIOLATED on exact minimizer -- derivation wrong!"
    states = [GAP_EMPTY]
    for level in range(1, 21):
        states = [extend_gap(s, d) for s in states for d in (0, 1)]
        best = min(states, key=lambda s: s.residue)
        if level in (10, 16, 20):
            prof = describe_word(f"GAP    exact-min", best.word, best.residue)
            fb, info = forced_seed_gap(best.word)
            ok = best.residue >= fb
            print(f"    certificate: forced A >= ({fb.bit_length()} bits) from pair {info}; "
                  f"actual {best.residue.bit_length()} bits; holds={ok}  "
                  f"tightness={fb.bit_length()/best.residue.bit_length():.3f}")
            assert ok, "LEMMA U VIOLATED on exact gap minimizer!"


def state_key(state):
    return (state.residue.bit_length(), state.residue, sum(state.word))


def run_beam(max_length=120, beam_width=4000):
    print("=" * 78)
    print(f"BEAM SEARCH to L={max_length}, width {beam_width}: minimizer complexity")
    print("=" * 78)
    rs = [RETURN_EMPTY]
    gs = [GAP_EMPTY]
    for level in range(1, max_length + 1):
        rs = sorted([extend_return(s, d) for s in rs for d in (0, 1)], key=state_key)[:beam_width]
        gs = sorted([extend_gap(s, d) for s in gs for d in (0, 1)], key=state_key)[:beam_width]
        if level in (40, 80, max_length):
            for tag, pool, forced in (("RETURN", rs, forced_seed_return),
                                      ("GAP   ", gs, forced_seed_gap)):
                best = pool[0]
                describe_word(f"{tag} beam-best", best.word, best.residue)
                fb, info = forced(best.word)
                ok = best.residue >= fb
                print(f"    certificate: forced >= {fb.bit_length()} bits (pair {info}); "
                      f"actual {best.residue.bit_length()} bits; holds={ok} "
                      f"tightness={fb.bit_length()/max(1,best.residue.bit_length()):.3f}")
                assert ok, f"LEMMA U VIOLATED on {tag} beam minimizer!"
    # diversity statistics at final level: complexity of the whole surviving beam
    print("-" * 78)
    for tag, pool in (("RETURN", rs), ("GAP", gs)):
        stats = []
        for s in pool[:200]:
            prof = complexity_profile(s.word, mmax=len(s.word) - 1)
            mx = max(p / m for m, p in enumerate(prof, start=1))
            stats.append((mx, sum(s.word) / len(s.word), s.residue.bit_length()))
        mxs = [x[0] for x in stats]
        dens = [x[1] for x in stats]
        bits = [x[2] for x in stats]
        print(f"  {tag} beam top-200 at L={max_length}: max p(m)/m over words: "
              f"min={min(mxs):.3f} mean={sum(mxs)/len(mxs):.3f} max={max(mxs):.3f}; "
              f"density min={min(dens):.3f} mean={sum(dens)/len(dens):.3f} max={max(dens):.3f}; "
              f"residue bits min={min(bits)} mean={sum(bits)/len(bits):.1f}")
    print()
    print("readout: are minimizer complexities ABOVE the liminf thresholds "
          f"(T_R={T_R_REF}, T_G={T_G_REF})?  See max p(m)/m values above; note these are")
    print("finite prefixes; the thresholds constrain infinite words via liminf, so the")
    print("comparison is diagnostic only.")


if __name__ == "__main__":
    run_exact_minima()
    run_beam()
