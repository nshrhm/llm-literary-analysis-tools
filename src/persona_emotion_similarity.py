import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.preprocessing import StandardScaler
import os
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, EMOTION_DIMENSIONS, PERSONA_MAPPING,
    ensure_output_directories, save_figure
)

def create_correlation_heatmap(emotion_trends):
    """ペルソナ間の相関分析とヒートマップの作成"""
    # ペルソナ間の相関係数を計算
    corr = emotion_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title('ペルソナ間の感情評価相関', pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'persona_emotion_correlation')
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'persona_emotion_correlation.csv'))
    return corr

def analyze_emotion_patterns(emotion_trends):
    """感情パターンの詳細分析"""
    pattern_analysis = {}
    
    # 各ペルソナの感情パターンを分析
    for persona in emotion_trends.index:
        values = emotion_trends.loc[persona]
        pattern_analysis[persona] = {
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
    
    # ペルソナごとのカラー設定
    colors = ['#4285F4', '#EA4335', '#34A853', '#FBBC05']  # 4つのペルソナ用に色を追加
    
    # 感情次元の数
    categories = list(data.columns)
    num_vars = len(categories)
    
    # 角度の計算
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    angles += angles[:1]
    
    # プロットの初期化
    ax = plt.subplot(111, projection='polar')
    
    # 各ペルソナのプロット
    for idx, (persona, values) in enumerate(data.iterrows()):
        values_list = values.tolist()
        values_list += values_list[:1]
        ax.plot(angles, values_list, 'o-', linewidth=2, label=persona, color=colors[idx])
        ax.fill(angles, values_list, alpha=0.25, color=colors[idx])
    
    # レーダーチャートの設定
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title('ペルソナごとの感情パターン')
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # 保存
    save_figure(plt, 'persona_emotion_patterns')
    plt.close()

def print_pattern_analysis(pattern_analysis):
    """感情パターン分析結果の表示"""
    print("\nペルソナごとの感情パターン分析:")
    for persona, analysis in pattern_analysis.items():
        print(f"\n{persona}:")
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
    print(f"- {os.path.join(OUTPUT_DIR, 'persona_emotion_correlation.csv')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'persona_emotion_correlation.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'persona_emotion_correlation.svg')}")
    
    print("\n2. 感情パターン分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'persona_emotion_patterns.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'persona_emotion_patterns.svg')}")

def main():
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    print("感情評価データを読み込んでいます...")
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'persona_emotion.csv'))
    
    # モデルごとの平均を計算し、ペルソナをインデックスとして設定
    emotion_trends = df.groupby('persona')[list(EMOTION_DIMENSIONS.keys())].mean()
    # ペルソナ識別子を日本語名に変換
    emotion_trends.index = emotion_trends.index.map(PERSONA_MAPPING)
    
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
