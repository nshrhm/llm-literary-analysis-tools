import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import os
import json
import argparse
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG,
    ensure_output_directories, save_figure
)

def load_messages(lang='ja'):
    """メッセージファイルを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages

def create_overall_plot(emotion_df, emotions, messages_lang, lang='ja'):
    """感情次元のデータをtemperatureごとに視覚化（全体平均）"""
    messages = messages_lang[lang]
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    for col, label in emotions.items():
        temp_means = emotion_df.groupby('temperature')[col].mean()
        plt.plot(temp_means.index, temp_means.values, marker='o', label=label)
    plt.xlabel(messages['xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.ylabel(messages['ylabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
    plt.title(messages['overall_plot_title'], fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
    plt.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., 
               fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'])
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    save_figure(plt, "temperature_emotion_overall", lang=lang)
    plt.close()

def create_model_plots(emotion_df, emotions, messages_lang, lang='ja'):
    """モデルごとの感情次元の変化をtemperatureで視覚化（全感情次元）"""
    messages = messages_lang[lang]
    for col, label in emotions.items():
        plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
        for model in emotion_df['model'].unique():
            model_data = emotion_df[emotion_df['model'] == model]
            if not model_data.empty:
                plt.plot(model_data['temperature'], model_data[col], marker='o', label=model)
        plt.xlabel(messages['xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
        plt.ylabel(messages['ylabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
        plt.title(messages['model_plot_title'].format(emotion=label), fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
        plt.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
        plt.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,
                   fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'])
        plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
        plt.tight_layout()
        save_figure(plt, f"temperature_emotion_{col}_all", lang=lang)
        plt.close()

def create_selected_model_plots(emotion_df, stats_df, emotions, messages_lang, lang='ja'):
    """統計データを用いた可視化（エラーバー付きプロット、上位3モデルと下位3モデルに絞る）"""
    messages = messages_lang[lang]
    for col, label in emotions.items():
        # モデルごとの平均値を計算し、上位3モデルと下位3モデルを選択
        model_means = stats_df.groupby('model')[f"{col}_mean"].mean().sort_values()
        selected_models = list(model_means.head(3).index) + list(model_means.tail(3).index)
        
        plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
        jitter = 0.02  # X軸のジッター量
        for i, model in enumerate(selected_models):
            model_data = stats_df[stats_df['model'] == model].sort_values('temperature')
            if not model_data.empty:
                # X軸にジッターを適用
                jittered_temp = model_data['temperature'] + (i - 2.5) * jitter
                plt.errorbar(jittered_temp, model_data[f"{col}_mean"], 
                           yerr=model_data[f"{col}_std"], marker='o', label=model, capsize=5)
        plt.xlabel(messages['xlabel'], fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
        plt.ylabel(messages['std_ylabel'].format(emotion=label), fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'])
        plt.title(messages['selected_plot_title'].format(emotion=label), fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'])
        plt.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
        plt.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'])
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,
                   fontsize=VISUALIZATION_CONFIG['figure']['legend_fontsize'])
        plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
        plt.tight_layout()
        save_figure(plt, f"temperature_emotion_{col}_std_selected", lang=lang)
        plt.close()

def main(lang='ja'):
    """メイン処理"""
    # 出力ディレクトリを作成
    ensure_output_directories()

    # CSVファイルを読み込む
    emotion_df = pd.read_csv(f"{OUTPUT_DIR}/temperature_emotion.csv")
    stats_df = pd.read_csv(f"{OUTPUT_DIR}/temperature_emotion_statistics.csv")

    # メッセージファイルを読み込む
    all_messages = load_messages(lang)
    if 'temperature_emotion' in all_messages:
        messages_lang = all_messages['temperature_emotion']
    else:
        # フォールバック: 基本的なメッセージを作成
        messages_lang = {
            'ja': {
                'title': '温度パラメータと感情評価の関係',
                'xlabel': '温度',
                'ylabel': '感情値'
            },
            'en': {
                'title': 'Relationship between Temperature Parameter and Emotion Evaluation',
                'xlabel': 'Temperature',
                'ylabel': 'Emotion Value'
            }
        }
    
    # emotions辞書は各グラフ作成関数で使用する感情次元のラベル辞書
    # messages.jsonのcommon.emotion_dimensionsから感情次元のラベルを取得
    if 'common' in all_messages and 'emotion_dimensions' in all_messages['common']:
        emotions_raw = all_messages['common']['emotion_dimensions']
        emotions = {k: v[lang] for k, v in emotions_raw.items()}
    else:
        # フォールバック: デフォルトの感情次元
        emotions = {
            'Q1value': '面白さ' if lang == 'ja' else 'Interesting',
            'Q2value': '驚き' if lang == 'ja' else 'Surprise',
            'Q3value': '悲しさ' if lang == 'ja' else 'Sadness',
            'Q4value': '怒り' if lang == 'ja' else 'Anger'
        }

    # 各種グラフを生成
    create_overall_plot(emotion_df, emotions, messages_lang, lang)
    create_model_plots(emotion_df, emotions, messages_lang, lang)
    create_selected_model_plots(emotion_df, stats_df, emotions, messages_lang, lang)

    lang_dir = 'ja' if lang == 'ja' else 'en'
    print(f"\nTemperatureによる感情値の可視化が完了しました。グラフは {os.path.join(OUTPUT_DIR, 'figures', lang_dir)} に保存されています。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate visualization for temperature emotion data.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
