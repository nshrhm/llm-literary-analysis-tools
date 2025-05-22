import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from config import (
    OUTPUT_DIR, VENDOR_PATTERNS, VENDOR_COLORS, MODEL_ORDER,
    ANALYSIS_COLUMNS, DATA_PATHS, ensure_output_directories, safe_read_csv
)

def get_vendor_color(model_name):
    """モデル名から対応する開発元の色を取得"""
    for vendor, patterns in VENDOR_PATTERNS.items():
        if any(model_name.startswith(pattern) for pattern in patterns):
            return VENDOR_COLORS[vendor]
    return '#808080'  # デフォルトの色（グレー）

def plot_missing_values(df, col):
    """特定の項目の欠損値をプロット"""
    # 欠損値が0でないデータのみをフィルタリング
    filtered_df = df[df[col] > 0].copy()
    
    if filtered_df.empty:
        print(f"欠損値が0のデータしかないため、グラフを生成しませんでした ({col})")
        return
    
    # モデルの順序を設定
    filtered_df['model'] = pd.Categorical(filtered_df['model'], categories=MODEL_ORDER, ordered=True)
    filtered_df = filtered_df.sort_values('model')
    
    # プロットの設定
    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(filtered_df)), filtered_df[col])
    
    # 各バーの色を設定
    for bar, model in zip(bars, filtered_df['model']):
        bar.set_color(get_vendor_color(model))
        bar.set_alpha(0.8)
    
    plt.yticks(range(len(filtered_df)), filtered_df['model'])
    plt.xlabel(f'欠損値の割合 ({col})')
    plt.ylabel('モデル')
    plt.title(f'モデル別欠損値の割合 ({col})')
    
    # 凡例を追加
    legend_elements = [plt.Rectangle((0,0),1,1, color=color, alpha=0.8, label=vendor)
                      for vendor, color in VENDOR_COLORS.items()]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    
    # ファイルの保存
    plt.savefig(f'{OUTPUT_DIR}/figures/missing_values_{col.lower()}.png', bbox_inches='tight', dpi=300)
    plt.savefig(f'{OUTPUT_DIR}/figures/missing_values_{col.lower()}.svg', bbox_inches='tight')
    plt.close()
    
    print(f"欠損値の割合をモデルごとに視覚化したグラフを保存しました ({col})")

def main():
    # 出力ディレクトリの作成
    ensure_output_directories()
    
    # CSVファイルの読み込み
    df, error = safe_read_csv(DATA_PATHS['missing_by_model'])
    if error:
        print(error)
        return
    
    # 個別項目のグラフ生成
    for col in ANALYSIS_COLUMNS['all']:
        plot_missing_values(df, col)
    
    # 総合欠損値の計算
    df['TotalMissing'] = df[ANALYSIS_COLUMNS['all']].mean(axis=1)
    plot_missing_values(df, 'TotalMissing')

if __name__ == "__main__":
    main()
