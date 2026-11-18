"""Rule-removal prover driver (srs-termination track).

usage: prove.py [--sched quick|deep|...] [--tag TAG] [--maxstages N] SYSTEM [SYSTEM ...]

For each system: repeatedly search (encoder.py, one SAT call per child process,
killed at its timeout) for an interpretation that removes at least one rule;
every SAT answer is re-verified by the independent checker (check.py) before the
rules are removed.  Writes
  results/<tag>.jsonl                one line per SAT call
  certs/<system>.<tag>.json          the (possibly partial) chain of certificates
"""
import json
import multiprocessing as mp
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import systems          # noqa: E402
import check            # noqa: E402  (independent checker; no shared code with encoder)

MEM = 1400 * 1024 * 1024


def orient(rules, rev):
    return [(l[::-1], r[::-1]) for l, r in rules] if rev else list(rules)


def marker_set(rules):
    """largest symbol set K with: every rule has no K-symbol, or exactly one on
    each side, in first position"""
    K = {s for l, r in rules for s in l + r}
    changed = True
    while changed:
        changed = False
        for l, r in rules:
            bad = set()
            for side in (l, r):
                bad |= {s for s in side[1:] if s in K}
            hl = bool(l) and l[0] in K
            hr = bool(r) and r[0] in K
            if hl != hr:
                if hl:
                    bad.add(l[0])
                if hr:
                    bad.add(r[0])
            if bad:
                K -= bad
                changed = True
    return K


def _child(q, rules, kind, mode, d, V, lo, cand, solver, seed, negphase):
    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEM, MEM))
        import encoder
        q.put(encoder.solve(rules, kind, mode, d, V, lo, cand, solver=solver, seed=seed,
                            negphase=negphase))
    except MemoryError:
        q.put(('MEMOUT', None, {}))
    except Exception as e:                       # noqa
        q.put(('ERROR', None, {'err': repr(e)}))


def call(rules, kind, mode, d, V, lo, cand, timeout, solver='cadical195', seed=None, negphase=False):
    q = mp.Queue()
    p = mp.Process(target=_child, args=(q, rules, kind, mode, d, V, lo, cand, solver, seed, negphase))
    t0 = time.time()
    p.start()
    try:
        res = q.get(timeout=timeout)
    except Exception:
        res = ('TIMEOUT', None, {})
    if p.is_alive():
        p.kill()
    p.join()
    if res[0] not in ('SAT', 'UNSAT', 'TIMEOUT') and p.exitcode not in (0, None):
        res = (res[0], None, res[2])
    res[2]['wall'] = round(time.time() - t0, 2)
    return res


# schedule entries: (kind, mode, reversed, d, V, lo, timeout)
def sched(name):
    S = []

    def nat(d, V, t, modes=('fo', 'fr', 'to', 'tr')):
        for m in modes:
            S.append(('natural', 'full' if m[0] == 'f' else 'top', m[1] == 'r', d, V, 0, t))

    def arc(d, V, t, modes=('fo', 'to', 'tr'), lo=0):
        for m in modes:
            S.append(('arctic', 'full' if m[0] == 'f' else 'top', m[1] == 'r', d, V, lo, t))
    if name == 'quick':
        for V in (2, 3, 4, 5):
            nat(1, V, 20)
        arc(1, 3, 20); arc(1, 4, 20)
        nat(2, 2, 20); nat(2, 3, 20); arc(2, 3, 20); arc(2, 4, 20)
        nat(3, 2, 30); arc(3, 3, 30); nat(2, 4, 30); nat(3, 3, 30); arc(3, 4, 30)
    elif name == 'deep':
        S += sched('quick')
        nat(4, 2, 60); arc(4, 3, 60); arc(3, 5, 60); nat(3, 4, 60)
        nat(4, 3, 120); arc(4, 4, 120); nat(5, 2, 120); arc(5, 3, 120)
    elif name == 'd4':
        nat(4, 2, 300, modes=('to',)); arc(3, 4, 300, modes=('to',)); arc(4, 3, 300, modes=('to',))
        S += sched('tiny')
    elif name == 'mini':
        for V in (2, 3, 4):
            nat(1, V, 8)
        arc(1, 3, 8); nat(2, 2, 8); nat(2, 3, 8); arc(2, 3, 8)
    elif name == 'tiny':
        for V in (2, 3, 4):
            nat(1, V, 10)
        arc(1, 3, 10); nat(2, 2, 10); nat(2, 3, 10); arc(2, 3, 10); arc(2, 4, 10)
        nat(3, 2, 15); arc(3, 3, 15)
    else:
        raise SystemExit('unknown schedule')
    return S


RIGHT_MARKERS = ('R', 'R0', 'R1', 'O')


def is_dyn(rule):
    return any(s in RIGHT_MARKERS for s in rule[0])


def parse_grid(spec):
    """kind:mode:d:V:timeout[:lo],...  mode in fo fr to tr"""
    out = []
    for item in spec.split(','):
        p = item.split(':')
        kind = {'n': 'natural', 'a': 'arctic'}[p[0][0]]
        out.append((kind, 'full' if p[1][0] == 'f' else 'top', p[1][1] == 'r', int(p[2]), int(p[3]),
                    int(p[5]) if len(p) > 5 else 0, float(p[4])))
    return out


def prove(name, rules, schedule, tag, log, maxstages=40, solver='cadical195', negphase=False,
          cand_filter=None, grid=None):
    """cand_filter(rule) -> bool restricts which rules may be made strict.
    grid: if given, while dynamic rules remain ONLY the grid entries are used and
    only dynamic rules may be strict (the relative problems of the YAH paper)."""
    cur = [(tuple(l), tuple(r)) for l, r in rules]
    chain = dict(system=name, rules=[[list(l), list(r)] for l, r in cur], steps=[])
    stage = 0
    status = 'PROVED'
    while cur and stage < maxstages:
        found = False
        use_grid = grid is not None and any(is_dyn(x) for x in cur)
        for (kind, mode, rev, d, V, lo, tmo) in (grid if use_grid else schedule):
            R = orient(cur, rev)
            if mode == 'top':
                K = marker_set(R)
                cand = [i for i, (l, r) in enumerate(R) if l and l[0] in K]
            else:
                cand = list(range(len(R)))
            if cand_filter:
                cand = [i for i in cand if cand_filter(cur[i])]
            if use_grid:
                cand = [i for i in cand if is_dyn(cur[i])]
            if not cand:
                continue
            res, interp, st = call(R, kind, mode, d, V, lo, cand, tmo, solver=solver, negphase=negphase)
            rec = dict(system=name, stage=stage, nrules=len(cur), kind=kind, mode=mode, rev=rev,
                       d=d, V=V, lo=lo, timeout=tmo, result=res, **st)
            if res == 'SAT':
                cert = dict(rules=[[list(l), list(r)] for l, r in cur], reversed=rev, kind=kind,
                            mode=mode, dim=d, V=V, strict=st['strict_flags'], interp=interp)
                # maximise the strict set: every rule that happens to be strict and allowed
                strict = check.check_step(cert, quiet=True)      # raises SystemExit on failure
                rec['removed'] = [' '.join(cur[i][0]) + ' -> ' + ' '.join(cur[i][1]) for i in strict]
                chain['steps'].append(cert)
                cur = [x for i, x in enumerate(cur) if i not in set(strict)]
                found = True
            log.write(json.dumps(rec) + '\n')
            log.flush()
            print('%-10s st%d n=%2d %-7s %-4s %s d=%d V=%d  %-7s %6.1fs %s' % (
                name, stage, rec['nrules'], kind, mode, 'rev' if rev else 'org', d, V, res,
                st.get('wall', 0), '; '.join(rec.get('removed', []))), flush=True)
            if found:
                break
        if not found:
            status = 'STUCK'
            break
        stage += 1
    chain['status'] = status if not cur or status == 'STUCK' else 'MAXSTAGES'
    chain['remaining'] = [[list(l), list(r)] for l, r in cur]
    os.makedirs(os.path.join(HERE, 'certs'), exist_ok=True)
    json.dump(chain, open(os.path.join(HERE, 'certs', '%s.%s.json' % (name, tag)), 'w'))
    print('== %s: %s, %d rules remain: %s' % (
        name, chain['status'], len(cur), ' | '.join(' '.join(l) + ' -> ' + ' '.join(r) for l, r in cur)),
        flush=True)
    return chain


if __name__ == '__main__':
    args = sys.argv[1:]
    opt = dict(sched='quick', tag=None, maxstages='40', solver='cadical195', neg='0', grid=None)
    names = []
    while args:
        a = args.pop(0)
        if a.startswith('--'):
            opt[a[2:]] = args.pop(0)
        else:
            names.append(a)
    tag = opt['tag'] or opt['sched']
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    log = open(os.path.join(HERE, 'results', tag + '.jsonl'), 'a')
    for n in names:
        prove(n, systems.SYSTEMS[n]['rules'], sched(opt['sched']), tag, log,
              maxstages=int(opt['maxstages']), solver=opt['solver'], negphase=opt['neg'] == '1',
              grid=parse_grid(opt['grid']) if opt['grid'] else None)
