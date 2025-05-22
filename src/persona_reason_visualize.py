import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, REASON_DIMENSIONS, PERSONA_MAPPING,
    ensure_output_directories, save_figure
)

def create_bar_plot(data, personas):
    """棒グラフによる理由文長の比較を作成"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # グラフ上部のテキスト
    header_text = '※各ペルソナの棒グラフは左から順に: 面白さ（薄）→ 驚き → 悲しみ → 怒り（濃）'
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
    
    # 各理由文の文字数を計算
    for i, (col, label) in enumerate(REASON_DIMENSIONS.items()):
        values = []
        for persona_jp in personas:
            persona_id = [k for k, v in PERSONA_MAPPING.items() if v == persona_jp][0]
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
    ax.set_xlabel('ペルソナ')
    ax.set_ylabel('文字数')
    ax.set_title('ペルソナごとの理由文長の比較')
    ax.set_xticks([p + 1.5 * bar_width for p in x])
    ax.set_xticklabels(personas)
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title='理由の種類')

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_reason")
    plt.close()

def create_distribution_plot(data, personas):
    """バイオリンプロットとスウォームプロットによる分布の可視化"""
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])

    # データを縦持ちに変換
    melted_data = pd.melt(data, 
                         id_vars=['persona'],
                         value_vars=list(REASON_DIMENSIONS.keys()),
                         var_name='reason_type',
                         value_name='length')

    # ペルソナ識別子を日本語名に変換
    melted_data['persona'] = melted_data['persona'].map(PERSONA_MAPPING)
    
    # 理由ラベルを日本語に変換
    melted_data['reason_type'] = melted_data['reason_type'].map(REASON_DIMENSIONS)
    melted_data['persona'] = pd.Categorical(melted_data['persona'], categories=personas, ordered=True)

    # バイオリンプロット
    sns.violinplot(data=melted_data, x='persona', y='length', hue='reason_type',
                  ax=ax, inner=None, fill=False, linewidth=2.0)

    # スウォームプロット
    sns.swarmplot(data=melted_data, x='persona', y='length', hue='reason_type',
                  ax=ax, dodge=True, size=3, alpha=0.4)

    # グラフの設定
    ax.set_title('ペルソナごとの理由文長の分布と個別データ点')
    ax.set_xlabel('ペルソナ')
    ax.set_ylabel('文字数')
    ax.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    ax.legend(title='理由の種類', bbox_to_anchor=(1.05, 1), loc='upper left')

    # レイアウトの調整
    plt.tight_layout()
    save_figure(plt, "persona_reason_distribution")
    plt.close()

def main():
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # データの読み込み
    df = pd.read_csv(f"{OUTPUT_DIR}/persona_reason.csv")
    
    # ペルソナの順序を定義
    personas = ['大学1年生', '文学研究者', '感情豊かな詩人', '無感情なロボット']

    # 2つのグラフを生成
    create_bar_plot(df, personas)
    create_distribution_plot(df, personas)

    # ペルソナごとの平均値を表示
    print("\nペルソナごとの理由文長平均値:")
    for persona_jp in personas:
        print(f"\n{persona_jp}:")
        persona_id = [k for k, v in PERSONA_MAPPING.items() if v == persona_jp][0]
        persona_data = df[df['persona'] == persona_id]
        for col, label in REASON_DIMENSIONS.items():
            print(f"  {label}: {persona_data[col].mean():.2f}")

    print("\nグラフを保存しました:")
    print(f"- {OUTPUT_DIR}/figures/persona_reason.png")
    print(f"- {OUTPUT_DIR}/figures/persona_reason.svg")
    print(f"- {OUTPUT_DIR}/figures/persona_reason_distribution.png")
    print(f"- {OUTPUT_DIR}/figures/persona_reason_distribution.svg")

if __name__ == "__main__":
    main()
