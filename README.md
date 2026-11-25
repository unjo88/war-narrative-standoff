# 고전 전쟁 서사 스탠드오프 데이터: 국역 *난중일기*·*일리아스*

국역 *난중일기*(노승석 역)와 *일리아스*(천병희 역, 이준석 역)를 원시 데이터로 삼아 만든 **스탠드오프(stand-off) 공개 데이터**입니다. 세 번역본은 모두 저작권 보호 대상이므로, 이 저장소에는 **번역문 본문이 한 문장도 들어 있지 않습니다**. 대신 위치 좌표, 연구자가 만든 주석과 요지, 정서 범주별 집계, 사전, 온톨로지, 코드를 공개합니다. 번역본을 가진 연구자는 좌표와 코드를 이용해 자신의 작업 코퍼스에서 같은 분석을 재현할 수 있습니다.

> 관련 발표문: 「고전 전쟁 서사 데이터 분석 방법 시론: 국역 *난중일기*·*일리아스* 원시 데이터의 정제에서 활용까지」(2026. 12. 5. 추계 연합학술대회 발표 글). 현재 판: **v0.1-pilot**(시범 구축, 교정 전).

## 구성

자료는 **원천 자료**(연구자가 손으로 만들고 관리)와 **파생 자료**(코드가 작업 코퍼스에서 생성)로 나뉩니다. 파생 자료는 모두 `code/export_standoff.py` 한 번으로 다시 만들어집니다.

| 폴더 | 내용 | 구분 | 라이선스 |
|---|---|---|---|
| `data/provenance/` | 출처 대장: 번역본 서지·저본·권리 범주 | 원천 | CC0 1.0 |
| `lexicon/` | 정서어 사전 v1·v2, 고유명사 표기 사전, 수식어구 패턴 (코드가 읽는 유일한 사전) | 원천 | CC BY 4.0 |
| `annotations/` | 1597년 주요 항목의 연구자 요지·예비 판정, 일치도 측정 표본 ID | 원천 | CC BY 4.0 |
| `ontology/` | RDF/OWL(Turtle) 온톨로지와 예시 인스턴스 | 원천 | CC BY 4.0 |
| `docs/` | 데이터 사전, 검증 계획, 주석 지침, 검증 질의 설명, 교정 기록 양식 | 원천 | CC BY 4.0 |
| `data/nanjung/` | 1,655개 항목 좌표 색인(지문 포함), 1597년 266항목 정서 범주 집계, 정유일기Ⅰ·Ⅱ 64일 정렬표 | 파생 | CC BY 4.0 |
| `data/iliad/` | 두 번역본의 권·행 → 쪽 좌표 색인, 권별 행수 대조, 18권 수식어구 행 | 파생 | CC BY 4.0 |
| `aggregates/` | 조건별 정서어 수·밀도, 월별·50행 구간 밀도, 편차 지표, 수식어구 유지율, 판독 불일치율, 붓스트랩 95% 구간, 온톨로지 검증 질의의 답, 실행 기록 | 파생 | CC BY 4.0 |
| `code/` | 내보내기·대조·일치도(α)·그림·데이터 패키지 스크립트 | — | MIT |
| `tests/`, `.github/` | 자동 검사 10종(붓스트랩 구간, ID·참조 무결성, 번역문 유출 의심, 체크섬, 발표문 수치, 주석–집계 일치, 사전 버전, 검증 질의 답, 온톨로지) | — | MIT |
| `datapackage.json`, `SHA256SUMS.txt` | 열 형식·설명(Frictionless Data Package), 파일 체크섬(저자명·주소를 적는 README·CITATION.cff·LICENSE·온톨로지 파일은 제외; 다시 만들기: `python code/update_checksums.py`) | 파생 | CC BY 4.0 |

## 발표문과의 대응
| 발표문(26쪽 판) | 저장소 파일 |
|---|---|
| <표 3> 고유명사 표기 사전 | `lexicon/proper_names.csv` |
| <표 4> 정서어 사전의 구조 | `lexicon/emotion_lexicon_v1.csv`, `v2.csv` |
| <표 5> 편차 지표의 기록 예 | `aggregates/witness_deviation_examples.csv` |
| <표 6> 1597년 주요 항목의 태깅 | `annotations/pilot_1597_key_entries.csv`, `data/nanjung/pilot_1597_records.csv` |
| <표 7> 조건별 정서어 수와 밀도 | `aggregates/conditions_table.csv` |
| <그림 1> (가) 1597년 월별 밀도 / (나) 18권 50행 구간 | `aggregates/monthly_density_1597.csv` / `aggregates/iliad18_bins50.csv` → `aggregates/fig1_emotion_density.png`(`code/make_figure.py`) |
| 정유일기Ⅰ·Ⅱ 64일 비교(3 대 7, 자카드 평균 0.22) | `data/nanjung/overlap_1597_I_II.csv` |
| 수식어구 행 11/19, 유지율 90.9% | `data/iliad/epithet_lines_book18.csv`, `aggregates/epithet_retention_book18.csv` |
| 두 판독 간 불일치율 2.3%·2.2%·8.3% | `aggregates/ocr_disagreement.csv` |
| Ⅲ장 3절 붓스트랩 95% 구간(1.31[1.03, 1.61], 차이 0.13[−0.02, 0.33] 등) | `aggregates/bootstrap_ci.csv` |
| Ⅳ장 5절 투고 전 검증 계획(α 50항목, CER 표본) | `docs/validation_plan.md`, `docs/annotation_guideline.md`, `annotations/agreement_sample_ids.csv`, `code/agreement.py` |
| Ⅲ장 2절 온톨로지 검증 질의의 답 | `aggregates/competency_questions.csv`, `docs/competency_questions.md` |

## 공개하지 않는 것
- 번역문 본문, 레코드별 표제어(어휘) 목록, 날씨 기록 문구, OCR 결과와 스캔 이미지

레코드별 표제어 목록은 번역문의 내용을 사실상 재구성할 수 있으므로 정서 **범주별 개수**만 공개합니다. 항목 대조용 지문(`simhash64`)은 본문 글자쌍의 해시를 합친 64비트 값으로, 본문을 복원할 수 없습니다.

## 재현과 대조
번역본을 가진 연구자는 다음 순서로 이 데이터를 자신의 판독본과 맞출 수 있습니다. 판독이 다르면 수치도 조금씩 달라지므로, 엄밀히는 '같은 결과의 재생산'이 아니라 '좌표에 맞춘 대조'입니다. 그 차이 자체가 판독·정제 조건의 차이를 보여 줍니다.

1. 번역본(서지는 `data/provenance/sources.csv`)을 연구 목적으로 텍스트화하여 작업 코퍼스(JSON)를 만듭니다. 형식은 `docs/data_dictionary.md`.
2. `pip install -r requirements.txt`
3. **항목 맞추기**: `python code/match_corpus.py <내 merged_nan.json>` → 날짜·권차로 레코드 ID를 찾고, 지문(SimHash)과 글자 수로 분할·병합·판독 차이를 걸러 `match_report.csv`를 만듭니다. 시험 삼아 다른 판독본으로 돌렸을 때 1,655개 중 1,567개(94.7%)가 자동으로 맞았고 88개가 확인 대상으로 걸렸습니다.
4. **파생 자료 다시 만들기**: `python code/export_standoff.py <작업 코퍼스 폴더> <출력 폴더>`
5. **검사**: `pytest -q tests`

작업 코퍼스 폴더(`corpus/`)와 대조 보고서는 `.gitignore`로 제외됩니다. **번역문이 든 파일을 커밋하지 마십시오.**

## 아직 비어 있거나 제한된 것 (v0.1-pilot)
| 항목 | 상태 | 계획 |
|---|---|---|
| *난중일기* 날짜별 저본(`base_text`) | 비어 있음 | 전체 구축에서 교주의 출처 표시를 옮겨 적음 |
| 정렬 유형(`alignment`, 항목 색인) | 비어 있음 | 전체 구축(정유일기Ⅰ·Ⅱ 64일은 `overlap_1597_I_II.csv`에 기입) |
| 이준석 역의 그리스어 통용 행 번호(`line_canonical`) | 행수가 원문과 다른 10개 권은 비어 있음 | 옥스퍼드판과 행별 대조 후 기입(이준석 역의 저본은 West 토이브너판). 권별 차이는 `data/iliad/line_count_by_book.csv` |
| 연구자 요지·예비 판정 | 1597년 8개 항목만 | 시범 범위 확대 시 추가 |
| 정서 태그의 주석자·확신도 | 시범 레코드는 자동 태깅(`auto-v1`)만 | v0.2: 50항목 2인 주석과 Krippendorff's α(`docs/validation_plan.md`) |
| 문자 오류율(CER) | 미측정(두 판독 간 불일치율만 공개) | v0.2: 1597년 20항목·18권 100행 표본으로 측정(`docs/validation_plan.md`) |

## 수치에 관한 주의
- 모든 수치는 **교정 전 이중 판독본**과 초기 정서어 사전(v1)에서 얻은 값입니다. 두 판독 간 한글 글자 불일치율은 *일리아스* 18권 2.2~2.3%, *난중일기* 1597년 항목별 중앙값 8.3%입니다(`aggregates/ocr_disagreement.csv`). 이는 문자 오류율(CER)이 아닙니다.
- 정서 집계는 자동 태깅 결과이며 오탐을 포함합니다(예: 인명 '안도', '닭이 울 때'). 확인된 오탐은 `overlap_1597_I_II.csv`의 note 열에 적었습니다.
- *일리아스*의 `IL-권-행-B` ID와 50행 구간은 **번역본에서 센 행 번호** 기준입니다. 이준석 역은 저본(West 토이브너판)과 행 배치의 차이로 10개 권에서 옥스퍼드판과 1–4행 차이가 있으므로(`line_count_by_book.csv`), A와 B를 행 단위로 맞댈 때는 장면 단위로 맞추십시오. 천병희 역은 옥스퍼드판(Monro·Allen, 1920)을 저본으로 24권 모두 원문 행수와 같아 `line_canonical`이 채워져 있습니다.
- `solar_date_kasi`는 한국천문연구원 역법 데이터를 쓰는 korean-lunar-calendar 패키지의 변환값입니다. 역사 문헌의 양력 표기와 하루 차이가 날 수 있습니다(예: 명량해전 음력 9월 16일 → 1597-10-25).
- 붓스트랩 구간(`aggregates/bootstrap_ci.csv`)은 이웃한 10행 블록·날짜가 서로 독립이라는 가정 아래의 값이어서 실제 불확실성은 더 클 수 있습니다. 정유일기 비교는 재표집 일부에서 Ⅰ의 정서어가 0개가 되어 상한이 정의되지 않습니다(`∞`, `share_undefined` 열).
- 실행에 쓴 소프트웨어 버전과 사전 해시값은 `aggregates/run_metadata.json`에 기록됩니다.
- CSV는 엑셀에서 한글이 깨지지 않도록 BOM이 있는 UTF-8(`utf-8-sig`)로 저장했습니다. pandas에서는 `encoding="utf-8-sig"`로 읽으십시오.

## 판 관리와 인용
- 데이터가 바뀔 때마다 릴리스 태그로 판을 고정합니다(예: `v0.1-pilot`, `v1.0`). 논문에는 태그를 함께 적어 주십시오.
- 장기 보존과 DOI는 데이터를 인용하는 논문 게재, 과제 1단계 종료, 연구 종료 시점에 Zenodo로 연결합니다.
- 인용 정보는 `CITATION.cff`를 참고하십시오.

## 연구 지원
2025년 교육부·한국연구재단 인문사회분야 학술연구교수(A유형) 과제 「고전 전쟁 서사 데이터 분석 및 글로컬 콘텐츠 개발」의 1단계 성과입니다.

---
**English summary.** Stand-off data for Korean translations of *Nanjungilgi* and the *Iliad*. Because all three translations are under copyright, no translated text is included: only coordinates (date / book-line → page), researcher annotations, category-level emotion counts, lexicons, an RDF ontology and code. Researchers who own the translations can align their own OCR to the public record IDs (`code/match_corpus.py`) and regenerate every derived file (`code/export_standoff.py`). Data: CC BY 4.0; provenance ledger: CC0; code: MIT. Figures are from an uncorrected double-OCR pilot (v0.1-pilot).
