"""Configuration settings for analysis scripts."""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Output directory for analysis results
OUTPUT_DIR = "results"

# 感情次元の定義
EMOTION_DIMENSIONS = {
    'Q1value': '面白さ',
    'Q2value': '驚き',
    'Q3value': '悲しみ',
    'Q4value': '怒り'
}

# 理由文の定義
REASON_DIMENSIONS = {
    'Q1reason': '面白さの理由',
    'Q2reason': '驚きの理由',
    'Q3reason': '悲しみの理由',
    'Q4reason': '怒りの理由'
}

# 視覚化の共通設定
VISUALIZATION_CONFIG = {
    'figure': {
        'default_size': (20, 12),
        'dpi': 300,
    },
    'plot': {
        'grid_alpha': 0.3,
        'text_box_alpha': 0.8,
    },
    'save': {
        'formats': ['png', 'svg'],
        'bbox_inches': 'tight'
    }
}

# Analysis target columns
ANALYSIS_COLUMNS = {
    'values': list(EMOTION_DIMENSIONS.keys()),
    'reasons': ['Q1reason', 'Q2reason', 'Q3reason', 'Q4reason'],
}
ANALYSIS_COLUMNS['all'] = ANALYSIS_COLUMNS['values'] + ANALYSIS_COLUMNS['reasons']

# クラスタリング分析の設定
CLUSTERING_CONFIG = {
    'max_clusters': 10,
    'colors': {
        'cluster': ['#9932CC', '#FFD700']  # パープル、ゴールド
    },
    'text': {
        'cluster_description': {
            1: '高感情表現型（面白さが特に高い、12モデル）',
            2: 'バランス型（感情値が均一、24モデル）'
        }
    }
}

# Common file paths
DATA_PATHS = {
    'input': './data_all.csv',
    'missing_report': f"{OUTPUT_DIR}/missing_values_report.csv",
    'missing_by_model': f"{OUTPUT_DIR}/missing_values_by_model.csv",
    'missing_summary': f"{OUTPUT_DIR}/missing_values_summary.csv"
}

# ファイル操作の共通関数
def ensure_output_directories():
    """必要な出力ディレクトリを作成"""
    dirs = [
        OUTPUT_DIR,
        f"{OUTPUT_DIR}/figures"
    ]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"ディレクトリを作成しました: {dir_path}")

def save_figure(plt, filename, output_dir=OUTPUT_DIR):
    """図を複数フォーマットで保存する共通関数"""
    fig_dir = os.path.join(output_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    base_path = os.path.join(fig_dir, filename)
    saved_files = []
    for fmt in VISUALIZATION_CONFIG['save']['formats']:
        full_path = f"{base_path}.{fmt}"
        plt.savefig(
            full_path,
            dpi=VISUALIZATION_CONFIG['figure']['dpi'],
            bbox_inches=VISUALIZATION_CONFIG['save']['bbox_inches']
        )
        saved_files.append(full_path)
    return saved_files

def safe_read_csv(file_path):
    """エラーハンドリング付きでCSVファイルを読み込む"""
    try:
        return pd.read_csv(file_path), None
    except FileNotFoundError:
        return None, f"エラー：ファイル '{file_path}' が見つかりません。"
    except Exception as e:
        return None, f"エラー：ファイル '{file_path}' の読み込み中にエラーが発生しました：{e}"

# データ読み込みの共通関数
def load_emotion_data(filename="model_emotion.csv"):
    """感情分析データの読み込み共通関数"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")

# モデル開発元の定義
VENDOR_PATTERNS = {
    'OpenAI': ['gpt-', 'o'],
    'Anthropic': ['claude-'],
    'Google': ['gemini-'],
    'DeepSeek': ['DeepSeek-'],
    'Llama': ['Llama-'],
    'Qwen': ['Qwen'],
    'Gemma': ['gemma-'],
    'Grok': ['grok-']
}

# ペルソナの定義
PERSONA_MAPPING = {
    'p1': '大学1年生',
    'p2': '文学研究者',
    'p3': '感情豊かな詩人',
    'p4': '無感情なロボット'
}

# 開発元ごとの色定義
VENDOR_COLORS = {
    'OpenAI': '#74AA9C',      # ティールグリーン
    'Anthropic': '#7B61FF',   # パープル
    'Google': '#4285F4',      # Googleブルー
    'DeepSeek': '#FF6B6B',    # コーラル
    'Llama': '#FFB86C',       # オレンジ
    'Qwen': '#50FA7B',        # ライムグリーン
    'Gemma': '#BD93F9',       # ライトパープル
    'Grok': '#FF79C6'         # ピンク
}

# モデルの順序定義
MODEL_ORDER = [
    "o4-mini", "o3", "o3-mini", "o1-mini",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4o", "gpt-4o-mini",
    "gemini-2.5-pro-preview-03-25", "gemini-2.5-flash-preview-04-17",
    "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.0-pro-exp",
    "gemini-2.0-flash-thinking-exp", "gemma-3-27b-it", "gemma-3-12b-it",
    "gemma-3-4b-it", "gemma-3-1b-it", "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022",
    "claude-3-haiku-20240307", "grok-3-latest", "grok-3-fast-latest",
    "grok-3-mini-latest", "grok-3-mini-fast-latest", "grok-2-latest",
    "DeepSeek-R1", "DeepSeek-V3-0324", "DeepSeek-V3",
    "Llama-4-Maverick-17B", "Llama-4-Scout-17B", "Llama-3.3-70B-Instruct-Turbo",
    "Qwen3-235B-A22B-FP8", "Qwen2.5-VL-7B-Instruct"
]
