import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from fcmeans import FCM
from sklearn.metrics import silhouette_score
import os
import json
import argparse
from config import (
    OUTPUT_DIR, VISUALIZATION_CONFIG, CLUSTERING_CONFIG,
    ensure_output_directories, save_figure, get_message
)
from adjustText import adjust_text

def load_messages(lang='ja'):
    """言語に応じたメッセージと理由文の定義を読み込む"""
    with open('src/messages.json', 'r', encoding='utf-8') as f:
        messages_data = json.load(f)
    
    # model_reason_similarity のメッセージ
    similarity_messages = messages_data['model_reason_similarity'][lang]
    
    # model_reason の reason_dimensions も読み込む
    reason_dimensions = get_message('common.reason_dimensions', lang)
    
    # 両方を結合して返す
    return {**similarity_messages, 'reason_dimensions': reason_dimensions}

# 出力ディレクトリの作成
ensure_output_directories()

def load_reason_data():
    """理由文長データの読み込み"""
    filepath = os.path.join(OUTPUT_DIR, 'model_reason.csv')
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")

def create_correlation_heatmap(reason_trends, lang='ja'):
    """モデル間の相関分析とヒートマップの作成"""
    # モデル間の相関係数を計算
    corr = reason_trends.T.corr()
    
    # ヒートマップの作成
    plt.figure(figsize=VISUALIZATION_CONFIG['figure']['default_size'])
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    messages = load_messages(lang)
    plt.title(messages['correlation_title'], pad=20)
    plt.tight_layout()
    
    # 保存
    save_figure(plt, 'model_reason_correlation', lang=lang)
    
    # 相関行列をCSVとして保存
    corr.to_csv(os.path.join(OUTPUT_DIR, 'model_reason_correlation.csv'))
    return corr

def find_optimal_clusters(reason_trends, lang='ja'):
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
    messages = load_messages(lang)
    plt.xlabel(messages['silhouette_xlabel'])
    plt.ylabel(messages['silhouette_ylabel'])
    plt.title(messages['silhouette_title'])
    plt.grid(True, alpha=VISUALIZATION_CONFIG['plot']['grid_alpha'])
    
    # 保存
    save_figure(plt, 'model_reason_silhouette', lang=lang)
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

def visualize_fcm_gradients(reason_trends, membership, centers, lang='ja', messages=None):
    """FCM結果をグラデーションで可視化"""
    # messages = load_messages(lang) # この行を削除
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
               c='black', marker='x', s=200, label=messages['cluster_center_label_gradient'])
    
    # テキストの重なりを調整
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

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
    save_figure(plt, 'model_reason_fcm_gradient', lang=lang)
    plt.close()

def visualize_fcm_with_memberships(reason_trends, membership, centers, lang='ja', messages=None):
    """FCM結果を所属度付きで可視化"""
    # messages = load_messages(lang) # この行は削除済み
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
               c='black', marker='x', s=200, label=messages['cluster_center_label_membership'])
    
    # テキストの重なりを調整
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

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
    save_figure(plt, 'model_reason_fcm_membership', lang=lang)
    plt.close()

def analyze_cluster_characteristics(reason_trends, membership, centers, n_clusters, messages):
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

def print_generated_files(lang='ja'):
    """生成されたファイルの一覧を表示"""
    messages = load_messages(lang)
    print(messages['generated_files_header'])
    print(messages['correlation_analysis_header'])
    print(f"- {os.path.join(OUTPUT_DIR, 'model_reason_correlation.csv')}")
    figures_dir = os.path.join(OUTPUT_DIR, 'figures', lang)
    print(f"- {os.path.join(figures_dir, 'model_reason_correlation.png')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_correlation.svg')}")
    
    print(messages['cluster_analysis_header'])
    print(f"- {os.path.join(figures_dir, 'model_reason_silhouette.png')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_silhouette.svg')}")
    
    print(messages['fcm_analysis_header'])
    print(f"- {os.path.join(OUTPUT_DIR, 'model_reason_cluster_characteristic.json')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_fcm_gradient.png')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_fcm_gradient.svg')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_fcm_membership.png')}")
    print(f"- {os.path.join(figures_dir, 'model_reason_fcm_membership.svg')}")

def main(lang='ja'):
    # 日本語フォントのインポート（日本語の場合のみ）
    if lang == 'ja':
        import japanize_matplotlib

    # データの読み込み
    messages = load_messages(lang)
    print(messages['loading_data'])
    reason_trends = load_reason_data().set_index('model')
    
    print(messages['running_correlation'])
    corr = create_correlation_heatmap(reason_trends, lang)
    
    print(messages['calculating_clusters'])
    n_clusters = find_optimal_clusters(reason_trends, lang)
    print(messages['optimal_clusters'].format(n_clusters=n_clusters))
    
    print(messages['running_fcm'])
    membership, centers, fcm = perform_fcm_analysis(reason_trends, n_clusters)
    
    print(messages['visualizing_results'])
    print(messages['generating_gradient'])
    visualize_fcm_gradients(reason_trends, membership, centers, lang, messages)
    print(messages['generating_membership'])
    visualize_fcm_with_memberships(reason_trends, membership, centers, lang, messages)
    
    print(messages['analyzing_characteristics'])
    characteristics = analyze_cluster_characteristics(reason_trends, membership, centers, n_clusters, messages)
    
    print(messages['cluster_characteristics_header'])
    for cluster, info in characteristics.items():
        print(f"\n{cluster}:")
        print(messages['cluster_size'].format(size=info['size']))
        print(messages['mean_char_count'])
        for reason, value in info['mean'].items():
            # messagesからreason_dimensionsを取得して使用
            if reason in messages['reason_dimensions']:
                reason_name = messages['reason_dimensions'][reason]
                print(f"  {reason_name}: {value:.2f}")

    print(messages['analysis_complete'])
    print(messages['results_saved_to'].format(output_dir=OUTPUT_DIR))
    print_generated_files(lang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate similarity analysis visualizations.')
    parser.add_argument('--lang', choices=['ja', 'en'], default='ja',
                       help='Language for visualization (ja/en)')
    args = parser.parse_args()
    main(args.lang)
