"""정서어 집계 함수: Kiwi 형태소 분석·표제어화, 역자 층 분리, 날씨 기록 분리.
정서어 사전과 수식어구 패턴은 lexicon/ 폴더의 CSV에서만 읽는다(사전의 단일 출처)."""
import csv, os, re
from kiwipiepy import Kiwi
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _read(name): return list(csv.DictReader(open(os.path.join(ROOT,'lexicon',name),encoding='utf-8-sig')))
def load_lexicon(version):
    lex,up={}, {}
    for r in _read(f'emotion_lexicon_{version}.csv'):
        lex.setdefault(r['sub_emotion'],[]).append(r['lemma']); up[r['sub_emotion']]=r['category']
    return lex,up
LEX1,UP1=load_lexicon('v1'); LEX2,UP2=load_lexicon('v2')
UP={**UP1,**UP2}
_EP=_read('epithet_patterns_ko.csv')
EPI_REMOVE=[r['pattern_regex'] for r in _EP if r['remove_as_repetition']=='Y']
EPI_LINE=[r['pattern_regex'] for r in _EP if r['tag_epithet_line']=='Y']
K=Kiwi()
def inv(lex): return {w:c for c,ws in lex.items() for w in ws}
I1,I2=inv(LEX1),inv(LEX2)
def lemmas(text):
    toks=K.tokenize(text); out=[]
    for k,t in enumerate(toks):
        tag=t.tag.split('-')[0]; nxt=toks[k+1] if k+1<len(toks) else None
        if tag in('NNG','NNP','XR'):
            if nxt is not None and nxt.tag.split('-')[0] in('XSV','XSA'):
                out.append(t.form+'스럽다' if nxt.form=='스럽' else t.form+'하다')
            else: out.append(t.form)
        elif tag in('VV','VA'): out.append(t.form+'다')
    return out
def count(text,lex,lemmatize=True):
    if lemmatize: return [l for l in lemmas(text) if l in lex]
    stems=sorted({re.sub(r'(하다|스럽다|다)$','',w) for w in lex},key=len,reverse=True); out=[]
    for st in stems:
        if len(st)>=2: out+=[st]*len(re.findall(st,text))
    return out
def body_layer(t):
    t=re.sub(r'\([^()]*\)|\[[^\]]*\]|（[^）]*）','',t)
    return re.sub(r'(?<=[가-힣.,!?”"\)])\s?\d{1,3}(?=[\s가-힣,.“"]|$)','',t)
def translator_marks(t):
    return len(re.findall(r'\([^()]*\)|\[[^\]]*\]|（[^）]*）',t))+len(re.findall(r'(?<=[가-힣.,!?”"\)])\s?\d{1,3}(?=[\s가-힣,.“"]|$)',t))
def strip_date(t): return re.sub(r'^\s*\d{1,2}\s*[일얼열엘]\S{0,6}\s*','',t)
WX=re.compile(r'^([^.]{0,60}?(맑|흐리|흐림|비가|비는|눈이|바람|안개|개었|겠다|겼다|갰다)[^.]{0,40}\.)')
def weather_split(t):
    m=WX.match(t); return (m.group(1),t[m.end():]) if m else ('',t)
def eojeol(t): return len(re.findall(r'\S+',t))
def category(word,lexinv,lex):
    if word in lexinv: return UP[lexinv[word]]
    stem={re.sub(r'(하다|스럽다|다)$','',k):v for k,v in lexinv.items()}
    return UP[stem.get(word,'불안')]
# ---- 비공개 본문 대신 공개하는 지문(SimHash): 본문을 복원할 수 없고, OCR 오차가 있어도 가까운 값이 나온다
import hashlib
def simhash64(text):
    t=re.sub(r'[^가-힣]','',text); v=[0]*64
    for i in range(len(t)-1):
        h=int.from_bytes(hashlib.md5(t[i:i+2].encode()).digest()[:8],'big')
        for b in range(64): v[b]+=1 if h>>b&1 else -1
    return f"{sum(1<<b for b in range(64) if v[b]>0):016x}"
def hamming(a,b): return bin(int(a,16)^int(b,16)).count('1')
