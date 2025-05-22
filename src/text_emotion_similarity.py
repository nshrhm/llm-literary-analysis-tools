import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.preprocessing import StandardScaler
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, EMOTION_DIMENSIONS,
    ensure_output_directories, save_figure
)

# テキスト識別子から日本語名へのマッピング
TEXT_MAPPING = {
    't1': '懐中時計',
    't2': 'お金とピストル',
    't3': 'ぼろぼろな駝鳥'
}

def create_correlation_heatmap(emotion_trends):
    """文学作品間の相関分析とヒートマップの作成"""
    # 文学作品間の相関係数を計算
    corr = emotion_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title('文学作品間の感情評価相関', pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'text_emotion_correlation')
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'text_emotion_correlation.csv'))
    return corr

def analyze_emotion_patterns(emotion_trends):
    """感情パターンの詳細分析"""
    pattern_analysis = {}
    
    # 各文学作品の感情パターンを分析
    for text in emotion_trends.index:
        values = emotion_trends.loc[text]
        pattern_analysis[text] = {
            'dominant_emotion': EMOTION_DIMENSIONS[values.idxmax()],
            'max_value': values.max(),
            'min_emotion': EMOTION_DIMENSIONS[values.idxmin()],
            'min_value': values.min(),
            'mean_value': values.mean(),
            'std_value': values.std(),
            'emotion_profile': {
                EMOTION_DIMENSIONS[col]: float(values[col])
                for col in EMOTION_DIMENSIONS.keys()
            }
        }
    
    return pattern_analysis

def visualize_emotion_patterns(emotion_trends):
    """感情パターンの可視化"""
    # データの準備
    data = emotion_trends.copy()
    data.columns = [EMOTION_DIMENSIONS[col] for col in data.columns]
    
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
    ax.set_title('文学作品ごとの感情パターン')
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # 保存
    save_figure(plt, 'text_emotion_patterns')
    plt.close()

def print_pattern_analysis(pattern_analysis):
    """感情パターン分析結果の表示"""
    print("\n文学作品ごとの感情パターン分析:")
    for text, analysis in pattern_analysis.items():
        print(f"\n{text}:")
        print(f"  主要な感情: {analysis['dominant_emotion']} ({analysis['max_value']:.2f})")
        print(f"  最も弱い感情: {analysis['min_emotion']} ({analysis['min_value']:.2f})")
        print(f"  平均感情値: {analysis['mean_value']:.2f}")
        print(f"  感情値の標準偏差: {analysis['std_value']:.2f}")
        print("  感情プロファイル:")
        for emotion, value in analysis['emotion_profile'].items():
            print(f"    {emotion}: {value:.2f}")

def print_generated_files():
    """生成されたファイルの一覧を表示"""
    print("\n生成されたファイル:")
    print("\n1. 相関分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'text_emotion_correlation.csv')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_emotion_correlation.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_emotion_correlation.svg')}")
    
    print("\n2. 感情パターン分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_emotion_patterns.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'text_emotion_patterns.svg')}")

def main():
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    print("感情評価データを読み込んでいます...")
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'text_emotion.csv'))
    
    # モデルごとの平均を計算し、文学作品をインデックスとして設定
    emotion_trends = df.groupby('text')[list(EMOTION_DIMENSIONS.keys())].mean()
    # テキスト識別子を日本語名に変換
    emotion_trends.index = emotion_trends.index.map(TEXT_MAPPING)
    
    print("相関分析を実行中...")
    corr = create_correlation_heatmap(emotion_trends)
    
    print("感情パターンを分析中...")
    pattern_analysis = analyze_emotion_patterns(emotion_trends)
    
    print("感情パターンを可視化中...")
    visualize_emotion_patterns(emotion_trends)
    
    # 結果の表示
    print_pattern_analysis(pattern_analysis)
    
    print("\n分析が完了しました。")
    print(f"結果は '{OUTPUT_DIR}' ディレクトリに保存されました。")
    print_generated_files()

if __name__ == "__main__":
    main()
