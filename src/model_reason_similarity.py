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
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, CLUSTERING_CONFIG,
    ensure_output_directories, save_figure
)
from adjustText import adjust_text

# 理由文の種類の定義
REASON_DIMENSIONS = {
    'Q1reason': '面白さの理由',
    'Q2reason': '驚きの理由',
    'Q3reason': '悲しみの理由',
    'Q4reason': '怒りの理由'
}

# 出力ディレクトリの作成
ensure_output_directories()

def load_reason_data():
    """理由文長データの読み込み"""
    filepath = os.path.join(OUTPUT_DIR, 'model_reason.csv')
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")

def create_correlation_heatmap(reason_trends):
    """モデル間の相関分析とヒートマップの作成"""
    # モデル間の相関係数を計算
    corr = reason_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title('モデル間の理由文長相関', pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'model_reason_correlation')
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'model_reason_correlation.csv'))
    return corr

def find_optimal_clusters(reason_trends):
    """最適なクラスター数の決定"""
    scaled_data = StandardScaler().fit_transform(reason_trends)
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
    plt.xlabel('クラスター数')
    plt.ylabel('シルエットスコア')
    plt.title('クラスター数の最適化')
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_reason_silhouette')
    plt.close()
    
    optimal_clusters = np.argmax(silhouette_scores) + 2
    return optimal_clusters

def perform_fcm_analysis(reason_trends, n_clusters):
    """Fuzzy C-Means クラスタリングの実行"""
    # データの正規化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(reason_trends)
    
    # FCMの実行
    fcm = FCM(n_clusters=n_clusters, random_state=42)
    fcm.fit(scaled_data)
    
    # 所属度とクラスター中心を元のスケールに戻す
    centers = scaler.inverse_transform(fcm.centers)
    
    return fcm.u, centers, fcm

def visualize_fcm_gradients(reason_trends, membership, centers):
    """FCM結果をグラデーションで可視化"""
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(StandardScaler().fit_transform(reason_trends))
    centers_2d = pca.transform(StandardScaler().fit_transform(centers))
    
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # クラスターごとの色を定義
    colors = CLUSTERING_CONFIG['colors']['cluster']
    
    # 各点をプロット
    texts = []
    for i in range(len(data_2d)):
        # 所属度に基づいて色をブレンド
        color = np.zeros(3)
        for j in range(len(colors)):
            rgb = plt.cm.colors.to_rgb(colors[j])
            color += np.array(rgb) * membership[i,j]
            
        plt.scatter(data_2d[i, 0], data_2d[i, 1], 
                   color=color, s=100)
        texts.append(plt.text(data_2d[i, 0], data_2d[i, 1], 
                            reason_trends.index[i], fontsize=8))
    
    # クラスター中心のプロット
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
               c='black', marker='x', s=200, label='クラスター中心（1, 2）')
    
    # テキストの重なりを調整
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    plt.title('Fuzzy C-Means クラスタリング結果\n（理由文長パターンに基づく分類）')
    
    # 説明テキストの追加
    plt.text(0.02, 0.02,
            '※色の濃さはクラスターへの所属度を表します\n'
            '※クラスター特性は分析結果ファイルを参照',
            transform=plt.gca().transAxes,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8))
    plt.xlabel('第1主成分')
    plt.ylabel('第2主成分')
    plt.legend()
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_reason_fcm_gradient')
    plt.close()

def visualize_fcm_with_memberships(reason_trends, membership, centers):
    """FCM結果を所属度付きで可視化"""
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(StandardScaler().fit_transform(reason_trends))
    centers_2d = pca.transform(StandardScaler().fit_transform(centers))
    
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    
    # 各点をプロット
    texts = []
    for i in range(len(data_2d)):
        dominant_cluster = np.argmax(membership[i])
        alpha = max(membership[i])
        plt.scatter(data_2d[i, 0], data_2d[i, 1], 
                   c=CLUSTERING_CONFIG['colors']['cluster'][dominant_cluster], 
                   alpha=VISUALIZATION_CONFIG['plot']['text_box_alpha'],
                   label=f'Cluster {dominant_cluster+1}' if i == 0 else "")
        
        # モデル名と所属度を表示
        memberships_text = [f'C{j+1}:{membership[i,j]:.2f}'
                          for j in range(membership.shape[1])]
        text_content = f'{reason_trends.index[i]}\n({", ".join(memberships_text)})'
        texts.append(plt.text(data_2d[i, 0], data_2d[i, 1], text_content,
                            fontsize=7, bbox=dict(facecolor='white', alpha=0.7)))
    
    # クラスター中心のプロット
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
               c='black', marker='x', s=200, label='クラスター中心')
    
    # テキストの重なりを調整
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    plt.title('Fuzzy C-Means クラスタリング結果\n（理由文長パターンに基づく分類）')
    
    # 説明テキストの追加
    plt.text(0.02, 0.02,
            '※クラスターへの所属度を数値で表示\n'
            '※クラスター特性は分析結果ファイルを参照',
            transform=plt.gca().transAxes,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8))
    plt.xlabel('第1主成分')
    plt.ylabel('第2主成分')
    plt.legend()
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_reason_fcm_membership')
    plt.close()

def analyze_cluster_characteristics(reason_trends, membership, centers, n_clusters):
    """クラスター特性の分析"""
    characteristics = {}
    
    for i in range(n_clusters):
        # 所属度が0.5以上のモデルを抽出
        high_membership = membership[:, i] > 0.5
        cluster_models = reason_trends[high_membership]
        
        characteristics[f'cluster_{i+1}'] = {
            'size': len(cluster_models),
            'mean': cluster_models.mean().to_dict(),
            'std': cluster_models.std().to_dict(),
            'models': list(cluster_models.index),
            'center': centers[i].tolist()
        }
    
    # 結果をJSONとして保存
    import json
    with open(os.path.join(OUTPUT_DIR, 'model_reason_cluster_characteristic.json'), 'w', encoding='utf-8') as f:
        json.dump(characteristics, f, ensure_ascii=False, indent=2)
    
    return characteristics

def print_generated_files():
    """生成されたファイルの一覧を表示"""
    print("\n生成されたファイル:")
    print("\n1. 相関分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'model_reason_correlation.csv')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_correlation.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_correlation.svg')}")
    
    print("\n2. クラスター分析:")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_silhouette.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_silhouette.svg')}")
    
    print("\n3. FCM分析結果:")
    print(f"- {os.path.join(OUTPUT_DIR, 'model_reason_cluster_characteristic.json')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_fcm_gradient.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_fcm_gradient.svg')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_fcm_membership.png')}")
    print(f"- {os.path.join(OUTPUT_DIR, 'figures', 'model_reason_fcm_membership.svg')}")

def main():
    # データの読み込み
    print("理由文長データを読み込んでいます...")
    reason_trends = load_reason_data().set_index('model')
    
    print("相関分析を実行中...")
    corr = create_correlation_heatmap(reason_trends)
    
    print("最適なクラスター数を計算中...")
    n_clusters = find_optimal_clusters(reason_trends)
    print(f"最適なクラスター数: {n_clusters}")
    
    print("Fuzzy C-Means クラスタリングを実行中...")
    membership, centers, fcm = perform_fcm_analysis(reason_trends, n_clusters)
    
    print("結果を可視化中...")
    print("- グラデーション表現の生成...")
    visualize_fcm_gradients(reason_trends, membership, centers)
    print("- 所属度表示の生成...")
    visualize_fcm_with_memberships(reason_trends, membership, centers)
    
    print("クラスター特性を分析中...")
    characteristics = analyze_cluster_characteristics(reason_trends, membership, centers, n_clusters)
    
    print("\nクラスター特性:")
    for cluster, info in characteristics.items():
        print(f"\n{cluster}:")
        print(f"サイズ: {info['size']}モデル")
        print("平均文字数:")
        for reason, value in info['mean'].items():
            if reason in REASON_DIMENSIONS:
                reason_name = REASON_DIMENSIONS[reason]
                print(f"  {reason_name}: {value:.2f}")

    print("\n分析が完了しました。")
    print(f"結果は '{OUTPUT_DIR}' ディレクトリに保存されました。")
    print_generated_files()

if __name__ == "__main__":
    main()
