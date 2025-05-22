import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from config import (
    OUTPUT_DIR, EMOTION_DIMENSIONS
)

def calculate_statistics(data):
    """各メトリクスの統計量を計算"""
    stats = {
        'maximum': np.max(data),
        'minimum': np.min(data),
        'mean': np.mean(data),
        'std_dev': np.std(data),
        'median': np.median(data),
        'skewness': skew(data),
        'kurtosis': kurtosis(data)
    }
    return pd.Series(stats)

def main():
    # 入力データを読み込む
    input_path = f"{OUTPUT_DIR}/text_emotion_average.csv"
    df = pd.read_csv(input_path)
    
    # 文学作品と感情次元のカラムを取得
    texts = df['text'].unique()
    metric_cols = list(EMOTION_DIMENSIONS.keys())
    
    # 文学作品ごとに統計量を計算
    all_stats = []
    for text in texts:
        text_data = df[df['text'] == text]
        stats_dict = {}
        for col in metric_cols:
            stats = calculate_statistics(text_data[col])
            stats_dict[col] = stats
        
        # 文学作品ごとの統計情報をDataFrameに変換
        stats_df = pd.DataFrame(stats_dict)
        stats_df.index = [f"{text}_{idx}" for idx in stats_df.index]
        all_stats.append(stats_df)
    
    # 全文学作品の統計情報を結合
    combined_stats = pd.concat(all_stats)
    
    # 読みやすさのために小数点以下3桁に丸める
    combined_stats = combined_stats.round(3)
    
    # CSVファイルとして保存
    output_path = f"{OUTPUT_DIR}/text_emotion_statistics.csv"
    combined_stats.to_csv(output_path)
    print(f"統計情報を保存しました: {output_path}")
    
    # 結果を表示
    print("\n計算された統計情報:")
    print(combined_stats)
    
    # 感情次元の日本語名での結果も表示
    jp_cols = {col: EMOTION_DIMENSIONS[col] for col in metric_cols}
    stats_df_jp = combined_stats.rename(columns=jp_cols)
    print("\n感情次元の統計情報（日本語）:")
    print(stats_df_jp)

if __name__ == "__main__":
    main()
