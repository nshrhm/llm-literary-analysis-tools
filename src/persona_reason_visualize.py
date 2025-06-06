import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import json
import argparse
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure, create_melted_data, setup_figure, add_header_text
)


def load_messages(lang):
    """言語に応じたメッセージと共通メッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages

def create_bar_plot(data, personas, lang='ja'):
    """棒グラフによる理由文長の比較を作成"""
    messages_full = load_messages(lang)
    messages = messages_full['persona_reason'][lang]
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = messages['header_text']
    ax.text(0.5, 1.05, header_text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 感情次元ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く
    colors = ['#4285F4', '#4285F4', '#4285F4', '#4285F4']  # 統一的な色使い

    # 各ペルソナのデータをプロット
    bar_width = 0.2
    x = range(len(personas))
    
    # 共通メッセージからreason_dimensionsを読み込む（言語別）
    reason_dimensions_raw = messages_full['common']['reason_dimensions']
    reason_dimensions = {k: v[lang] for k, v in reason_dimensions_raw.items()}
    
    # 各理由文の文字数を計算
    for i, (col, label) in enumerate(reason_dimensions.items()):
        values = []
        for persona_name in personas:
            # persona_mapping逆引きのため、言語別の値を使用
            persona_mapping = {v[lang]: k for k, v in messages_full['common']['persona_mapping'].items()}
            persona_id = persona_mapping[persona_name]
            value = data[data['persona'] == persona_id][col].mean()
            values.append(value)
        
        bars = ax.bar([p + i * bar_width for p in x], values, bar_width,
                      label=label, alpha=alphas[i], color=colors[i])
        
        # 値のラベルを表示
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{height:.1f}', ha='center', va='bottom')

    # グラフの設定
    ax.set_xlabel(messages['xlabel'])
    ax.set_ylabel(messages['ylabel'])
    ax.set_title(messages['bar_plot_title'])
    ax.set_xticks([p + 1.5 * bar_width for p in x])
    ax.set_xticklabels(personas)
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['reason_legend_title'])

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_reason", lang=lang)
    plt.close()

def create_distribution_plot(data, personas, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages_full = load_messages(lang)
    messages = messages_full['persona_reason'][lang]
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    reason_dimensions_raw = messages_full['common']['reason_dimensions']
    reason_dimensions = {k: v[lang] for k, v in reason_dimensions_raw.items()}
    melted_data = pd.melt(data, 
                         id_vars=['persona'],
                         value_vars=list(reason_dimensions_raw.keys()),
                         var_name='reason_type',
                         value_name='length')

    # ペルソナ識別子を言語別名に変換
    persona_mapping = {k: v[lang] for k, v in messages_full['common']['persona_mapping'].items()}
    melted_data['persona'] = melted_data['persona'].map(persona_mapping)
    
    # 理由ラベルを変換
    melted_data['reason_type'] = melted_data['reason_type'].map(reason_dimensions)
    melted_data['persona'] = pd.Categorical(melted_data['persona'], categories=personas, ordered=True)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='persona', y='length', hue='reason_type',
                  ax=ax, inner=None, fill=False, linewidth=2.0)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='persona', y='length', hue='reason_type',
                  ax=ax, dodge=True, size=3, alpha=0.4)

    # グラフの設定
    ax.set_title(messages['distribution_plot_title'])
    ax.set_xlabel(messages['xlabel'])
    ax.set_ylabel(messages['ylabel'])
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['reason_legend_title'], bbox_to_anchor=(1.05, 1), loc='upper left')

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_reason_distribution", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # データの読み込み
    df = pd.read_csv(f"{OUTPUT_DIR}/persona_reason.csv")
    
    # ペルソナの順序を定義（言語に応じて）
    messages_full = load_messages(lang)
    persona_mapping = {k: v[lang] for k, v in messages_full['common']['persona_mapping'].items()}
    personas = list(persona_mapping.values())

    # 2つのグラフを生成
    create_bar_plot(df, personas, lang)
    create_distribution_plot(df, personas, lang)

    # ペルソナごとの平均値を表示
    print("\nペルソナごとの理由文長平均値:")
    # 言語に応じたメッセージと共通メッセージを読み込む
    messages_full = load_messages(lang)
    messages = messages_full['persona_reason'][lang]
    reason_dimensions_raw = messages_full['common']['reason_dimensions']
    reason_dimensions = {k: v[lang] for k, v in reason_dimensions_raw.items()}
    for persona_name in personas:
        print(f"\n{persona_name}:")
        # persona_mapping逆引き辞書を使用
        persona_id_mapping = {v[lang]: k for k, v in messages_full['common']['persona_mapping'].items()}
        persona_id = persona_id_mapping[persona_name]
        persona_data = df[df['persona'] == persona_id]
        for col, label in reason_dimensions.items():
            print(f"  {label}: {persona_data[col].mean():.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_reason.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_reason.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_reason_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_reason_distribution.svg')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for persona reason data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
