# DM_Teamproj

데이터마이닝 기말 프로젝트 — KEEP 패널 데이터 기반 시대 비교 분석

## 프로젝트 개요

**연구 질문**: 대학 시절 선택(전공 계열, 학점, 스펙)이 졸업 후 직장 성취도에 미치는 영향력은 어느 정도이며, 이는 시대(2010 vs 2024)에 따라 어떻게 변했는가?

**사용 데이터**:
- KEEP2 8차년도 (2024, 만 24세 전후 임금근로자)
- KEEP1 7차년도 고3 코호트 (2010, 만 24세 전후 임금근로자)

**발표일**: 2026년 6월 17일

**팀원**: 경윤 · 시현 · 성빈

## 폴더 구조

```
DM_Teamproj/
├── README.md
├── variable_mapping_FINAL.xlsx     # KEEP1 ↔ KEEP2 변수 매핑표
│
├── origin_data/                    # 원본 데이터 (수정 금지)
│   ├── f6_h_youth.sas7bdat          # KEEP1 7차 고3 코호트
│   └── KEEP2 8차년도 데이터.SAV
│
├── clean_data/                     # 전처리 완료 데이터 (분석 시작점)
│   ├── keep1_clean.csv              # 1,061명
│   └── keep2_clean.csv              # 970명
│
├── gy_codes/                       # 경윤 작업 코드
│   ├── preprocessing.py             # 전처리 핵심 파일
│   ├── data_inspect.py              # 데이터 탐색
│   ├── check_values.py              # 응답값 검증
│   ├── check_gpa_label.py           # GPA 만점 변수 검증
│   ├── check_major_keep1.py         # KEEP1 전공 코드 검증
│   └── diagnose.py                  # 진단용 스크립트
│
└── gy_output/                      # 경윤 작업 중간 결과물
    ├── keep1_variables.xlsx         # KEEP1 변수 전체 리스트
    ├── keep2_variables.xlsx         # KEEP2 변수 전체 리스트
    ├── keep1_summary.txt            # KEEP1 데이터 요약
    ├── keep2_summary.txt            # KEEP2 데이터 요약
    └── value_comparison.txt         # 응답값 비교 결과
```

## 사용 가이드

**분석을 시작하려면**: `clean_data/` 안의 두 CSV 파일을 바로 쓰면 됨

**전처리 과정이 궁금하면**: `gy_codes/preprocessing.py` 참고

**중간 검증 결과가 궁금하면**: `gy_output/` 폴더 확인

**변수 매핑 정보가 필요하면**: `variable_mapping_FINAL.xlsx` 참고

## 분석 변수 (clean_data 기준)

| 컬럼 | 의미 | 값 |
|---|---|---|
| `major` | 전공 대분류 코드 | 1~7 (1인문·2사회·3교육·4공학·5자연·6의약·7예체능) |
| `major_name` | 전공 이름 | 텍스트 |
| `gpa` | 졸업 평점 | 0~4.5 (4.5 만점 정규화) |
| `cert_count` | 자격증 개수 | 0 이상 |
| `english_test_taken` | 영어시험 응시 여부 | 0/1 |
| `gender` | 성별 | 1(남) / 2(여) |
| `high_income` | 고소득 여부 | 0/1 (패널별 중위소득 기준) |
| `high_satisfaction` | 직장 만족 여부 | 0/1 (4점 이상 = 1) |
| `regular_employment` | 정규직 여부 | 0/1 |
| `cohort` | 조사 연도 | 2024 / 2010 |

## 진행 상황

- [x] Week 1 (5/26~6/1) — 데이터 전처리 (경윤)
- [ ] Week 2 (6/2~6/8) — 분류 모델링 (시현)
- [ ] Week 3 (6/9~6/15) — 시각화 및 발표 자료 (성빈)
- [ ] 6/16 리허설
- [ ] 6/17 발표

## 작업 환경

- 코드: Python 3.x (pandas, pyreadstat, scikit-learn)