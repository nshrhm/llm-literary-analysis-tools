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
    VISUALIZATION_CONFIG, ensure_output_directories,
    save_figure, get_message
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
    return messages[lang]['model_reason']

def create_bar_plot(filtered_data, reasons, lang='ja'):
    """棒グラフによる理由文長の比較を作成"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: 理由文長の棒グラフ
    ax1 = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    ax1.text(0.5, 1.05, messages['header_text'],
             horizontalalignment='center',
             transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 理由文ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く

    # 各モデルのデータをプロット
    bar_width = 0.2
    x = range(len(filtered_data['model']))
    for i, (col, label_dict) in enumerate(reasons.items()):
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
    save_figure(plt, "model_reason", lang=lang)
    plt.close()

def create_sorted_bar_plot(data, title, filename, reason_cols=None, header_text=None, lang='ja'):
    """ソートされた棒グラフを作成する共通関数"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
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
        reason_cols = list(get_message('common.reason_dimensions', lang).keys())

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
    ax1.set_xlabel(messages['xlabel'])
    ax1.set_ylabel(messages['ylabel'])
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
              title=messages['vendor_legend_title'], 
              loc='center', 
              ncol=len(VENDOR_COLORS),
              bbox_to_anchor=(0.5, 0.5))

    # レイアウトの調整
    plt.subplots_adjust(right=0.85, hspace=0.3)
    save_figure(plt, filename, lang=lang)
    plt.close()

def create_sorted_all_plot(filtered_data, reasons, lang='ja'):
    """全理由文の合計長でソートしたグラフを作成"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    # 合計長を計算してソート
    data = filtered_data.copy()
    data['total'] = data[list(reasons.keys())].sum(axis=1)
    sorted_data = data.sort_values('total', ascending=False).drop('total', axis=1)

    create_sorted_bar_plot(
        sorted_data,
        messages['bar_plot_title'],
        'model_reason_sorted_all',
        header_text=messages['header_text'],
        lang=lang
    )

def create_sorted_individual_plots(filtered_data, reasons, lang='ja'):
    """各理由文ごとにソートしたグラフを作成"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    for i, (col, label_dict) in enumerate(reasons.items(), 1):
        sorted_data = filtered_data.sort_values(col, ascending=False)
        title = messages['sorted_individual_plot_title'].format(reason_label=label_dict[lang])
        create_sorted_bar_plot(
            sorted_data,
            title,
            f'model_reason_sorted_q{i}',
            [col],
            lang=lang
        )

def create_distribution_plot(filtered_data, reasons, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages = load_messages(lang) # messagesは他の場所で
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # 上段: バイオリンプロットとスウォームプロット
    ax_violin = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    melted_data = pd.melt(filtered_data, 
                          id_vars=['model', 'vendor'],
                          value_vars=list(reasons.keys()),
                          var_name='reason_type',
                          value_name='length')

    # 理由ラベルを言語に応じて変換
    melted_data['reason_type'] = melted_data['reason_type'].map(
        {col: label_dict[lang] for col, label_dict in reasons.items()}
    )

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='reason_type', y='length', hue='vendor',
                   ax=ax_violin, inner=None, fill=False, linewidth=2.0, palette=VENDOR_COLORS)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='reason_type', y='length', hue='vendor',
                  ax=ax_violin, dodge=True, size=3, alpha=0.4,
                  palette=VENDOR_COLORS, legend=False)

    ax_violin.set_title(messages['distribution_plot_title'])
    ax_violin.set_xlabel(messages['xlabel'])
    ax_violin.set_ylabel(messages['ylabel'])
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
    save_figure(plt, "model_reason_distribution", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # CSVファイルからデータを読み込む
    df = pd.read_csv(f"{OUTPUT_DIR}/model_reason.csv")

    # データをモデル順序に基づいて並べ替え
    filtered_data = df.set_index('model').reindex(MODEL_ORDER).reset_index()

    # 開発元情報を追加
    filtered_data['vendor'] = filtered_data['model'].apply(get_vendor)

    # 言語に応じたメッセージを読み込む
    # messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    # 言語に応じた理由文の定義を使用
    reasons = get_message('common.reason_dimensions', lang)

    # グラフを生成
    create_bar_plot(filtered_data, reasons, lang)
    create_distribution_plot(filtered_data, reasons, lang)
    create_sorted_all_plot(filtered_data, reasons, lang)
    create_sorted_individual_plots(filtered_data, reasons, lang)

    # 開発元ごとの平均値を計算して表示
    print("\n開発元ごとの理由文長平均値:")
    vendor_means = filtered_data.groupby('vendor')[list(reasons.keys())].mean()
    for vendor in vendor_means.index:
        print(f"\n{vendor}:")
        for col, label_dict in reasons.items():
            print(f"  {label_dict[lang]}: {vendor_means.loc[vendor, col]:.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason_distribution.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason_sorted_all.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'model_reason_sorted_all.svg')}")
    for i in range(1, 5):
        print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, f'model_reason_sorted_q{i}.png')}")
        print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, f'model_reason_sorted_q{i}.svg')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for model reason data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
