import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.preprocessing import StandardScaler
import os
import json
import argparse
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, CLUSTERING_CONFIG, TEXT_ORDER,
    ensure_output_directories, save_figure, safe_read_csv, get_message
)

def load_messages(lang='ja'):
    """言語に応じたメッセージを読み込む"""
    import json
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    # text_emotion_similarityセクションがない場合はデフォルトメッセージを使用
    if 'text_emotion_similarity' in messages and lang in messages['text_emotion_similarity']:
        combined_messages = messages['text_emotion_similarity'][lang].copy()
    else:
        # フォールバックとして基本的なメッセージを作成
        combined_messages = {
            'correlation_title': '文章間の感情評価相関' if lang == 'ja' else 'Correlation of Emotional Evaluations between Texts',
            'xlabel_pca': '第1主成分' if lang == 'ja' else 'First Principal Component',
            'ylabel_pca': '第2主成分' if lang == 'ja' else 'Second Principal Component',
            'pattern_title': '感情パターンの比較' if lang == 'ja' else 'Comparison of Emotional Patterns',
            'legend_title': '文学作品' if lang == 'ja' else 'Literary Works'
        }
    
    # text_mappingを言語固有の辞書に変換
    text_mapping_raw = get_message('common.text_mapping', lang)
    combined_messages['text_mapping'] = {k: v[lang] for k, v in text_mapping_raw.items()}
        
    return combined_messages


def create_correlation_heatmap(emotion_trends, lang='ja'):
    """文学作品間の相関分析とヒートマップの作成"""
    # 文学作品間の相関係数を計算
    corr = emotion_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    messages = load_messages(lang)
    plt.title(messages['correlation_title'], pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'text_emotion_correlation', lang=lang)
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'text_emotion_correlation.csv'))
    return corr

def analyze_emotion_patterns(emotion_trends, lang='ja'):
    """感情パターンの詳細分析"""
    pattern_analysis = {}
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    
    # emotion_dimensionsを言語固有の辞書に変換
    emotion_dimensions_raw = get_message('common.emotion_dimensions', lang)
    emotion_dimensions = {k: v[lang] for k, v in emotion_dimensions_raw.items()}
    
    # 各文学作品の感情パターンを分析
    for text in emotion_trends.index:
        values = emotion_trends.loc[text]
        pattern_analysis[text] = {
            'dominant_emotion': emotion_dimensions[values.idxmax()],
            'max_value': values.max(),
            'min_emotion': emotion_dimensions[values.idxmin()],
            'min_value': values.min(),
            'mean_value': values.mean(),
            'std_value': values.std(),
            'emotion_profile': {
                emotion_dimensions[col]: float(values[col])
                for col in emotion_dimensions.keys()
            }
        }
    
    return pattern_analysis

def visualize_emotion_patterns(emotion_trends, lang='ja'):
    """感情パターンの可視化"""
    # データの準備
    data = emotion_trends.copy()
    messages = load_messages(lang) # messagesは他の場所で使用されているため残す
    
    # emotion_dimensionsを言語固有の辞書に変換
    emotion_dimensions_raw = get_message('common.emotion_dimensions', lang)
    emotion_dimensions = {k: v[lang] for k, v in emotion_dimensions_raw.items()}
    
    data.columns = [emotion_dimensions[col] for col in data.columns]
    
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
    messages = load_messages(lang)
    ax.set_title(messages['pattern_title'])
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), title=messages['legend_title'])
    
    # 保存
    save_figure(plt, 'text_emotion_patterns', lang=lang)
    plt.close()

def print_pattern_analysis(pattern_analysis, lang='ja'):
    """感情パターン分析結果の表示"""
    messages = load_messages(lang)
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

def print_generated_files(lang='ja'):
    """生成されたファイルの一覧を表示"""
    print("\n生成されたファイル:")
    print("\n1. 相関分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'text_emotion_correlation.csv')}")
    figures_dir = os.path.join(OUTPUT_DIR, 'figures', lang)
    print(f"- {os.path.join(figures_dir, 'text_emotion_correlation.png')}")
    print(f"- {os.path.join(figures_dir, 'text_emotion_correlation.pdf')}")
    
    print("\n2. 感情パターン分析:")
    print(f"- {os.path.join(figures_dir, 'text_emotion_patterns.png')}")
    print(f"- {os.path.join(figures_dir, 'text_emotion_patterns.pdf')}")

def main(lang='ja'):
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    print("感情評価データを読み込んでいます...")
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'text_emotion.csv'))
    messages = load_messages(lang)
    
    # emotion_dimensionsを言語固有の辞書に変換
    emotion_dimensions_raw = get_message('common.emotion_dimensions', lang)
    emotion_dimensions = {k: v[lang] for k, v in emotion_dimensions_raw.items()}
    
    # モデルごとの平均を計算し、文学作品をインデックスとして設定
    emotion_trends = df.groupby('text')[list(emotion_dimensions.keys())].mean()
    # テキスト識別子を言語名に変換
    emotion_trends.index = emotion_trends.index.map(messages['text_mapping'])
    
    print("相関分析を実行中...")
    corr = create_correlation_heatmap(emotion_trends, lang)
    
    print("感情パターンを分析中...")
    pattern_analysis = analyze_emotion_patterns(emotion_trends, lang)
    
    print("感情パターンを可視化中...")
    visualize_emotion_patterns(emotion_trends, lang)
    
    # 結果の表示
    print_pattern_analysis(pattern_analysis, lang)
    
    print("\n分析が完了しました。")
    print(f"結果は '{OUTPUT_DIR}' ディレクトリに保存されました。")
    print_generated_files(lang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate similarity analysis visualizations.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
