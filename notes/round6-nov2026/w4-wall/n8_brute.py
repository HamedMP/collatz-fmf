"""n8_brute.py -- exhaustive maximum of |T_k(xi)| over ALL odd xi mod 2^k (FFT), and identification of
the maximisers as +-3^n*u/t mod 2^k (t in {1,11}, small u).  usage: python n8_brute.py k"""
import sys, numpy as np, math
k=int(sys.argv[1]); m=1<<k
E=[[0],[0,1],[0,3],[0,7]]
for j in range(4,k+1):
    mm=1<<j; i9=pow(9,-1,mm); i27=pow(27,-1,mm)
    E.append([((8*z-1)*i9)%mm for z in E[j-3]]+[(16*z*i27)%mm for z in E[j-4]])
ind=np.zeros(m,dtype=np.complex64); ind[E[k]]=1
F=np.abs(np.fft.fft(ind)); Nk=len(E[k])
odd=np.arange(1,m,2); Fo=F[odd]
order=np.argsort(-Fo)[:12]
tab={}
for n in range(0,k):
    for t in (1,11):
        for u in (1,3,5,7,9):
            for sg in (1,-1):
                tab.setdefault(sg*pow(3,n,m)*u*pow(t,-1,m)%m,(sg,n,u,t))
print("k=%d N_k=%d sqrt(N_k)=%.1f ; random-set heuristic for the max over 2^k frequencies: sqrt(N k ln2)=%.1f"%(k,Nk,math.sqrt(Nk),math.sqrt(Nk*k*math.log(2))))
for o in order:
    xi=int(odd[o]); d=tab.get(xi)
    print("  xi=%9d |T|=%7.2f = N^%.3f  %s"%(xi,Fo[o],math.log(Fo[o])/math.log(Nk), ("= %+d*3^%d*%d/%d (n/k=%.2f)"%(d[0],d[1],d[2],d[3],d[1]/k)) if d else ""))
