import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import json
import argparse
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure, create_melted_data, setup_figure, add_header_text, get_message
)

def load_messages(lang):
    """言語に応じたメッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    combined_messages = messages[lang]['persona_emotion'].copy()
    combined_messages['persona_mapping'] = get_message('common.persona_mapping', lang)
    combined_messages['emotion_dimensions'] = get_message('common.emotion_dimensions', lang)
    return combined_messages

def create_bar_plot(data, personas, lang='ja'):
    """棒グラフによる感情次元の平均値比較を作成"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
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
    
    # 言語に応じた感情次元の定義を使用
    emotions = get_message('common.emotion_dimensions', lang)

    # 各感情次元のデータを計算
    for i, (col, label) in enumerate(emotions.items()):
        values = []
        for persona_name in personas:
            persona_id = [k for k, v in messages['persona_mapping'].items() if v == persona_name][0]
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
    ax.legend(title=messages['emotion_legend_title'])

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_emotion", lang=lang)
    plt.close()

def create_distribution_plot(data, personas, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    emotions = get_message('common.emotion_dimensions', lang)
    melted_data = create_melted_data(data, 
                                   id_vars=['persona'],
                                   value_vars=list(emotions.keys()),
                                   value_mapping=emotions)

    # ペルソナ識別子を言語に応じた名前に変換
    melted_data['persona'] = melted_data['persona'].map(messages['persona_mapping'])
    melted_data['persona'] = pd.Categorical(melted_data['persona'], categories=personas, ordered=True)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='persona', y='value', hue='emotion',
                  ax=ax, inner=None, fill=False, linewidth=2.0)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='persona', y='value', hue='emotion',
                  ax=ax, dodge=True, size=3, alpha=0.4)

    # グラフの設定
    ax.set_title(messages['distribution_plot_title'])
    ax.set_xlabel(messages['emotion_xlabel'])
    ax.set_ylabel(messages['emotion_ylabel'])
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['emotion_legend_title'], bbox_to_anchor=(1.05, 1), loc='upper left')

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_emotion_distribution", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # データの読み込み
    df = pd.read_csv(f"{OUTPUT_DIR}/persona_emotion.csv")
    
    # 言語に応じたメッセージを読み込む
    messages = load_messages(lang)

    # ペルソナの順序を定義（言語に応じて）
    personas = list(messages['persona_mapping'].values())

    # 2つのグラフを生成
    create_bar_plot(df, personas, lang)
    create_distribution_plot(df, personas, lang)

    # ペルソナごとの平均値を表示
    print("\nペルソナごとの感情次元平均値:")
    emotions = get_message('common.emotion_dimensions', lang)
    for persona_jp in personas:
        print(f"\n{persona_jp}:")
        persona_id = [k for k, v in messages['persona_mapping'].items() if v == persona_jp][0]
        persona_data = df[df['persona'] == persona_id]
        for col, label in emotions.items():
            print(f"  {label}: {persona_data[col].mean():.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_emotion.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_emotion.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_emotion_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'persona_emotion_distribution.svg')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for persona emotion data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
