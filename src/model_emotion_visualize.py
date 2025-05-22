import pandas as pd
import matplotlib.pyplot as plt
import os
import japanize_matplotlib
import numpy as np
import seaborn as sns
import json
import argparse
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS, MODEL_ORDER,
    EMOTION_DIMENSIONS, VISUALIZATION_CONFIG, ensure_output_directories,
    save_figure, load_emotion_data, create_melted_data, setup_figure, add_header_text, get_message
)

def get_vendor_color(model_name):
    """モデル名から対応する開発元の色を取得"""
    for vendor, patterns in VENDOR_PATTERNS.items():
        if any(model_name.startswith(pattern) for pattern in patterns):
            return VENDOR_COLORS[vendor]
    return '#808080'  # デフォルトの色（グレー）

def get_vendor(model_name):
    """モデル名から開発元を取得"""
    for vendor, patterns in VENDOR_PATTERNS.items():
        if any(model_name.startswith(pattern) for pattern in patterns):
            return vendor
    return 'Other'


def load_messages(lang):
    """言語に応じたメッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages[lang]['model_emotion']

def create_bar_plot(filtered_data, emotions, lang='ja'):
    """棒グラフによる感情次元の平均値比較を作成"""
    messages = load_messages(lang)
    fig, gs = setup_figure(gridspec=[2, 1, {'height_ratios': [4, 1]}])

    # 上段: 感情次元の棒グラフ
    ax1 = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    add_header_text(ax1, messages['header_text'])

    # 感情次元ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く

    # 各モデルのデータをプロット
    bar_width = 0.2
    x = range(len(filtered_data['model']))
    for i, (col, _) in enumerate(emotions.items()):
        bars = ax1.bar([p + i * bar_width for p in x], filtered_data[col], 
                       bar_width)
        
        # 各バーを開発元の色で装飾
        for bar, model in zip(bars, filtered_data['model']):
            color = get_vendor_color(model)
            bar.set_color(color)
            bar.set_alpha(alphas[i])

    # グラフの設定
    ax1.set_xlabel(messages['xlabel'])
    ax1.set_ylabel(messages['ylabel'])
    ax1.set_title(messages['bar_plot_title'])
    ax1.set_xticks([p + 1.5 * bar_width for p in x])
    ax1.set_xticklabels(filtered_data['model'], rotation=45, ha='right')
    ax1.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])

    # 下段: 開発元の凡例
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')

    legend_elements = [plt.Rectangle((0,0),1,1, color=color, 
                      alpha=VISUALIZATION_CONFIG['plot']['text_box_alpha'], label=vendor)
                      for vendor, color in VENDOR_COLORS.items()]
    ax2.legend(handles=legend_elements, 
              title=messages['vendor_legend_title'], 
              loc='center', 
              ncol=len(VENDOR_COLORS),
              bbox_to_anchor=(0.5, 0.5))

    # レイアウトの調整
    plt.subplots_adjust(right=0.85, hspace=0.3)
    save_figure(plt, "model_emotion", lang=lang)
    plt.close()

def create_distribution_plot(filtered_data, emotions, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages = load_messages(lang)
    fig, gs = setup_figure(gridspec=[2, 1, {'height_ratios': [4, 1]}])

    # 上段: バイオリンプロットとスウォームプロット
    ax_violin = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    melted_data = create_melted_data(filtered_data, 
                                     id_vars=['model', 'vendor'],
                                     value_vars=list(emotions.keys()),
                                     value_mapping=emotions)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='emotion', y='value', hue='vendor',
                   ax=ax_violin, inner=None, fill=False, linewidth=2.0, palette=VENDOR_COLORS)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='emotion', y='value', hue='vendor',
                  ax=ax_violin, dodge=True, size=3, alpha=0.4,
                  palette=VENDOR_COLORS, legend=False)

    ax_violin.set_title(messages['distribution_plot_title'])
    ax_violin.set_xlabel(messages['emotion_xlabel'])
    ax_violin.set_ylabel(messages['emotion_ylabel'])
    ax_violin.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])

    # バイオリンプロットの凡例を調整
    handles, labels = ax_violin.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax_violin.legend_.remove()

    # 下段: 開発元の凡例
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')

    legend_elements = [plt.Rectangle((0,0),1,1, color=color, 
                      alpha=VISUALIZATION_CONFIG['plot']['text_box_alpha'], label=vendor)
                      for vendor, color in VENDOR_COLORS.items()]
    ax2.legend(handles=legend_elements, 
              title=messages['vendor_legend_title'], 
              loc='center', 
              ncol=len(VENDOR_COLORS),
              bbox_to_anchor=(0.5, 0.5))

    # レイアウトの調整
    plt.subplots_adjust(right=0.85, hspace=0.3)
    save_figure(plt, "model_emotion_distribution", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # CSVファイルからデータを読み込む
    data = load_emotion_data()

    # データをモデル順序に基づいて並べ替え
    filtered_data = data.set_index('model').reindex(MODEL_ORDER).reset_index()

    # 開発元情報を追加
    filtered_data['vendor'] = filtered_data['model'].apply(get_vendor)

    # 言語に応じた感情次元の定義を使用
    # messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    emotions = get_message('common.emotion_dimensions', lang)

    # 2つのグラフを生成
    create_bar_plot(filtered_data, emotions, lang)
    create_distribution_plot(filtered_data, emotions, lang)

    # 開発元ごとの平均値を計算して表示
    print("\n開発元ごとの感情次元平均値:")
    vendor_means = filtered_data.groupby('vendor')[list(emotions.keys())].mean()
    for vendor in vendor_means.index:
        print(f"\n{vendor}:")
        for col, label in emotions.items():
            print(f"  {label}: {vendor_means.loc[vendor, col]:.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_emotion.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_emotion.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_emotion_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_emotion_distribution.svg')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for model emotion data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
