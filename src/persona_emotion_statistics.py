import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from config import (
    OUTPUT_DIR, ANALYSIS_COLUMNS, EMOTION_DIMENSIONS, get_message
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
    input_path = f"{OUTPUT_DIR}/persona_emotion_average.csv"
    df = pd.read_csv(input_path)
    
    # ペルソナと感情次元のカラムを取得
    personas = df['persona'].unique()
    metric_cols = ANALYSIS_COLUMNS['values']
    emotion_names_ja = get_message('common.emotion_dimensions', 'ja')
    
    # ペルソナごとに統計量を計算
    all_stats = []
    for persona in personas:
        persona_data = df[df['persona'] == persona]
        stats_dict = {}
        for col in metric_cols:
            stats = calculate_statistics(persona_data[col])
            stats_dict[col] = stats
        
        # ペルソナごとの統計情報をDataFrameに変換
        stats_df = pd.DataFrame(stats_dict)
        stats_df.index = [f"{persona}_{idx}" for idx in stats_df.index]
        all_stats.append(stats_df)
    
    # 全ペルソナの統計情報を結合
    combined_stats = pd.concat(all_stats)
    
    # 読みやすさのために小数点以下3桁に丸める
    combined_stats = combined_stats.round(3)
    
    # CSVファイルとして保存
    output_path = f"{OUTPUT_DIR}/persona_emotion_statistics.csv"
    combined_stats.to_csv(output_path)
    print(f"統計情報を保存しました: {output_path}")
    
    # 結果を表示
    print("\n計算された統計情報:")
    print(combined_stats)
    
    # 感情次元の日本語名での結果も表示
    jp_cols = {col: emotion_names_ja[col] for col in metric_cols}
    stats_df_jp = combined_stats.rename(columns=jp_cols)
    print("\n感情次元の統計情報（日本語）:")
    print(stats_df_jp)

if __name__ == "__main__":
    main()
