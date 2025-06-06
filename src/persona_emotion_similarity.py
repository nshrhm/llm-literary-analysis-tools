import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os
import json
import argparse
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, CLUSTERING_CONFIG,
    ensure_output_directories, save_figure, get_message,
    PERSONA_COLORS
)


def create_correlation_heatmap(emotion_trends, lang='ja'):
    """ペルソナ間の相関分析とヒートマップの作成"""
    # ペルソナ間の相関係数を計算
    corr = emotion_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    # 相関係数を可視化（0.995-1.000の範囲で赤のグラデーション）
    sns.heatmap(corr, 
                annot=True, 
                cmap='Reds',
                vmin=0.995,
                vmax=1.0,
                fmt='.4f', 
                square=True)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'persona_emotion_correlation', lang=lang)
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'persona_emotion_correlation.csv'))
    return corr

def analyze_emotion_patterns(emotion_trends, lang='ja'):
    """感情パターンの詳細分析"""
    pattern_analysis = {}
    emotion_dimensions = get_message('common.emotion_dimensions')
    
    # 各ペルソナの感情パターンを分析
    for persona in emotion_trends.index:
        values = emotion_trends.loc[persona]
        pattern_analysis[persona] = {
            'dominant_emotion': emotion_dimensions[values.idxmax()][lang],
            'max_value': values.max(),
            'min_emotion': emotion_dimensions[values.idxmin()][lang],
            'min_value': values.min(),
            'mean_value': values.mean(),
            'std_value': values.std(),
            'emotion_profile': {
                emotion_dimensions[col][lang]: float(values[col])
                for col in emotion_dimensions.keys()
            }
        }
    
    return pattern_analysis

def visualize_emotion_patterns(emotion_trends, lang='ja'):
    """感情パターンの可視化"""
    # データの準備
    data = emotion_trends.copy()
    analysis_messages = get_message(f'persona_emotion_analysis.{lang}', lang='')
    plot_messages = get_message(f'persona_emotion.{lang}', lang='')
    emotion_dimensions = get_message('common.emotion_dimensions')
    data.columns = [emotion_dimensions[col][lang] for col in data.columns]
    
    # ペルソナごとのカラー設定をconfigから取得
    colors = [PERSONA_COLORS[f'p{i+1}'] for i in range(len(PERSONA_COLORS))]
    
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
        ax.plot(angles, values_list, 'o-', linewidth=2.5, label=persona, color=colors[idx % len(colors)], markersize=6)
    
    # レーダーチャートの設定
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), title=plot_messages['legend_title'])
    
    # 保存
    save_figure(plt, 'persona_emotion_patterns', lang=lang)
    plt.close()

def print_pattern_analysis(pattern_analysis, lang='ja'):
    """感情パターン分析結果の表示"""
    analysis_messages = get_message(f'persona_emotion_analysis.{lang}', lang='')
    print(f"\n{analysis_messages['header_text']}")
    for persona, analysis in pattern_analysis.items():
        print(f"\n{persona}:")
        
        print(f"  {analysis_messages['dominant_text']}: {analysis['dominant_emotion']} ({analysis['max_value']:.2f})")
        print(f"  {analysis_messages['min_text']}: {analysis['min_emotion']} ({analysis['min_value']:.2f})")
        print(f"  {analysis_messages['mean_text']}: {analysis['mean_value']:.2f}")
        print(f"  {analysis_messages['std_text']}: {analysis['std_value']:.2f}")
        print(f"  {analysis_messages['profile_text']}:")
        for emotion, value in analysis['emotion_profile'].items():
            print(f"    {emotion}: {value:.2f}")

def print_generated_files(lang='ja'):
    """生成されたファイルの一覧を表示"""
    analysis_messages = get_message(f'persona_emotion_analysis.{lang}', lang='')
    
    print(f"\n{analysis_messages['generated_files']}")
    print(f"\n{analysis_messages['correlation_files']}")
    print(f"- {os.path.join(OUTPUT_DIR, 'persona_emotion_correlation.csv')}")
    figures_dir = os.path.join(OUTPUT_DIR, 'figures', lang)
    print(f"- {os.path.join(figures_dir, 'persona_emotion_correlation.png')}")
    print(f"- {os.path.join(figures_dir, 'persona_emotion_correlation.pdf')}")
    
    print(f"\n{analysis_messages['pattern_files']}")
    print(f"- {os.path.join(figures_dir, 'persona_emotion_patterns.png')}")
    print(f"- {os.path.join(figures_dir, 'persona_emotion_patterns.pdf')}")

def main(lang='ja'):
    # 言語に応じてmatplotlibの設定を行う
    if lang == 'ja':
        import japanize_matplotlib

    # 出力ディレクトリの作成
    ensure_output_directories()
    
    # メッセージの取得
    analysis_messages = get_message(f'persona_emotion_analysis.{lang}', lang='')
    
    print(analysis_messages['loading_text'])
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'persona_emotion.csv'))
    
    # 感情次元とペルソナのマッピングを取得
    emotion_dimensions = get_message('common.emotion_dimensions', lang='')
    persona_mapping = get_message('common.persona_mapping', lang='')
    
    # 感情次元の列でグループ化して平均を計算
    emotion_trends = df.groupby('persona')[list(emotion_dimensions.keys())].mean()
    # ペルソナ識別子を言語に応じた名前に変換
    emotion_trends.index = emotion_trends.index.map(lambda x: persona_mapping[x][lang])
    
    print(analysis_messages['correlation_text'])
    corr = create_correlation_heatmap(emotion_trends, lang)
    
    print(analysis_messages['pattern_text'])
    pattern_analysis = analyze_emotion_patterns(emotion_trends, lang)
    
    print(analysis_messages['visualization_text'])
    visualize_emotion_patterns(emotion_trends, lang)
    
    # 結果の表示
    print_pattern_analysis(pattern_analysis, lang)
    
    print(f"\n{analysis_messages['completion_text']}")
    print(analysis_messages['save_text'].format(OUTPUT_DIR))
    print_generated_files(lang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate similarity analysis visualizations.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
