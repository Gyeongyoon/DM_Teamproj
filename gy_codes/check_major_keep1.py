"""
KEEP1 전공 계열 변수(F6Y01004c) 3자리 코드 분포 + 메타데이터 확인
- 목적: 3자리 세분 코드를 7개 대분류로 매핑하기 위한 규칙 파악
"""
import pyreadstat

# ===== 경로 (본인 PC 기준) =====
PATH_K1 = '/Users/ruddbs/Desktop/teamproj/f6_h_youth.sas7bdat'

df_k1, meta = pyreadstat.read_sas7bdat(PATH_K1)

VAR = 'F6Y01004c'

print("=" * 70)
print(f"📌 {VAR} 코드값 분포 (결측 -5 등 음수 제외)")
print("=" * 70)
vc = df_k1[VAR][df_k1[VAR] >= 0].value_counts().sort_index()
print(vc.to_string())
print(f"\n유효 응답 합계: {int(vc.sum())}명")

print("\n" + "=" * 70)
print("📌 변수 라벨 (column label)")
print("=" * 70)
print(meta.column_names_to_labels.get(VAR))

print("\n" + "=" * 70)
print("📌 값 라벨 (value labels) — 매핑 규칙 힌트")
print("=" * 70)
val_labels = meta.variable_value_labels.get(VAR)
if val_labels:
    for k, v in sorted(val_labels.items()):
        print(f"  {k} = {v}")
else:
    print("  (값 라벨 없음 → 코드북 PDF로 수동 매핑 필요)")
