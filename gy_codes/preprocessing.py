"""
데이터마이닝 기말 프로젝트 — 전처리 (v6 FINAL)
KEEP2 8차(2024) + KEEP1 7차 고3코호트(2010)
출력: 분석용 통합 데이터셋 2개 (df_k2_clean, df_k1_clean) + CSV
"""
import pandas as pd
import numpy as np
import pyreadstat

# ============================================================
# 경로 (본인 PC 기준 — 필요시 수정)
# ============================================================
BASE = '/Users/ruddbs/Desktop/DM_Teamproj/origin_data/'
PATH_K2 = BASE + 'KEEP2 8차년도 데이터.SAV'
PATH_K1 = BASE + 'f6_h_youth.sas7bdat'
OUT_K2  = BASE + 'output/keep2_clean.csv'
OUT_K1  = BASE + 'output/keep1_clean.csv'

MISSING_CODES = [-9, -6, -5, -4, -3, -2, 99, 999, 9999]
MAJOR_NAMES = {1:'인문', 2:'사회', 3:'교육', 4:'공학',
               5:'자연', 6:'의약', 7:'예체능'}

# ============================================================
# Step 1. 로드
# ============================================================
print("[1] 데이터 로드")
df_k2, _ = pyreadstat.read_sav(PATH_K2)
df_k1, _ = pyreadstat.read_sas7bdat(PATH_K1)
print(f"    KEEP2 원본: {len(df_k2)}  / KEEP1 원본: {len(df_k1)}")


# ============================================================
# Step 2. 임금근로자 필터링 (종사상 지위 1·2·3 & 소득 존재)
#   KEEP2: 지위 Y24SH02012 / 소득 Y24SH02039
#   KEEP1: 지위 F6Y05011   / 소득 F6Y05029
# ============================================================
print("[2] 임금근로자 필터링")
df_k2 = df_k2[df_k2['Y24SH02012'].isin([1, 2, 3])].copy()
df_k2 = df_k2[df_k2['Y24SH02039'] > 0].copy()

df_k1 = df_k1[df_k1['F6Y05011'].isin([1, 2, 3])].copy()
df_k1 = df_k1[df_k1['F6Y05029'] > 0].copy()
print(f"    KEEP2: {len(df_k2)}  / KEEP1: {len(df_k1)}")


# ============================================================
# Step 3. 결측치 처리 (음수 결측코드 → NaN)
# ============================================================
print("[3] 결측치 처리")
df_k2 = df_k2.replace(MISSING_CODES, np.nan)
df_k1 = df_k1.replace(MISSING_CODES, np.nan)


# ============================================================
# Step 4. 전공 계열 → 7개 대분류
#   KEEP2: Y24SB02003C_1 (이미 01~07, object) → int
#   KEEP1: F6Y01004c (3자리) → 백의 자리 (// 100)
# ============================================================
print("[4] 전공 계열 인코딩")
df_k2['major'] = pd.to_numeric(df_k2['Y24SB02003C_1'], errors='coerce')
df_k2.loc[~df_k2['major'].isin(range(1, 8)), 'major'] = np.nan

df_k1['major'] = (df_k1['F6Y01004c'] // 100)
df_k1.loc[~df_k1['major'].isin(range(1, 8)), 'major'] = np.nan  # 999 등 제거

df_k2['major_name'] = df_k2['major'].map(MAJOR_NAMES)
df_k1['major_name'] = df_k1['major'].map(MAJOR_NAMES)


# ============================================================
# Step 5. Y 변수 이진화 (패널별 중위소득 기준!)
# ============================================================
print("[5] Y 변수 이진화")
def build_y(df, inc, sat, reg, reg_pos):
    med = df[inc].median()
    df['high_income']        = (df[inc] >= med).astype(int)
    df['high_satisfaction']  = (df[sat] >= 4).astype(int)
    df['regular_employment'] = df[reg].isin(reg_pos).astype(int)
    return df

df_k2 = build_y(df_k2, 'Y24SH02039', 'Y24SH02058', 'Y24SH02014', [1, 2])
df_k1 = build_y(df_k1, 'F6Y05029',  'F6Y05050',  'F6Y05013',  [1])


# ============================================================
# Step 6. 기타 X 변수
# ============================================================
print("[6] X 변수 정리")
def build_x(df, gpa, gpa_max, cert, eng, gender):
    # GPA 정규화 (그대로 유지)
    raw, mx = df[gpa].copy(), df[gpa_max].copy()
    mx = mx.where(((mx >= 3.0) & (mx <= 4.5)) | (mx == 100), np.nan)
    ratio = raw / mx
    ratio = ratio.where((ratio > 0) & (ratio <= 1.0), np.nan)
    df['gpa'] = (ratio * 4.5).round(3)
    
    df['cert_count'] = df[cert].fillna(0)
    
    # ✅ 수정: 양수만 응시자로 처리
    eng_numeric = pd.to_numeric(df[eng], errors='coerce')
    df['english_test_taken'] = (eng_numeric > 0).astype(int)
    
    df['gender'] = df[gender]
    return df

df_k2 = build_x(df_k2, 'Y24SB11002', 'Y24SB11003', 'Y24SF01002', 'Y24SE01021', 'GENDER')
df_k1 = build_x(df_k1, 'F6Y02087',  'F6Y02088',  'F6Y10098',  'F6Y10016',  'GENDER')


# ============================================================
# Step 7. 분석용 컬럼만 추출 + 더미화
# ============================================================
print("[7] 분석용 셋 구성")
KEEP_COLS = ['major', 'major_name', 'gpa', 'cert_count', 'english_test_taken',
             'gender', 'high_income', 'high_satisfaction', 'regular_employment']

df_k2_clean = df_k2[KEEP_COLS].copy()
df_k1_clean = df_k1[KEEP_COLS].copy()
df_k2_clean['cohort'] = 2024
df_k1_clean['cohort'] = 2010

print(f"    KEEP2 최종: {len(df_k2_clean)}  (전공 결측 {df_k2_clean['major'].isna().sum()})")
print(f"    KEEP1 최종: {len(df_k1_clean)}  (전공 결측 {df_k1_clean['major'].isna().sum()})")
print(f"    [GPA 정규화] KEEP2 유효 {df_k2_clean['gpa'].notna().sum()}명 "
      f"(min {df_k2_clean['gpa'].min():.2f}~max {df_k2_clean['gpa'].max():.2f}) / "
      f"KEEP1 유효 {df_k1_clean['gpa'].notna().sum()}명 "
      f"(min {df_k1_clean['gpa'].min():.2f}~max {df_k1_clean['gpa'].max():.2f})")


# ============================================================
# Step 8. 저장
# ============================================================
import os
os.makedirs(BASE + 'output', exist_ok=True)
df_k2_clean.to_csv(OUT_K2, index=False, encoding='utf-8-sig')
df_k1_clean.to_csv(OUT_K1, index=False, encoding='utf-8-sig')
print("[8] 저장 완료 →", OUT_K2, "/", OUT_K1)

# 전공 분포 확인
print("\n[전공 분포 비교]")
print(pd.concat([
    df_k2_clean['major_name'].value_counts().rename('2024'),
    df_k1_clean['major_name'].value_counts().rename('2010'),
], axis=1))
