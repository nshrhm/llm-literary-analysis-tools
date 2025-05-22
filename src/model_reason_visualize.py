import pandas as pd
import matplotlib.pyplot as plt
import os
import japanize_matplotlib
import numpy as np
import seaborn as sns
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS, MODEL_ORDER,
    VISUALIZATION_CONFIG, ensure_output_directories,
    save_figure
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
def load_reason_data():
    """理由文データの読み込み"""
    filepath = os.path.join(OUTPUT_DIR, 'model_reason.csv')
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")

data = load_reason_data()

# データをモデル順序に基づいて並べ替え
filtered_data = data.set_index('model').reindex(MODEL_ORDER).reset_index()

# 開発元情報を追加
filtered_data['vendor'] = filtered_data['model'].apply(get_vendor)

# 理由文カラムの定義
reason_dimensions = {
    'Q1reason': '面白さの理由',
    'Q2reason': '驚きの理由',
    'Q3reason': '悲しみの理由',
    'Q4reason': '怒りの理由'
}

def create_bar_plot(filtered_data, reason_dimensions):
    """棒グラフによる理由文長の比較を作成"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: 理由文長の棒グラフ
    ax1 = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = '※各モデルの棒グラフは左から順に: 面白さ（薄）→ 驚き → 悲しみ → 怒り（濃）'
    ax1.text(0.5, 1.05, header_text,
             horizontalalignment='center',
             transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 理由文ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く

    # 各モデルのデータをプロット
    bar_width = 0.2
    x = range(len(filtered_data['model']))
    for i, (col, _) in enumerate(reason_dimensions.items()):
        bars = ax1.bar([p + i * bar_width for p in x], filtered_data[col], 
                       bar_width)
        
        # 各バーを開発元の色で装飾
        for bar, model in zip(bars, filtered_data['model']):
            color = get_vendor_color(model)
            bar.set_color(color)
            bar.set_alpha(alphas[i])

    # グラフの設定
    ax1.set_xlabel('モデル')
    ax1.set_ylabel('文字数')
    ax1.set_title('モデルごとの理由文長の比較（開発元別）')
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
    save_figure(plt, "model_reason")
    plt.close()

def create_sorted_bar_plot(data, title, filename, reason_cols=None, header_text=None):
    """ソートされた棒グラフを作成する共通関数"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: 理由文長の棒グラフ
    ax1 = fig.add_subplot(gs[0])

    if header_text:
        ax1.text(0.5, 1.05, header_text,
                horizontalalignment='center',
                transform=ax1.transAxes,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 理由文ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く
    if reason_cols is None:
        reason_cols = list(reason_dimensions.keys())

    # 各モデルのデータをプロット
    bar_width = 0.2
    x = range(len(data['model']))
    for i, col in enumerate(reason_cols):
        bars = ax1.bar([p + i * bar_width for p in x], data[col], bar_width)
        
        # 各バーを開発元の色で装飾
        for bar, model in zip(bars, data['model']):
            color = get_vendor_color(model)
            bar.set_color(color)
            bar.set_alpha(alphas[i] if len(reason_cols) > 1 else 0.8)

    # グラフの設定
    ax1.set_xlabel('モデル')
    ax1.set_ylabel('文字数')
    ax1.set_title(title)
    ax1.set_xticks([p + (len(reason_cols)-1) * bar_width/2 for p in x])
    ax1.set_xticklabels(data['model'], rotation=45, ha='right')
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
    save_figure(plt, filename)
    plt.close()

def create_sorted_all_plot(filtered_data, reason_dimensions):
    """全理由文の合計長でソートしたグラフを作成"""
    # 合計長を計算してソート
    data = filtered_data.copy()
    data['total'] = data[list(reason_dimensions.keys())].sum(axis=1)
    sorted_data = data.sort_values('total', ascending=False).drop('total', axis=1)

    header_text = '※各モデルの棒グラフは左から順に: 面白さ（薄）→ 驚き → 悲しみ → 怒り（濃）'
    create_sorted_bar_plot(
        sorted_data,
        '理由文長の総計による比較（開発元別、降順）',
        'model_reason_sorted_all',
        header_text=header_text
    )

def create_sorted_individual_plots(filtered_data, reason_dimensions):
    """各理由文ごとにソートしたグラフを作成"""
    for i, (col, label) in enumerate(reason_dimensions.items(), 1):
        sorted_data = filtered_data.sort_values(col, ascending=False)
        create_sorted_bar_plot(
            sorted_data,
            f'{label}の文字数による比較（開発元別、降順）',
            f'model_reason_sorted_q{i}',
            [col]
        )

def create_distribution_plot(filtered_data, reason_dimensions):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: バイオリンプロットとスウォームプロット
    ax_violin = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    melted_data = pd.melt(filtered_data, 
                          id_vars=['model', 'vendor'],
                          value_vars=list(reason_dimensions.keys()),
                          var_name='reason_type',
                          value_name='length')

    # 理由ラベルを日本語に変換
    melted_data['reason_type'] = melted_data['reason_type'].map(reason_dimensions)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='reason_type', y='length', hue='vendor',
                   ax=ax_violin, inner=None, fill=False, linewidth=2.0, palette=VENDOR_COLORS)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='reason_type', y='length', hue='vendor',
                  ax=ax_violin, dodge=True, size=3, alpha=0.4,
                  palette=VENDOR_COLORS, legend=False)

    ax_violin.set_title('理由文長の分布と個別データ点')
    ax_violin.set_xlabel('理由の種類')
    ax_violin.set_ylabel('文字数')
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
    save_figure(plt, "model_reason_distribution")
    plt.close()

# グラフを生成
create_bar_plot(filtered_data, reason_dimensions)
create_distribution_plot(filtered_data, reason_dimensions)
create_sorted_all_plot(filtered_data, reason_dimensions)
create_sorted_individual_plots(filtered_data, reason_dimensions)

# 開発元ごとの平均値を計算して表示
print("\n開発元ごとの理由文長平均値:")
vendor_means = filtered_data.groupby('vendor')[list(reason_dimensions.keys())].mean()
for vendor in vendor_means.index:
    print(f"\n{vendor}:")
    for col, label in reason_dimensions.items():
        print(f"  {label}: {vendor_means.loc[vendor, col]:.2f}")

print("\nグラフを保存しました:")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason.png')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason.svg')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_distribution.png')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_distribution.svg')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_sorted_all.png')}")
print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_sorted_all.svg')}")
for i in range(1, 5):
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', f'model_reason_sorted_q{i}.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', f'model_reason_sorted_q{i}.svg')}")
