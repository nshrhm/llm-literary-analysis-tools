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
    OUTPUT_DIR, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure
)

def load_messages(lang='ja'):
    """言語に応じたメッセージと共通メッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    # persona_reason_similarityメッセージと共通辞書を言語固有に変換
    combined_messages = messages['persona_reason_similarity'][lang].copy()
    
    # reason_dimensionsを言語固有の辞書に変換
    reason_dimensions_raw = messages['common']['reason_dimensions']
    combined_messages['reason_dimensions'] = {k: v[lang] for k, v in reason_dimensions_raw.items()}
    
    # persona_mappingを言語固有の辞書に変換
    persona_mapping_raw = messages['common']['persona_mapping']
    combined_messages['persona_mapping'] = {k: v[lang] for k, v in persona_mapping_raw.items()}
    
    return combined_messages

def create_correlation_heatmap(reason_trends, lang='ja'):
    """ペルソナ間の相関分析とヒートマップの作成"""
    # ペルソナ間の相関係数を計算
    corr = reason_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    messages = load_messages(lang)
    plt.title(messages['correlation_title'], pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'persona_reason_correlation', lang=lang)
    plt.close()
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'persona_reason_correlation.csv'))
    return corr

def analyze_reason_patterns(reason_trends, lang='ja'):
    """理由文長パターンの詳細分析"""
    pattern_analysis = {}
    messages = load_messages(lang)
    reason_dimensions = messages['reason_dimensions']
    
    # 各ペルソナの理由文長パターンを分析
    for persona in reason_trends.index:
        values = reason_trends.loc[persona]
        pattern_analysis[persona] = {
            'longest_reason': reason_dimensions[values.idxmax()],
            'max_length': values.max(),
            'shortest_reason': reason_dimensions[values.idxmin()],
            'min_length': values.min(),
            'mean_length': values.mean(),
            'std_length': values.std(),
            'length_profile': {
                reason_dimensions[col]: float(values[col])
                for col in reason_dimensions.keys()
            }
        }
    
    return pattern_analysis

def visualize_reason_patterns(reason_trends, lang='ja'):
    """理由文長パターンの可視化"""
    # データの準備
    data = reason_trends.copy()
    messages = load_messages(lang)
    reason_dimensions = messages['reason_dimensions']
    data.columns = [reason_dimensions[col] for col in data.columns]
    
    # レーダーチャートの作成
    fig = plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # ペルソナごとのカラー設定
    colors = ['#4285F4', '#EA4335', '#34A853', '#FF9900'] # 4つのペルソナに対応
    
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
    ax.set_title(messages['pattern_title'])
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), title=messages['legend_title'])
    
    # 保存
    save_figure(plt, 'persona_reason_patterns', lang=lang)
    plt.close()

def print_pattern_analysis(pattern_analysis, lang='ja'):
    """理由文長パターン分析結果の表示"""
    messages = load_messages(lang)
    print(f"\n{messages['header_text']}")
    for persona, analysis in pattern_analysis.items():
        print(f"\n{persona}:")
        print(f"  {messages['longest_text']}: {analysis['longest_reason']} ({analysis['max_length']:.2f})")
        print(f"  {messages['shortest_text']}: {analysis['shortest_reason']} ({analysis['min_length']:.2f})")
        print(f"  {messages['mean_text']}: {analysis['mean_length']:.2f}")
        print(f"  {messages['std_text']}: {analysis['std_length']:.2f}")
        print(f"  {messages['profile_text']}:")
        for reason, length in analysis['length_profile'].items():
            print(f"    {reason}: {length:.2f}")

def print_generated_files(lang='ja'):
    """生成されたファイルの一覧を表示"""
    messages = load_messages(lang)
    print(f"\n{messages['generated_files']}")
    print(f"\n{messages['correlation_files']}")
    print(f"- {os.path.join(OUTPUT_DIR, 'persona_reason_correlation.csv')}")
    figures_dir = os.path.join(OUTPUT_DIR, 'figures', lang)
    print(f"- {os.path.join(figures_dir, 'persona_reason_correlation.png')}")
    print(f"- {os.path.join(figures_dir, 'persona_reason_correlation.pdf')}")
    
    print(f"\n{messages['pattern_files']}")
    print(f"- {os.path.join(figures_dir, 'persona_reason_patterns.png')}")
    print(f"- {os.path.join(figures_dir, 'persona_reason_patterns.pdf')}")

def main(lang='ja'):
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    messages = load_messages(lang)
    print(messages['loading_text'])
    # データの読み込みと前処理
    df = pd.read_csv(os.path.join(OUTPUT_DIR, 'persona_reason.csv'))
    
    # モデルごとの平均を計算し、ペルソナをインデックスとして設定
    reason_trends = df.groupby('persona')[list(messages['reason_dimensions'].keys())].mean()
    # ペルソナ識別子を日本語名に変換
    reason_trends.index = reason_trends.index.map(messages['persona_mapping'])
    
    print(messages['correlation_text'])
    corr = create_correlation_heatmap(reason_trends, lang)
    
    print(messages['pattern_text'])
    pattern_analysis = analyze_reason_patterns(reason_trends, lang)
    
    print(messages['visualization_text'])
    visualize_reason_patterns(reason_trends, lang)
    
    # 結果の表示
    print_pattern_analysis(pattern_analysis, lang)
    
    print(f"\n{messages['completion_text']}")
    print(messages['save_text'].format(OUTPUT_DIR))
    print_generated_files(lang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate similarity analysis visualizations.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
