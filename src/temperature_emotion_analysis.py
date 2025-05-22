import pandas as pd
import os
from config import OUTPUT_DIR, EMOTION_DIMENSIONS, ensure_output_directories

# 出力ディレクトリを作成
ensure_output_directories()

# CSVファイルを読み込む
df = pd.read_csv("data_all.csv")

# temperature設定による感情次元の変化を計算
temperature_effect = df.groupby(['model', 'temperature'])[list(EMOTION_DIMENSIONS.keys())].mean()
temperature_effect.to_csv(os.path.join(OUTPUT_DIR, "temperature_emotion.csv"))

print(f"temperature設定による感情次元分析が完了しました。結果は '{OUTPUT_DIR}/temperature_emotion.csv' に保存されています。")
