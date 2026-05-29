"""
전처리 결측 원인 진단
- KEEP1 전공 결측 78%, GPA 결측 82% 가 '응답 없음'인지 '필터 오류'인지 구분
"""
import pyreadstat
import numpy as np

BASE = '/Users/ruddbs/Desktop/teamproj/'
df_k2, _ = pyreadstat.read_sav(BASE + 'KEEP2 8차년도 데이터.SAV')
df_k1, _ = pyreadstat.read_sas7bdat(BASE + 'f6_h_youth.sas7bdat')

# 임금근로자 필터만 적용 (결측 replace 전 = 원본 상태)
k2 = df_k2[df_k2['Y24SH02012'].isin([1,2,3]) & (df_k2['Y24SH02039']>0)].copy()
k1 = df_k1[df_k1['F6Y05011'].isin([1,2,3]) & (df_k1['F6Y05029']>0)].copy()
print(f"임금근로자 필터 후 → KEEP2 {len(k2)} / KEEP1 {len(k1)}\n")

print("="*60); print("① 전공 변수 원본 상태 (replace/매핑 전)"); print("="*60)
print("[KEEP2 Y24SB02003C_1] 값 분포 (원본 그대로):")
print(k2['Y24SB02003C_1'].value_counts(dropna=False).sort_index().to_string())
print("\n[KEEP1 F6Y01004c] 음수(결측코드) 비율:", round((k1['F6Y01004c']<0).mean(),3))
print("[KEEP1 F6Y01004c] 값 분포:")
print(k1['F6Y01004c'].value_counts(dropna=False).sort_index().head(45).to_string())

print("\n"+"="*60); print("② GPA 변수 원본 상태 (★ 결측의 진짜 원인)"); print("="*60)
print("[KEEP2 Y24SB11002] describe:"); print(k2['Y24SB11002'].describe().to_string())
print("  NaN 비율(원본):", round(k2['Y24SB11002'].isna().mean(),3))
print("  0~4.5 범위 밖(잘릴 값) 비율:",
      round(((k2['Y24SB11002']<=0)|(k2['Y24SB11002']>4.5)).mean(),3))
print("  >4.5 인 값들 상위:", sorted(k2['Y24SB11002'][k2['Y24SB11002']>4.5].dropna().unique())[:15])

print("\n[KEEP1 F6Y02087] describe:"); print(k1['F6Y02087'].describe().to_string())
print("  NaN 비율(원본):", round(k1['F6Y02087'].isna().mean(),3))
print("  0~4.5 범위 밖(잘릴 값) 비율:",
      round(((k1['F6Y02087']<=0)|(k1['F6Y02087']>4.5)).mean(),3))
print("  >4.5 인 값들 상위:", sorted(k1['F6Y02087'][k1['F6Y02087']>4.5].dropna().unique())[:15])

print("\n"+"="*60); print("③ GPA 만점 변수가 따로 있는지 확인"); print("="*60)
# 만점 변수 후보 탐색
for df,name,key in [(k2,'KEEP2','Y24SB1100'),(k1,'KEEP1','F6Y0208')]:
    cands = [c for c in df.columns if c.startswith(key)]
    print(f"[{name}] {key}* 컬럼:", cands)
