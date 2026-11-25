"""저장소 검사: ID 형식·참조 무결성, 번역문 유출 의심 문자열, 체크섬, 발표문 수치, 온톨로지."""
import csv, glob, hashlib, os, re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rows(p): return list(csv.DictReader(open(os.path.join(R,p),encoding='utf-8-sig')))
NJ={r['record_id'] for r in rows('data/nanjung/entries_index.csv')}
def test_ids_ascii_unique():
    for p in glob.glob(os.path.join(R,'data/**/*.csv'),recursive=True):
        ids=[r['record_id'] for r in csv.DictReader(open(p,encoding='utf-8-sig')) if 'record_id' in r]
        assert all(re.fullmatch(r'[A-Za-z0-9-]+',i) for i in ids), p
    assert len(NJ)==1655
def test_references_exist():
    for r in rows('annotations/pilot_1597_key_entries.csv'): assert r['record_id'] in NJ
    for r in rows('data/nanjung/overlap_1597_I_II.csv'): assert r['record_id_I'] in NJ and r['record_id_II'] in NJ
    for r in rows('data/nanjung/pilot_1597_records.csv'): assert r['record_id'] in NJ
def test_no_long_korean_text():
    # 번역문 문장이 섞였는지 거칠게 검사: 공백 포함 한글 26자 이상 연속은 연구자 요지·설명 열에서만 허용
    allowed={'summary_by_researcher','note','main_category_match','condition','description','measure','base_text'}
    for p in glob.glob(os.path.join(R,'data/**/*.csv'),recursive=True)+glob.glob(os.path.join(R,'aggregates/*.csv')):
        for r in csv.DictReader(open(p,encoding='utf-8-sig')):
            for k,v in r.items():
                if k not in allowed and v and re.search(r'[가-힣][가-힣 ]{25,}',v): raise AssertionError((p,k,v[:30]))
def test_checksums():
    for line in open(os.path.join(R,'SHA256SUMS.txt'),encoding='utf-8'):
        h,p=line.rstrip('\n').split('  ',1)
        assert hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()==h, p
def test_paper_figures():
    c={r['condition']:r for r in rows('aggregates/conditions_table.csv')}
    base=c['기본(본문 층·반복 제외·표제어화·사전 v1)']
    assert (base['NJ1597_hits'],base['IL18A_hits'],base['IL18B_hits'])==('86','52','44')
    assert c['정서어 사전 v2(불안 범주 추가)']['NJ1597_hits']=='103'
    o=rows('data/nanjung/overlap_1597_I_II.csv')
    assert len(o)==64 and sum(int(r['emo_v1_I']) for r in o)==3 and sum(int(r['emo_v1_II']) for r in o)==7
def test_ontology():
    import rdflib
    g=rdflib.Graph(); g.parse(os.path.join(R,'ontology/war_narrative.ttl'))
    for s in set(g.subjects())|set(g.objects()):
        m=re.search(r'#(NJ-[\w-]+)$',str(s))
        if m: assert m.group(1) in NJ, m.group(1)

def test_annotations_match_counts():
    P={r['record_id']:r for r in rows('data/nanjung/pilot_1597_records.csv')}
    for a in rows('annotations/pilot_1597_key_entries.csv'):
        p=P[a['record_id']]; tagged={k for k in ('상실','분노','의지','해소') if int(p['v1_'+k])>0}
        named={k for k in ('상실','분노','의지','해소') if k in a['auto_tag_v1(category)']}
        assert tagged==named, a['record_id']
def test_lexicon_versions():
    v1={(r['lemma'],r['sub_emotion']) for r in rows('lexicon/emotion_lexicon_v1.csv')}
    v2={(r['lemma'],r['sub_emotion']) for r in rows('lexicon/emotion_lexicon_v2.csv')}
    assert v1<v2 and {s for _,s in v2-v1}=={'불안'}
    # 발표문 <표 4>의 표제어 예가 사전 v1에 있는지
    lem={l for l,_ in v1}
    for w in ['통곡하다','울다','슬프다','애통하다','죄스럽다','부끄럽다','분하다','원통하다','노하다','맹세하다','각오하다','결심하다','다행스럽다','안심하다','기쁘다','즐겁다']:
        assert w in lem, w

def test_competency_answers_match_paper():
    q={r['qid']:r for r in rows('aggregates/competency_questions.csv')}
    assert q['Q2']['n']=='5' and q['Q2']['answer'].startswith('10.8') and '10.13(상실·분노)' in q['Q2']['answer']
    assert q['Q3']['n']=='7' and '8.7' in q['Q3']['note'] and '8.10' in q['Q3']['note'] and '8.9' in q['Q3']['note']

def test_bootstrap_matches_paper():
    b=rows('aggregates/bootstrap_ci.csv')
    assert (b[0]['ratio'],b[0]['ci95_low'],b[0]['ci95_high'])==('1.31','1.03','1.61')
    assert (b[1]['ratio'],b[1]['ci95_low'],b[1]['ci95_high'])==('1.19','0.97','1.39')
    assert (b[2]['ratio'],b[2]['ci95_low'],b[2]['ci95_high'])==('0.13','-0.02','0.33')
    assert (b[3]['ratio'],b[3]['ci95_low'],b[3]['ci95_high'])==('1.96','0.53','∞')
    assert (b[4]['ratio'],b[4]['ci95_low'])==('1.68','0.43')

def test_agreement_alpha():
    import sys; sys.path.insert(0, os.path.join(R,'code'))
    from agreement import alpha_nominal
    assert alpha_nominal([('1','1'),('0','0'),('1','1'),('0','0')])==1.0
    # 참조값(krippendorff 패키지): 아래 자료의 명목형 α = 0.6042
    v=alpha_nominal([('1','1'),('1','0'),('0','0'),('0','0'),('1','1'),('0','1'),('0','0'),('1','1'),('0','0'),('0','0')])
    assert abs(v-0.6042)<0.001
    ids=[r['record_id'] for r in rows('annotations/agreement_sample_ids.csv')]
    assert len(ids)==53 and len(set(ids))==53 and all(i in NJ for i in ids)
