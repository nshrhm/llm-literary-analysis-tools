import pandas as pd
import os
from config import (
    OUTPUT_DIR, EMOTION_DIMENSIONS, DATA_PATHS,
    ensure_output_directories, safe_read_csv
)

def analyze_emotion_trends():
    """モデルごとの感情次元傾向を分析"""
    # 出力ディレクトリを作成
    ensure_output_directories()
    
    # CSVファイルを読み込む
    df, error = safe_read_csv(DATA_PATHS['input'])
    if error:
        print(error)
        return
    
    # 感情次元の傾向をモデルごとに計算
    emotion_trends = df.groupby('model')[list(EMOTION_DIMENSIONS.keys())].mean()
    output_file = os.path.join(OUTPUT_DIR, "model_emotion.csv")
    emotion_trends.to_csv(output_file)
    
    print(f"感情次元傾向分析が完了しました。結果は '{output_file}' に保存されています。")

if __name__ == "__main__":
    analyze_emotion_trends()
