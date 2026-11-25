# 데이터 사전

## 레코드 ID
- *난중일기*: `NJ-연도-월일[-증언]-순번`. 윤달은 월 앞에 `L`을 붙인다(예: `NJ-1594-L0801-01`). 증언은 정유일기Ⅰ·Ⅱ에만 ASCII `I`/`II`를 붙인다(예: `NJ-1597-1014-II-01`). 사람이 읽는 라벨(Ⅰ/Ⅱ)은 `witness_label` 열에 둔다. ID는 ASCII 영문·숫자·하이픈만 쓴다(URI·파일명 호환).
- *일리아스*: `IL-권-행-번역본`(예: `IL-18-022-A`). A = 천병희 역, B = 이준석 역. 행은 **번역본에서 센 행 번호**(`line_in_translation`). 그리스어 통용 번호는 `line_canonical`(권별 행수가 원문과 같을 때만 기입).

## data/nanjung/entries_index.csv
| 열 | 내용 |
|---|---|
| record_id | 레코드 ID |
| source_id | 출처 대장의 ID |
| witness_label | 증언 라벨(Ⅰ/Ⅱ, 정유일기만) |
| hangul_chars | 항목 본문 한글 글자 수(대조용) |
| simhash64 | 항목 본문 SimHash 지문(대조용, 본문 복원 불가) |
| section | 원문 권차(임진일기…무술일기, 정유일기Ⅰ·Ⅱ) |
| year_lunar, year_ganzhi, leap, month, day | 음력 날짜(윤달은 leap=윤) |
| day_ganzhi, day_ganzhi_hanja | 일진(60갑자). 번역본 표기와 역산값을 대조해 확정 |
| solar_date_kasi | 양력 환산(ISO 8601, KASI 역법 기준) |
| book_page / scan_page | 번역본 쪽 / 스캔 파일 쪽 |
| ocr_reading | 이중 판독 결과(일치 / 한쪽만 / 앞 날짜에서 분리) |
| base_text | 날짜별 저본(초고본·일기초·전서본). 전체 구축에서 기입 |
| alignment | 정렬 유형(일치·분할·병합·단독 수록). 전체 구축에서 기입 |

## data/nanjung/pilot_1597_records.csv
1597년 정유일기Ⅰ(4.1–10.8) + 정유일기Ⅱ의 10.9 이후 기록 = 266항목.
- eojeol_body: 날씨 기록과 역자 층(괄호 보충어·역주 번호)을 뺀 본문 층 어절 수
- eojeol_with_weather: 날씨 기록을 포함한 어절 수
- translator_layer_marks: 괄호 보충어·역주 표지 수(역자 층)
- annotator / confidence: 자동 태깅은 `auto-v1`, 확신도는 연구자 검토 후 기입
- v1_상실…v1_해소, v1_total: 정서어 사전 v1의 범주별 개수(Kiwi 표제어화)
- v2_불안, v2_total: 사전 v2(불안 범주 추가)
- v1_density_per100: 100어절당 정서어 수

## data/nanjung/overlap_1597_I_II.csv
정유일기Ⅰ·Ⅱ가 모두 확인되는 64일. jaccard_lemmas는 두 기록의 표제어 집합 자카드 계수(날짜 표기 제외, 날씨 기록 포함 — 발표문과 같은 기준). 정서어 수·밀도는 날씨 기록과 역자 층을 뺀 본문 층 기준. note에 확인된 오탐·행위자 문제를 적는다.

## data/iliad/line_index_*.csv
권·행(`line_in_translation`)마다 번역본 쪽(book_page)과 스캔 쪽(scan_page), 그리스어 통용 행(`line_canonical`). 천병희 역은 24권 모두 그리스어 원문 행수와 일치(15,693행). 이준석 역은 10개 권에서 1–4행 차이(15,688행).

## 작업 코퍼스(비공개) 형식
- `merged_nan.json`: `{"rows":[{"sec","year","gy","mon","leap","day","gz","gzh","wx","A","B","pdf","bp","src"}...]}` — A/B는 두 판독의 항목 본문
- `merged_cheon.json`, `merged_lee.json`: `{"rows":[[권,행,본문,대안 판독,판독 출처,일치 여부,표지,스캔 쪽,책 쪽],...]}`

## 원천 자료와 파생 자료
- 원천(손으로 관리): `lexicon/`, `annotations/`, `data/provenance/`, `ontology/`, `docs/`
- 파생(코드 생성): `data/nanjung/`, `data/iliad/`, `aggregates/`, `datapackage.json`, `SHA256SUMS.txt`
- 열 형식과 설명 전체는 `datapackage.json`에 있다.
