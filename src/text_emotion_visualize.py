import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import json
import argparse
import os
from config import (
    OUTPUT_DIR, EMOTION_DIMENSIONS, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure, create_melted_data, setup_figure, add_header_text, get_message
)


def load_messages(lang):
    """言語に応じたメッセージと共通メッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages

def create_bar_plot(data, texts, lang='ja'):
    """棒グラフによる感情次元の平均値比較を作成"""
    messages_full = load_messages(lang)
    messages = messages_full[lang]['text_emotion']
    fig, gs = setup_figure()
    ax = fig.add_subplot(111)

    # グラフ上部のテキスト
    add_header_text(ax, messages['header_text'])

    # 言語に応じた感情次元の定義を使用
    emotions = messages_full['common']['emotion_dimensions']
    
    # 感情次元ごとの透明度を設定
    alphas = [0.4, 0.6, 0.8, 1.0]  # 面白さから怒りまで徐々に濃く
    colors = ['#4285F4', '#4285F4', '#4285F4', '#4285F4']  # 統一的な色使い

    # 各文学作品のデータをプロット
    bar_width = 0.2
    x = range(len(texts))
    
    # 各感情次元のデータを計算
    for i, (col, label) in enumerate(emotions.items()):
        values = []
        for text_name in texts:
            text_id = [k for k, v in messages_full['common']['text_mapping'].items() if v == text_name][0]
            value = data[data['text'] == text_id][col].mean()
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
    ax.set_xticklabels(texts)
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['emotion_legend_title'])

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "text_emotion", lang=lang)
    plt.close()

def create_distribution_plot(data, texts, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages_full = load_messages(lang)
    messages = messages_full[lang]['text_emotion']
    fig, gs = setup_figure()
    ax = fig.add_subplot(111)

    # 言語に応じた感情次元の定義を使用
    emotions = messages_full['common']['emotion_dimensions']
    
    # データを縦持ちに変換
    melted_data = create_melted_data(data, 
                                     id_vars=['text'],
                                     value_vars=list(emotions.keys()),
                                     value_mapping=emotions)

    # テキスト識別子を言語別名に変換
    melted_data['text'] = melted_data['text'].map(messages_full['common']['text_mapping'])
    melted_data['text'] = pd.Categorical(melted_data['text'], categories=texts, ordered=True)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='text', y='value', hue='emotion',
                  ax=ax, inner=None, fill=False, linewidth=2.0)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='text', y='value', hue='emotion',
                  ax=ax, dodge=True, size=3, alpha=0.4)

    # グラフの設定
    ax.set_title(messages['distribution_plot_title'])
    ax.set_xlabel(messages['emotion_xlabel'])
    ax.set_ylabel(messages['emotion_ylabel'])
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['emotion_legend_title'], bbox_to_anchor=(1.05, 1), loc='upper left')

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "text_emotion_distribution", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # データの読み込み
    df = pd.read_csv(f"{OUTPUT_DIR}/text_emotion.csv")
    
    # 文学作品の順序を定義（言語に応じて）
    messages_full = load_messages(lang)
    texts = list(messages_full['common']['text_mapping'].values())

    # 2つのグラフを生成
    create_bar_plot(df, texts, lang)
    create_distribution_plot(df, texts, lang)

    # 文学作品ごとの平均値を表示
    print("\n文学作品ごとの感情次元平均値:")
    messages = messages_full[lang]['text_emotion']
    emotions = messages_full['common']['emotion_dimensions']
    for text_name in texts:
        print(f"\n{text_name}:")
        text_id = [k for k, v in messages_full['common']['text_mapping'].items() if v == text_name][0]
        text_data = df[df['text'] == text_id]
        for col, label in emotions.items():
            print(f"  {label}: {text_data[col].mean():.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion_distribution.svg')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for text emotion data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
