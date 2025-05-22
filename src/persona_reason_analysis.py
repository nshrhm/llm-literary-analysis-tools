import pandas as pd
import os
from config import (
    OUTPUT_DIR, DATA_PATHS,
    ensure_output_directories, safe_read_csv
)

def calculate_reason_lengths(df):
    """理由文の文字数を計算"""
    print("理由文の文字数を計算中...")
    
    # 各理由文の文字数を計算
    reason_columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    length_columns = [col + '_length' for col in reason_columns]
    
    for reason_col, length_col in zip(reason_columns, length_columns):
        # 文字列型に変換してからlen()を適用（NaNは0として扱う）
        df[length_col] = df[reason_col].fillna('').astype(str).str.len()
    
    return df

def analyze_persona_reasons(df):
    """ペルソナとモデルの組み合わせごとの理由文文字数を分析"""
    print("ペルソナごとの理由文文字数を分析中...")
    
    # 理由文の文字数を計算
    df = calculate_reason_lengths(df)
    
    # ペルソナとモデルの組み合わせごとにグループ化して平均値を計算
    length_columns = ['Q1reason_length', 'Q2reason_length', 'Q3reason_length', 'Q4reason_length']
    persona_model_reasons = df.groupby(['persona', 'model'])[length_columns].mean()
    
    # カラム名を変更（_lengthを削除）
    persona_model_reasons.columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    
    return persona_model_reasons

def analyze_persona_reason_trends():
    """ペルソナごとの理由文文字数傾向を分析"""
    # 出力ディレクトリを作成
    ensure_output_directories()
    
    # CSVファイルを読み込む
    df, error = safe_read_csv(DATA_PATHS['input'])
    if error:
        print(error)
        return
    
    # ペルソナとモデルの組み合わせごとに理由文文字数の傾向を計算
    persona_model_reasons = analyze_persona_reasons(df)
    
    # 結果をCSVファイルに保存
    output_file = os.path.join(OUTPUT_DIR, "persona_reason.csv")
    persona_model_reasons.to_csv(output_file)
    
    # ペルソナごとの平均理由文文字数も計算
    length_columns = ['Q1reason_length', 'Q2reason_length', 'Q3reason_length', 'Q4reason_length']
    persona_averages = df[['persona'] + length_columns].groupby('persona').mean()
    
    # カラム名を変更（_lengthを削除）
    persona_averages.columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    
    persona_output_file = os.path.join(OUTPUT_DIR, "persona_reason_average.csv")
    persona_averages.to_csv(persona_output_file)
    
    print(f"理由文文字数傾向分析が完了しました。")
    print(f"モデル別結果: '{output_file}'")
    print(f"ペルソナ別平均: '{persona_output_file}'")

if __name__ == "__main__":
    analyze_persona_reason_trends()
