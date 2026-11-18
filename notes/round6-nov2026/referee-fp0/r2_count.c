// referee counter: N(Q,m)=#{c in E_Q (as integer <2^Q): life(c)>=Q+m}; system dsg=+1 (3n+1) or -1 (3n-1: a(w)=(9w-1)/8 on w=1 mod 8)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int Q,dsg; static u128 MASK,i9,i27; static uint64_t hist[600],inf_; static int part,nparts,cntleaf;
static int life(u128 w){
  if(w==0) return -1; if(dsg<0&&w==1) return -1;
  int bits=0;
  for(;;){
    unsigned lo=(unsigned)(w&15);
    if(dsg>0? (lo&7)==7 : (lo&7)==1){ if(dsg>0) w=w+(w+1)/8; else w=w+(w-1)/8; bits+=3; }
    else if(lo==0){ w=(w>>4)*27; bits+=4; }
    else { unsigned t=dsg>0?((lo+1)&15):((lo-1)&15); // need max r<=3 with 2^r|w or 2^r|(w+d)
      int r=0; for(int j=3;j>=1;j--){ unsigned mk=(1u<<j)-1; if((lo&mk)==0||(t&mk)==0){r=j;break;} }
      return bits+r; }
    if(w>>124){fprintf(stderr,"overflow\n");exit(1);}
  }
}
static void emit(u128 c){ int L=life(c); if(L<0){inf_++;return;} if(L<Q){fprintf(stderr,"BUG\n");exit(1);} hist[L-Q]++; }
static void rec(int used,u128 mult,u128 add,int top){
  int rem=Q-used;
  if(top && used>=20){ if((cntleaf++)%nparts!=part) return; top=0; }
  if(rem<4){ emit(add&MASK); if(rem>0){ u128 z=dsg>0?(((u128)1<<rem)-1):1; emit((add+mult*z)&MASK);} return; }
  rec(used+3,(mult*8*i9)&MASK,(dsg>0?add-mult*i9:add+mult*i9)&MASK,top);
  rec(used+4,(mult*16*i27)&MASK,add,top);
}
static u128 inv(u128 a){u128 x=a;for(int i=0;i<8;i++)x*=2-a*x;return x;}
int main(int c,char**v){ Q=atoi(v[1]); dsg=atoi(v[2]); part=atoi(v[3]); nparts=atoi(v[4]);
  MASK=(((u128)1<<Q)-1); i9=inv(9)&MASK; i27=inv(27)&MASK;
  rec(0,1,0,Q>=40);
  printf("inf %llu\n",(unsigned long long)inf_); for(int m=0;m<600;m++) if(hist[m]) printf("%d %llu\n",m,(unsigned long long)hist[m]);
  return 0; }
