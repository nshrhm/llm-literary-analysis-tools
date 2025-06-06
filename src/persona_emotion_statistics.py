import pandas as pd
import numpy as np
import argparse
from scipy.stats import skew, kurtosis
from config import (
    OUTPUT_DIR, ANALYSIS_COLUMNS, get_message
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
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description='ペルソナ感情統計の分析スクリプト')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='言語設定 (ja: 日本語, en: 英語)')
    args = parser.parse_args()
    
    # 入力データを読み込む
    input_path = f"{OUTPUT_DIR}/persona_emotion.csv"
    df = pd.read_csv(input_path)
    
    # ペルソナと感情次元のカラムを取得
    personas = df['persona'].unique()
    metric_cols = ANALYSIS_COLUMNS['values']
    
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
    
    # 感情次元の選択された言語での結果も表示
    localized_cols = {col: get_message(f'common.emotion_dimensions.{col}.{args.lang}') for col in metric_cols}
    stats_df_localized = combined_stats.rename(columns=localized_cols)
    print(f"\n感情次元の統計情報（{args.lang}）:")
    print(stats_df_localized)

if __name__ == "__main__":
    main()
