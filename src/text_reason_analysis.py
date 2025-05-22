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

def analyze_text_reasons(df):
    """文学作品とモデルの組み合わせごとの理由文文字数を分析"""
    print("文学作品ごとの理由文文字数を分析中...")
    
    # 理由文の文字数を計算
    df = calculate_reason_lengths(df)
    
    # 文学作品とモデルの組み合わせごとにグループ化して平均値を計算
    length_columns = ['Q1reason_length', 'Q2reason_length', 'Q3reason_length', 'Q4reason_length']
    text_model_reasons = df.groupby(['text', 'model'])[length_columns].mean()
    
    # カラム名を変更（_lengthを削除）
    text_model_reasons.columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    
    return text_model_reasons

def analyze_text_reason_trends():
    """文学作品ごとの理由文文字数傾向を分析"""
    # 出力ディレクトリを作成
    ensure_output_directories()
    
    # CSVファイルを読み込む
    df, error = safe_read_csv(DATA_PATHS['input'])
    if error:
        print(error)
        return
    
    # 文学作品とモデルの組み合わせごとに理由文文字数の傾向を計算
    text_model_reasons = analyze_text_reasons(df)
    
    # 結果をCSVファイルに保存
    output_file = os.path.join(OUTPUT_DIR, "text_reason.csv")
    text_model_reasons.to_csv(output_file)
    
    # 文学作品ごとの平均理由文文字数も計算
    length_columns = ['Q1reason_length', 'Q2reason_length', 'Q3reason_length', 'Q4reason_length']
    text_averages = df[['text'] + length_columns].groupby('text').mean()
    
    # カラム名を変更（_lengthを削除）
    text_averages.columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    
    text_output_file = os.path.join(OUTPUT_DIR, "text_reason_average.csv")
    text_averages.to_csv(text_output_file)
    
    print(f"理由文文字数傾向分析が完了しました。")
    print(f"モデル別結果: '{output_file}'")
    print(f"文学作品別平均: '{text_output_file}'")

if __name__ == "__main__":
    analyze_text_reason_trends()
