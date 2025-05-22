import pandas as pd
import os
from config import OUTPUT_DIR, EMOTION_DIMENSIONS, ensure_output_directories

# 出力ディレクトリを作成
ensure_output_directories()

# CSVファイルを読み込む
df = pd.read_csv("data_all.csv")

# temperature設定による感情次元の統計的指標を計算
stats_data = []
for model in df['model'].unique():
    for temp in df['temperature'].unique():
        subset = df[(df['model'] == model) & (df['temperature'] == temp)]
        if not subset.empty:
            record = {'model': model, 'temperature': temp}
            for col in EMOTION_DIMENSIONS.keys():
                record[f"{col}_mean"] = subset[col].mean()
                record[f"{col}_std"] = subset[col].std()
                record[f"{col}_median"] = subset[col].median()
                record[f"{col}_max"] = subset[col].max()
                record[f"{col}_min"] = subset[col].min()
                record[f"{col}_skew"] = subset[col].skew()
                record[f"{col}_kurtosis"] = subset[col].kurtosis()
            stats_data.append(record)

# データフレームに変換して保存
stats_df = pd.DataFrame(stats_data)
stats_df.to_csv(os.path.join(OUTPUT_DIR, "temperature_emotion_statistics.csv"), index=False)

print(f"temperature設定による感情次元の統計分析が完了しました。結果は '{OUTPUT_DIR}/temperature_emotion_statistics.csv' に保存されています。")
