import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from fcmeans import FCM
from sklearn.metrics import silhouette_score
import os
import json
import argparse
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, CLUSTERING_CONFIG, EMOTION_DIMENSIONS,
    ensure_output_directories, save_figure, load_emotion_data
)
from adjustText import adjust_text

def load_messages(lang='ja'):
    """言語に応じたメッセージを読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)
    return messages['model_emotion_similarity'][lang]

# 出力ディレクトリの作成
ensure_output_directories()

def create_correlation_heatmap(emotion_trends, lang='ja'):
    """モデル間の相関分析とヒートマップの作成"""
    messages = load_messages(lang)
    
    # モデル間の相関係数を計算
    corr = emotion_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title(messages['correlation_title'], pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'model_emotion_correlation', lang=lang)
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'model_emotion_correlation.csv'))
    return corr

def find_optimal_clusters(emotion_trends, lang='ja'):
    """最適なクラスター数の決定"""
    scaled_data = StandardScaler().fit_transform(emotion_trends)
    silhouette_scores = []
    
    for n in range(2, CLUSTERING_CONFIG['max_clusters'] + 1):
        fcm = FCM(n_clusters=n, random_state=42)
        fcm.fit(scaled_data)
        labels = fcm.u.argmax(axis=1)
        score = silhouette_score(scaled_data, labels)
        silhouette_scores.append(score)
    
    # シルエットスコアの可視化
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    plt.plot(range(2, CLUSTERING_CONFIG['max_clusters'] + 1), silhouette_scores, 'bo-')
    messages = load_messages(lang)
    plt.xlabel(messages['silhouette_xlabel'])
    plt.ylabel(messages['silhouette_ylabel'])
    plt.title(messages['silhouette_title'])
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_emotion_silhouette', lang=lang)
    plt.close()
    
    optimal_clusters = np.argmax(silhouette_scores) + 2
    return optimal_clusters

def perform_fcm_analysis(emotion_trends, n_clusters):
    """Fuzzy C-Means クラスタリングの実行"""
    # データの正規化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(emotion_trends)
    
    # FCMの実行
    fcm = FCM(n_clusters=n_clusters, random_state=42)
    fcm.fit(scaled_data)
    
    # 所属度とクラスター中心を元のスケールに戻す
    centers = scaler.inverse_transform(fcm.centers)
    
    return fcm.u, centers, fcm

def visualize_fcm_gradients(emotion_trends, membership, centers, lang='ja'):
    """FCM結果をグラデーションで可視化"""
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(StandardScaler().fit_transform(emotion_trends))
    centers_2d = pca.transform(StandardScaler().fit_transform(centers))
    
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # クラスターごとの色を定義
    colors = CLUSTERING_CONFIG['colors']['cluster']
    
    # 各点をプロット
    texts = [] # 追加
    for i in range(len(data_2d)):
        # 所属度に基づいて色をブレンド
        color = np.zeros(3)
        for j in range(len(colors)):
            rgb = plt.cm.colors.to_rgb(colors[j])
            color += np.array(rgb) * membership[i,j]
            
        plt.scatter(data_2d[i, 0], data_2d[i, 1], 
                   color=color, s=100)
        # plt.annotate(emotion_trends.index[i], 
        #             (data_2d[i, 0], data_2d[i, 1]),
        #             xytext=(5, 5), textcoords='offset points',
        #             fontsize=8) # 変更前
        texts.append(plt.text(data_2d[i, 0], data_2d[i, 1], emotion_trends.index[i], fontsize=8)) # 変更後
    
    # クラスター中心のプロット
    messages = load_messages(lang)
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
               c='black', marker='x', s=200, label=messages['cluster_center_label'])
    
    # テキストの重なりを調整
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5)) # 追加
    plt.title(messages['fcm_gradient_title'])
    
    # 説明テキストの追加
    plt.text(0.02, 0.02,
            messages['cluster_description'],
            transform=plt.gca().transAxes,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8))
    plt.xlabel(messages['xlabel_pca'])
    plt.ylabel(messages['ylabel_pca'])
    plt.legend()
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_emotion_fcm_gradient', lang=lang)
    plt.close()

def visualize_fcm_with_memberships(emotion_trends, membership, centers, lang='ja'):
    """FCM結果を所属度付きで可視化"""
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(StandardScaler().fit_transform(emotion_trends))
    centers_2d = pca.transform(StandardScaler().fit_transform(centers))
    
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # 各点をプロット
    texts = [] # 追加
    for i in range(len(data_2d)):
        dominant_cluster = np.argmax(membership[i])
        alpha = max(membership[i])
        plt.scatter(data_2d[i, 0], data_2d[i, 1], 
                   c=CLUSTERING_CONFIG['colors']['cluster'][dominant_cluster], 
                   alpha=VISUALIZATION_CONFIG['plot']['text_box_alpha'],
                   label=f'Cluster {dominant_cluster+1}' if i == 0 else "")
        
        # モデル名と所属度を表示
        memberships_text = [f'C{j+1}:{membership[i,j]:.2f}' # Cluster を C に短縮
                          for j in range(membership.shape[1])]
        text_content = f'{emotion_trends.index[i]}\n({", ".join(memberships_text)})'
        # plt.annotate(text_content, (data_2d[i, 0], data_2d[i, 1]),
        #             xytext=(5, 5), textcoords='offset points',
        #             fontsize=7, bbox=dict(facecolor='white', alpha=0.7)) # 変更前
        texts.append(plt.text(data_2d[i, 0], data_2d[i, 1], text_content, fontsize=7, bbox=dict(facecolor='white', alpha=0.7))) # 変更後
    
    # クラスター中心のプロット
    # クラスター中心のプロット（黒でクラスター中心を表示）
    messages = load_messages(lang)
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
               c='black', marker='x', s=200, label=messages['cluster_center_label'])
    
    # テキストの重なりを調整
    adjust_text(texts, 
                # expand_points=(1.2, 1.2), # 必要に応じて調整
                # expand_text=(1.2, 1.2),   # 必要に応じて調整
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.5)) # 追加 (arrowpropsはお好みで調整)

    messages = load_messages(lang)
    plt.title(messages['fcm_membership_title'])
    
    # 説明テキストの追加
    plt.text(0.02, 0.02,
            messages['cluster_membership_description'],
            transform=plt.gca().transAxes,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8))
    plt.xlabel(messages['xlabel_pca'])
    plt.ylabel(messages['ylabel_pca'])
    plt.legend()
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_emotion_fcm_membership', lang=lang)
    plt.close()

def analyze_cluster_characteristics(emotion_trends, membership, centers, n_clusters):
    """クラスター特性の分析"""
    characteristics = {}
    
    for i in range(n_clusters):
        # 所属度が0.5以上のモデルを抽出
        high_membership = membership[:, i] > 0.5
        cluster_models = emotion_trends[high_membership]
        
        characteristics[f'cluster_{i+1}'] = {
            'size': len(cluster_models),
            'mean': cluster_models.mean().to_dict(),
            'std': cluster_models.std().to_dict(),
            'models': list(cluster_models.index),
            'center': centers[i].tolist()
        }
    
    # 結果をJSONとして保存
    import json
    with open(os.path.join(OUTPUT_DIR, 'model_emotion_cluster_characteristic.json'), 'w', encoding='utf-8') as f:
        json.dump(characteristics, f, ensure_ascii=False, indent=2)
    
    return characteristics

def print_generated_files(lang='ja'):
    """生成されたファイルの一覧を表示"""
    figures_dir = os.path.join(OUTPUT_DIR, 'figures', lang)
    print("\n生成されたファイル:")
    print("\n1. 相関分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'model_emotion_correlation.csv')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_correlation.png')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_correlation.pdf')}")
    
    print("\n2. クラスター分析:")
    print(f"- {os.path.join(figures_dir, 'model_emotion_silhouette_score.png')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_silhouette_score.pdf')}")

    print("\n3. FCM分析結果:")
    print(f"- {os.path.join(OUTPUT_DIR, 'model_emotion_cluster_characteristic.json')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_fcm_gradient.png')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_fcm_gradient.pdf')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_fcm_membership.png')}")
    print(f"- {os.path.join(figures_dir, 'model_emotion_fcm_membership.pdf')}")

def main(lang='ja'):
    # 感情次元の定義を取得
    emotion_dimensions = {k: v[lang] for k, v in EMOTION_DIMENSIONS.items()}
    
    # データの読み込み
    print("感情評価データを読み込んでいます...")
    emotion_trends = load_emotion_data().set_index('model')
    
    print("相関分析を実行中...")
    corr = create_correlation_heatmap(emotion_trends, lang)
    
    print("最適なクラスター数を計算中...")
    n_clusters = find_optimal_clusters(emotion_trends, lang)
    print(f"最適なクラスター数: {n_clusters}")
    
    print("Fuzzy C-Means クラスタリングを実行中...")
    membership, centers, fcm = perform_fcm_analysis(emotion_trends, n_clusters)
    
    print("結果を可視化中...")
    print("- グラデーション表現の生成...")
    visualize_fcm_gradients(emotion_trends, membership, centers, lang)
    print("- 所属度表示の生成...")
    visualize_fcm_with_memberships(emotion_trends, membership, centers, lang)
    
    print("クラスター特性を分析中...")
    characteristics = analyze_cluster_characteristics(emotion_trends, membership, centers, n_clusters)
    
    print("\nクラスター特性:")
    for cluster, info in characteristics.items():
        print(f"\n{cluster}:")
        print(f"サイズ: {info['size']}モデル")
        print("平均値:")
        for emotion, value in info['mean'].items():
            if emotion.endswith('value'):
                emotion_name = emotion_dimensions[emotion]
                print(f"  {emotion_name}: {value:.2f}")

    print("\n分析が完了しました。")
    print(f"結果は '{OUTPUT_DIR}' ディレクトリに保存されました。")
    print_generated_files(lang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate similarity analysis visualizations.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
