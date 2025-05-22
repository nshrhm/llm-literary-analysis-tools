# Active Context

## Current Work Focus
- グラフ画像内のテキストを英語と日本語に切り替える機能が主要な視覚化スクリプトに実装されました。これにより、`results/figures/ja`と`results/figures/en`にそれぞれ日本語と英語のグラフが保存されるようになりました。
- `src/messages.json`と`src/config.py`間の設定の重複を解消し、共通設定を`messages.json`に一元化する作業に着手しました。

## Recent Changes
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
- `src/messages.json`と`src/config.py`の整理を完了させる。

## Active Decisions and Considerations
- 国際学術誌向けの論文投稿を考慮し、英語と日本語のグラフを切り替えて生成する機能をすべての視覚化スクリプトに適用。
- プログラムの共通化により、スクリプトの保守性と一貫性をさらに向上させる。
- 視覚的な統一性を保つため、開発元ごとの色設定を厳密に適用し、グラフの視認性を高める。

## Important Patterns and Preferences
- スクリプトは「config.py」から設定と共通関数を読み込み、一貫性のある出力ディレクトリや視覚化設定を維持。
- 日本語フォント対応のために「japanize_matplotlib」を使用し、グラフのタイトルやラベルを適切に表示。
- 言語切り替え機能では、日本語グラフを 'results/figures/ja' に、英語グラフを 'results/figures/en' に保存することで、言語を明確に区別する規則を採用。
- コマンドラインオプション --lang で言語を切り替え（ja: 日本語、en: 英語）

## Learnings and Project Insights
- モデルの絞り込みやX軸ジッターの適用が、グラフの視認性向上に有効であることを確認。
- 開発元ごとの色統一が、視覚的な一貫性を保ち、論文でのプレゼンテーションを強化することを認識。
- 言語切り替え機能の追加が、国際的な論文投稿において重要な要素であると理解し、主要な視覚化スクリプトに実装完了。
- 共通関数の使用により、コードの重複が減り、スクリプトの保守性が向上したことを実感。
