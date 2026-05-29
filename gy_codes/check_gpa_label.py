"""
GPA 만점 변수 찾기 — 평점 주변 변수들의 라벨 확인
목적: KEEP1 GPA(F6Y02087)의 만점 기준 변수를 찾아 정규화에 사용
"""
import pyreadstat

BASE = '/Users/ruddbs/Desktop/teamproj/'
df_k1, meta1 = pyreadstat.read_sas7bdat(BASE + 'f6_h_youth.sas7bdat')
df_k2, meta2 = pyreadstat.read_sav(BASE + 'KEEP2 8차년도 데이터.SAV')

print("=" * 60)
print("[KEEP1] 평점(F6Y02087) 주변 변수 라벨")
print("=" * 60)
for v in ['F6Y02085', 'F6Y02086', 'F6Y02087', 'F6Y02088', 'F6Y02089']:
    print(f"  {v} → {meta1.column_names_to_labels.get(v)}")

print("\n" + "=" * 60)
print("[KEEP2] 평점(Y24SB11002) 주변 변수 라벨")
print("=" * 60)
for v in ['Y24SB11001', 'Y24SB11002', 'Y24SB11003', 'Y24SB11004']:
    print(f"  {v} → {meta2.column_names_to_labels.get(v)}")

# 만점 후보 변수의 값 분포도 같이 확인 (4.0/4.3/4.5 같은 값이 나오면 그게 만점)
print("\n" + "=" * 60)
print("[참고] 만점 후보 변수 값 분포 (4.0/4.3/4.5 보이면 만점 변수!)")
print("=" * 60)
print("KEEP1 F6Y02086:", df_k1['F6Y02086'].value_counts().sort_index().head(10).to_dict())
print("KEEP1 F6Y02088:", df_k1['F6Y02088'].value_counts().sort_index().head(10).to_dict())
print("KEEP2 Y24SB11003:", df_k2['Y24SB11003'].value_counts().sort_index().head(10).to_dict())
