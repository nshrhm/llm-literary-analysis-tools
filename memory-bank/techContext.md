## Statistical Analysis Tools and Methods
- Using Python data science libraries:
  - pandas: Data manipulation and CSV I/O. (Note: When using `Series.map()` with a dictionary, ensure the dictionary values are hashable types, not nested dictionaries, to avoid `TypeError`.)
  - numpy: Core numerical operations
  - scipy.stats: Advanced statistical calculations (skewness, kurtosis)
  
## Model Emotion Analysis Framework
- Statistical measures implemented:
  - Descriptive stats: max, min, mean, median, std_dev
  - Distribution analysis: skewness, kurtosis
- Data processing workflow:
  1. Read model_emotion.csv
  2. Calculate statistics per metric (Q1-Q4)
  3. Output formatted results to CSV
  4. Round values to 3 decimal places for clarity

## Visualization Tools and Standards
- Using Python visualization libraries:
  - matplotlib: Core plotting functionality
  - seaborn: Enhanced statistical visualizations
  - japanize_matplotlib: Used for Japanese font support. Imported conditionally only when `lang='ja'` to avoid unnecessary font setting changes in English-only graphs.
- Visualization principles:
  - Consistent styling defined in src/config.py (e.g., figure sizes, DPI, color schemes, and font sizes like `title_fontsize`, `label_fontsize`, `tick_labelsize`, `legend_fontsize` within `VISUALIZATION_CONFIG['figure']`).
  - Vendor-specific color coding using VENDOR_COLORS from config.py
  - Specific ordering of literary works on X-axis as defined in config.py ('懐中時計', 'お金とピストル', 'ぼろぼろな駝鳥')
  - Violin plot styling with transparent fill and emphasized outlines (fill=False, linewidth=2.0)
  - Persona-based emotion dimension coloring: Graphs now use persona's base color with varying lightness for different emotion dimensions, achieved via `get_emotion_color_from_persona_base` in `src/config.py`.
  - `src/persona_model_emotion.py` generates a single combined bar plot displaying persona-specific emotion scores for each model across all four emotional dimensions (Q1-Q4). The subplots are arranged vertically, sharing a common X-axis and legend. Bar colors are set according to `PERSONA_COLORS` defined in `config.py`.

## Future Development Plans
- Language switching functionality:
  - グラフ画像内のテキストを英語と日本語に切り替える機能が主要な視覚化スクリプトに実装されました。
  - `src/messages.json`に日本語と英語のメッセージを構造化して定義し、`src/config.py`からこれらのメッセージを読み込む共通関数を導入しました。
  - コマンドラインオプション `--lang` を使用して、グラフのテキストを日本語または英語に切り替える機能が実装されました。
  - 日本語グラフは `results/figures/ja` に、英語グラフは `results/figures/en` に保存されるようになりました。
- Code centralization:
  - `src/config.py`と`src/messages.json`間の設定の重複を解消し、`REASON_DIMENSIONS`、`EMOTION_DIMENSIONS`、`PERSONA_MAPPING`、`CLUSTERING_CONFIG['text']['cluster_description']`を`messages.json`に一元化する作業が完了しました。
  - `config.py`からは、これらの情報を`messages.json`から読み込むように変更し、重複する読み込み関数を削除しました。
  - `config.py`に、指定された言語とキーに基づいて`messages.json`からメッセージを取得する共通関数を導入しました。
