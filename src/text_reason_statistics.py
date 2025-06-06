import pandas as pd
import numpy as np
import argparse
from scipy.stats import skew, kurtosis
from config import (
    OUTPUT_DIR, get_message
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
    parser = argparse.ArgumentParser(description='文章理由統計の分析スクリプト')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='言語設定 (ja: 日本語, en: 英語)')
    args = parser.parse_args()
    
    # 理由次元の取得
    reason_dimensions_raw = get_message('common.reason_dimensions')
    reason_dimensions = {k: v[args.lang] for k, v in reason_dimensions_raw.items()}
    
    # 入力データを読み込む
    input_path = f"{OUTPUT_DIR}/text_reason_average.csv"
    df = pd.read_csv(input_path)
    
    # 文学作品と理由文のカラムを取得
    texts = df['text'].unique()
    metric_cols = list(reason_dimensions.keys())
    
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
    output_path = f"{OUTPUT_DIR}/text_reason_statistics.csv"
    combined_stats.to_csv(output_path)
    print(f"統計情報を保存しました: {output_path}")
    
    # 結果を表示
    print("\n計算された統計情報:")
    print(combined_stats)
    
    # 理由文の選択された言語での結果も表示
    stats_df_localized = combined_stats.rename(columns=reason_dimensions)
    print(f"\n理由文の統計情報（{args.lang}）:")
    print(stats_df_localized)

if __name__ == "__main__":
    main()
