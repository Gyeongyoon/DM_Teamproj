"""
변수 응답값 검증 스크립트 (v2 — 타입 문제 수정)
============================================
KEEP1과 KEEP2의 핵심 변수들이 같은 척도·코딩을 쓰는지 검증.

사용법:
    cd /Users/ruddbs/teamproj
    python3 check_values.py
"""

import pyreadstat
import pandas as pd
from pathlib import Path

BASE_DIR = "/Users/ruddbs/Desktop/teamproj"
KEEP1_SAV = f"{BASE_DIR}/f6_h_youth.sas7bdat"
KEEP2_SAV = f"{BASE_DIR}/KEEP2 8차년도 데이터.SAV"
OUTPUT = Path(BASE_DIR) / "output" / "value_comparison.txt"

variable_pairs = [
    ("Y24SH02039", "F6Y05029", "월평균 근로소득 (연속형)"),
    ("Y24SH02058", "F6Y05050", "전반적 직장 만족도 (5점 척도 예상)"),
    ("Y24SH02050", "F6Y05042", "업무 만족도 (5점 척도 예상)"),
    ("Y24SH02014", "F6Y05013", "근무 형태 (정규/비정규)"),
    ("Y24SH02012", "F6Y05011", "종사상 지위 (필터링용)"),
    ("Y24SH02047", "F6Y05039", "전공-직무 일치도 (5점 척도 예상)"),
    ("Y24SB02003C", "F6Y01004c", "전공 계열 (대학교 계열) - 수정"),
    ("Y24SB11002", "F6Y02087", "졸업 평점 (연속형)"),
    ("Y24SB11003", "F6Y02088", "졸업 평점 만점"),
    ("Y24SF01002", "F6Y10098", "자격증 개수"),
    ("Y24SE01021", "F6Y10016", "영어 시험 점수"),
    ("Y24SE01020", "F6Y10015", "최근 본 영어 시험 종류"),
    ("Y24SH02025", "F6Y05021", "회사 규모"),
    ("Y24SH02031", "F6Y05027", "주당 근무시간"),
    ("GENDER", "GENDER", "성별 (1=남, 2=여 예상)"),
    ("Y24SB02003C_1", "F6Y01004c", "★ 통합 추정 변수"),
    ("Y24SB02003C_N", "F6Y01004c", "응답차수 (참고용)"),
]


def get_value_distribution(df, var_name):
    """변수의 응답값 분포 반환 (타입 안전)"""
    if var_name not in df.columns:
        return None, "변수 없음"

    s = df[var_name].dropna()

    if len(s) == 0:
        return None, "데이터 없음"

    n_unique = s.nunique()
    dtype_str = str(s.dtype)

    # 숫자로 변환 시도
    s_numeric = pd.to_numeric(s, errors='coerce')
    is_numeric = s_numeric.notna().sum() > len(s) * 0.5  # 절반 이상 변환되면 숫자형

    # 연속형 판단 (숫자형이고 고유값 많음)
    if is_numeric and n_unique > 20:
        s_clean = s_numeric.dropna()
        return {
            'type': '연속형',
            'dtype': dtype_str,
            'n': len(s_clean),
            'unique': int(s_clean.nunique()),
            'min': float(s_clean.min()),
            'max': float(s_clean.max()),
            'mean': float(s_clean.mean()),
            'median': float(s_clean.median())
        }, None

    # 범주형 (숫자든 문자든)
    counts = s.value_counts().sort_index()
    # 응답값을 보기 좋게
    values_dict = {}
    for k, v in counts.head(20).items():
        # numpy/float 값을 깔끔하게
        if isinstance(k, float) and k.is_integer():
            k = int(k)
        values_dict[str(k)] = int(v)

    return {
        'type': '범주형',
        'dtype': dtype_str,
        'n': len(s),
        'unique': int(n_unique),
        'values': values_dict
    }, None


def format_output(info):
    if info is None:
        return "  데이터 없음 또는 변수 없음"
    if info['type'] == '연속형':
        return (f"  타입: 연속형 ({info['dtype']}) | N={info['n']:,} | 고유값={info['unique']:,}\n"
                f"  min={info['min']:.2f}, max={info['max']:.2f}, "
                f"mean={info['mean']:.2f}, median={info['median']:.2f}")
    else:
        # 값이 너무 많으면 처음 15개만
        items = list(info['values'].items())[:15]
        values_str = ", ".join([f"{k}={v}" for k, v in items])
        if info['unique'] > 15:
            values_str += f" ... (총 {info['unique']}개)"
        return (f"  타입: 범주형 ({info['dtype']}) | N={info['n']:,} | 고유값={info['unique']}\n"
                f"  값 분포: {values_str}")


if __name__ == "__main__":
    print("데이터 로딩 중...")
    df1, _ = pyreadstat.read_sas7bdat(KEEP1_SAV)
    print(f"  KEEP1: {len(df1):,}명, {len(df1.columns):,}개 변수")
    df2, _ = pyreadstat.read_sav(KEEP2_SAV, apply_value_formats=False)
    print(f"  KEEP2: {len(df2):,}명, {len(df2.columns):,}개 변수")

    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("  KEEP1 vs KEEP2 변수 응답값 비교")
    output_lines.append("=" * 80)

    for keep2_var, keep1_var, desc in variable_pairs:
        output_lines.append("")
        output_lines.append("=" * 80)
        output_lines.append(f"📌 {desc}")
        output_lines.append(f"   KEEP2: {keep2_var}  ↔  KEEP1: {keep1_var}")
        output_lines.append("=" * 80)

        # KEEP2
        try:
            info2, err2 = get_value_distribution(df2, keep2_var)
        except Exception as e:
            info2, err2 = None, f"에러: {e}"
        output_lines.append(f"\n[KEEP2 - {keep2_var}]")
        if err2:
            output_lines.append(f"  ❌ {err2}")
        else:
            output_lines.append(format_output(info2))

        # KEEP1
        try:
            info1, err1 = get_value_distribution(df1, keep1_var)
        except Exception as e:
            info1, err1 = None, f"에러: {e}"
        output_lines.append(f"\n[KEEP1 - {keep1_var}]")
        if err1:
            output_lines.append(f"  ❌ {err1}")
        else:
            output_lines.append(format_output(info1))

        # 동일성 자동 체크
        output_lines.append("")
        if info1 and info2:
            if info1['type'] != info2['type']:
                output_lines.append("  ⚠️  타입이 다름! (한쪽 연속, 한쪽 범주)")
                output_lines.append("     → 한쪽이 숫자인데 문자로 저장됐을 가능성. 확인 필요.")
            elif info1['type'] == '범주형':
                k1_vals = set(info1['values'].keys())
                k2_vals = set(info2['values'].keys())
                if k1_vals == k2_vals:
                    output_lines.append("  ✅ 응답값 범위 동일")
                elif k1_vals.issubset(k2_vals) or k2_vals.issubset(k1_vals):
                    output_lines.append("  ⚠️  응답값 범위 부분 일치 — 한쪽이 더 많음")
                    only_k1 = k1_vals - k2_vals
                    only_k2 = k2_vals - k1_vals
                    if only_k1:
                        output_lines.append(f"     KEEP1만 있는 값: {only_k1}")
                    if only_k2:
                        output_lines.append(f"     KEEP2만 있는 값: {only_k2}")
                else:
                    output_lines.append("  ❌ 응답값 범위 다름! 코딩 다를 가능성 ↑")
                    output_lines.append(f"     KEEP1만 있는 값: {k1_vals - k2_vals}")
                    output_lines.append(f"     KEEP2만 있는 값: {k2_vals - k1_vals}")
            else:
                # 연속형
                if info1['min'] != 0:
                    ratio_min = info2['min'] / info1['min']
                else:
                    ratio_min = float('inf')
                if info1['max'] != 0:
                    ratio_max = info2['max'] / info1['max']
                else:
                    ratio_max = float('inf')
                output_lines.append(f"  📊 KEEP2/KEEP1 비율 — min: {ratio_min:.2f}x, max: {ratio_max:.2f}x")
                output_lines.append("     (소득은 인플레이션 고려 — 1.5~2배 차이는 정상)")

    # 저장
    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # 화면 출력
    print("\n".join(output_lines))

    print(f"\n\n✅ 결과 저장: {OUTPUT}")