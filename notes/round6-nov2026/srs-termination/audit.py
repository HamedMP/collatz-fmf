"""Re-verify every certificate chain in certs/ with the independent checker,
apply the negative-control criterion, and print the frontier tables from
results/*.jsonl.

usage: audit.py
"""
import glob
import json
import os
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import systems
import loops

PY = sys.executable
ok = True
print('=== certificate chains (each re-checked by a fresh `check.py` process) ===')
for fn in sorted(glob.glob(os.path.join(HERE, 'certs', '*.json'))):
    ch = json.load(open(fn))
    name = ch['system']
    base = [[list(l), list(r)] for l, r in systems.SYSTEMS[name]['rules']]
    same = (ch['rules'] == base)
    out = subprocess.run([PY, os.path.join(HERE, 'check.py'), fn], capture_output=True, text=True)
    verified = out.returncode == 0 and 'CHECK FAILED' not in out.stdout + out.stderr
    full = 'TERMINATION PROOF VERIFIED' in out.stdout
    removed = []
    cur = list(range(len(ch['rules'])))
    for st in ch['steps']:
        s = set(st['strict'])
        removed += [cur[i] for i in sorted(s)]
        cur = [x for i, x in enumerate(cur) if i not in s]
    line = '%-28s rules==systems.py:%s checker:%s  %s  steps=%d removed=%s remaining=%s' % (
        os.path.basename(fn), same, 'OK' if verified else 'FAILED',
        'FULL PROOF' if full else 'partial', len(ch['steps']), removed, cur)
    if name in loops.START:
        lr = loops.loop_rules(name)
        badrem = sorted(set(removed) & set(lr['used']))
        ctl = 'CONTROL OK (no loop rule removed)' if not badrem and not full else \
            'CONTROL VIOLATED: removed loop rules %s' % badrem
        line += '  ' + ctl
        ok &= not badrem and not full
    ok &= same and verified
    print(line)
print('ALL CHECKS PASSED' if ok else 'SOME CHECK FAILED')

print()
print('=== SAT-call log summary: per (tag, system, stage): kind/mode/orientation -> results by (d,V) ===')
for fn in sorted(glob.glob(os.path.join(HERE, 'results', '*.jsonl'))):
    tag = os.path.basename(fn)[:-6]
    tab = defaultdict(dict)
    order = []
    for ln in open(fn):
        r = json.loads(ln)
        key = (r['system'], r['stage'], r['nrules'])
        if key not in order:
            order.append(key)
        cfg = '%s/%s/%s' % (r['kind'][:3], r['mode'], 'rev' if r['rev'] else 'org')
        res = {'SAT': 'S', 'UNSAT': 'U', 'TIMEOUT': 'T%d' % r['timeout']}.get(r['result'], r['result'])
        tab[key].setdefault(cfg, []).append('(%d,%d)%s' % (r['d'], r['V'], res))
    print('--- %s' % tag)
    for key in order:
        cells = tab[key]
        if all(c[-1].endswith('S') and len(c) <= 3 for c in cells.values()) and len(cells) == 1:
            continue                      # trivial stage: immediate SAT
        print('  %s stage %d (%d rules)' % key)
        for cfg in sorted(cells):
            print('      %-16s %s' % (cfg, ' '.join(cells[cfg])))
