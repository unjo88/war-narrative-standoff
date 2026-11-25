"""내 작업 코퍼스의 난중일기 항목을 공개 레코드 ID에 맞춘다(재현의 첫 단계).
사용법: python code/match_corpus.py <내 merged_nan.json> [저장소 루트]
1) 연도·윤달·월·일·권차(정유일기Ⅰ·Ⅱ)로 후보를 찾고, 2) SimHash 해밍 거리로 같은 항목인지 확인한다.
판정: 날짜·권차가 같고 해밍 거리 20 이하, 한글 글자 수 비율 0.8–1.25이면 '같은 항목', 아니면 '확인 필요'(분할·병합·판독 차이).
SimHash는 짧은 항목에서 변별력이 낮으므로 주 키는 날짜이고, 지문은 이상 항목을 걸러 내는 보조 장치다."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emotion import simhash64, hamming
mine=json.load(open(sys.argv[1]))['rows']; R=sys.argv[2] if len(sys.argv)>2 else '.'
idx=list(csv.DictReader(open(os.path.join(R,'data/nanjung/entries_index.csv'),encoding='utf-8-sig')))
key=lambda sec,y,l,m,d:(sec,int(y),bool(l),int(m),int(d))
pub={}
for r in idx: pub.setdefault(key(r['section'],r['year_lunar'],r['leap'],r['month'],r['day']),[]).append(r)
out=[]; stat={'같은 항목':0,'확인 필요':0,'공개 색인에 없음':0}
for r in mine:
    t=(r.get('B') or r.get('A') or '').replace('\n',''); h=simhash64(t)
    cands=pub.get(key(r['sec'],r['year'],r['leap'],r['mon'],r['day']),[])
    if not cands: out.append(['',r['sec'],r['year'],r['mon'],r['day'],'','공개 색인에 없음']); stat['공개 색인에 없음']+=1; continue
    n=len(''.join(ch for ch in t if '가'<=ch<='힣'))
    best=min(cands,key=lambda c:hamming(c['simhash64'],h)); dist=hamming(best['simhash64'],h)
    ratio=n/max(1,int(best['hangul_chars']))
    v='같은 항목' if dist<=20 and 0.8<=ratio<=1.25 else '확인 필요'; stat[v]+=1
    out.append([best['record_id'],r['sec'],r['year'],r['mon'],r['day'],dist,round(ratio,2),v])
w=csv.writer(open('match_report.csv','w',newline='',encoding='utf-8-sig'))
w.writerow(['record_id','section','year','month','day','hamming','char_ratio','verdict']); w.writerows(out)
print(stat)
