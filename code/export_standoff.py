"""작업 코퍼스(비공개, 번역문 포함)에서 공개용 파생 데이터를 모두 만든다.
사용법: python code/export_standoff.py <작업 코퍼스 폴더> [저장소 루트]
작업 코퍼스: merged_nan.json, merged_cheon.json, merged_lee.json (형식은 docs/data_dictionary.md)
손으로 만드는 원천 자료(lexicon/, annotations/, data/provenance/, ontology/)는 읽기만 하고 고치지 않는다."""
import json, re, csv, os, sys, hashlib, platform
from collections import Counter, defaultdict
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emotion import (LEX1, LEX2, I1, I2, UP, EPI_REMOVE, EPI_LINE, lemmas, count, body_layer, translator_marks,
                     strip_date, weather_split, eojeol, category, simhash64)
from korean_lunar_calendar import KoreanLunarCalendar
D=sys.argv[1]; R=sys.argv[2] if len(sys.argv)>2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def W(path,header,rows):
    p=os.path.join(R,path); os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
GREEK={1:611,2:877,3:461,4:544,5:909,6:529,7:482,8:565,9:713,10:579,11:848,12:471,13:837,14:522,15:746,16:867,17:761,18:617,19:424,20:503,21:611,22:515,23:897,24:804}
N=json.load(open(f'{D}/merged_nan.json'))['rows']
C=json.load(open(f'{D}/merged_cheon.json'))['rows']; L=json.load(open(f'{D}/merged_lee.json'))['rows']
txt=lambda r:(r['B'] or r['A']).replace('\n','')
# ================= 난중일기 항목 색인 =================
WIT={'정유일기Ⅰ':('I','Ⅰ'),'정유일기Ⅱ':('II','Ⅱ')}
seen=Counter(); RID={}
for i,r in enumerate(N):
    base=f"NJ-{r['year']}-{'L' if r['leap'] else ''}{r['mon']:02d}{r['day']:02d}"+(f"-{WIT[r['sec']][0]}" if r['sec'] in WIT else '')
    seen[base]+=1; RID[i]=f"{base}-{seen[base]:02d}"
cal=KoreanLunarCalendar()
def solar(r):
    try: return cal.SolarIsoFormat() if cal.setLunarDate(r['year'],r['mon'],r['day'],bool(r['leap'])) else ''
    except Exception: return ''
OCR={'양쪽':'이중 판독 일치','분리(양쪽)':'이중 판독(앞 날짜에서 분리)','올린 파일':'판독 A만','재판독(신규)':'판독 B만(신규)',
     '재판독만':'판독 B만','올린 파일만':'판독 A만'}
rows=[]
for i,r in enumerate(N):
    t=txt(r)
    rows.append([RID[i],'S-NJ-01',r['sec'],WIT.get(r['sec'],('',''))[1],r['year'],r['gy'],'윤' if r['leap'] else '',r['mon'],r['day'],
                 r['gz'],r['gzh'],solar(r),r['bp'],r['pdf'],OCR.get(r['src'],r['src']),len(re.sub(r'[^가-힣]','',t)),simhash64(t),'',''])
W('data/nanjung/entries_index.csv',['record_id','source_id','section','witness_label','year_lunar','year_ganzhi','leap','month','day','day_ganzhi',
  'day_ganzhi_hanja','solar_date_kasi','book_page','scan_page','ocr_reading','hangul_chars','simhash64','base_text','alignment'],rows)
# ================= 1597년 시범 =================
J1=[(i,r) for i,r in enumerate(N) if r['sec']=='정유일기Ⅰ']; J2=[(i,r) for i,r in enumerate(N) if r['sec']=='정유일기Ⅱ']
end1=max((r['mon'],r['day']) for _,r in J1)
year=J1+[(i,r) for i,r in J2 if (r['mon'],r['day'])>end1]
def nj(r,c):
    t=strip_date(txt(r)); wx,rest=weather_split(t)
    b=t if c.get('rep') else rest
    b=b if c.get('layer') else body_layer(b)
    return count(b,I2 if c.get('v2') else I1,not c.get('nolem')),eojeol(b)
CONDS=[('기본(본문 층·반복 제외·표제어화·사전 v1)',{}),('역자 층 포함',{'layer':1}),('반복 표현(날씨) 포함',{'rep':1}),
       ('표제어화 없이 어간 문자열 대조',{'nolem':1}),('정서어 사전 v2(불안 범주 추가)',{'v2':1})]
prow=[]; mon=defaultdict(lambda:[0,0])
for i,r in year:
    t=strip_date(txt(r)); wx,rest=weather_split(t); b=body_layer(rest)
    l=lemmas(b); h1=[w for w in l if w in I1]; h2=[w for w in l if w in I2]
    c1=Counter(UP[I1[w]] for w in h1); c2=Counter(UP[I2[w]] for w in h2); n=eojeol(b)
    prow.append([RID[i],r['sec'],f"1597-{r['mon']:02d}-{r['day']:02d}",n,eojeol(body_layer(t)),'Y' if wx else 'N',translator_marks(rest),
      c1.get('상실',0),c1.get('분노',0),c1.get('의지',0),c1.get('해소',0),len(h1),round(100*len(h1)/n,2) if n else 0,c2.get('불안',0),len(h2),'auto-v1',''])
    mon[r['mon']][0]+=len(h1); mon[r['mon']][1]+=n
W('data/nanjung/pilot_1597_records.csv',['record_id','section','date_lunar','eojeol_body','eojeol_with_weather','weather_record','translator_layer_marks',
  'v1_상실','v1_분노','v1_의지','v1_해소','v1_total','v1_density_per100','v2_불안','v2_total','annotator','confidence'],prow)
W('aggregates/monthly_density_1597.csv',['month_lunar','emotion_words_v1','eojeol_body','density_per100'],[[m,a,b,round(100*a/b,2) if b else 0] for m,(a,b) in sorted(mon.items())])
# ---- 정유일기Ⅰ·Ⅱ 중복
D2={(r['mon'],r['day']):(i,r) for i,r in J2}; orow=[]
NOTE={'1597-08-10':'Ⅰ의 정서어 1개는 인명 안도(오탐)','1597-08-07':'Ⅱ의 정서어 1개는 닭이 우는 용례(오탐)','1597-08-09':'Ⅱ의 정서어 2개는 낙안 고을 사람들의 정서(행위자 비이순신)'}
for i,r in J1:
    k=(r['mon'],r['day'])
    if k not in D2: continue
    j,r2=D2[k]; ba=body_layer(weather_split(strip_date(txt(r)))[1]); bb=body_layer(weather_split(strip_date(txt(r2)))[1])
    la,lb=lemmas(ba),lemmas(bb); ha=[w for w in la if w in I1]; hb=[w for w in lb if w in I1]
    ca,cb=Counter(UP[I1[w]] for w in ha),Counter(UP[I1[w]] for w in hb); ea,eb=eojeol(ba),eojeol(bb)
    ja=set(lemmas(body_layer(strip_date(txt(r))))); jb=set(lemmas(body_layer(strip_date(txt(r2)))))  # 자카드: 날씨 기록 포함(발표문과 같은 기준)
    jac=len(ja&jb)/max(1,len(ja|jb)); d=f"1597-{k[0]:02d}-{k[1]:02d}"
    orow.append([d,RID[i],RID[j],'일치' if ea and eb else ('Ⅰ 본문 없음(날씨만)' if not ea else 'Ⅱ 본문 없음(날씨만)'),ea,eb,len(ha),len(hb),
      round(100*len(ha)/ea,2) if ea else 0,round(100*len(hb)/eb,2) if eb else 0,ca.most_common(1)[0][0] if ca else '',cb.most_common(1)[0][0] if cb else '',round(jac,2),NOTE.get(d,'')])
W('data/nanjung/overlap_1597_I_II.csv',['date_lunar','record_id_I','record_id_II','alignment','eojeol_I','eojeol_II','emo_v1_I','emo_v1_II','density_I','density_II',
  'top_category_I','top_category_II','jaccard_lemmas','note'],orow)
# ================= 일리아스 =================
SRCW={'A':'S-IL-A','B':'S-IL-B'}
def lidx(Rw,path,wn):
    cnt=Counter(x[0] for x in Rw); out=[]
    for x in Rw:
        canon=x[1] if cnt[x[0]]==GREEK[x[0]] else ''
        out.append([f"IL-{x[0]:02d}-{x[1]:03d}-{wn}",SRCW[wn],x[0],x[1],canon,x[8],x[7],OCR.get(x[5],x[5])])
    W(path,['record_id','source_id','book','line_in_translation','line_canonical','book_page','scan_page','ocr_reading'],out)
    return {b:cnt[b]-GREEK[b] for b in GREEK if cnt[b]!=GREEK[b]}
offA=lidx(C,'data/iliad/line_index_A_cheon.csv','A'); offB=lidx(L,'data/iliad/line_index_B_lee.csv','B')
W('data/iliad/line_count_by_book.csv',['book','greek_lines_OCT','A_lines','B_lines','B_minus_greek'],
  [[b,GREEK[b],sum(1 for x in C if x[0]==b),sum(1 for x in L if x[0]==b),sum(1 for x in L if x[0]==b)-GREEK[b]] for b in GREEK])
def il_clean(t): return re.sub(r"(?<=[가-힣])['?*`\"]?\d{0,3}(?=[의이가을를은는에과와도,\s])", '', t)
def il_rows(Rw,b,lo,hi): return [x for x in Rw if x[0]==b and lo<=x[1]<=hi]
def il_count(rows,c):
    h=[];n=0
    for x in rows:
        t=x[2]; t2=t if c.get('layer') else il_clean(re.sub(r'\([^()]*\)','',t))
        if not c.get('rep'):
            for p in EPI_REMOVE: t2=re.sub(p,'',t2)
        h+=count(t2,I2 if c.get('v2') else I1,not c.get('nolem')); n+=eojeol(t2)
    return h,n
bins=[]
for lo in range(1,618,50):
    row=[f"18.{lo}-{min(lo+49,617)}"]
    for Rw in (C,L):
        h,n=il_count(il_rows(Rw,18,lo,lo+49),{}); row+=[len(h),n,round(100*len(h)/n,2) if n else 0]
    bins.append(row)
W('aggregates/iliad18_bins50.csv',['range_line_in_translation','A_emo_v1','A_eojeol','A_density','B_emo_v1','B_eojeol','B_density'],bins)
def ep_lines(Rw): return sorted({x[1] for x in Rw if x[0]==18 and any(re.search(p,x[2]) for p in EPI_LINE)})
ea,eb=ep_lines(C),ep_lines(L)
W('data/iliad/epithet_lines_book18.csv',['record_id','witness','book','line_in_translation'],
  [[f"IL-18-{l:03d}-A",'A',18,l] for l in ea]+[[f"IL-18-{l:03d}-B",'B',18,l] for l in eb])
keep=sum(1 for l in ea if any(k in eb for k in (l-1,l,l+1)))
W('aggregates/epithet_retention_book18.csv',['A_epithet_lines','B_epithet_lines','A_lines_retained_in_B(±1행)','retention_percent'],[[len(ea),len(eb),keep,round(100*keep/max(1,len(ea)),1)]])
# ================= 조건별 표 =================
crow=[]
for name,c in CONDS:
    h=[];n=0
    for _,r in year: x,e=nj(r,c); h+=x; n+=e
    ha,na=il_count(il_rows(C,18,1,700),c); hb,nb=il_count(il_rows(L,18,1,700),c)
    crow.append([name,len(h),n,round(100*len(h)/n,2),len(ha),na,round(100*len(ha)/na,2),len(hb),nb,round(100*len(hb)/nb,2)])
W('aggregates/conditions_table.csv',['condition','NJ1597_hits','NJ1597_eojeol','NJ1597_density','IL18A_hits','IL18A_eojeol','IL18A_density','IL18B_hits','IL18B_eojeol','IL18B_density'],crow)
# ================= 편차 지표 예 =================
sa,na=il_count(il_rows(C,18,22,35),{}); sb,nb=il_count(il_rows(L,18,22,35),{})
la=set(lemmas(' '.join(il_clean(x[2]) for x in il_rows(C,18,22,35)))); lb=set(lemmas(' '.join(il_clean(x[2]) for x in il_rows(L,18,22,35))))
O={x[0]:x for x in orow}
def ovr(d,lab,match): x=O[d]; return [lab,x[6],x[7],x[8],x[9],match,x[12]]
W('aggregates/witness_deviation_examples.csv',['unit','emo_1','emo_2','density_1','density_2','main_category_match','jaccard'],[
  ovr('1597-09-14','1597-09-14 (Ⅰ/Ⅱ)','불일치(없음/분노·통분)'),ovr('1597-08-09','1597-08-09 (Ⅰ/Ⅱ)','불일치(없음/상실·비탄; 행위자 고을 사람들)'),
  ovr('1597-09-16','1597-09-16 (Ⅰ/Ⅱ)','양쪽 정서어 없음'),
  ['18.22-35 (A/B)',len(sa),len(sb),round(100*len(sa)/na,2),round(100*len(sb)/nb,2),'상위·하위 일치(상실·비탄)',round(len(la&lb)/len(la|lb),2)]])
# ================= 두 판독 불일치율 =================
def hg(s): return re.sub(r'[^가-힣]','',str(s or ''))
def lev(a,b):
    if len(a)<len(b): a,b=b,a
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1): cur.append(min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
def il_dis(Rw):
    E=Nn=k=0
    for x in Rw:
        if x[0]==18:
            a,b=hg(x[2]),hg(x[3])
            if a and b: E+=lev(a,b); Nn+=max(len(a),len(b)); k+=1
    return k,round(100*E/Nn,2)
kA,dA=il_dis(C); kB,dB=il_dis(L)
rs=[lev(hg(r['A']),hg(r['B']))/max(len(hg(r['A'])),len(hg(r['B']))) for r in N if r['year']==1597 and hg(r['A']) and hg(r['B'])]
W('aggregates/ocr_disagreement.csv',['target','unit','measure','value_percent','note'],[
  ['일리아스 18권 천병희 역',f'행 {kA}','한글 글자 편집 거리/길이(전체)',dA,'두 판독(내장 글자 정보 / Tesseract 5) 간 불일치. CER 아님'],
  ['일리아스 18권 이준석 역',f'행 {kB}','한글 글자 편집 거리/길이(전체)',dB,'같음'],
  ['난중일기 1597년',f'항목 {len(rs)}','항목별 중앙값',round(100*median(rs),2),'각주 번호·괄호 속 한자·항목 경계 차이 포함. CER 아님']])
# ================= 붓스트랩 95% 구간(발표문 Ⅲ장 3절) =================
import random
def il_blocks(Rw,lex,size=10):
    out={}
    for x in Rw:
        if x[0]!=18: continue
        t=il_clean(re.sub(r'\([^()]*\)','',x[2]))
        for p in EPI_REMOVE: t=re.sub(p,'',t)
        b=(x[1]-1)//size; h,n=out.get(b,(0,0)); out[b]=(h+len(count(t,lex)),n+eojeol(t))
    return out
def dens_ratio(keys,X,Y):
    hx=sum(X[k][0] for k in keys); nx=sum(X[k][1] for k in keys); hy=sum(Y[k][0] for k in keys); ny=sum(Y[k][1] for k in keys)
    return float('inf') if hy==0 else (hx/nx)/(hy/ny)
def boot(keys,pairs,seed,B=5000):
    rng=random.Random(seed); res=[[] for _ in pairs]
    for _ in range(B):
        smp=[rng.choice(keys) for _ in keys]
        for j,(X,Y) in enumerate(pairs): res[j].append(dens_ratio(smp,X,Y))
    out=[]
    for j,(X,Y) in enumerate(pairs):
        r=sorted(res[j]); lo,hi=r[int(.025*B)],r[int(.975*B)-1]
        out.append((round(dens_ratio(keys,X,Y),2),round(lo,2),'∞' if hi==float('inf') else round(hi,2),round(sum(1 for v in r if v==float('inf'))/B,3)))
    return out
A1,B1,A2,B2=il_blocks(C,I1),il_blocks(L,I1),il_blocks(C,I2),il_blocks(L,I2); kb=sorted(set(A1)&set(B1))
(i1,i2)=boot(kb,[(A1,B1),(A2,B2)],seed=1)
O2={i:(x[7],x[5]) for i,x in enumerate(orow)}; O1={i:(x[6],x[4]) for i,x in enumerate(orow)}
FIX={'1597-08-10':(1,0),'1597-08-07':(0,1),'1597-08-09':(0,2)}
C1={i:(x[6]-FIX.get(x[0],(0,0))[0],x[4]) for i,x in enumerate(orow)}; C2={i:(x[7]-FIX.get(x[0],(0,0))[1],x[5]) for i,x in enumerate(orow)}
(n1,)=boot(list(O1),[(O2,O1)],seed=2); (n2,)=boot(list(O1),[(C2,C1)],seed=3)
def boot_diff(keys,P1,P2,seed,B=5000):
    rng=random.Random(seed); r=[]
    for _ in range(B):
        smp=[rng.choice(keys) for _ in keys]; r.append(dens_ratio(smp,*P1)-dens_ratio(smp,*P2))
    r.sort(); return (round(dens_ratio(keys,*P1)-dens_ratio(keys,*P2),2),round(r[int(.025*B)],2),round(r[int(.975*B)-1],2),0.0)
dd=boot_diff(kb,(A1,B1),(A2,B2),seed=1)
W('aggregates/bootstrap_ci.csv',['comparison','unit','resamples','dictionary','ratio','ci95_low','ci95_high','share_undefined','note'],[
 ['일리아스 18권 밀도 비(천병희/이준석)',f'10행 블록 {len(kb)}개',5000,'v1',*i1,''],
 ['일리아스 18권 밀도 비(천병희/이준석)',f'10행 블록 {len(kb)}개',5000,'v2',*i2,''],
 ['일리아스 18권 밀도 비의 차이(v1−v2)',f'10행 블록 {len(kb)}개',5000,'v1−v2',*dd,'0을 포함하면 사전이 효과 크기를 유의하게 바꾸지 않은 것(Gelman & Stern, 2006)'],
 ['정유일기 Ⅱ/Ⅰ 밀도 비',f'겹치는 날 {len(O1)}일',5000,'v1',*n1,'자동 태깅 그대로'],
 ['정유일기 Ⅱ/Ⅰ 밀도 비',f'겹치는 날 {len(O1)}일',5000,'v1',*n2,'오탐(8.7·8.10)과 타인 정서(8.9) 제외'],])
# ================= 온톨로지 검증 질의(발표문 Ⅲ장 2절) =================
def md(x): m,d=map(int,x[5:].split('-')); return m,d
q1=[r for r in prow if r[7]>0]
q2=[r for r in prow if (9,17)<=md(r[2])<=(10,16) and r[11]>0]
q3=[x for x in orow if x[10]!=x[11]]
def lab(r): 
    c=[k for k,v in zip(('상실','분노','의지','해소'),r[7:11]) if v]; return f"{int(r[2][5:7])}.{int(r[2][8:])}({'·'.join(c)})"
W('aggregates/competency_questions.csv',['qid','question','answer','n','source','note'],[
 ['Q1','1597년에 상실 범주의 정서어가 잡힌 날짜는?','; '.join(lab(r) for r in q1),len(q1),'data/nanjung/pilot_1597_records.csv','사전 v1 자동 태깅(오탐 포함)'],
 ['Q2','명량해전(9.16) 이후 30일(9.17–10.16) 안에 나타난 정서는?','; '.join(lab(r) for r in q2),len(q2),'data/nanjung/pilot_1597_records.csv',
  f"정서어 {sum(r[11] for r in q2)}개 중 10.14에 {sum(r[11] for r in q2 if r[2]=='1597-10-14')}개"],
 ['Q3','정유일기Ⅰ·Ⅱ에서 주된 정서 범주가 갈리는 날짜는?','; '.join(f"{int(x[0][5:7])}.{int(x[0][8:])}({x[10] or '없음'}/{x[11] or '없음'})" for x in q3),len(q3),
  'data/nanjung/overlap_1597_I_II.csv','오탐·행위자 문제: '+'; '.join(f"{int(x[0][5:7])}.{int(x[0][8:])}" for x in q3 if x[13])],
 ['Q4','일리아스 18권 22–35행 장면에서 두 번역의 정서 범주는 일치하는가?','상위·하위 일치(상실·비탄)',1,'aggregates/witness_deviation_examples.csv','A 6개 / B 5개']])
# ================= 실행 기록·데이터 패키지·체크섬 =================
from make_datapackage import build as build_dp
import kiwipiepy, korean_lunar_calendar
meta=dict(data_version='v0.1-pilot',python=platform.python_version(),kiwipiepy=kiwipiepy.__version__,
          korean_lunar_calendar=__import__('importlib.metadata',fromlist=['version']).version('korean-lunar-calendar'),
          lexicon_sha256={f:hashlib.sha256(open(os.path.join(R,'lexicon',f),'rb').read()).hexdigest()[:16] for f in sorted(os.listdir(os.path.join(R,'lexicon')))},
          iliad_B_line_offsets=offB)
json.dump(meta,open(os.path.join(R,'aggregates/run_metadata.json'),'w'),ensure_ascii=False,indent=1)
build_dp(R)
import subprocess; subprocess.run([sys.executable,os.path.join(os.path.dirname(os.path.abspath(__file__)),'make_figure.py'),R],check=True,stdout=subprocess.DEVNULL)
from update_checksums import write as write_sums; write_sums(R)
print('done', len(rows), len(prow), len(orow), crow[0][1:4], crow[4][1], 'B offsets', offB)
