#!/usr/bin/env python3
"""
ペルソナと感情次元の関係をモデルごとに分析・可視化するプログラム。
各感情次元（Q1-Q4）について、モデルごとのペルソナの評価値を棒グラフで表示する。
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from config import (
    MODEL_ORDER,
    VISUALIZATION_CONFIG,
    get_message,
    save_figure,
    safe_read_csv
)

# ペルソナの表示順
PERSONA_ORDER = ['p1', 'p2', 'p3', 'p4']

def load_data(lang='ja'):
    """データの読み込みと前処理"""
    df, error = safe_read_csv("./data_all.csv")
    if error:
        print(error)
        sys.exit(1)
    
    # ペルソナ名のマッピング
    try:
        # ペルソナ名のマッピング
        if lang == 'en':
            persona_mapping = get_message('persona_model_emotion.en.persona')
        else:
            persona_mapping = get_message('common.persona_mapping')
        
        # ペルソナを定義順に並び替え
        df['persona'] = pd.Categorical(df['persona'], categories=PERSONA_ORDER, ordered=True)
        df['persona'] = df['persona'].map(persona_mapping)
        return df
    except KeyError as e:
        print(f"Error: Could not find persona mapping for language '{lang}': {e}")
        sys.exit(1)

def create_emotion_plot(data, emotion_col, lang='ja'):
    """
    指定された感情次元について、モデルごとのペルソナの評価値を棒グラフで表示

    Parameters
    ----------
    data : DataFrame
        分析対象のデータ
    emotion_col : str
        感情次元のカラム名（例：'Q1value'）
    lang : str
        言語設定（'ja'または'en'）
    """
    # グラフサイズを横長に設定
    plt.figure(figsize=(40, 10))  # 横幅を40インチに拡大

    # データの集計
    pivot_data = data.pivot_table(
        values=emotion_col,
        index='model',
        columns='persona',
        aggfunc='mean',
        observed=True  # 将来のバージョンに対応
    ).reindex(MODEL_ORDER)

    # 棒グラフの作成
    ax = pivot_data.plot(
        kind='bar',
        width=0.8
    )
    
    # モデル間の距離を調整
    ax.margins(x=0.1)  # X軸方向のマージンを10%に設定

    # グラフの装飾
    emotion_name = get_message(f'common.emotion_dimensions.{emotion_col}.{lang}')
    title = get_message(f'persona_model_emotion.{lang}.title').format(emotion=emotion_name)
    xlabel = get_message(f'persona_model_emotion.{lang}.xlabel')
    ylabel = get_message(f'persona_model_emotion.{lang}.ylabel')
    legend_title = get_message(f'persona_model_emotion.{lang}.legend_title')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # X軸ラベルの回転と位置調整
    plt.xticks(rotation=45, ha='right', fontsize=6)  # フォントサイズを6に調整
    
    # 凡例の設定
    plt.legend(
        title=legend_title,
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=6  # デフォルトの10 * 0.6 = 6
    )
    
    # レイアウトの調整
    plt.tight_layout()
    
    # グラフの保存
    emotion_num = emotion_col[1]  # Q1value -> 1
    try:
        files = save_figure(plt, f'persona_model_emotion_q{emotion_num}', lang=lang)
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
    
    # 各感情次元についてグラフを生成
    emotion_cols = [f"Q{i}value" for i in range(1, 5)]
    saved_files = []
    for emotion_col in emotion_cols:
        files = create_emotion_plot(df, emotion_col, lang)
        saved_files.extend(files)
    
    print("\n生成したファイル:")
    for file in saved_files:
        print(f"- {file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ペルソナと感情次元の関係を可視化")
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja', help='言語設定（ja/en）')
    args = parser.parse_args()
    main(args.lang)
