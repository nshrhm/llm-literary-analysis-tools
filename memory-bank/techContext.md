## Statistical Analysis Tools and Methods
- Using Python data science libraries:
  - pandas: Data manipulation and CSV I/O
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
  - japanize_matplotlib: Japanese font support for proper rendering of text in graphs
- Visualization principles:
  - Consistent styling defined in src/config.py (e.g., figure sizes, DPI, color schemes)
  - Vendor-specific color coding using VENDOR_COLORS from config.py
  - Specific ordering of literary works on X-axis as defined in config.py ('懐中時計', 'お金とピストル', 'ぼろぼろな駝鳥')
  - Violin plot styling with transparent fill and emphasized outlines (fill=False, linewidth=2.0)

## Future Development Plans
- Language switching functionality:
  - Implementation of message files for Japanese and English text in graphs
  - Command-line options for language selection (--lang=ja/en) during script execution
  - Separate output directories or filename suffixes for different language versions
- Code centralization:
  - Extension of src/config.py to include more common functions and utilities
  - Consolidation of repeated code blocks (data loading, graph saving, statistical calculations) into shared modules
  - Unified visualization settings in config.py for consistent styling across scripts
