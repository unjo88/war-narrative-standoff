"""두 주석자(R1·R2)의 태깅 시트에서 범주별 Krippendorff's α(명목형)를 계산한다.
사용법: python code/agreement.py R1_태깅시트.xlsx R2_태깅시트.xlsx [저장소 루트]
출력: aggregates/krippendorff_alpha.csv(범주별 α·일치율·판정), aggregates/disagreements.csv(갈린 항목의 ID와 값만; 번역문 없음)
판정 기준(Krippendorff, 2004): α ≥ 0.800 확정, 0.667 ≤ α < 0.800 잠정, α < 0.667 재정의 후 재측정."""
import csv, os, sys
from collections import Counter
from itertools import product
CATS=['상실','분노','의지','해소','불안']
def alpha_nominal(pairs):
    """pairs: [(a,b), ...] 두 주석자가 같은 단위에 준 값. 결측 없음."""
    o=Counter()
    for a,b in pairs: o[(a,b)]+=1; o[(b,a)]+=1
    vals=sorted({v for p in pairs for v in p},key=str); n=2*len(pairs)
    nc={c:sum(o[(c,k)] for k in vals) for c in vals}
    Do=sum(o[(c,k)] for c,k in product(vals,vals) if c!=k)/n
    De=sum(nc[c]*nc[k] for c,k in product(vals,vals) if c!=k)/(n*(n-1))
    return None if De==0 else 1-Do/De
def verdict(a):
    if a is None: return '계산 불가(한 값만 나옴)'
    return '확정' if a>=0.8 else ('잠정' if a>=0.667 else '재정의 후 재측정')
def load(path):
    from openpyxl import load_workbook
    ws=load_workbook(path,data_only=True)['본태깅']; hdr=[c.value for c in ws[3]]; H={h:i for i,h in enumerate(hdr)}
    out={}
    for row in ws.iter_rows(min_row=4,values_only=True):
        rid=row[H['레코드 ID']]
        if not rid or not str(rid).startswith('NJ-'): continue
        out[rid]={**{c:row[H[c]] for c in CATS},'주된 범주':row[H['주된 범주']],'타인 정서':row[H['타인 정서']],'확신도':row[H['확신도']]}
    return out
def main(p1,p2,R):
    A,B=load(p1),load(p2); ids=sorted(set(A)&set(B))
    missing=[i for i in ids for k in CATS+['주된 범주'] if A[i][k] in (None,'') or B[i][k] in (None,'')]
    if missing: sys.exit(f'빈칸이 있는 항목: {sorted(set(missing))}')
    rows=[]; dis=[]
    for k in CATS+['주된 범주','타인 정서']:
        pairs=[(str(A[i][k]),str(B[i][k])) for i in ids]
        a=alpha_nominal(pairs); agree=sum(x==y for x,y in pairs)/len(pairs)
        pos=sum(1 for x,y in pairs if '1' in (x,y)) if k in CATS else ''
        rows.append([k,len(ids),round(agree,3),'' if a is None else round(a,3),verdict(a),pos])
        dis+=[[i,k,A[i][k],B[i][k],A[i]['확신도'],B[i]['확신도']] for i,(x,y) in zip(ids,pairs) if x!=y]
    pooled=[(str(A[i][k]),str(B[i][k])) for i in ids for k in CATS]; a=alpha_nominal(pooled)
    rows.append(['다섯 범주 통합(항목×범주)',len(pooled),round(sum(x==y for x,y in pooled)/len(pooled),3),round(a,3),verdict(a),''])
    os.makedirs(os.path.join(R,'aggregates'),exist_ok=True)
    with open(os.path.join(R,'aggregates/krippendorff_alpha.csv'),'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['category','units','percent_agreement','alpha_nominal','verdict','units_any_coder_positive']); w.writerows(rows)
    with open(os.path.join(R,'aggregates/disagreements.csv'),'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['record_id','field','R1','R2','R1_confidence','R2_confidence']); w.writerows(dis)
    for r in rows: print(r)
if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
