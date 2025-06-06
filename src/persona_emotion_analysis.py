import pandas as pd
import os
import argparse
from config import (
    OUTPUT_DIR, ANALYSIS_COLUMNS, DATA_PATHS, EMOTION_DIMENSIONS,
    ensure_output_directories, safe_read_csv
)

def analyze_persona_emotion_trends():
    """ペルソナごとの感情次元傾向を分析"""
    parser = argparse.ArgumentParser(description='Persona emotion analysis')
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

    # 結果を表示（ローカライズされた列名で）
    print("\n分析結果（ペルソナ別平均）:")
    persona_averages_display = persona_averages.copy()
    persona_averages_display.columns = list(emotion_dimensions.values())
    print(persona_averages_display)

if __name__ == "__main__":
    analyze_persona_emotion_trends()
