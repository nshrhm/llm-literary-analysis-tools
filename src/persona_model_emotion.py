#!/usr/bin/env python3
"""
ペルソナと感情次元の関係をモデルごとに分析・可視化するプログラム。
各感情次元（Q1-Q4）について、モデルごとのペルソナの評価値を1つの図にまとめて棒グラフで表示する。
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import japanize_matplotlib # langに応じてmain関数内でインポート
from config import (
    MODEL_ORDER,
    PERSONA_COLORS,
    VISUALIZATION_CONFIG,
    get_message,
    save_figure,
    safe_read_csv
)

# ペルソナの表示順
PERSONA_ORDER = ['p1', 'p2', 'p3', 'p4']
# 感情次元のカラム名
EMOTION_COLS = [f"Q{i}value" for i in range(1, 5)]

def load_data(lang='ja'):
    """データの読み込みと前処理"""
    df, error = safe_read_csv("./data_all.csv")
    if error:
        print(error)
        sys.exit(1)
    
    try:
        if lang == 'en':
            persona_mapping = get_message('persona_model_emotion.en.persona')
        else:
            raw_persona_mapping = get_message('common.persona_mapping')
            persona_mapping = {key: value.get(lang, value.get('ja')) for key, value in raw_persona_mapping.items()}
        
        df['persona'] = pd.Categorical(df['persona'], categories=PERSONA_ORDER, ordered=True)
        df['persona'] = df['persona'].map(persona_mapping)
        return df
    except KeyError as e:
        print(f"Error: Could not find persona mapping for language '{lang}': {e}")
        sys.exit(1)

def create_combined_emotion_plot(data, lang='ja'):
    """
    全感情次元について、モデルごとのペルソナの評価値を1つの図にまとめて棒グラフで表示

    Parameters
    ----------
    data : DataFrame
        分析対象のデータ
    lang : str
        言語設定（'ja'または'en'）
    """
    if lang == 'ja':
        import japanize_matplotlib # 日本語の場合のみインポート

    fig, axes = plt.subplots(4, 1, figsize=(VISUALIZATION_CONFIG['figure']['default_size'][0] * 2, VISUALIZATION_CONFIG['figure']['default_size'][1] * 3), sharex=True) # 横幅を少し広げ、高さを調整
    fig.subplots_adjust(hspace=0.4) # サブプロット間の縦方向の間隔を調整

    # PERSONA_ORDER に基づいて色のリストを作成
    plot_colors = [PERSONA_COLORS[p] for p in PERSONA_ORDER if p in PERSONA_COLORS]

    for i, emotion_col in enumerate(EMOTION_COLS):
        ax = axes[i]
        pivot_data = data.pivot_table(
            values=emotion_col,
            index='model',
            columns='persona',
            aggfunc='mean',
            observed=True
        ).reindex(MODEL_ORDER)

        pivot_data.plot(
            kind='bar',
            width=0.8,
            color=plot_colors,
            ax=ax,
            legend=False # 各サブプロットの凡例は非表示
        )
        
        ax.margins(x=0.05) # X軸方向のマージンを調整

        emotion_name = get_message(f'common.emotion_dimensions.{emotion_col}.{lang}')
        # サブプロットごとのタイトル（Y軸ラベルとして機能させるため、Y軸ラベルに設定）
        ax.set_ylabel(emotion_name, fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'] * 2) # Y軸ラベルを感情名に
        ax.tick_params(axis='y', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'] * 2)

        if i < len(EMOTION_COLS) - 1:
            ax.set_xlabel('') # 最後のサブプロット以外はX軸ラベルを非表示
            ax.tick_params(axis='x', labelbottom=False) # X軸の目盛りラベルを非表示にする
        else:
            # 最後のサブプロットにX軸ラベルと目盛りラベルを設定
            xlabel = get_message(f'persona_model_emotion.{lang}.xlabel')
            ax.set_xlabel(xlabel, fontsize=VISUALIZATION_CONFIG['figure']['label_fontsize'] * 3)
            ax.tick_params(axis='x', labelsize=VISUALIZATION_CONFIG['figure']['tick_labelsize'] * 1.6) # rotationとhaを削除

            # X軸の目盛りラベルの回転と位置調整を別途行う
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right') # haはset_xticklabelsで設定

    # 図全体のタイトル
    overall_title = get_message(f'persona_model_emotion.{lang}.combined_title')
    fig.suptitle(overall_title, fontsize=VISUALIZATION_CONFIG['figure']['title_fontsize'] * 1.1, y=0.99) # yでタイトルの位置を調整

    # 共通の凡例を図の下側に配置
    handles, labels = axes[0].get_legend_handles_labels() # いずれかのサブプロットから凡例情報を取得
    legend_title_text = get_message(f'persona_model_emotion.{lang}.legend_title')
    legend_font_size = VISUALIZATION_CONFIG['figure']['legend_fontsize'] * 2
    legend_title_font_size = legend_font_size * 2 # 凡例タイトルのフォントサイズを少し大きく

    fig.legend(
        handles,
        labels,
        title=legend_title_text,
        loc='lower center', # 下部中央に配置
        bbox_to_anchor=(0.5, -0.04), # Y座標を調整してグラフの下に配置、Xは中央
        ncol=len(PERSONA_ORDER), # ペルソナの数だけ列を作成
        fontsize=legend_font_size,
        title_fontsize=legend_title_font_size # 凡例タイトルのフォントサイズ
    )

    # レイアウト調整：凡例が下に来るので、bottomの値を調整
    plt.tight_layout(rect=[0, 0.05, 1, 0.97]) # rectのbottomを調整して凡例スペースを確保

    try:
        files = save_figure(fig, 'persona_model_emotion_combined', lang=lang)
        plt.close()
        return files
    except Exception as e:
        print(f"Error saving figure: {e}")
        plt.close()
        return []

def main(lang='ja'):
    """メイン関数"""
    # データの読み込み
    df = load_data(lang)
    
    # 結合グラフの生成
    saved_files = create_combined_emotion_plot(df, lang)
    
    if saved_files:
        print("\n生成したファイル:")
        for file in saved_files:
            print(f"- {file}")
    else:
        print("グラフファイルの生成に失敗しました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ペルソナと感情次元の関係を可視化（結合グラフ）")
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='言語設定（ja/en）')
    args = parser.parse_args()
    main(args.lang)
