import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.preprocessing import StandardScaler
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure
)

# テキスト識別子から日本語名へのマッピング
TEXT_MAPPING = {
    't1': '懐中時計',
    't2': 'お金とピストル',
    't3': 'ぼろぼろな駝鳥'
}

# 理由文の種類の定義
REASON_DIMENSIONS = {
    'Q1reason': '面白さの理由',
    'Q2reason': '驚きの理由',
    'Q3reason': '悲しみの理由',
    'Q4reason': '怒りの理由'
}

def create_correlation_heatmap(reason_trends):
    """文学作品間の相関分析とヒートマップの作成"""
    # 文学作品間の相関係数を計算
    corr = reason_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title('文学作品間の理由文長相関', pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'text_reason_correlation')
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'text_reason_correlation.csv'))
    return corr

def analyze_reason_patterns(reason_trends):
    """理由文長パターンの詳細分析"""
    pattern_analysis = {}
    
    # 各文学作品の理由文長パターンを分析
    for text in reason_trends.index:
        values = reason_trends.loc[text]
        pattern_analysis[text] = {
            'longest_reason': REASON_DIMENSIONS[values.idxmax()],
            'max_length': values.max(),
            'shortest_reason': REASON_DIMENSIONS[values.idxmin()],
            'min_length': values.min(),
            'mean_length': values.mean(),
            'std_length': values.std(),
            'length_profile': {
                REASON_DIMENSIONS[col]: float(values[col])
                for col in REASON_DIMENSIONS.keys()
            }
        }
    
    return pattern_analysis

def visualize_reason_patterns(reason_trends):
    """理由文長パターンの可視化"""
    # データの準備
    data = reason_trends.copy()
    data.columns = [REASON_DIMENSIONS[col] for col in data.columns]
    
    # レーダーチャートの作成
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # 文学作品ごとのカラー設定
    colors = ['#4285F4', '#EA4335', '#34A853']
    
    # 感情次元の数
    categories = list(data.columns)
    num_vars = len(categories)
    
    # 角度の計算
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    angles += angles[:1]
    
    # プロットの初期化
    ax = plt.subplot(111, projection='polar')
    
    # 各文学作品のプロット
    for idx, (text, values) in enumerate(data.iterrows()):
        values_list = values.tolist()
        values_list += values_list[:1]
        ax.plot(angles, values_list, 'o-', linewidth=2, label=text, color=colors[idx])
        ax.fill(angles, values_list, alpha=0.25, color=colors[idx])
    
    # レーダーチャートの設定
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title('文学作品ごとの理由文長パターン')
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # 保存
    save_figure(plt, 'text_reason_patterns')
    plt.close()

def print_pattern_analysis(pattern_analysis):
    """理由文長パターン分析結果の表示"""
    print("\n文学作品ごとの理由文長パターン分析:")
    for text, analysis in pattern_analysis.items():
        print(f"\n{text}:")
        print(f"  最も長い理由: {analysis['longest_reason']} ({analysis['max_length']:.2f}文字)")
        print(f"  最も短い理由: {analysis['shortest_reason']} ({analysis['min_length']:.2f}文字)")
        print(f"  平均文字数: {analysis['mean_length']:.2f}")
        print(f"  文字数の標準偏差: {analysis['std_length']:.2f}")
        print("  理由文長プロファイル:")
        for reason, length in analysis['length_profile'].items():
            print(f"    {reason}: {length:.2f}文字")

def print_generated_files():
    """生成されたファイルの一覧を表示"""
    print("\n生成されたファイル:")
    print("\n1. 相関分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'text_reason_correlation.csv')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_reason_correlation.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_reason_correlation.svg')}")
    
    print("\n2. 理由文長パターン分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_reason_patterns.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_reason_patterns.svg')}")

def main():
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    print("理由文長データを読み込んでいます...")
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'text_reason.csv'))
    
    # モデルごとの平均を計算し、文学作品をインデックスとして設定
    reason_trends = df.groupby('text')[list(REASON_DIMENSIONS.keys())].mean()
    # テキスト識別子を日本語名に変換
    reason_trends.index = reason_trends.index.map(TEXT_MAPPING)
    
    print("相関分析を実行中...")
    corr = create_correlation_heatmap(reason_trends)
    
    print("理由文長パターンを分析中...")
    pattern_analysis = analyze_reason_patterns(reason_trends)
    
    print("理由文長パターンを可視化中...")
    visualize_reason_patterns(reason_trends)
    
    # 結果の表示
    print_pattern_analysis(pattern_analysis)
    
    print("\n分析が完了しました。")
    print(f"結果は '{OUTPUT_DIR}' ディレクトリに保存されました。")
    print_generated_files()

if __name__ == "__main__":
    main()
