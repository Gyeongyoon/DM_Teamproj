# 대학 선택이 졸업 후 직장 성취에 미치는 영향: 2010 vs 2024

2026년 1학기 데이터마이닝 기말 팀 프로젝트. 한국교육고용패널(KEEP) 데이터로 대학 시절 선택(전공, 학점, 스펙)이 졸업 후 직장 성취에 미치는 영향을 분석하고, 2010년과 2024년 두 시대를 비교함.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

## 연구 질문

대학 시절 선택(전공 계열, 학점, 스펙)이 졸업 후 직장 성취도에 미치는 영향력은 어느 정도이며, 이는 시대(2010 vs 2024)에 따라 어떻게 변했는가?

| 가설 | 내용 | 결과 |
|---|---|---|
| H1 | 전공 계열이 직장 성취에 영향을 준다 | 지지 |
| H2 | 개인 스펙(자격증, 영어)이 직장 성취에 영향을 준다 | 기각 |
| H3 | 각 요인의 영향력은 시대에 따라 변했다 | 경향은 뚜렷하나 통계적 확정은 일부 |

## 데이터

| 패널 | 조사 연도 | 대상 | 임금근로자 | 전공 응답자 |
|---|---|---|---|---|
| KEEP2 8차년도 | 2024 | 만 24세 전후 | 970명 | 766명 |
| KEEP1 7차년도 고3 코호트 | 2010 | 만 24세 전후 | 1,061명 | 235명 |

> 원본 데이터는 KEEP 이용 약관에 따라 레포에 포함하지 않음. `origin_data/`에 직접 내려받아 넣어야 함.

### 분석 변수

| 구분 | 컬럼 | 의미 |
|---|---|---|
| X | `major` / `major_name` | 전공 대분류 (1 인문, 2 사회, 3 교육, 4 공학, 5 자연, 6 의약, 7 예체능) |
| X | `gpa` | 졸업 평점 (4.5 만점으로 정규화) |
| X | `cert_count` | 자격증 개수 |
| X | `english_test_taken` | 영어시험 응시 여부 (0/1) |
| X | `gender` | 성별 (1 남, 2 여) |
| Y | `high_income` | 고소득 여부 (패널별 중위소득 이상 = 1) |
| Y | `high_satisfaction` | 직장 만족 여부 (4점 이상 = 1) |
| Y | `regular_employment` | 정규직 여부 (0/1) |
| - | `cohort` | 조사 연도 (2010 / 2024) |

---

## 분석 과정

### 1. 전처리 (`gy_codes/preprocessing.py`)

- 종사상 지위와 소득으로 **임금근로자만 필터링**함
- 음수 결측 코드(-9, -6 등)를 `NaN`으로 변환함
- 응답률이 1~3%에 불과했던 전공 변수 대신 KEEP 통합 변수(`Y24SB02003C_1`)를 찾아 **전공 응답자 5,960명을 확보**함
- 두 패널의 서로 다른 전공 코드를 **7개 대분류로 통일**함
- 학교마다 만점이 다른 학점을 **4.5 만점 기준으로 정규화**함
- 소득, 만족도, 고용 형태를 이진 변수로 변환함. 소득은 시대별 물가 차이를 고려해 **패널별 중위소득**을 기준으로 삼음
- KEEP1 ↔ KEEP2 변수 대응 관계를 `variable_mapping_FINAL.xlsx`로 정리함

### 2. 모델링 (`modeling_final.ipynb`)

- **분류 모델 4종 비교**: Logistic Regression, Decision Tree, KNN, Naive Bayes를 5-fold 교차검증으로 평가함
- **평가 지표**: 정규직 비율이 75%로 불균형하여 정확도 대신 **ROC-AUC를 주 지표**로 사용함. 혼동행렬, 임계값 조정, 하이퍼파라미터 튜닝(KNN k, 트리 깊이)도 함께 검토함
- **변수 중요도**: 로지스틱 계수와 트리 중요도를 교차 비교하고, statsmodels로 p값과 신뢰구간을 확인함
- **시대 비교**: 전공 × 시대 상호작용 항으로 2010 → 2024 변화의 유의성을 검정함
- **비지도 분석**: PCA, K-means로 성취 유형과 대학 선택 유형을 군집화함
- **심화 분석**: 전공 × 자격증 상호작용, 성별 분리 분석, 예측 실패 사례 분석, 학습곡선

---

## 주요 결과

**1. 전공이 스펙보다 결정적임**
- 고소득에 통계적으로 유의한 변수는 전공뿐임: 공학(+), 자연(+), 예체능(−)
- 자격증, 영어시험 응시는 유의하지 않음 (p > 0.05)

**2. 성취 종류마다 결정 구조가 다름**
- 고소득: 전공이 단독으로 결정함
- 정규직: 전공, 성별, 영어가 함께 작용함
- 만족도: 어떤 대학 변수로도 설명되지 않음 (AUC 0.47)

**3. 이공계 프리미엄이 커지는 경향**
- 고소득에 대한 공학 계수가 2010년 +0.14에서 2024년 +0.39로 약 3배 증가함
- 다만 통계적으로 유의한 변화는 자연계열의 정규직 효과(p = 0.043) 하나뿐임. KEEP1 표본(235명)이 작아 검정력에 한계가 있음

**4. 대학 변수의 설명력에는 한계가 있음**
- 모든 모델에서 AUC 0.6대에 머무르며, 학습곡선상 데이터를 늘려도 0.62 부근에서 정체함
- 대학 선택은 성취의 출발점을 정하지만, 나머지는 직무, 산업, 회사 규모 같은 졸업 후 요인이 결정함

---

## 폴더 구조

```
DM_Teamproj/
├── README.md
├── variable_mapping_FINAL.xlsx     # KEEP1 ↔ KEEP2 변수 매핑표
├── modeling.ipynb                  # 모델링 초안
├── modeling_final.ipynb            # 최종 모델링 및 분석
│
├── origin_data/                    # 원본 데이터 (git 미포함)
│   ├── f6_h_youth.sas7bdat          # KEEP1 7차 고3 코호트
│   └── KEEP2 8차년도 데이터.SAV
│
├── clean_data/                     # 전처리 완료 데이터 (분석 시작점)
│   ├── keep1_clean.csv
│   └── keep2_clean.csv
│
├── gy_codes/                       # 전처리 코드
│   ├── preprocessing.py             # 전처리 메인
│   ├── data_inspect.py              # 데이터 탐색
│   ├── check_values.py              # 응답값 검증
│   ├── check_gpa_label.py           # GPA 만점 변수 검증
│   ├── check_major_keep1.py         # KEEP1 전공 코드 검증
│   └── diagnose.py                  # 진단용 스크립트
│
└── gy_output/                      # 전처리 중간 결과물
    ├── keep1_variables.xlsx         # KEEP1 변수 전체 목록
    ├── keep2_variables.xlsx         # KEEP2 변수 전체 목록
    ├── keep1_summary.txt
    ├── keep2_summary.txt
    └── value_comparison.txt         # 패널 간 응답값 비교
```

## 실행 방법

```bash
pip install pandas numpy pyreadstat scikit-learn statsmodels matplotlib jupyter
```

- 분석만 재현하려면 `clean_data/`의 CSV를 그대로 쓰고 `modeling_final.ipynb`를 실행하면 됨
- 전처리부터 재현하려면 원본 데이터를 `origin_data/`에 넣고 `preprocessing.py` 상단의 `BASE` 경로를 수정한 뒤 실행하면 됨

## 역할 분담

| 팀원 | 담당 |
|---|---|
| 경윤 ([@Gyeongyoon](https://github.com/Gyeongyoon)) | 데이터 탐색, 변수 매핑, 전처리 |
| 시현 | 분류 모델링 및 분석 |
| 성빈 | 시각화 및 발표 자료 |
