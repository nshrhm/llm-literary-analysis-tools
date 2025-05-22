import pandas as pd
import os
from config import (
    OUTPUT_DIR, ANALYSIS_COLUMNS, DATA_PATHS,
    ensure_output_directories, safe_read_csv
)

def analyze_persona_emotion_trends():
    """ペルソナごとの感情次元傾向を分析"""
    # 出力ディレクトリを作成
    ensure_output_directories()
    
    # CSVファイルを読み込む
    df, error = safe_read_csv(DATA_PATHS['input'])
    if error:
        print(error)
        return
    
    # ペルソナとモデルの組み合わせごとに感情次元の傾向を計算
    emotion_trends = df.groupby(['persona', 'model'])[ANALYSIS_COLUMNS['values']].mean()
    
    # 結果をCSVファイルに保存
    output_file = os.path.join(OUTPUT_DIR, "persona_emotion.csv")
    emotion_trends.to_csv(output_file)
    
    # ペルソナごとの平均感情値も計算
    persona_averages = df.groupby('persona')[ANALYSIS_COLUMNS['values']].mean()
    persona_output_file = os.path.join(OUTPUT_DIR, "persona_emotion_average.csv")
    persona_averages.to_csv(persona_output_file)
    
    print(f"感情次元傾向分析が完了しました。")
    print(f"モデル別結果: '{output_file}'")
    print(f"ペルソナ別平均: '{persona_output_file}'")

if __name__ == "__main__":
    analyze_persona_emotion_trends()
