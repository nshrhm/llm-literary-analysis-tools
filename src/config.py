"""Configuration settings for analysis scripts."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import json

# Output directory for analysis results
OUTPUT_DIR = "results"

# messages.jsonのキャッシュ
_messages_cache = None

def _load_messages():
    """messages.jsonを読み込み、キャッシュする内部関数"""
    global _messages_cache
    if _messages_cache is None:
        with open('src/messages.json', 'r', encoding='utf-8') as f:
            _messages_cache = json.load(f)
    return _messages_cache

def get_message(key_path, lang='ja'):
    """
    messages.jsonから指定されたキーパスと言語のメッセージを取得する。
    例: get_message('common.emotion_dimensions.Q1value', 'ja')
    """
    messages = _load_messages()
    keys = key_path.split('.')

    current_dict = messages # トップレベルから検索を開始

    for i, key in enumerate(keys):
        if key in current_dict:
            current_dict = current_dict[key]
        elif i == 0 and key == lang: # 最初のキーが言語の場合
            current_dict = messages.get(lang, {})
        elif i == 0 and key == 'common': # 最初のキーがcommonの場合
            current_dict = messages.get('common', {})
        else:
            raise KeyError(f"Key path '{key_path}' not found in messages.json for language '{lang}' or common section.")
    return current_dict

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
    'values': list(get_message('common.emotion_dimensions').keys()),
    'reasons': list(get_message('common.reason_dimensions').keys()),
}
ANALYSIS_COLUMNS['all'] = ANALYSIS_COLUMNS['values'] + ANALYSIS_COLUMNS['reasons']

# 感情次元の定義
EMOTION_DIMENSIONS = get_message('common.emotion_dimensions')

# 理由次元の定義
REASON_DIMENSIONS = get_message('common.reason_dimensions')

# クラスタリング分析の設定
CLUSTERING_CONFIG = {
    'max_clusters': 10,
    'colors': {
        'cluster': ['#9932CC', '#FFD700']  # パープル、ゴールド
    },
    'text': {
        'cluster_description': {
            1: get_message('model_emotion_similarity.ja.cluster_description').split('\n')[1].strip().replace('　', ''), # 日本語のクラスタ1の説明
            2: get_message('model_emotion_similarity.ja.cluster_description').split('\n')[2].strip().replace('　', '')  # 日本語のクラスタ2の説明
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

def save_figure(plt, filename, output_dir=OUTPUT_DIR, lang='ja'):
    """図を複数フォーマットで保存する共通関数。言語に応じたディレクトリに保存"""
    lang_dir = 'ja' if lang == 'ja' else 'en'
    fig_dir = os.path.join(output_dir, 'figures', lang_dir)
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

# 視覚化の共通関数
def create_melted_data(data, id_vars, value_vars, var_name='emotion', value_name='value', value_mapping=None):
    """データを縦持ちに変換する共通関数"""
    melted_data = pd.melt(data, 
                          id_vars=id_vars,
                          value_vars=value_vars,
                          var_name=var_name,
                          value_name=value_name)
    if value_mapping:
        melted_data[var_name] = melted_data[var_name].map(value_mapping)
    return melted_data

def setup_figure(figsize=None, gridspec=None):
    """図とサブプロットの設定を統一する共通関数"""
    if figsize is None:
        figsize = VISUALIZATION_CONFIG['figure']['default_size']
    fig = plt.figure(figsize=figsize, dpi=VISUALIZATION_CONFIG['figure']['dpi'])
    if gridspec:
        if isinstance(gridspec, (list, tuple)) and len(gridspec) == 3:
            gs = fig.add_gridspec(gridspec[0], gridspec[1], **gridspec[2])
        else:
            gs = fig.add_gridspec(*gridspec)
        return fig, gs
    return fig, None

def add_header_text(ax, text, position=(0.5, 1.05), alpha=0.8):
    """グラフ上部にヘッダーテキストを追加する共通関数"""
    ax.text(position[0], position[1], text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=alpha, edgecolor='none'))

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

# モデル開発元の色の定義
VENDOR_COLORS = {
    'OpenAI': '#4285F4',  # Google Blue
    'Anthropic': '#EA4335', # Google Red
    'Google': '#34A853',   # Google Green
    'DeepSeek': '#8B008B', # Dark Magenta
    'Llama': '#FF9900',    # Orange
    'Qwen': '#00CED1',     # Dark Cyan
    'Gemma': '#FF69B4',    # Hot Pink
    'Grok': '#A0522D'      # Sienna
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

# 文学作品の順序定義
TEXT_ORDER = list(get_message('common.text_mapping').keys())
