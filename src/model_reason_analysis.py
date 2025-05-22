import pandas as pd
import numpy as np
import os
from config import ensure_output_directories, OUTPUT_DIR

# 出力ディレクトリの作成
ensure_output_directories()

def load_data():
  """データの読み込み"""
  print("実験結果データを読み込んでいます...")
  df = pd.read_csv("data_all.csv")
  return df

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

def analyze_model_reasons(df):
  """モデルごとの理由文文字数の分析"""
  print("モデルごとの理由文文字数を分析中...")
  
  # モデルごとにグループ化して平均値を計算
  length_columns = ['Q1reason_length', 'Q2reason_length', 'Q3reason_length', 'Q4reason_length']
  model_reasons = df.groupby('model')[length_columns].mean().round(2)

  # カラム名を変更（_lengthを削除）
  model_reasons.columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']

  return model_reasons

def main():
  # データの読み込み
  df = load_data()

  # 理由文の文字数を計算
  df = calculate_reason_lengths(df)

  # モデルごとの分析
  model_reasons = analyze_model_reasons(df)

  # 結果の保存
  output_path = os.path.join(OUTPUT_DIR, 'model_reason.csv')
  model_reasons.to_csv(output_path)
  print(f"\n分析が完了しました。")
  print(f"結果は '{output_path}' に保存されました。")

if __name__ == "__main__":
  main()
