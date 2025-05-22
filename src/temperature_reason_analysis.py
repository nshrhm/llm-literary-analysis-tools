import pandas as pd
import os
from config import OUTPUT_DIR, REASON_DIMENSIONS, ensure_output_directories

# 出力ディレクトリを作成
ensure_output_directories()

# CSVファイルを読み込む
df = pd.read_csv("data_all.csv")

# モデルごとの生成テキスト量（理由の文字数）を計算
for col, label in REASON_DIMENSIONS.items():
    df[f"{col}_length"] = df[col].str.len().fillna(0)
df['total_reason_length'] = sum(df[f"{col}_length"] for col in REASON_DIMENSIONS.keys())

# temperature設定による生成テキスト量の変化を計算
temperature_text_effect = df.groupby(['model', 'temperature'])['total_reason_length'].mean()
temperature_text_effect.to_csv(os.path.join(OUTPUT_DIR, "temperature_reason.csv"))

# 詳細な分析：各感情次元ごとのテキスト量
detailed_text_effect = df.groupby(['model', 'temperature'])[[f"{col}_length" for col in REASON_DIMENSIONS.keys()]].mean()
detailed_text_effect.to_csv(os.path.join(OUTPUT_DIR, "temperature_reason_detailed.csv"))

print(f"temperature設定による生成テキスト量分析が完了しました。結果は '{OUTPUT_DIR}/temperature_reason.csv' に保存されています。")
print(f"詳細な分析結果は '{OUTPUT_DIR}/temperature_reason_detailed.csv' に保存されています。")
