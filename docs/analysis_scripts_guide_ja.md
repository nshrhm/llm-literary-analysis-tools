# データ分析スクリプト ガイド

本ドキュメントでは、LLMを用いた感情分析プロジェクトで使用される主要なデータ分析Pythonスクリプトについて説明します。

## 前提条件と注意事項
- 各スクリプトは実行時に必要なディレクトリ（results/およびそのサブディレクトリ）が存在しない場合、自動的に作成します
- 出力ファイルは全てresultsディレクトリ以下に生成されます
- プロジェクトルートディレクトリから実行することを想定しています

## スクリプト一覧

### 1. `src/missing_values_analysis.py`
- **説明**: 実験結果データ ( `data_all.csv` ) を読み込み、モデルごとの欠損値割合を計算し、期待される結果数 (120件) に満たないモデルを特定し、各感情次元の値と理由の欠損率および平均欠損率をレポートします。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/missing_values_analysis.py
  ```
- **生成されるファイル**: `results/missing_values_by_model.csv`, `results/missing_values_report.csv`, `results/missing_values_summary.csv`

### 2. `src/missing_values_visualize.py`
- **説明**: 実験結果データ ( `data_all.csv` ) を読み込み、モデルごとの欠損値割合を視覚化したグラフを作成します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/missing_values_visualize.py
  ```
- **生成されるファイル**: `results/missing_values_q1value.png`, `results/missing_values_q1reason.png`, ... 、q1,q2,q3,q4のvalueとreasonについてpngとsvg形式のグラフが生成されます。
- **注意**: `missing_values_visualize.py`は、`missing_values_analysis.py`を実行した後に実行することを推奨します。

### 3. `src/model_emotion_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、モデルごとの感情次元の傾向を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_emotion_analysis.py
  ```
- **生成されるファイル**: `results/model_emotion.csv`

### 4. `src/model_emotion_statistics.py`
- **説明**: 分析データ ( `results/model_emotion.csv` ) を読み込み、モデルごとの感情次元の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_emotion_statistics.py
  ```
- **生成されるファイル**: `results/model_emotion_statistics.csv`
- **注意**:  `src/model_emotion_statistics.py` は、 `src/model_emotion_analysis.py` を実行した後に実行することを推奨します。

### 5. `src/model_emotion_visualize.py`
- **説明**: 分析データ ( `results/model_emotion.csv` ) を読み込み、モデルごとの感情次元を視覚的に表現します。
- **実行方法**:
  ```bash
  python ./src/model_emotion_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/model_emotion.png`, `results/figures/model_emotion_distribution.png`
  - `results/figures/model_emotion.svg`, `results/figures/model_emotion_distribution.svg`
- **注意**: `src/model_emotion_visualize.py` は、 `src/model_emotion_analysis.py` を実行した後に実行することを推奨します。

### 6. `src/model_emotion_similarity.py`
- **説明**: モデルごとの感情次元の傾向について相関分析、FCMクラスタリング分析を行います。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_emotion_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: `results/model_emotion_correlations.csv`, `results/figures/model_emotion_correlations.png`, `results/figures/model_emotion_correlations.svg`
  2. クラスター分析: `results/figures/model_emotion_silhouette.png`, `results/figures/model_emotion_silhouette.svg`
  3. FCM分析結果: `results/model_emotion_cluster_characteristics.json`, `results/figures/model_emotion_fcm_gradient.png`, `results/figures/model_emotion_fcm_gradient.svg`, `results/figures/model_emotion_fcm_membership.png`, `results/figures/model_emotion_fcm_membership.svg`
- **注意**: `src/model_emotion_similarity.py`は、`src/model_emotion_analysis.py`を実行した後に実行することを推奨します。

### 7. `src/model_reason_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、モデルごとの理由生成文の文字数の傾向を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_reason_analysis.py
  ```
- **生成されるファイル**: `results/model_reason.csv`

### 8. `src/model_reason_statistics.py`
- **説明**: 分析データ ( `results/model_reason.csv` ) を読み込み、モデルごとのモデルごとの理由生成文の文字数の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_reason_statistics.py
  ```
- **生成されるファイル**: `results/model_reason_statistics.csv`
- **注意**:  `src/model_reason_statistics.py` は、 `src/model_reason_analysis.py` を実行した後に実行することを推奨します。

### 9. `src/model_reason_visualize.py`
- **説明**: 分析データ ( `results/model_reason.csv` ) を読み込み、モデルごとのモデルごとの理由生成文の文字数の傾向を可視化します。
- **実行方法**:
  ```bash
  python ./src/model_reason_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/model_reason.png`, `results/figures/model_reason_distribution.png`
  - `results/figures/model_reason.svg`, `results/figures/model_reason_distribution.svg`
  - `results/figures/model_reason_sorted_all.png`, `results/figures/model_reason_sorted_all.svg`
  - `results/figures/model_reason_sorted_q1.png`, `results/figures/model_reason_sorted_q2.png`, `results/figures/model_reason_sorted_q3.png`, `results/figures/model_reason_sorted_q4.png`
  - `results/figures/model_reason_sorted_q1.svg`, `results/figures/model_reason_sorted_q2.svg`, `results/figures/model_reason_sorted_q3.svg`, `results/figures/model_reason_sorted_q4.svg`
- **注意**: `src/model_reason_visualize.py` は、 `src/model_reason_analysis.py` を実行した後に実行することを推奨します。

### 10. `src/model_reason_similarity.py`
- **説明**: モデルごとの理由生成文の文字数の傾向について相関分析、FCMクラスタリング分析を行ないます。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/model_reason_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: `results/model_reason_correlations.csv`, `results/figures/model_reason_correlations.png`, `results/figures/model_reason_correlations.svg`
  2. クラスター分析: `results/figures/model_reason_silhouette.png`, `results/figures/model_reason_silhouette.svg`
  3. FCM分析結果: `results/model_reason_cluster_characteristics.json`, `results/figures/model_reason_fcm_gradient.png`, `results/figures/model_reason_fcm_gradients.svg`, `results/figures/model_reason_fcm_membership.png`, `results/figures/model_reason_fcm_membership.svg`
- **注意**: `src/model_reason_similarity.py`は、`src/model_reason_analysis.py`を実行した後に実行することを推奨します。

### 11. `src/text_emotion_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、文学作品ごとの感情次元の傾向を分析します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_emotion_analysis.py
  ```
- **生成されるファイル**:
  - `results/text_emotion.csv`: 文学作品とモデルの組み合わせごとの感情値
  - `results/text_emotion_average.csv`: 文学作品ごとの平均感情値

### 12. `src/text_emotion_statistics.py`
- **説明**: 分析データ ( `results/text_emotion.csv` ) を読み込み、文学作品ごとの感情次元の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_emotion_statistics.py
  ```
- **生成されるファイル**: `results/text_emotion_statistics.csv`
- **注意**: `src/text_emotion_statistics.py` は、 `src/text_emotion_analysis.py` を実行した後に実行することを推奨します。

### 13. `src/text_emotion_visualize.py`
- **説明**: 分析データ ( `results/text_emotion.csv` ) を読み込み、文学作品ごとの感情次元を視覚的に表現します。
- **実行方法**:
  ```bash
  python ./src/text_emotion_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/text_emotion.png`: 感情次元の平均値比較グラフ
  - `results/figures/text_emotion.svg`: 同上（SVG形式）
  - `results/figures/text_emotion_distribution.png`: 感情値分布のバイオリンプロット
  - `results/figures/text_emotion_distribution.svg`: 同上（SVG形式）
- **注意**: `src/text_emotion_visualize.py` は、 `src/text_emotion_analysis.py` を実行した後に実行することを推奨します。

### 14. `src/text_emotion_similarity.py`
- **説明**: 文学作品間の感情パターンの類似性を分析します。相関分析とレーダーチャートによる可視化を行います。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_emotion_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: 
     - `results/text_emotion_correlation.csv`: 文学作品間の感情値相関行列
     - `results/figures/text_emotion_correlation.png`: 相関ヒートマップ
     - `results/figures/text_emotion_correlation.svg`: 同上（SVG形式）
  2. 感情パターン分析:
     - `results/figures/text_emotion_patterns.png`: レーダーチャートによる感情パターン比較
     - `results/figures/text_emotion_patterns.svg`: 同上（SVG形式）
- **注意**: `src/text_emotion_similarity.py`は、`src/text_emotion_analysis.py`を実行した後に実行することを推奨します。

### 15. `src/text_reason_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、文学作品ごとの理由生成文の文字数の傾向を分析します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_reason_analysis.py
  ```
- **生成されるファイル**:
  - `results/text_reason.csv`: 文学作品とモデルの組み合わせごとの理由文長
  - `results/text_reason_average.csv`: 文学作品ごとの平均理由文長

### 16. `src/text_reason_statistics.py`
- **説明**: 分析データ (`results/text_reason.csv`) を読み込み、文学作品ごとの理由文長の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_reason_statistics.py
  ```
- **生成されるファイル**: `results/text_reason_statistics.csv`
- **注意**: `src/text_reason_statistics.py`は、`src/text_reason_analysis.py`を実行した後に実行することを推奨します。

### 17. `src/text_reason_similarity.py`
- **説明**: 文学作品間の理由文長パターンの類似性を分析します。相関分析とレーダーチャートによる可視化を行います。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_reason_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: 
     - `results/text_reason_correlation.csv`: 文学作品間の理由文長相関行列
     - `results/figures/text_reason_correlation.png`: 相関ヒートマップ
     - `results/figures/text_reason_correlation.svg`: 同上（SVG形式）
  2. パターン分析:
     - `results/figures/text_reason_patterns.png`: レーダーチャートによる理由文長パターン比較
     - `results/figures/text_reason_patterns.svg`: 同上（SVG形式）
- **注意**: `src/text_reason_similarity.py`は、`src/text_reason_analysis.py`を実行した後に実行することを推奨します。

### 18. `src/text_reason_visualize.py`
- **説明**: 分析データ (`results/text_reason.csv`) を読み込み、文学作品ごとの理由文長を視覚的に表現します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/text_reason_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/text_reason.png`: 理由文長の平均値比較グラフ
  - `results/figures/text_reason.svg`: 同上（SVG形式）
  - `results/figures/text_reason_distribution.png`: 理由文長分布のバイオリンプロット
  - `results/figures/text_reason_distribution.svg`: 同上（SVG形式）
- **注意**: `src/text_reason_visualize.py` は、`src/text_reason_analysis.py` を実行した後に実行することを推奨します。

### 19. `src/persona_emotion_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、ペルソナごとの感情次元の傾向を分析します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_emotion_analysis.py
  ```
- **生成されるファイル**:
  - `results/persona_emotion.csv`: ペルソナとモデルの組み合わせごとの感情値
  - `results/persona_emotion_average.csv`: ペルソナごとの平均感情値

### 20. `src/persona_emotion_statistics.py`
- **説明**: 分析データ (`results/persona_emotion_average.csv`) を読み込み、ペルソナごとの感情次元の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_emotion_statistics.py
  ```
- **生成されるファイル**: `results/persona_emotion_statistics.csv`
- **注意**: `src/persona_emotion_statistics.py` は、 `src/persona_emotion_analysis.py` を実行した後に実行することを推奨します。

### 21. `src/persona_emotion_visualize.py`
- **説明**: 分析データ (`results/persona_emotion.csv`) を読み込み、ペルソナごとの感情次元を視覚的に表現します。
- **実行方法**:
  ```bash
  python ./src/persona_emotion_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/persona_emotion.png`: 感情次元の平均値比較グラフ
  - `results/figures/persona_emotion.svg`: 同上（SVG形式）
  - `results/figures/persona_emotion_distribution.png`: 感情値分布のバイオリンプロット
  - `results/figures/persona_emotion_distribution.svg`: 同上（SVG形式）
- **注意**: `src/persona_emotion_visualize.py` は、 `src/persona_emotion_analysis.py` を実行した後に実行することを推奨します。

### 22. `src/persona_model_emotion.py`
- **説明**: ペルソナと感情次元の関係をモデルごとに分析・可視化します。4つの感情次元（Q1-Q4）すべての棒グラフを縦に並べ、凡例とX軸（モデル名、最下部のみ表示）を共通化した単一の結合画像ファイルを生成します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_model_emotion.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**: 
  - `results/figures/ja/persona_model_emotion_combined.png`
  - `results/figures/ja/persona_model_emotion_combined.svg`
  - (英語版は `results/figures/en/` に保存されます)
- **注意**: このスクリプトは `data_all.csv` を直接読み込みます。

### 23. `src/persona_emotion_similarity.py`
- **説明**: ペルソナ間の感情パターンの類似性を分析します。相関分析とレーダーチャートによる可視化を行います。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_emotion_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: 
     - `results/persona_emotion_correlation.csv`: ペルソナ間の感情値相関行列
     - `results/figures/persona_emotion_correlation.png`: 相関ヒートマップ
     - `results/figures/persona_emotion_correlation.svg`: 同上（SVG形式）
  2. 感情パターン分析:
     - `results/figures/persona_emotion_patterns.png`: レーダーチャートによる感情パターン比較
     - `results/figures/persona_emotion_patterns.svg`: 同上（SVG形式）
- **注意**: `src/persona_emotion_similarity.py`は、`src/persona_emotion_analysis.py`を実行した後に実行することを推奨します。

### 24. `src/persona_reason_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、ペルソナごとの理由生成文の文字数の傾向を分析します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_reason_analysis.py
  ```
- **生成されるファイル**:
  - `results/persona_reason.csv`: ペルソナとモデルの組み合わせごとの理由文長
  - `results/persona_reason_average.csv`: ペルソナごとの平均理由文長

### 25. `src/persona_reason_statistics.py`
- **説明**: 分析データ (`results/persona_reason.csv`) を読み込み、ペルソナごとの理由文長の基本統計量を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_reason_statistics.py
  ```
- **生成されるファイル**: `results/persona_reason_statistics.csv`
- **注意**: `src/persona_reason_statistics.py`は、`src/persona_reason_analysis.py`を実行した後に実行することを推奨します。

### 26. `src/persona_reason_visualize.py`
- **説明**: 分析データ (`results/persona_reason.csv`) を読み込み、ペルソナごとの理由文長を視覚的に表現します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_reason_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/persona_reason.png`: 理由文長の平均値比較グラフ
  - `results/figures/persona_reason.svg`: 同上（SVG形式）
  - `results/figures/persona_reason_distribution.png`: 理由文長分布のバイオリンプロット
  - `results/figures/persona_reason_distribution.svg`: 同上（SVG形式）
- **注意**: `src/persona_reason_visualize.py` は、`src/persona_reason_analysis.py` を実行した後に実行することを推奨します。

### 27. `src/persona_reason_similarity.py`
- **説明**: ペルソナ間の理由文長パターンの類似性を分析します。相関分析とレーダーチャートによる可視化を行います。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/persona_reason_similarity.py [--lang {ja,en}]
  ```
- **オプション**:
  - `--lang`: 可視化時の言語 (デフォルト: ja)
    - `ja`: 日本語
    - `en`: 英語
- **生成されるファイル**:
  1. 相関分析: 
     - `results/persona_reason_correlation.csv`: ペルソナ間の理由文長相関行列
     - `results/figures/persona_reason_correlation.png`: 相関ヒートマップ
     - `results/figures/persona_reason_correlation.svg`: 同上（SVG形式）
  2. パターン分析:
     - `results/figures/persona_reason_patterns.png`: レーダーチャートによる理由文長パターン比較
     - `results/figures/persona_reason_patterns.svg`: 同上（SVG形式）
- **注意**: `src/persona_reason_similarity.py`は、`src/persona_reason_analysis.py`を実行した後に実行することを推奨します。

### 28. `src/temperature_emotion_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、temperature設定による感情次元の変化を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/temperature_emotion_analysis.py
  ```
- **生成されるファイル**: `results/temperature_emotion.csv`
- **注意**: このスクリプトは、実験結果データが `data_all.csv` に存在することを前提としています。

### 29. `src/temperature_emotion_statistics.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、temperature設定による感情次元の統計的指標を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/temperature_emotion_statistics.py
  ```
- **生成されるファイル**: `results/temperature_emotion_statistics.csv`
- **注意**: このスクリプトは、実験結果データが `data_all.csv` に存在することを前提としています。

### 30. `src/temperature_emotion_visualize.py`
- **説明**: 分析データ (`results/temperature_emotion.csv` および `results/temperature_emotion_statistics.csv`) を読み込み、temperatureによる感情値の変化を視覚的に表現します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/temperature_emotion_visualize.py
  ```
- **生成されるファイル**: 
  - `results/figures/temperature_emotion_overall.png`, `results/figures/temperature_emotion_overall.svg`
  - 各感情次元ごとのグラフ: `results/figures/temperature_emotion_{dimension}_all.png`, `results/figures/temperature_emotion_{dimension}_all.svg`
  - 標準偏差付きグラフ: `results/figures/temperature_emotion_{dimension}_std_selected.png`, `results/figures/temperature_emotion_{dimension}_std_selected.svg`
- **注意**: `src/temperature_emotion_visualize.py` は、`src/temperature_emotion_analysis.py` および `src/temperature_emotion_statistics.py` を実行した後に実行することを推奨します。

### 31. `src/temperature_reason_analysis.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、temperature設定による生成テキスト量（理由の文字数）の変化を計算します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/temperature_reason_analysis.py
  ```
- **生成されるファイル**: 
  - `results/temperature_reason.csv`: 全体のテキスト量の平均値
  - `results/temperature_reason_detailed.csv`: 各感情次元ごとのテキスト量の詳細分析
- **注意**: このスクリプトは、実験結果データが `data_all.csv` に存在することを前提としています。

### 32. `src/temperature_reason_visualize.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、temperatureによる生成テキストの多様性や類似度を分析し視覚化します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/temperature_reason_visualize.py
  ```
- **生成されるファイル**: 
  - `results/temperature_reason_diversity.csv`: 多様性スコアの分析結果
  - `results/temperature_reason_correlation_diversity.csv`: temperatureと多様性指標の相関分析結果
  - グラフ: `results/figures/temperature_reason_similarity_selected.png`, `results/figures/temperature_reason_similarity_selected.svg`
  - グラフ: `results/figures/temperature_reason_diversity_selected.png`, `results/figures/temperature_reason_diversity_selected.svg`
  - グラフ: `results/figures/temperature_reason_correlation_similarity_sorted.png`, `results/figures/temperature_reason_correlation_similarity_sorted.svg`
  - グラフ: `results/figures/temperature_reason_correlation_diversity_sorted.png`, `results/figures/temperature_reason_correlation_diversity_sorted.svg`
- **注意**: このスクリプトは、実験結果データが `data_all.csv` に存在することを前提としています。

### 33. `src/create_data_sample.py`
- **説明**: 実験結果データ (`data_all.csv`) を読み込み、trial値が1から3までのデータを抽出し、サンプルデータとして保存します。
- **実行方法**: プロジェクトルートディレクトリから以下のコマンドを実行します。
  ```bash
  python ./src/create_data_sample.py
  ```
- **生成されるファイル**: 
  - `data_sample.csv`: trial値が1から3までのデータを抽出したサンプルデータ
- **注意**: このスクリプトは、実験結果データが `data_all.csv` に存在することを前提としています。
