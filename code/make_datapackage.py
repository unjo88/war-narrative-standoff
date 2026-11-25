"""Frictionless Data Package(datapackage.json)를 만든다: 각 CSV의 열 이름·형식·설명과 라이선스."""
import csv, json, os, re
DESC={
 'record_id':'레코드 ID(ASCII). NJ-연도-[L]월일[-I|-II]-순번 / IL-권-행-A|B',
 'source_id':'data/provenance/sources.csv의 출처 ID','witness_label':'사람이 읽는 증언 라벨(Ⅰ/Ⅱ)',
 'solar_date_kasi':'양력 환산(ISO 8601). 한국천문연구원 역법 데이터 기반 korean-lunar-calendar 변환값',
 'hangul_chars':'항목 본문의 한글 글자 수(대조용)','simhash64':'항목 본문의 64비트 SimHash 지문(본문 복원 불가, 대조용)',
 'base_text':'날짜별 저본(초고본·일기초·전서본). 전체 구축에서 기입','alignment':'정렬 유형. 전체 구축에서 기입',
 'line_in_translation':'번역본에서 센 행 번호','line_canonical':'그리스어 통용 행 번호. 권별 행수가 원문과 일치하는 경우에만 기입',
 'translator_layer_marks':'괄호 보충어·역주 표지 수(역자 층)','eojeol_body':'날씨 기록·역자 층을 뺀 본문 층 어절 수',
 'jaccard_lemmas':'두 기록 표제어 집합의 자카드 계수(날짜 표기 제외, 날씨 기록 포함)'}
def infer(vals):
    v=[x for x in vals if x!='']
    if v and all(re.fullmatch(r'-?\d+',x) for x in v): return 'integer'
    if v and all(re.fullmatch(r'-?\d+(\.\d+)?',x) for x in v): return 'number'
    return 'string'
def build(R):
    res=[]
    for top in ('data','aggregates','annotations','lexicon','docs'):
        for root,_,fs in sorted(os.walk(os.path.join(R,top))):
            for f in sorted(fs):
                if not f.endswith('.csv'): continue
                p=os.path.join(root,f); rel=os.path.relpath(p,R)
                rows=list(csv.reader(open(p,encoding='utf-8-sig'))); hdr=rows[0]
                fields=[{'name':h,'type':infer([r[i] for r in rows[1:] if i<len(r)]),**({'description':DESC[h]} if h in DESC else {})} for i,h in enumerate(hdr)]
                lic='CC0-1.0' if 'provenance' in rel else 'CC-BY-4.0'
                res.append({'name':re.sub(r'[^a-z0-9_.-]','-',rel.lower().replace('/','-').replace('.csv','')),'path':rel,'format':'csv',
                            'encoding':'utf-8-sig','licenses':[{'name':lic}],'schema':{'fields':fields}})
    dp={'name':'war-narrative-standoff','title':'고전 전쟁 서사 스탠드오프 데이터: 국역 난중일기·일리아스','version':'0.1.0-pilot',
        'licenses':[{'name':'CC-BY-4.0','path':'https://creativecommons.org/licenses/by/4.0/'}],'resources':res}
    json.dump(dp,open(os.path.join(R,'datapackage.json'),'w'),ensure_ascii=False,indent=1)
    return len(res)
if __name__=='__main__':
    import sys; print(build(sys.argv[1] if len(sys.argv)>1 else '.'))
