# Active Context

## Current Work Focus
- `src/persona_model_emotion.py` の新規作成とMemory Bankへの記録。
- `src/persona_emotion_visualize.py` のレイアウト調整（凡例とグラフの間のスペース調整、横幅調整）。
- `src/messages.json`と`src/config.py`間の設定の重複解消と一元化が完了。

## Recent Changes
- `src/persona_model_emotion.py` を新規作成: ペルソナと感情次元の関係をモデルごとに分析・可視化するスクリプト。
- `src/persona_emotion_visualize.py` を修正:
  - `TypeError: unhashable type: 'dict'` エラーを解決。
  - Seabornの `FutureWarning` を解消。
  - グラフの色設定を、ペルソナの基調色をベースにした感情次元の明度グラデーションに変更。
  - 凡例がグラフと重ならないように、凡例を図の右側に配置し、図の横幅を拡大（(14, 8)）、右側に余白を追加。
- 以前の変更点:
  - 以下の視覚化スクリプトに言語切り替え機能を実装完了:
    - model_emotion_visualize.py
    - text_emotion_visualize.py
    - persona_emotion_visualize.py
    - temperature_emotion_visualize.py
    - model_reason_visualize.py
    - text_reason_visualize.py
    - persona_reason_visualize.py
    - temperature_reason_visualize.py
  - `src/messages.json`を更新し、各視覚化スクリプト用の日本語/英語メッセージを追加。
  - `src/config.py`から`REASON_DIMENSIONS`、`EMOTION_DIMENSIONS`、`PERSONA_MAPPING`、`CLUSTERING_CONFIG['text']['cluster_description']`の定義を削除し、`messages.json`から読み込むように変更。
  - `src/config.py`から重複する読み込み関数を削除し、`get_message`共通関数を導入。

## Next Steps
- `src/persona_emotion_visualize.py` のレイアウト再調整（凡例とグラフの間のスペース、図の横幅）。
- similarity系の視覚化スクリプトに言語切り替え機能を実装:
  1. model_emotion_similarity.py
  2. model_reason_similarity.py
  3. persona_emotion_similarity.py
  4. persona_reason_similarity.py
  5. text_emotion_similarity.py
  6. text_reason_similarity.py
- docs/フォルダ内のドキュメントを更新:
  - analysis_scripts_guide.md と analysis_scripts_guide_ja.md に言語切り替え機能の説明を追加
  - --lang オプションの使用方法を記載
  - 出力ディレクトリ構造（ja/enサブディレクトリ）の変更を説明

## Active Decisions and Considerations
- 国際学術誌向けの論文投稿を考慮し、英語と日本語のグラフを切り替えて生成する機能をすべての視覚化スクリプトに適用。
- プログラムの共通化により、スクリプトの保守性と一貫性をさらに向上させる。
- 視覚的な統一性を保つため、開発元ごとの色設定を厳密に適用し、グラフの視認性を高める。
- ペルソナ関連のグラフでは、ペルソナの基調色を維持しつつ、感情次元を明度で区別する方針を採用。

## Important Patterns and Preferences
- スクリプトは「config.py」から設定と共通関数を読み込み、一貫性のある出力ディレクトリや視覚化設定を維持。
- 日本語フォント対応のために「japanize_matplotlib」を使用し、グラフのタイトルやラベルを適切に表示。
- 言語切り替え機能では、日本語グラフを 'results/figures/ja' に、英語グラフを 'results/figures/en' に保存することで、言語を明確に区別する規則を採用。
- コマンドラインオプション --lang で言語を切り替え（ja: 日本語、en: 英語）

## Learnings and Project Insights
- `sns.FacetGrid` を使用することで、カテゴリごとのサブプロット作成と、各サブプロット内での動的な色設定が可能になることを確認。
- `pd.Categorical` を使用してデータの順序を明示的に指定することの重要性を再認識。
- 欠損値 (`NaN`) がカテゴリカルデータの処理に影響を与える可能性があるため、適切なハンドリングが必要であることを学習。
- モデルの絞り込みやX軸ジッターの適用が、グラフの視認性向上に有効であることを確認。
- 開発元ごとの色統一が、視覚的な一貫性を保ち、論文でのプレゼンテーションを強化することを認識。
- 言語切り替え機能の追加が、国際的な論文投稿において重要な要素であると理解し、主要な視覚化スクリプトに実装完了。
- 共通関数の使用により、コードの重複が減り、スクリプトの保守性が向上したことを実感。
- グラフのレイアウト調整（特に凡例の位置と図のサイズ）は、試行錯誤が必要な場合があることを学習。
