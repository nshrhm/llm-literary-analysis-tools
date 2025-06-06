# Active Context

## Current Work Focus
- `src/persona_model_emotion.py` の改修:
  - 4つの感情次元のグラフを1つの結合グラフとして出力するように変更。
  - グラフ全体のフォントサイズを調整（`src/config.py` の設定値を1.6倍）。
  - 凡例をグラフ下部に移動し、凡例タイトルのフォントサイズを調整。
- `src/config.py` の更新:
  - `VISUALIZATION_CONFIG['figure']` にフォントサイズ関連の設定（`title_fontsize`, `label_fontsize`, `tick_labelsize`, `legend_fontsize`）を追加し、値を更新。
- `src/messages.json` の更新:
  - `persona_model_emotion` セクションに結合グラフ用のタイトルメッセージ (`combined_title`) を追加。
- ドキュメント (`docs/analysis_scripts_guide.md`, `docs/analysis_scripts_guide_ja.md`) の更新:
  - `src/persona_model_emotion.py` の説明と出力ファイル名を最新の状態に修正。
- Memory Bankの更新（本作業）。

## Recent Changes
- `src/persona_model_emotion.py` を大幅に改修:
  - 従来は感情次元ごとに個別のグラフを生成していたものを、4つの感情次元のグラフを縦に並べた1つの結合グラフ (`persona_model_emotion_combined.png/.svg`) を生成するように変更。
  - X軸（モデル名）と凡例（ペルソナ）を共通化。X軸ラベルは最下部のサブプロットにのみ表示。
  - 凡例をグラフ下部中央に配置し、凡例タイトルのフォントサイズを他の凡例テキストより大きく調整。
  - 各サブプロットのY軸ラベルに感情次元名を表示。
  - 全体のフォントサイズ（タイトル、軸ラベル、目盛りラベル、凡例）を `src/config.py` の設定に基づいて調整可能にし、今回は1.6倍に拡大。
- `src/config.py` を更新:
  - `VISUALIZATION_CONFIG['figure']` に `title_fontsize`, `label_fontsize`, `tick_labelsize`, `legend_fontsize` を追加し、それぞれの値を設定（直近では1.6倍に拡大）。
- `src/messages.json` を更新:
  - `persona_model_emotion` の `ja` と `en` の両方に `combined_title` キーを追加し、結合グラフ用のタイトル文字列を定義。
- `docs/analysis_scripts_guide.md` および `docs/analysis_scripts_guide_ja.md` を更新:
  - `src/persona_model_emotion.py` の説明を、結合グラフを生成する現在の動作に合わせて修正。
  - 生成されるファイル名を `persona_model_emotion_combined.png` および `persona_model_emotion_combined.svg` に更新。
- (以前の変更) `src/persona_model_emotion.py` を修正:
  - `load_data` 関数における `TypeError: unhashable type: 'dict'` エラーを修正（`common.persona_mapping` からの言語別文字列抽出を実装）。
  - グラフ描画時に `PERSONA_COLORS` を使用してペルソナごとの色を適用。
  - `lang='ja'` の場合にのみ `japanize_matplotlib` をインポートするように変更。
- (以前の変更) `src/persona_emotion_visualize.py` を修正:
  - `TypeError: unhashable type: 'dict'` エラーを解決。
  - Seabornの `FutureWarning` を解消。
  - グラフの色設定を、ペルソナの基調色をベースにした感情次元の明度グラデーションに変更。
  - 凡例がグラフと重ならないように、凡例を図の右側に配置し、図の横幅を拡大（(14, 8)）、右側に余白を追加。
- (以前の変更) ペルソナの色定義を`src/messages.json`に移動し、`src/config.py`がそこから読み込むように変更。
- (以前の変更) `.clinerules` を更新:
  - 「視覚化プログラムの原則」に `japanize_matplotlib` の条件付き利用に関するルールを追記。
  - 「Pythonライブラリ利用時の注意点」セクションを新設し、Pandas `map()` 関数のネストした辞書に関する注意点を記載。

## Next Steps
- ユーザーからの次の指示待ち。
- 保留中のタスク:
    - `src/persona_emotion_visualize.py` のレイアウト再調整（凡例とグラフの間のスペース、図の横幅）。
    - similarity系の視覚化スクリプトに言語切り替え機能を実装:
      1. model_emotion_similarity.py
      2. model_reason_similarity.py
      3. persona_emotion_similarity.py
      4. persona_reason_similarity.py
      5. text_emotion_similarity.py
      6. text_reason_similarity.py
    - docs/フォルダ内のドキュメントを更新 (similarity系スクリプトの言語切り替え機能について)。

## Active Decisions and Considerations
- 国際学術誌向けの論文投稿を考慮し、英語と日本語のグラフを切り替えて生成する機能をすべての視覚化スクリプトに適用。
- プログラムの共通化により、スクリプトの保守性と一貫性をさらに向上させる。
- 視覚的な統一性を保つため、開発元ごとの色設定を厳密に適用し、グラフの視認性を高める。
- ペルソナ関連のグラフでは、ペルソナの基調色を維持しつつ、感情次元を明度で区別する方針を採用。
- フォントサイズやレイアウトの調整は、`src/config.py` と各描画スクリプト内のパラメータで行う。

## Important Patterns and Preferences
- スクリプトは「config.py」から設定と共通関数を読み込み、一貫性のある出力ディレクトリや視覚化設定を維持。
- 日本語フォント対応のために「japanize_matplotlib」を使用し、グラフのタイトルやラベルを適切に表示。
- 言語切り替え機能では、日本語グラフを 'results/figures/ja' に、英語グラフを 'results/figures/en' に保存することで、言語を明確に区別する規則を採用。
- コマンドラインオプション --lang で言語を切り替え（ja: 日本語、en: 英語）

## Learnings and Project Insights
- `fig.legend()` の `title_fontsize` パラメータは凡例タイトルのフォントサイズ調整に有効。
- `plt.tight_layout(rect=[left, bottom, right, top])` を使用することで、図全体のレイアウト調整、特に凡例のためのスペース確保が柔軟に行える。
- `VISUALIZATION_CONFIG` のような共通設定ファイルでフォントサイズを一元管理することの重要性。キーの階層構造を正確に把握する必要がある。
- `ax.tick_params` の `ha` 引数は無効であり、X軸ラベルの水平位置調整は `plt.setp(ax.get_xticklabels(), ha='right')` などで行う必要がある。
- (以前の学習) `sns.FacetGrid` を使用することで、カテゴリごとのサブプロット作成と、各サブプロット内での動的な色設定が可能になることを確認。
- (以前の学習) `pd.Categorical` を使用してデータの順序を明示的に指定することの重要性を再認識。
- (以前の学習) Pandas `Series.map()` でネストした辞書を使用すると `TypeError` が発生する可能性があるため、フラットな辞書を渡す必要があることを再確認。
- (以前の学習) `japanize_matplotlib` は日本語表示が必要な場合に限定してインポートすることで、他言語環境への意図しない影響を避けられることを学習。
