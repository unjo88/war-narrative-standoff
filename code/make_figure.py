"""발표문 <그림 1>을 공개 집계값에서 다시 그린다(번역문 불필요).
사용법: python code/make_figure.py [저장소 루트] → aggregates/fig1_emotion_density.png"""
import csv, os, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
R=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in font_manager.findSystemFonts():
    if 'NotoSansCJK-Regular' in f: font_manager.fontManager.addfont(f); plt.rcParams['font.family']=font_manager.FontProperties(fname=f).get_name(); break
plt.rcParams['axes.unicode_minus']=False

from matplotlib.textpath import TextPath, TextToPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D, ScaledTranslation
from matplotlib.font_manager import FontProperties
def rich_title(ax, segs, size=12, pad=6):
    """서명만 기울임(skew)으로 그리는 제목. segs=[(글자, 기울임 여부), ...]"""
    fp=FontProperties(family=plt.rcParams['font.family'], size=size)
    t2p=TextToPath(); ws=[t2p.get_text_width_height_descent(t,fp,ismath=False)[0] for t,_ in segs]
    x=-sum(ws)/2; k=ax.figure.dpi/72
    for (t,it),w in zip(segs,ws):
        tp=TextPath((0,0),t,prop=fp,size=size)
        tr=(Affine2D().skew_deg(12 if it else 0,0).translate(x,pad).scale(k)
            + ScaledTranslation(0.5,1.0,ax.transAxes))
        ax.add_patch(PathPatch(tp,transform=tr,color='black',lw=0,clip_on=False)); x+=w
    ax.set_title(' ',fontsize=size)
rows=lambda p: list(csv.DictReader(open(os.path.join(R,p),encoding='utf-8-sig')))
M=rows('aggregates/monthly_density_1597.csv'); Bn=rows('aggregates/iliad18_bins50.csv')
fig,(a,b)=plt.subplots(1,2,figsize=(10.8,4.05),dpi=200)
x=[f"{r['month_lunar']}월" for r in M]; y=[float(r['density_per100']) for r in M]
a.bar(x,y,color='#444444',width=0.6)
for lab,m in (('모친상','4월'),('명량','9월'),('아들 전사','10월')):
    i=x.index(m); a.text(i,y[i]+0.07,lab,ha='center',fontsize=10)
rich_title(a,[('(가) ',False),('난중일기',True),(' 1597년 월별',False)]); a.set_ylabel('정서어 / 100어절'); a.set_ylim(0,1.8)
s=[int(r['range_line_in_translation'].split('.')[1].split('-')[0]) for r in Bn]
b.plot(range(len(s)),[float(r['A_density']) for r in Bn],'-o',color='#222222',ms=4,label='천병희 역(A)')
b.plot(range(len(s)),[float(r['B_density']) for r in Bn],'--s',color='#888888',ms=4,label='이준석 역(B)')
b.set_xticks(range(len(s))); b.set_xticklabels(s); b.set_xlabel('시작 행(번역본 행 번호)')
rich_title(b,[('(나) ',False),('일리아스',True),(' 18권 50행 구간별',False)]); b.legend(frameon=False)
for ax in (a,b): ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); out=os.path.join(R,'aggregates/fig1_emotion_density.png'); fig.savefig(out); print(out)
