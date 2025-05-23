# Progress

## What Works
- すべての感情分析スクリプトが完成し、動作確認済み。特に「temperature_emotion_visualize.py」と「temperature_reason_visualize.py」を更新し、論文向けの特定グラフ（「*_sorted.png (svg)」と「*_selected.png (svg)」）のみを生成するように最適化。
- グラフの視認性向上のため、モデルを上位3モデルと下位3モデルに絞り、X軸にジッターを適用。
- 開発元ごとに色を統一するために「config.py」に定義されている「VENDOR_COLORS」を参照し、グラフの視覚的な一貫性を確保。
- 以下の視覚化スクリプトに言語切り替え機能を実装完了:
  - model_emotion_visualize.py
  - text_emotion_visualize.py
  - persona_emotion_visualize.py
  - temperature_emotion_visualize.py
  - model_reason_visualize.py
  - text_reason_visualize.py
  - persona_reason_visualize.py
  - temperature_reason_visualize.py
- プログラムの共通化を進め、src/config.pyに視覚化の共通関数を追加し、スクリプトの保守性を向上。
- 日本語グラフを 'results/figures/ja' に、英語グラフを 'results/figures/en' に保存する機能を追加。
- `src/messages.json`と`src/config.py`間の設定の重複を解消し、共通設定を`messages.json`に一元化する作業に着手しました。

## What's Left to Build
- similarity系の視覚化スクリプトへの言語切り替え機能の実装:
  1. model_emotion_similarity.py
  2. model_reason_similarity.py
  3. persona_emotion_similarity.py
  4. persona_reason_similarity.py
  5. text_emotion_similarity.py
  6. text_reason_similarity.py
- ドキュメントの更新:
  - docs/analysis_scripts_guide.md と analysis_scripts_guide_ja.md に言語切り替え機能の説明を追加
  - --lang オプションの使用方法を記載
  - 出力ディレクトリ構造の変更説明を追加
- `src/messages.json`と`src/config.py`の整理を完了させる。

## Current Status
- 感情分析スクリプトの開発が一通り完了し、動作確認が済んでいる状態。
- 主要なスクリプトへの言語切り替え機能の実装が完了し、similarity系スクリプトへの実装を開始予定。
- messages.jsonにすべての必要なメッセージを追加し、言語切り替えの基盤を整備完了。

## Known Issues
- なし（現在のところ、ユーザーのリクエストに基づく修正はすべて実施済み）。

## Evolution of Project Decisions
- 初期のスクリプトではすべてのモデルとグラフを生成していたが、論文での使用を考慮し、必要なグラフのみを生成するように変更。
- 視認性向上のため、標準偏差付きグラフでモデルを上位3モデルと下位3モデルに絞り、X軸にジッターを適用する決定。
- 視覚的な統一性を保つため、開発元ごとの色設定を「config.py」から参照して適用する方針を採用。
- 国際学術誌向けの論文投稿を考慮し、英語と日本語のグラフを切り替えて生成する機能を追加し、主要なスクリプトに実装完了。
- プログラムの共通化を進めるため、視覚化の共通関数を「config.py」に追加し、スクリプトの保守性を向上させる方針を採用。
- 日本語グラフを 'results/figures/ja' に、英語グラフを 'results/figures/en' に保存する方針を採用し、コードとドキュメントに反映。
- コマンドラインオプション --lang による言語切り替え方式を標準化し、すべてのスクリプトで統一的に実装する方針を採用。
