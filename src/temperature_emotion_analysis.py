import pandas as pd
import os
import argparse
from config import OUTPUT_DIR, EMOTION_DIMENSIONS, ensure_output_directories

def main():
    parser = argparse.ArgumentParser(description='Temperature emotion analysis')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for output (ja or en)')
    args = parser.parse_args()

    # 感情次元の定義を取得
    emotion_dimensions = {k: v[args.lang] for k, v in EMOTION_DIMENSIONS.items()}

    # 出力ディレクトリを作成
    ensure_output_directories()

    # CSVファイルを読み込む
    df = pd.read_csv("data_all.csv")

    # temperature設定による感情次元の変化を計算
    temperature_effect = df.groupby(['model', 'temperature'])[list(EMOTION_DIMENSIONS.keys())].mean()
    temperature_effect.to_csv(os.path.join(OUTPUT_DIR, "temperature_emotion.csv"))

    print(f"temperature設定による感情次元分析が完了しました。結果は '{OUTPUT_DIR}/temperature_emotion.csv' に保存されています。")
    
    # 結果を表示（ローカライズされた列名で）
    print("\n分析結果:")
    localized_columns = ['model', 'temperature'] + list(emotion_dimensions.values())
    temperature_effect_display = temperature_effect.copy()
    temperature_effect_display.columns = list(emotion_dimensions.values())
    print(temperature_effect_display)

if __name__ == "__main__":
    main()
