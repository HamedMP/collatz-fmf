"""Explicit rewriting loops for the negative controls.

For each control system a start string is rewritten with a deterministic
strategy (dynamic rule at the right end if one matches, otherwise the rightmost
applicable auxiliary rule) until a string repeats.  Every step is a literal
rule application.  Output: the loop length and the set of rule indices used
inside the loop.  A rule used in a loop can NOT be removed by any sound
relative-termination step, so a certificate that removes one is a bug.

usage: loops.py            (prints the table; also importable: loop_rules(name))
"""
import systems

START = {  # system -> start string (value on a known cycle)
    'C5': 'L t f t R',          # 13
    'C3m': 'L f t R',           # 5
    'FMF3m': 'L f O',           # 5
    'FMF5': 'L t f O',          # 13
    'S3m': 'L f f f O',         # 17
    'G5': 'L t f O',            # 13
}
MARKERS = ('R', 'R0', 'R1', 'O')


def step(s, rules):
    n = len(s)
    # dynamic rule at the right end
    for idx, (l, r) in enumerate(rules):
        if l[-1] in MARKERS and n >= len(l) and s[n - len(l):] == l:
            return s[:n - len(l)] + r, idx
    # rightmost applicable auxiliary rule
    for pos in range(n - 1, -1, -1):
        for idx, (l, r) in enumerate(rules):
            if l[-1] not in MARKERS and s[pos:pos + len(l)] == l:
                return s[:pos] + r + s[pos + len(l):], idx
    return None, None


def loop_rules(name, maxsteps=100000):
    rules = systems.SYSTEMS[name]['rules']
    s = tuple(START[name].split())
    seen = {s: 0}
    trace = []
    for k in range(1, maxsteps):
        s, idx = step(s, rules)
        if s is None:
            return None
        trace.append(idx)
        if s in seen:
            return dict(loop_len=k - seen[s], prefix=seen[s], used=sorted(set(trace[seen[s]:])),
                        string=' '.join(s))
        seen[s] = k
    return None


if __name__ == '__main__':
    for nm in START:
        res = loop_rules(nm)
        rules = systems.SYSTEMS[nm]['rules']
        if res is None:
            print('%-6s NO LOOP FOUND' % nm)
            continue
        unused = [i for i in range(len(rules)) if i not in res['used']]
        print('%-6s loop of %d rewrite steps through "%s" (after %d steps); rules used: %s; not used: %s'
              % (nm, res['loop_len'], res['string'], res['prefix'], res['used'],
                 ['%d: %s -> %s' % (i, ' '.join(rules[i][0]), ' '.join(rules[i][1])) for i in unused]))
