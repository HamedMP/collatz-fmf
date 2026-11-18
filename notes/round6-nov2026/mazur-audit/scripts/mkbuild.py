#!/usr/bin/env python
"""Generate a Makefile compiling a Lean source tree by direct `lean` calls
(no lake, no network).  Usage: python -I mkbuild.py SRC_DIR OUT_DIR ROOT_MODULE > Makefile
Only modules reachable from ROOT_MODULE whose files exist under SRC_DIR are built."""
import os, re, sys
src, out, root = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
imp = re.compile(r'^\s*(?:public\s+)?import\s+(?:all\s+)?([A-Za-z0-9_.]+)', re.M)
def path(m): return os.path.join(src, *m.split('.')) + '.lean'
deps, todo = {}, [root]
while todo:
    m = todo.pop()
    if m in deps: continue
    txt = open(path(m), encoding='utf-8').read()
    # strip block comments crudely before scanning imports
    txt2 = re.sub(r'/-.*?-/', '', txt, flags=re.S)
    ds = [d for d in imp.findall(txt2) if os.path.exists(path(d))]
    deps[m] = ds; todo += ds
def ol(m): return os.path.join(out, *m.split('.')) + '.olean'
print('all: ' + ol(root) + '\n')
for m, ds in sorted(deps.items()):
    o = ol(m)
    print(f"{o}: {path(m)} {' '.join(ol(d) for d in ds)}")
    print(f"\t@mkdir -p {os.path.dirname(o)}")
    print(f"\t@echo BUILD {m}")
    print(f"\t@lean --root={src} -o {o} -i {o[:-6]}.ilean {path(m)} > {o[:-6]}.log 2>&1 || (echo FAIL {m}; exit 1)\n")
sys.stderr.write(f"{len(deps)} modules\n")
