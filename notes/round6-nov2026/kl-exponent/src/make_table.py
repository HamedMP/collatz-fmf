#!/usr/bin/env python3
"""Print the k / gamma table from cert/k*_search.json and the VERIFIED lines of the logs."""
import glob, json, math, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KL = {2: (0.4365880, 1.3534010), 3: (0.6112620, 1.5275960), 4: (0.6891080, 1.6122870), 5: (0.7335790, 1.6627590),
      6: (0.7608180, 1.6944520), 7: (0.7825670, 1.7201900), 8: (0.8031960, 1.7449630), 9: (0.8168300, 1.7615320),
      10: (0.8295450, 1.7771270), 11: (0.8417560, 1.7922310)}
# kollatz RESULTS.md: "numerical optimum lambda_k" (k>=12) and certified feasible / infeasible lambda
KO = {12: (1.8064236, 1.8064, 1.80644), 13: (1.8188237, 1.8188, 1.81884), 14: (1.8307723, 1.8307, 1.83079),
      15: (1.8419687, 1.8419, 1.84198), 16: (1.8522346, 1.8522, 1.85225), 17: (1.8616888, 1.8616, 1.86170),
      18: (1.8703250, 1.8703, 1.87034), 19: (1.8783132, 1.8783, 1.87833),
      2: (None, 1.3534, 1.35342), 3: (None, 1.5275, 1.5278), 4: (None, 1.6122, 1.61230), 5: (None, 1.6627, 1.66277),
      6: (None, 1.6944, 1.69447), 7: (None, 1.7201, 1.72020), 8: (None, 1.7449, 1.74498), 9: (None, 1.7615, 1.76155),
      10: (None, 1.7771, 1.77714), 11: (None, 1.7922, 1.79225)}
ver = {}
for lg in glob.glob(os.path.join(ROOT, "logs", "run_k*.log")):
    for line in open(lg):
        m = re.match(r"VERIFIED k=(\d+) N=\d+ mode=(\w+) gamma=(\d+)/2\^40", line)
        if m:
            ver[(int(m.group(1)), m.group(2))] = int(m.group(3))
print("| k | gamma_lo (certified feasible) | gamma_hi (certified infeasible) | lambda_lo | lambda_hi | KL 2003 gamma / lambda | kollatz lambda_k (float) [cert feasible, infeasible] | consistent |")
print("|---|---|---|---|---|---|---|---|")
for k in range(2, 23):
    if (k, "lower") not in ver:
        continue
    lo, hi = ver[(k, "lower")] / 2 ** 40, ver.get((k, "upper"), float("nan")) / 2 ** 40
    llo, lhi = 2 ** lo, 2 ** hi
    kl = f"{KL[k][0]:.7f} / {KL[k][1]:.7f}" if k in KL else "-"
    ko = KO.get(k)
    kos = f"{ko[0] if ko[0] else '-'} [{ko[1]}, {ko[2]}]" if ko else "-"
    ok = []
    if k in KL:
        ok.append("KL gamma " + ("in bracket" if lo <= KL[k][0] <= hi else f"{'below' if KL[k][0] < lo else 'above'} by {abs(KL[k][0] - (lo if KL[k][0] < lo else hi)):.1e}"))
        ok.append("KL lambda " + ("in bracket" if llo <= KL[k][1] <= lhi else f"{'below' if KL[k][1] < llo else 'ABOVE'} by {abs(KL[k][1] - (llo if KL[k][1] < llo else lhi)):.1e}"))
    if ko:
        ok.append("kollatz ok" if (ko[1] <= lhi and ko[2] >= llo and (ko[0] is None or abs(ko[0] - 0.5 * (llo + lhi)) < 2e-5)) else "kollatz MISMATCH")
    print(f"| {k} | {lo:.9f} | {hi:.9f} | {llo:.8f} | {lhi:.8f} | {kl} | {kos} | {'; '.join(ok)} |")
