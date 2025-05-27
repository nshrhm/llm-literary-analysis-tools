import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import json
import argparse
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, PERSONA_COLORS, # EMOTION_COLORSを削除
    ensure_output_directories, save_figure, create_melted_data, setup_figure, add_header_text, get_message,
    get_emotion_color_from_persona_base # 新しい関数を追加
)

def load_messages(lang):
    """言語に応じたメッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    # persona_emotionセクションからメッセージを取得
    combined_messages = messages['persona_emotion'][lang].copy()
    
    # common.persona_mappingの翻訳を処理
    if lang == 'en':
        # 英語の場合はpersona_model_emotionから英語名を取得
        combined_messages['persona_mapping'] = messages['persona_model_emotion']['en']['persona']
    else:
        # 日本語の場合は従来通り
        combined_messages['persona_mapping'] = messages['common']['persona_mapping']
    
    # emotion_dimensionsの言語別の値を取得
    combined_messages['emotion_dimensions'] = {
        k: v[lang] for k, v in messages['common']['emotion_dimensions'].items()
    }
    
    return combined_messages

def create_bar_plot(data, personas, lang='ja'):
    """棒グラフによる感情次元の平均値比較を作成"""
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    fig = plt.figure(figsize=(12.5, 8))  # 横幅を調整
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = messages['header_text']
    ax.text(0.5, 1.05, header_text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'),
            fontsize=20)  # ヘッダーテキストも大きく

    # 各ペルソナのデータをプロット
    bar_width = 0.2
    x = range(len(personas))
    
    # 言語に応じた感情次元の定義を確実に使用
    emotions_for_bar_plot = messages['emotion_dimensions']
    # print(f"Debug - Emotion dimensions for {lang}:", emotions_for_bar_plot)  # デバッグ出力を追加

    # 各感情次元のデータをプロット
    emotion_labels = []  # 凡例用のラベル
    emotion_bars = []    # 凡例用のバー
    
    for j, (col, label) in enumerate(emotions_for_bar_plot.items()):
        emotion_bars_group = []
        for i, persona_name in enumerate(personas):
            persona_id = [k for k, v in messages['persona_mapping'].items() if v == persona_name][0]
            value = data[data['persona'] == persona_id][col].mean()
            
            # バーを作成
            bar = ax.bar(i + j * bar_width, value, bar_width,
                      alpha=0.8, color=get_emotion_color_from_persona_base(PERSONA_COLORS[persona_id], j)) # 動的に色を生成
            emotion_bars_group.append(bar[0])
            
            # 値のラベルを表示
            height = value
            ax.text(i + j * bar_width + bar_width/2, height,
                   f'{height:.1f}', ha='center', va='bottom',
                   fontsize=14)  # バー上の数値も大きく
        
        # 感情次元ごとに最初のバーのみを凡例用に保存
        emotion_bars.append(emotion_bars_group[0])
        emotion_labels.append(label)

    # グラフの設定
    ax.set_xlabel(messages['xlabel'], fontsize=20)
    ax.set_ylabel(messages['ylabel'], fontsize=20)
    ax.set_xticks([p + 1.5 * bar_width for p in x])
    ax.set_xticklabels(personas, fontsize=16)
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 凡例を手動で作成
    ax.legend(emotion_bars, emotion_labels, 
             title=messages['emotion_legend_title'],
             fontsize=20,
             title_fontsize=24,
             bbox_to_anchor=(1.18, 1.0))  # 凡例の位置を調整

    # レイアウトの調整
    plt.subplots_adjust(bottom=0.15, left=0.15, right=0.9)  # 右側の余白を減らす
    save_figure(plt, "persona_emotion", lang=lang)
    plt.close()

def create_distribution_plot(data, personas, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化 (ファセットグリッド使用)"""
    messages = load_messages(lang)
    
    # 言語に応じた感情次元の定義を確実に使用
    emotions_dict = messages['emotion_dimensions']
    # print(f"Debug - Distribution emotion dimensions for {lang}:", emotions_dict)  # デバッグ出力を追加
    value_vars = list(emotions_dict.keys())
    
    melted_data = create_melted_data(data, 
                                   id_vars=['persona'],
                                   value_vars=value_vars,
                                   value_name='value',
                                   var_name='emotion_code')
    
    melted_data['emotion'] = melted_data['emotion_code'].map(emotions_dict)
    # NaN値を含む行を削除
    melted_data.dropna(subset=['emotion'], inplace=True)
    emotion_order = [emotions_dict[v] for v in value_vars]
    melted_data['emotion'] = pd.Categorical(
        melted_data['emotion'],
        categories=emotion_order,
        ordered=True
    )

    # ペルソナ識別子を言語に応じた名前に変換
    persona_mapping = messages['persona_mapping']
    melted_data['persona_display'] = melted_data['persona'].map(persona_mapping)

    # FacetGridを作成
    g = sns.FacetGrid(melted_data, col='persona_display', col_order=personas, col_wrap=2, height=6, aspect=1.2)

    # 各サブプロットにバイオリンプロットとスウォームプロットをマッピング
    def plot_persona_emotion(data, **kwargs):
        persona_id = data['persona'].iloc[0]
        base_color_hex = PERSONA_COLORS[persona_id]
        
        # すべての感情次元に対して最も暗い色を使用
        emotion_palette = [get_emotion_color_from_persona_base(base_color_hex, 0) for _ in range(len(value_vars))]
        
        ax = plt.gca()
        
        sns.violinplot(data=data, x='emotion', y='value', hue='emotion',
                      ax=ax, inner=None, fill=False, linewidth=2.0,
                      palette=emotion_palette,
                      order=emotion_order, legend=False, dodge=False)

        sns.swarmplot(data=data, x='emotion', y='value', hue='emotion',
                     ax=ax, dodge=False, size=3, alpha=0.4,
                     palette=emotion_palette,
                     order=emotion_order, legend=False)
        
        ax.set_xlabel(messages['emotion_xlabel'], fontsize=14)
        ax.set_ylabel(messages['emotion_ylabel'], fontsize=14)
        ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
        
        ax.get_legend().remove() if ax.get_legend() else None

    g.map_dataframe(plot_persona_emotion)

    # 各サブプロットのタイトルを設定
    g.set_titles(col_template="{col_name}", size=12)

    # 全体のタイトルを設定
    g.fig.suptitle(messages['distribution_plot_title'], y=1.02, fontsize=16)

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

    # バープロットのみ生成
    create_bar_plot(df, personas, lang)
    # create_distribution_plot(df, personas, lang)  # 一時的にコメントアウト

    # ペルソナごとの平均値を表示
    print("\nペルソナごとの感情次元平均値:")
    # load_messagesから取得したmessages['emotion_dimensions']を使用
    emotions_for_print = messages['emotion_dimensions']
    for persona_jp in personas:
        print(f"\n{persona_jp}:")
        persona_id = [k for k, v in messages['persona_mapping'].items() if v == persona_jp][0]
        persona_data = df[df['persona'] == persona_id]
        for col, label in emotions_for_print.items():
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
