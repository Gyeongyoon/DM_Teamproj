"""
KEEP1 7차 / KEEP2 8차 데이터 검사 스크립트
============================================
사용법:
    cd /Users/ruddbs/teamproj
    python3 data_inspect.py

결과:
    ./output/ 폴더에 4개 파일 생성
"""

import pyreadstat
import pandas as pd
from pathlib import Path

# ============================================
# 경로 설정
# ============================================
BASE_DIR = "/Users/ruddbs/Desktop/teamproj"

# KEEP1 7차 — 고3 코호트 (만 24세) ⭐
KEEP1_SAV = f"{BASE_DIR}/f6_h_youth.sas7bdat"

# KEEP2 8차
KEEP2_SAV = f"{BASE_DIR}/KEEP2 8차년도 데이터.SAV"

# 출력 폴더
OUTPUT_DIR = Path(BASE_DIR) / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def inspect_data(filepath, label):
    """sav/sas7bdat 파일 검사하고 변수 리스트 추출"""
    print(f"\n{'='*60}")
    print(f"  {label} 데이터 검사 중...")
    print(f"  파일: {filepath}")
    print(f"{'='*60}")

    if filepath.lower().endswith('.sas7bdat'):
        df, meta = pyreadstat.read_sas7bdat(filepath)
    elif filepath.lower().endswith('.sav'):
        df, meta = pyreadstat.read_sav(filepath, apply_value_formats=False)
    else:
        raise ValueError(f"지원 안 하는 형식: {filepath}")

    n_rows, n_cols = df.shape
    print(f"  ✓ 응답자 수: {n_rows:,}명")
    print(f"  ✓ 변수 개수: {n_cols:,}개")

    var_list = []
    for var_name in df.columns:
        var_label = meta.column_names_to_labels.get(var_name, '')
        value_labels = meta.variable_value_labels.get(var_name, {})
        value_label_str = "; ".join([f"{k}={v}" for k, v in value_labels.items()])
        dtype = str(df[var_name].dtype)
        missing_pct = df[var_name].isna().mean() * 100

        var_list.append({
            "변수명": var_name,
            "변수설명": var_label,
            "타입": dtype,
            "결측치%": round(missing_pct, 1),
            "응답값_라벨": value_label_str[:200],
            "응답_고유값_수": df[var_name].nunique()
        })

    var_df = pd.DataFrame(var_list)

    output_path = OUTPUT_DIR / f"{label.lower()}_variables.xlsx"
    var_df.to_excel(output_path, index=False)
    print(f"  ✓ 변수 리스트 저장: {output_path}")

    summary_path = OUTPUT_DIR / f"{label.lower()}_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"{label} 데이터 요약\n")
        f.write(f"{'='*40}\n\n")
        f.write(f"파일: {filepath}\n")
        f.write(f"응답자 수: {n_rows:,}명\n")
        f.write(f"변수 개수: {n_cols:,}개\n\n")
        f.write(f"결측치 50% 이상: {(var_df['결측치%'] >= 50).sum()}개\n")
        f.write(f"결측치 0%: {(var_df['결측치%'] == 0).sum()}개\n\n")
        f.write("처음 30개 변수:\n")
        f.write("-" * 60 + "\n")
        for _, row in var_df.head(30).iterrows():
            f.write(f"  {row['변수명']}: {row['변수설명']}\n")

    print(f"  ✓ 요약 저장: {summary_path}")
    return var_df


def find_key_variables(var_df, keywords, label):
    """키워드로 변수 검색"""
    print(f"\n--- 🔍 {label}: 키워드 검색 결과 ---")
    for keyword in keywords:
        matches = var_df[
            var_df["변수설명"].fillna("").str.contains(keyword, case=False)
        ]
        if len(matches) > 0:
            print(f"\n  [{keyword}] ({len(matches)}개):")
            for _, row in matches.head(8).iterrows():
                desc = str(row['변수설명'])[:60]
                print(f"    {row['변수명']}: {desc}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  KEEP 데이터 검사 시작")
    print("="*60)

    keywords = [
        "전공", "일치", "소득", "임금", "급여",
        "만족", "직무", "정규", "종사상",
        "학점", "평점", "졸업",
        "자격증", "외국어", "영어",
        "부모", "아버지", "어머니",
    ]

    try:
        keep1_var_df = inspect_data(KEEP1_SAV, "KEEP1")
        find_key_variables(keep1_var_df, keywords, "KEEP1")
    except FileNotFoundError as e:
        print(f"\n❌ KEEP1 파일 못 찾음: {KEEP1_SAV}")
    except Exception as e:
        print(f"\n❌ KEEP1 에러: {e}")

    try:
        keep2_var_df = inspect_data(KEEP2_SAV, "KEEP2")
        find_key_variables(keep2_var_df, keywords, "KEEP2")
    except FileNotFoundError as e:
        print(f"\n❌ KEEP2 파일 못 찾음: {KEEP2_SAV}")
    except Exception as e:
        print(f"\n❌ KEEP2 에러: {e}")

    print("\n" + "="*60)
    print("  ✅ 완료!")
    print(f"  📁 결과 위치: {OUTPUT_DIR.absolute()}")
    print("="*60)
    print("\n📤 다음 단계:")
    print("  1. ./output/ 폴더의 4개 파일 확인")
    print("  2. GitHub에 업로드")
    print("  3. 카톡방에 완료 알림")