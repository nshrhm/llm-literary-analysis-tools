import pandas as pd
import os
import argparse
from config import OUTPUT_DIR, EMOTION_DIMENSIONS, ensure_output_directories

def main():
    parser = argparse.ArgumentParser(description='Temperature emotion statistics analysis')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for output (ja or en)')
    args = parser.parse_args()

    # 感情次元の定義を取得
    emotion_dimensions = {k: v[args.lang] for k, v in EMOTION_DIMENSIONS.items()}

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
    output_path = os.path.join(OUTPUT_DIR, "temperature_emotion_statistics.csv")
    stats_df.to_csv(output_path, index=False)
    
    print(f"統計情報を保存しました: {output_path}")
    
    # 結果を表示
    print("\n計算された統計情報:")
    print(stats_df)

    # 感情次元の選択された言語での結果も表示
    display_columns = ['model', 'temperature']
    for col_key in EMOTION_DIMENSIONS.keys():
        display_columns.extend([f"{col_key}_mean", f"{col_key}_std", f"{col_key}_median", f"{col_key}_max", f"{col_key}_min", f"{col_key}_skew", f"{col_key}_kurtosis"])
    
    localized_columns = ['model', 'temperature']
    for col_key, localized_name in emotion_dimensions.items():
        localized_columns.extend([f"{localized_name}_mean", f"{localized_name}_std", f"{localized_name}_median", f"{localized_name}_max", f"{localized_name}_min", f"{localized_name}_skew", f"{localized_name}_kurtosis"])
    
    stats_df_localized = stats_df.copy()
    stats_df_localized.columns = localized_columns
    print(f"\n感情次元の統計情報（{args.lang}）:")
    print(stats_df_localized)

if __name__ == "__main__":
    main()
