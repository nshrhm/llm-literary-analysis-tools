import pandas as pd
import os
import argparse
from config import (
    OUTPUT_DIR, EMOTION_DIMENSIONS, DATA_PATHS,
    ensure_output_directories, safe_read_csv
)

def analyze_text_emotion_trends():
    """文学作品ごとの感情次元傾向を分析"""
    parser = argparse.ArgumentParser(description='Text emotion analysis')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for output (ja or en)')
    args = parser.parse_args()

    # 感情次元の定義を取得
    emotion_dimensions = {k: v[args.lang] for k, v in EMOTION_DIMENSIONS.items()}

    # 出力ディレクトリを作成
    ensure_output_directories()
    
    # CSVファイルを読み込む
    df, error = safe_read_csv(DATA_PATHS['input'])
    if error:
        print(error)
        return
    
    # 文学作品とモデルの組み合わせごとに感情次元の傾向を計算
    emotion_trends = df.groupby(['text', 'model'])[list(EMOTION_DIMENSIONS.keys())].mean()
    
    # 結果をCSVファイルに保存
    output_file = os.path.join(OUTPUT_DIR, "text_emotion.csv")
    emotion_trends.to_csv(output_file)
    
    # 文学作品ごとの平均感情値も計算
    text_averages = df.groupby('text')[list(EMOTION_DIMENSIONS.keys())].mean()
    text_output_file = os.path.join(OUTPUT_DIR, "text_emotion_average.csv")
    text_averages.to_csv(text_output_file)
    
    print(f"感情次元傾向分析が完了しました。")
    print(f"モデル別結果: '{output_file}'")
    print(f"文学作品別平均: '{text_output_file}'")
    
    # 結果を表示（ローカライズされた列名で）
    print("\n文学作品別平均感情値:")
    text_averages_display = text_averages.copy()
    text_averages_display.columns = list(emotion_dimensions.values())
    print(text_averages_display)

if __name__ == "__main__":
    analyze_text_emotion_trends()
