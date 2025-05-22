import pandas as pd
import matplotlib.pyplot as plt
import os
import japanize_matplotlib
import numpy as np
import seaborn as sns
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS, MODEL_ORDER,
    EMOTION_DIMENSIONS, VISUALIZATION_CONFIG, ensure_output_directories,
    save_figure, load_emotion_data
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

# 出力ディレクトリを作成
ensure_output_directories()

# CSVファイルからデータを読み込む
data = load_emotion_data()

# データをモデル順序に基づいて並べ替え
filtered_data = data.set_index('model').reindex(MODEL_ORDER).reset_index()

# 開発元情報を追加
filtered_data['vendor'] = filtered_data['model'].apply(get_vendor)

# 感情次元の定義を使用
emotions = EMOTION_DIMENSIONS

def create_bar_plot(filtered_data, emotions):
    """棒グラフによる感情次元の平均値比較を作成"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: 感情次元の棒グラフ
    ax1 = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = '※各モデルの棒グラフは左から順に: 面白さ（薄）→ 驚き → 悲しみ → 怒り（濃）'
    ax1.text(0.5, 1.05, header_text,
             horizontalalignment='center',
             transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

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
    ax1.set_xlabel('モデル')
    ax1.set_ylabel('平均値')
    ax1.set_title('モデルごとの感情次元の平均値比較（開発元別）')
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
              title='開発元', 
              loc='center', 
              ncol=len(VENDOR_COLORS),
              bbox_to_anchor=(0.5, 0.5))

    # レイアウトの調整
    plt.subplots_adjust(right=0.85, hspace=0.3)
    save_figure(plt, "model_emotion")
    plt.close()

def create_distribution_plot(filtered_data, emotions):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: バイオリンプロットとスウォームプロット
    ax_violin = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    melted_data = pd.melt(filtered_data, 
                          id_vars=['model', 'vendor'],
                          value_vars=list(emotions.keys()),
                          var_name='emotion',
                          value_name='value')

    # 感情ラベルを日本語に変換
    melted_data['emotion'] = melted_data['emotion'].map(emotions)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='emotion', y='value', hue='vendor',
                   ax=ax_violin, inner=None, fill=False, linewidth=2.0, palette=VENDOR_COLORS)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='emotion', y='value', hue='vendor',
                  ax=ax_violin, dodge=True, size=3, alpha=0.4,
                  palette=VENDOR_COLORS, legend=False)

    ax_violin.set_title('感情次元ごとの分布と個別データ点')
    ax_violin.set_xlabel('感情次元')
    ax_violin.set_ylabel('値')
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
              title='開発元', 
              loc='center', 
              ncol=len(VENDOR_COLORS),
              bbox_to_anchor=(0.5, 0.5))

    # レイアウトの調整
    plt.subplots_adjust(right=0.85, hspace=0.3)
    save_figure(plt, "model_emotion_distribution")
    plt.close()

# 2つのグラフを生成
create_bar_plot(filtered_data, emotions)
create_distribution_plot(filtered_data, emotions)

# 開発元ごとの平均値を計算して表示
print("\n開発元ごとの感情次元平均値:")
vendor_means = filtered_data.groupby('vendor')[list(emotions.keys())].mean()
for vendor in vendor_means.index:
    print(f"\n{vendor}:")
    for col, label in emotions.items():
        print(f"  {label}: {vendor_means.loc[vendor, col]:.2f}")

print("\nグラフを保存しました:")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_emotion.png')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_emotion.svg')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_emotion_distribution.png')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_emotion_distribution.svg')}")
