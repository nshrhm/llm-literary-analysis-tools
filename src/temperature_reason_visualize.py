import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import os
import json
import argparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS,
    VISUALIZATION_CONFIG, ensure_output_directories, save_figure
)

def load_messages(lang):
    """言語に応じたメッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages['temperature_reason'][lang]

def create_similarity_plot(diversity_df, lang='ja'):
    """平均類似度の変化をプロット（選抜モデル）"""
    messages = load_messages(lang)

    # 多様性スコアに基づく選抜
    model_diversity_means = diversity_df.groupby('model')['diversity_score'].mean().sort_values(ascending=False)
    high_diversity_models = model_diversity_means.head(3).index.tolist()
    low_diversity_models = model_diversity_means.tail(3).index.tolist()
    selected_models = high_diversity_models + low_diversity_models

    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    for model in selected_models:
        model_data = diversity_df[diversity_df['model'] == model].sort_values('temperature')
        if not model_data.empty:
            # 開発元を判定して色を適用
            vendor = None
            for v, patterns in VENDOR_PATTERNS.items():
                if any(p in model for p in patterns):
                    vendor = v
                    break
            color = VENDOR_COLORS.get(vendor, 'gray') if vendor else 'gray'
            label = f"{model} ({messages['high_diversity'] if model in high_diversity_models else messages['low_diversity']})"
            plt.plot(model_data['temperature'], model_data['mean_similarity'], marker='o', label=label, color=color)

    # 全体平均を計算してプロット
    overall_mean_similarity = diversity_df.groupby('temperature')['mean_similarity'].mean().sort_index()
    plt.plot(overall_mean_similarity.index, overall_mean_similarity.values, marker='s', linestyle='--', color='black', label=messages['overall_average'])

    plt.xlabel(messages['xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.ylabel(messages['ylabel_similarity'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.title(messages['similarity_plot_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    plt.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,
               fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'])
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    save_figure(plt, "temperature_reason_similarity_selected", lang=lang)
    plt.close()

def create_diversity_plot(diversity_df, lang='ja'):
    """多様性スコアの変化をプロット（選抜モデル）"""
    messages = load_messages(lang)

    # 多様性スコアに基づく選抜
    model_diversity_means = diversity_df.groupby('model')['diversity_score'].mean().sort_values(ascending=False)
    high_diversity_models = model_diversity_means.head(3).index.tolist()
    low_diversity_models = model_diversity_means.tail(3).index.tolist()
    selected_models = high_diversity_models + low_diversity_models

    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    for model in selected_models:
        model_data = diversity_df[diversity_df['model'] == model].sort_values('temperature')
        if not model_data.empty:
            # 開発元を判定して色を適用
            vendor = None
            for v, patterns in VENDOR_PATTERNS.items():
                if any(p in model for p in patterns):
                    vendor = v
                    break
            color = VENDOR_COLORS.get(vendor, 'gray') if vendor else 'gray'
            label = f"{model} ({messages['high_diversity'] if model in high_diversity_models else messages['low_diversity']})"
            plt.plot(model_data['temperature'], model_data['diversity_score'], marker='o', label=label, color=color)

    # 全体平均を計算してプロット
    overall_mean_diversity = diversity_df.groupby('temperature')['diversity_score'].mean().sort_index()
    plt.plot(overall_mean_diversity.index, overall_mean_diversity.values, marker='s', linestyle='--', color='black', label=messages['overall_average'])

    plt.xlabel(messages['xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.ylabel(messages['ylabel_diversity'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.title(messages['diversity_plot_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    plt.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,
               fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'])
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    save_figure(plt, "temperature_reason_diversity_selected", lang=lang)
    plt.close()

def create_correlation_plots(correlation_df, lang='ja'):
    """相関係数の棒グラフを作成"""
    messages = load_messages(lang)

    # 平均類似度の相関係数プロット
    sorted_df_similarity = correlation_df.sort_values(by='corr_similarity', ascending=False)
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    bars = []
    for model in sorted_df_similarity['model']:
        # 開発元を判定して色を適用
        vendor = None
        for v, patterns in VENDOR_PATTERNS.items():
            if any(p in model for p in patterns):
                vendor = v
                break
        color = VENDOR_COLORS.get(vendor, 'gray') if vendor else 'gray'
        bar = plt.bar(model, sorted_df_similarity[sorted_df_similarity['model'] == model]['corr_similarity'], color=color)
        bars.extend(bar)

    plt.xlabel(messages['correlation_xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.ylabel(messages['correlation_similarity_ylabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.title(messages['correlation_similarity_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    plt.xticks(rotation=90, fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.yticks(fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    
    # 各棒の上に値を表示
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom' if yval >= 0 else 'top',
                fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'] * 0.6)
    
    save_figure(plt, "temperature_reason_correlation_similarity_sorted", lang=lang)
    plt.close()

    # 多様性スコアの相関係数プロット
    sorted_df_diversity = correlation_df.sort_values(by='corr_diversity', ascending=False)
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    bars = []
    for model in sorted_df_diversity['model']:
        # 開発元を判定して色を適用
        vendor = None
        for v, patterns in VENDOR_PATTERNS.items():
            if any(p in model for p in patterns):
                vendor = v
                break
        color = VENDOR_COLORS.get(vendor, 'gray') if vendor else 'gray'
        bar = plt.bar(model, sorted_df_diversity[sorted_df_diversity['model'] == model]['corr_diversity'], color=color)
        bars.extend(bar)

    plt.xlabel(messages['correlation_xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.ylabel(messages['correlation_diversity_ylabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.title(messages['correlation_diversity_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    plt.xticks(rotation=90, fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.yticks(fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.grid(True, axis='y', alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    
    # 各棒の上に値を表示
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom' if yval >= 0 else 'top',
                fontsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'] * 0.6)
    
    save_figure(plt, "temperature_reason_correlation_diversity_sorted", lang=lang)
    plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # データの読み込み
    df = pd.read_csv("data_all.csv")

    # テキストデータの列名を特定
    reason_columns = ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']

    # 各感情の理由を結合して1つのテキストデータとして扱う
    df['combined_reason'] = df[reason_columns].astype(str).agg(' '.join, axis=1)
    text_column = 'combined_reason'

    # テキスト多様性データを格納するリスト
    diversity_data = []

    # モデルとtemperatureごとにテキストの類似度を計算
    vectorizer = TfidfVectorizer()
    for model in df['model'].unique():
        for temp in df['temperature'].unique():
            subset = df[(df['model'] == model) & (df['temperature'] == temp)]
            if len(subset) >= 2:  # 類似度計算には少なくとも2つのテキストが必要
                texts = subset[text_column].astype(str).tolist()
                if len(texts) >= 2 and any(len(text.strip()) > 0 for text in texts):
                    # TF-IDFベクトル化
                    tfidf_matrix = vectorizer.fit_transform(texts)
                    # コサイン類似度を計算
                    similarity_matrix = cosine_similarity(tfidf_matrix)
                    # 対角成分（自己類似度）を除外し、平均類似度を計算
                    np.fill_diagonal(similarity_matrix, 0)
                    mean_similarity = np.mean(similarity_matrix)
                    std_similarity = np.std(similarity_matrix)
                    diversity_data.append({
                        'model': model,
                        'temperature': temp,
                        'mean_similarity': mean_similarity,
                        'std_similarity': std_similarity,
                        'diversity_score': 1 - mean_similarity  # 多様性スコア（類似度の逆）
                    })

    # データフレームに変換
    diversity_df = pd.DataFrame(diversity_data)

    # CSVとして保存
    diversity_df.to_csv(f"{OUTPUT_DIR}/temperature_reason_diversity.csv", index=False)

    # 相関係数の計算
    correlation_data = []
    for model in diversity_df['model'].unique():
        model_data = diversity_df[diversity_df['model'] == model]
        if not model_data.empty:
            corr_similarity = model_data['temperature'].corr(model_data['mean_similarity'])
            corr_diversity = model_data['temperature'].corr(model_data['diversity_score'])
            correlation_data.append({
                'model': model,
                'corr_similarity': corr_similarity,
                'corr_diversity': corr_diversity
            })

    # データフレームに変換
    correlation_df = pd.DataFrame(correlation_data)

    # CSVとして保存
    correlation_df.to_csv(f"{OUTPUT_DIR}/temperature_reason_correlation_diversity.csv", index=False)

    # グラフを生成
    create_similarity_plot(diversity_df, lang)
    create_diversity_plot(diversity_df, lang)
    create_correlation_plots(correlation_df, lang)

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\n生成テキストの多様性分析が完了しました。結果は '{OUTPUT_DIR}/temperature_reason_diversity.csv' に保存され、グラフは {os.path.join(OUTPUT_DIR, 'figures', lang_dir)} に保存されました。")
    print(f"また、temperatureと多様性指標の相関分析が完了しました。結果は '{OUTPUT_DIR}/temperature_reason_correlation_diversity.csv' に保存され、相関グラフも生成されました。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for temperature reason data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
