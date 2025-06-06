import pandas as pd
import matplotlib.pyplot as plt
import argparse
import json
import os
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS, MODEL_ORDER,
    ANALYSIS_COLUMNS, DATA_PATHS, ensure_output_directories, safe_read_csv,
    save_figure
)

def get_vendor_color(model_name):
    """モデル名から対応する開発元の色を取得"""
    for vendor, patterns in VENDOR_PATTERNS.items():
        if any(model_name.startswith(pattern) for pattern in patterns):
            return VENDOR_COLORS[vendor]
    return '#808080'  # デフォルトの色（グレー）

def plot_missing_values(df, col, messages, lang):
    """特定の項目の欠損値をプロット"""
    # 欠損値が0でないデータのみをフィルタリング
    filtered_df = df[df[col] > 0].copy()
    
    if filtered_df.empty:
        print(messages['no_data_message'].format(col=col))
        return
    
    # モデルの順序を設定
    filtered_df['model'] = pd.Categorical(filtered_df['model'], categories=MODEL_ORDER, ordered=True)
    filtered_df = filtered_df.sort_values('model')
    
    # プロットの設定
    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(filtered_df)), filtered_df[col])
    
    # 各バーの色を設定
    for bar, model in zip(bars, filtered_df['model']):
        bar.set_color(get_vendor_color(model))
        bar.set_alpha(0.8)
    
    plt.yticks(range(len(filtered_df)), filtered_df['model'])
    plt.xlabel(messages['xlabel'].format(col=col))
    plt.ylabel(messages['ylabel'])
    plt.title(messages['plot_title'].format(col=col))
    
    # 凡例を追加
    legend_elements = [plt.Rectangle((0,0),1,1, color=color, alpha=0.8, label=vendor)
                      for vendor, color in VENDOR_COLORS.items()]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left', title=messages['legend_title'])
    
    plt.tight_layout()
    
    # ファイルの保存
    save_figure(plt, f'missing_values_{col.lower()}', lang=lang)
    plt.close()
    
    print(messages['saved_message'].format(col=col))

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="Visualize missing values data.")
    parser.add_argument('--lang', type=str, default='ja', help='Language for plots (ja or en)')
    args = parser.parse_args()
    lang = args.lang

    # 日本語フォントのインポート（日本語の場合のみ）
    if lang == 'ja':
        import japanize_matplotlib

    # メッセージの読み込み
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages_data = json.load(f)
    messages = messages_data['missing_values'][lang]

    # 出力ディレクトリの作成
    ensure_output_directories()
    
    # CSVファイルの読み込み
    df, error = safe_read_csv(DATA_PATHS['missing_by_model'])
    if error:
        print(error)
        return
    
    # 個別項目のグラフ生成
    for col in ANALYSIS_COLUMNS['all']:
        plot_missing_values(df, col, messages, lang)
    
    # 総合欠損値の計算
    df['TotalMissing'] = df[ANALYSIS_COLUMNS['all']].mean(axis=1)
    plot_missing_values(df, 'TotalMissing', messages, lang)

if __name__ == "__main__":
    main()
