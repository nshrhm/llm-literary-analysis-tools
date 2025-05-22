import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import os
from config import OUTPUT_DIR, EMOTION_DIMENSIONS, VISUALIZATION_CONFIG, ensure_output_directories, save_figure

# 出力ディレクトリを作成
ensure_output_directories()

# 出力ディレクトリを確認し、存在しない場合は作成
figures_dir = f"{OUTPUT_DIR}/figures/"
os.makedirs(figures_dir, exist_ok=True)

# CSVファイルを読み込む
emotion_df = pd.read_csv(f"{OUTPUT_DIR}/temperature_emotion.csv")
stats_df = pd.read_csv(f"{OUTPUT_DIR}/temperature_emotion_statistics.csv")

# 感情次元のデータをtemperatureごとに視覚化（全体平均）
plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
for col, label in EMOTION_DIMENSIONS.items():
    temp_means = emotion_df.groupby('temperature')[col].mean()
    plt.plot(temp_means.index, temp_means.values, marker='o', label=label)
plt.xlabel('Temperature')
plt.ylabel('感情値の平均')
plt.title('Temperatureによる感情値の変化（全体平均）')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
plt.tight_layout()
save_figure(plt, "temperature_emotion_overall")
plt.close()

# モデルごとの感情次元の変化をtemperatureで視覚化（全感情次元）
for col, label in EMOTION_DIMENSIONS.items():
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    for model in emotion_df['model'].unique():
        model_data = emotion_df[emotion_df['model'] == model]
        if not model_data.empty:
            plt.plot(model_data['temperature'], model_data[col], marker='o', label=model)
    plt.xlabel('Temperature')
    plt.ylabel(f'{label}の平均値')
    plt.title(f'Temperatureによる{label}の変化（全モデル）')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    save_figure(plt, f"temperature_emotion_{col}_all")
    plt.close()

# 統計データを用いた可視化（エラーバー付きプロット、Temperatureの小さい順に並べ替え、上位3モデルと下位3モデルに絞る）
for col, label in EMOTION_DIMENSIONS.items():
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
    plt.xlabel('Temperature')
    plt.ylabel(f'{label}の平均値 ± 標準偏差')
    plt.title(f'Temperatureによる{label}の変化（標準偏差付き、上位3・下位3モデル）')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    plt.tight_layout()
    save_figure(plt, f"temperature_emotion_{col}_std_selected")
    plt.close()

print(f"Temperatureによる感情値の可視化が完了しました。グラフは '{figures_dir}' に保存されています。")
