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
    messages = messages_full['text_emotion'][lang]
    fig, gs = setup_figure()
    ax = fig.add_subplot(111)

    # グラフ上部のテキスト
    add_header_text(ax, messages['header_text'])

    # 言語に応じた感情次元の定義を使用
    emotions = messages_full['common']['emotion_dimensions']
    
    # 感情次元ごとの色をseabornのデフォルトパレットから取得
    # 感情次元の数に合わせて色を生成
    num_emotions = len(emotions)
    colors = sns.color_palette(n_colors=num_emotions)
    
    # 感情次元ごとの透明度を設定 (必要であれば調整)
    # alphas = [0.4, 0.6, 0.8, 1.0] # 今回は使用しないか、colorsに直接alphaを含める

    # 各文学作品のデータをプロット
    bar_width = 0.2
    x = range(len(texts))
    
    # 各感情次元のデータを計算
    for i, (col, label_dict) in enumerate(emotions.items()):
        label = label_dict[lang] # 言語に応じたラベルを取得
        values = []
        for text_name in texts:
            # text_mappingが辞書を返すように変更されたため、対応するキーを検索
            text_id = [k for k, v in messages_full['common']['text_mapping'].items() if v[lang] == text_name][0]
            value = data[data['text'] == text_id][col].mean()
            values.append(value)
        
        # alphaはcolorsに含めず、別途設定する場合はここで適用
        bars = ax.bar([p + i * bar_width for p in x], values, bar_width,
                      label=label, color=colors[i]) # alphaはcolorsに含めない
        
        # 値のラベルを表示
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{height:.1f}', ha='center', va='bottom')

    # グラフの設定
    ax.set_xlabel(messages['xlabel'], fontsize=14)
    ax.set_ylabel(messages['ylabel'], fontsize=14)
    ax.set_title(messages['bar_plot_title'], fontsize=16)
    ax.set_xticks([p + 1.5 * bar_width for p in x])
    ax.set_xticklabels(texts, fontsize=12)
    ax.tick_params(axis='y', labelsize=12) # Y軸目盛りラベルのフォントサイズ
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['emotion_legend_title'], title_fontsize=13, fontsize=12)

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "text_emotion", lang=lang)
    plt.close()

def create_distribution_plot(data, texts, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    messages_full = load_messages(lang)
    messages = messages_full['text_emotion'][lang]
    fig, gs = setup_figure()
    ax = fig.add_subplot(111)

    # 言語に応じた感情次元の定義を使用
    emotions = messages_full['common']['emotion_dimensions']
    
    # データを縦持ちに変換
    # value_mappingを言語に応じたものに変換
    emotion_value_mapping = {k: v[lang] for k, v in emotions.items()}
    melted_data = create_melted_data(data, 
                                     id_vars=['text'],
                                     value_vars=list(emotions.keys()),
                                     value_mapping=emotion_value_mapping)

    # テキスト識別子を言語別名に変換
    # text_mappingが辞書を返すように変更されたため、mapに渡す辞書も言語に応じたものに変換
    text_mapping_for_map = {k: v[lang] for k, v in messages_full['common']['text_mapping'].items()}
    melted_data['text'] = melted_data['text'].map(text_mapping_for_map)
    melted_data['text'] = pd.Categorical(melted_data['text'], categories=texts, ordered=True)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='text', y='value', hue='emotion',
                  ax=ax, inner=None, fill=False, linewidth=2.0)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='text', y='value', hue='emotion',
                  ax=ax, dodge=True, size=3, alpha=0.4)

    # グラフの設定
    ax.set_title(messages['distribution_plot_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    ax.set_xlabel(messages['emotion_xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    ax.set_ylabel(messages['emotion_ylabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    ax.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize']) # X軸目盛りラベルのフォントサイズ
    ax.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize']) # Y軸目盛りラベルのフォントサイズ
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title=messages['emotion_legend_title'], title_fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'], fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'], bbox_to_anchor=(1.05, 1), loc='upper left')

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
    # text_mappingが辞書を返すように変更されたため、values()ではなく、言語に応じた値のリストを取得
    texts = [v[lang] for v in messages_full['common']['text_mapping'].values()]

    # 2つのグラフを生成
    create_bar_plot(df, texts, lang)
    create_distribution_plot(df, texts, lang)

    # 文学作品ごとの平均値を表示
    print("\n文学作品ごとの感情次元平均値:")
    messages = messages_full['text_emotion'][lang]
    emotions = messages_full['common']['emotion_dimensions']
    for text_name in texts:
        print(f"\n{text_name}:")
        # text_mappingが辞書を返すように変更されたため、対応するキーを検索
        text_id = [k for k, v in messages_full['common']['text_mapping'].items() if v[lang] == text_name][0]
        text_data = df[df['text'] == text_id]
        for col, label_dict in emotions.items():
            label = label_dict[lang] # 言語に応じたラベルを取得
            print(f"  {label}: {text_data[col].mean():.2f}")

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n言語 {lang} のグラフを保存しました:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion.pdf')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion_distribution.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', lang_dir, 'text_emotion_distribution.pdf')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for text emotion data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
