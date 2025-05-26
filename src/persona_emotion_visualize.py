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
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = messages['header_text']
    ax.text(0.5, 1.05, header_text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 各ペルソナのデータをプロット
    bar_width = 0.2
    x = range(len(personas))
    
    # 言語に応じた感情次元の定義を使用
    # load_messagesから取得したmessages['emotion_dimensions']を使用
    emotions_for_bar_plot = messages['emotion_dimensions']

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
                   f'{height:.1f}', ha='center', va='bottom')
        
        # 感情次元ごとに最初のバーのみを凡例用に保存
        emotion_bars.append(emotion_bars_group[0])
        emotion_labels.append(label)

    # グラフの設定
    ax.set_xlabel(messages['xlabel'])
    ax.set_ylabel(messages['ylabel'])
    ax.set_title(messages['bar_plot_title'])
    ax.set_xticks([p + 1.5 * bar_width for p in x])
    ax.set_xticklabels(personas)
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 凡例を手動で作成
    ax.legend(emotion_bars, emotion_labels, title=messages['emotion_legend_title'])

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_emotion", lang=lang)
    plt.close()

def create_distribution_plot(data, personas, lang='ja'):
    """バイオリンプロットとスウォームプロットによる分布の可視化 (ファセットグリッド使用)"""
    messages = load_messages(lang)
    
    emotions_dict = messages['emotion_dimensions']
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
    def plot_persona_emotion(data, **kwargs): # data_subsetをdataに変更
        persona_id = data['persona'].iloc[0] # サブセットからペルソナIDを取得
        base_color_hex = PERSONA_COLORS[persona_id]
        
        # 感情次元の明度グラデーションパレットを動的に生成
        emotion_palette = [get_emotion_color_from_persona_base(base_color_hex, i) for i in range(len(value_vars))]
        
        ax = plt.gca() # 現在のサブプロットのAxesを取得
        
        sns.violinplot(data=data, x='emotion', y='value', hue='emotion', # hue='emotion' を再度追加
                       ax=ax, inner=None, fill=False, linewidth=2.0,
                       palette=emotion_palette,
                       order=emotion_order, legend=False, dodge=False) # dodge=False を追加

        sns.swarmplot(data=data, x='emotion', y='value', hue='emotion', # hue='emotion' を再度追加
                      ax=ax, dodge=False, size=3, alpha=0.4, # dodge=False に変更
                      palette=emotion_palette,
                      order=emotion_order, legend=False)
        
        ax.set_xlabel(messages['emotion_xlabel'])
        ax.set_ylabel(messages['emotion_ylabel'])
        ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
        
        # 凡例はFacetGridの外部で一括して作成するため、ここでは設定しない
        ax.get_legend().remove() if ax.get_legend() else None

    g.map_dataframe(plot_persona_emotion)

    # 各サブプロットのタイトルを設定
    g.set_titles(col_template="{col_name}")

    # 全体のタイトルを設定
    g.fig.suptitle(messages['distribution_plot_title'], y=1.02) # yを調整してタイトルが重ならないようにする

    # 共通の凡例を作成
    # 凡例用のダミープロットを作成
    handles = []
    labels = []
    for i, emotion_label in enumerate(emotion_order):
        # 任意のペルソナの基調色（例: p1）を使って凡例の色を生成
        dummy_color = get_emotion_color_from_persona_base(PERSONA_COLORS['p1'], i)
        handles.append(plt.Rectangle((0,0),1,1, color=dummy_color))
        labels.append(emotion_label)
    
    g.fig.legend(handles, labels, title=messages['emotion_legend_title'], 
                 bbox_to_anchor=(1.02, 0.95), loc='upper left', borderaxespad=0.)

    plt.tight_layout(rect=[0, 0, 1, 0.98]) # タイトルと凡例のためにレイアウトを調整
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
