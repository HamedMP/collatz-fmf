"""n6_rational.py -- adversarial search over 'rational' frequencies xi = 3^n * u / t mod 2^K (t odd):
runs n2_table with h = u * t^{-1} mod 2^K and prints the worst single-frequency delta and worst
sqrt(k)-window delta0 over the whole two-sided orbit n in [-0.35K, 0.72K].  usage: python n6_rational.py K"""
import sys, subprocess, re
K=int(sys.argv[1]); PY=sys.executable
res=[]
for (u,t) in [(1,1),(1,5),(1,7),(1,11),(3,11),(5,11),(1,13),(1,17),(1,19),(1,23),(1,25),(1,35),(1,55),(1,121),(1,243*11),(1,2**61-1),(12345678901234567891,1)]:
    h=u*pow(t,-1,1<<K)%(1<<K)
    o=subprocess.run([PY,'n2_table.py',str(K),str(h),'3','1',str(K)],capture_output=True,text=True).stdout
    g=re.search(r'worst single \(P=(-?\d+)\) delta=([\d.]+) worst window \(P0=(-?\d+)\) delta0=([\d.]+)',o)
    a=re.search(r'worst single n=(-?\d+) \(n/k=([\d.]+)\) delta=([\d.]+) ; worst window start n=(-?\d+)\.\.(-?\d+) \(n/k=[\d.]+\) delta0=([\d.]+)',o)
    print("K=%d xi=3^n*%d/%d : P>=0 zone worst delta=%s window delta0=%s | P<0 zone worst delta=%s at n=%s (n/k=%s), window delta0=%s"%(K,u,t,g.group(2),g.group(4),a.group(3),a.group(1),a.group(2),a.group(6)),flush=True)
