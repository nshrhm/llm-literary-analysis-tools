# Data Analysis Scripts Guide

This document provides an overview of the main data analysis Python scripts used in the LLM-based sentiment analysis project for Japanese literary works.

## Prerequisites and Notes
- Each script automatically creates necessary directories (`results/` and its subdirectories) if they do not exist.
- All output files are generated under the `results/` directory.
- Scripts are intended to be run from the project root directory.

## Script List

### 1. `src/missing_values_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`), calculates the missing value rate per model, identifies models with fewer than the expected number of results (120), and reports the missing rate and average missing rate for each emotional dimension's values and reasons.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/missing_values_analysis.py
  ```
- **Generated Files**: `results/missing_values_by_model.csv`, `results/missing_values_report.csv`, `results/missing_values_summary.csv`

### 2. `src/missing_values_visualize.py`
- **Description**: Reads experimental result data (`data_all.csv`) and creates visualizations of the missing value rates per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/missing_values_visualize.py
  ```
- **Generated Files**: `results/missing_values_q1value.png`, `results/missing_values_q1reason.png`, ..., graphs in PNG and SVG formats for Q1, Q2, Q3, Q4 values and reasons.
- **Note**: It is recommended to run `missing_values_visualize.py` after executing `missing_values_analysis.py`.

### 3. `src/model_emotion_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and calculates the emotional dimension trends per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_emotion_analysis.py
  ```
- **Generated Files**: `results/model_emotion.csv`

### 4. `src/model_emotion_statistics.py`
- **Description**: Reads analysis data (`results/model_emotion.csv`) and calculates basic statistics for emotional dimensions per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_emotion_statistics.py
  ```
- **Generated Files**: `results/model_emotion_statistics.csv`
- **Note**: It is recommended to run `src/model_emotion_statistics.py` after executing `src/model_emotion_analysis.py`.

### 5. `src/model_emotion_visualize.py`
- **Description**: Reads analysis data (`results/model_emotion.csv`) and visually represents the emotional dimensions per model.
- **Execution**:
  ```bash
  python ./src/model_emotion_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/model_emotion.png`, `results/figures/model_emotion_distribution.png`
  - `results/figures/model_emotion.svg`, `results/figures/model_emotion_distribution.svg`
- **Note**: It is recommended to run `src/model_emotion_visualize.py` after executing `src/model_emotion_analysis.py`.

### 6. `src/model_emotion_similarity.py`
- **Description**: Performs correlation analysis and FCM clustering on emotional dimension trends per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_emotion_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: `results/model_emotion_correlations.csv`, `results/figures/model_emotion_correlations.png`, `results/figures/model_emotion_correlations.svg`
  2. Cluster Analysis: `results/figures/model_emotion_silhouette.png`, `results/figures/model_emotion_silhouette.svg`
  3. FCM Analysis Results: `results/model_emotion_cluster_characteristics.json`, `results/figures/model_emotion_fcm_gradient.png`, `results/figures/model_emotion_fcm_gradient.svg`, `results/figures/model_emotion_fcm_membership.png`, `results/figures/model_emotion_fcm_membership.svg`
- **Note**: It is recommended to run `src/model_emotion_similarity.py` after executing `src/model_emotion_analysis.py`.

### 7. `src/model_reason_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and calculates the trend of character counts in reason texts per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_reason_analysis.py
  ```
- **Generated Files**: `results/model_reason.csv`

### 8. `src/model_reason_statistics.py`
- **Description**: Reads analysis data (`results/model_reason.csv`) and calculates basic statistics for character counts in reason texts per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_reason_statistics.py
  ```
- **Generated Files**: `results/model_reason_statistics.csv`
- **Note**: It is recommended to run `src/model_reason_statistics.py` after executing `src/model_reason_analysis.py`.

### 9. `src/model_reason_visualize.py`
- **Description**: Reads analysis data (`results/model_reason.csv`) and visually represents the trend of character counts in reason texts per model.
- **Execution**:
  ```bash
  python ./src/model_reason_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/model_reason.png`, `results/figures/model_reason_distribution.png`
  - `results/figures/model_reason.svg`, `results/figures/model_reason_distribution.svg`
  - `results/figures/model_reason_sorted_all.png`, `results/figures/model_reason_sorted_all.svg`
  - `results/figures/model_reason_sorted_q1.png`, `results/figures/model_reason_sorted_q2.png`, `results/figures/model_reason_sorted_q3.png`, `results/figures/model_reason_sorted_q4.png`
  - `results/figures/model_reason_sorted_q1.svg`, `results/figures/model_reason_sorted_q2.svg`, `results/figures/model_reason_sorted_q3.svg`, `results/figures/model_reason_sorted_q4.svg`
- **Note**: It is recommended to run `src/model_reason_visualize.py` after executing `src/model_reason_analysis.py`.

### 10. `src/model_reason_similarity.py`
- **Description**: Performs correlation analysis and FCM clustering on the trend of character counts in reason texts per model.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/model_reason_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: `results/model_reason_correlations.csv`, `results/figures/model_reason_correlations.png`, `results/figures/model_reason_correlations.svg`
  2. Cluster Analysis: `results/figures/model_reason_silhouette.png`, `results/figures/model_reason_silhouette.svg`
  3. FCM Analysis Results: `results/model_reason_cluster_characteristics.json`, `results/figures/model_reason_fcm_gradient.png`, `results/figures/model_reason_fcm_gradients.svg`, `results/figures/model_reason_fcm_membership.png`, `results/figures/model_reason_fcm_membership.svg`
- **Note**: It is recommended to run `src/model_reason_similarity.py` after executing `src/model_reason_analysis.py`.

### 11. `src/text_emotion_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and analyzes the emotional dimension trends per literary work.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_emotion_analysis.py
  ```
- **Generated Files**:
  - `results/text_emotion.csv`: Emotional values per combination of literary work and model
  - `results/text_emotion_average.csv`: Average emotional values per literary work

### 12. `src/text_emotion_statistics.py`
- **Description**: Reads analysis data (`results/text_emotion.csv`) and calculates basic statistics for emotional dimensions per literary work.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_emotion_statistics.py
  ```
- **Generated Files**: `results/text_emotion_statistics.csv`
- **Note**: It is recommended to run `src/text_emotion_statistics.py` after executing `src/text_emotion_analysis.py`.

### 13. `src/text_emotion_visualize.py`
- **Description**: Reads analysis data (`results/text_emotion.csv`) and visually represents the emotional dimensions per literary work.
- **Execution**:
  ```bash
  python ./src/text_emotion_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/text_emotion.png`: Comparison graph of average emotional dimensions
  - `results/figures/text_emotion.svg`: Same as above (SVG format)
  - `results/figures/text_emotion_distribution.png`: Violin plot of emotional value distribution
  - `results/figures/text_emotion_distribution.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/text_emotion_visualize.py` after executing `src/text_emotion_analysis.py`.

### 14. `src/text_emotion_similarity.py`
- **Description**: Analyzes the similarity of emotional patterns between literary works using correlation analysis and radar chart visualization.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_emotion_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: 
     - `results/text_emotion_correlation.csv`: Correlation matrix of emotional values between literary works
     - `results/figures/text_emotion_correlation.png`: Correlation heatmap
     - `results/figures/text_emotion_correlation.svg`: Same as above (SVG format)
  2. Emotional Pattern Analysis:
     - `results/figures/text_emotion_patterns.png`: Radar chart for emotional pattern comparison
     - `results/figures/text_emotion_patterns.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/text_emotion_similarity.py` after executing `src/text_emotion_analysis.py`.

### 15. `src/text_reason_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and analyzes the trend of character counts in reason texts per literary work.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_reason_analysis.py
  ```
- **Generated Files**:
  - `results/text_reason.csv`: Character counts of reason texts per combination of literary work and model
  - `results/text_reason_average.csv`: Average character counts of reason texts per literary work

### 16. `src/text_reason_statistics.py`
- **Description**: Reads analysis data (`results/text_reason.csv`) and calculates basic statistics for character counts in reason texts per literary work.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_reason_statistics.py
  ```
- **Generated Files**: `results/text_reason_statistics.csv`
- **Note**: It is recommended to run `src/text_reason_statistics.py` after executing `src/text_reason_analysis.py`.

### 17. `src/text_reason_similarity.py`
- **Description**: Analyzes the similarity of character count patterns in reason texts between literary works using correlation analysis and radar chart visualization.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_reason_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: 
     - `results/text_reason_correlation.csv`: Correlation matrix of reason text character counts between literary works
     - `results/figures/text_reason_correlation.png`: Correlation heatmap
     - `results/figures/text_reason_correlation.svg`: Same as above (SVG format)
  2. Pattern Analysis:
     - `results/figures/text_reason_patterns.png`: Radar chart for reason text character count pattern comparison
     - `results/figures/text_reason_patterns.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/text_reason_similarity.py` after executing `src/text_reason_analysis.py`.

### 18. `src/text_reason_visualize.py`
- **Description**: Reads analysis data (`results/text_reason.csv`) and visually represents the character counts in reason texts per literary work.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/text_reason_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/text_reason.png`: Comparison graph of average reason text character counts
  - `results/figures/text_reason.svg`: Same as above (SVG format)
  - `results/figures/text_reason_distribution.png`: Violin plot of reason text character count distribution
  - `results/figures/text_reason_distribution.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/text_reason_visualize.py` after executing `src/text_reason_analysis.py`.

### 19. `src/persona_emotion_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and analyzes the emotional dimension trends per persona.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_emotion_analysis.py
  ```
- **Generated Files**:
  - `results/persona_emotion.csv`: Emotional values per combination of persona and model
  - `results/persona_emotion_average.csv`: Average emotional values per persona

### 20. `src/persona_emotion_statistics.py`
- **Description**: Reads analysis data (`results/persona_emotion_average.csv`) and calculates basic statistics for emotional dimensions per persona.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_emotion_statistics.py
  ```
- **Generated Files**: `results/persona_emotion_statistics.csv`
- **Note**: It is recommended to run `src/persona_emotion_statistics.py` after executing `src/persona_emotion_analysis.py`.

### 21. `src/persona_emotion_visualize.py`
- **Description**: Reads analysis data (`results/persona_emotion.csv`) and visually represents the emotional dimensions per persona.
- **Execution**:
  ```bash
  python ./src/persona_emotion_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/persona_emotion.png`: Comparison graph of average emotional dimensions
  - `results/figures/persona_emotion.svg`: Same as above (SVG format)
  - `results/figures/persona_emotion_distribution.png`: Violin plot of emotional value distribution
  - `results/figures/persona_emotion_distribution.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/persona_emotion_visualize.py` after executing `src/persona_emotion_analysis.py`.

### 22. `src/persona_emotion_similarity.py`
- **Description**: Analyzes the similarity of emotional patterns between personas using correlation analysis and radar chart visualization.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_emotion_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: 
     - `results/persona_emotion_correlation.csv`: Correlation matrix of emotional values between personas
     - `results/figures/persona_emotion_correlation.png`: Correlation heatmap
     - `results/figures/persona_emotion_correlation.svg`: Same as above (SVG format)
  2. Emotional Pattern Analysis:
     - `results/figures/persona_emotion_patterns.png`: Radar chart for emotional pattern comparison
     - `results/figures/persona_emotion_patterns.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/persona_emotion_similarity.py` after executing `src/persona_emotion_analysis.py`.

### 23. `src/persona_reason_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and analyzes the trend of character counts in reason texts per persona.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_reason_analysis.py
  ```
- **Generated Files**:
  - `results/persona_reason.csv`: Character counts of reason texts per combination of persona and model
  - `results/persona_reason_average.csv`: Average character counts of reason texts per persona

### 24. `src/persona_reason_statistics.py`
- **Description**: Reads analysis data (`results/persona_reason.csv`) and calculates basic statistics for character counts in reason texts per persona.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_reason_statistics.py
  ```
- **Generated Files**: `results/persona_reason_statistics.csv`
- **Note**: It is recommended to run `src/persona_reason_statistics.py` after executing `src/persona_reason_analysis.py`.

### 25. `src/persona_reason_visualize.py`
- **Description**: Reads analysis data (`results/persona_reason.csv`) and visually represents the character counts in reason texts per persona.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_reason_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/persona_reason.png`: Comparison graph of average reason text character counts
  - `results/figures/persona_reason.svg`: Same as above (SVG format)
  - `results/figures/persona_reason_distribution.png`: Violin plot of reason text character count distribution
  - `results/figures/persona_reason_distribution.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/persona_reason_visualize.py` after executing `src/persona_reason_analysis.py`.

### 26. `src/persona_reason_similarity.py`
- **Description**: Analyzes the similarity of character count patterns in reason texts between personas using correlation analysis and radar chart visualization.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/persona_reason_similarity.py
  ```
- **Generated Files**:
  1. Correlation Analysis: 
     - `results/persona_reason_correlation.csv`: Correlation matrix of reason text character counts between personas
     - `results/figures/persona_reason_correlation.png`: Correlation heatmap
     - `results/figures/persona_reason_correlation.svg`: Same as above (SVG format)
  2. Pattern Analysis:
     - `results/figures/persona_reason_patterns.png`: Radar chart for reason text character count pattern comparison
     - `results/figures/persona_reason_patterns.svg`: Same as above (SVG format)
- **Note**: It is recommended to run `src/persona_reason_similarity.py` after executing `src/persona_reason_analysis.py`.

### 27. `src/temperature_emotion_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and calculates changes in emotional dimensions based on temperature settings.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/temperature_emotion_analysis.py
  ```
- **Generated Files**: `results/temperature_emotion.csv`
- **Note**: This script assumes that experimental result data exists in `data_all.csv`.

### 28. `src/temperature_emotion_statistics.py`
- **Description**: Reads experimental result data (`data_all.csv`) and calculates statistical metrics for emotional dimensions based on temperature settings.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/temperature_emotion_statistics.py
  ```
- **Generated Files**: `results/temperature_emotion_statistics.csv`
- **Note**: This script assumes that experimental result data exists in `data_all.csv`.

### 29. `src/temperature_emotion_visualize.py`
- **Description**: Reads analysis data (`results/temperature_emotion.csv` and `results/temperature_emotion_statistics.csv`) and visually represents changes in emotional values based on temperature.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/temperature_emotion_visualize.py
  ```
- **Generated Files**: 
  - `results/figures/temperature_emotion_overall.png`, `results/figures/temperature_emotion_overall.svg`
  - Graphs per emotional dimension: `results/figures/temperature_emotion_{dimension}_all.png`, `results/figures/temperature_emotion_{dimension}_all.svg`
  - Graphs with standard deviation: `results/figures/temperature_emotion_{dimension}_std_selected.png`, `results/figures/temperature_emotion_{dimension}_std_selected.svg`
- **Note**: It is recommended to run `src/temperature_emotion_visualize.py` after executing `src/temperature_emotion_analysis.py` and `src/temperature_emotion_statistics.py`.

### 30. `src/temperature_reason_analysis.py`
- **Description**: Reads experimental result data (`data_all.csv`) and calculates changes in generated text volume (character count of reasons) based on temperature settings.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/temperature_reason_analysis.py
  ```
- **Generated Files**: 
  - `results/temperature_reason.csv`: Average text volume overall
  - `results/temperature_reason_detailed.csv`: Detailed analysis of text volume per emotional dimension
- **Note**: This script assumes that experimental result data exists in `data_all.csv`.

### 31. `src/temperature_reason_visualize.py`
- **Description**: Reads experimental result data (`data_all.csv`) and analyzes and visualizes the diversity and similarity of generated text based on temperature.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/temperature_reason_visualize.py
  ```
- **Generated Files**: 
  - `results/temperature_reason_diversity.csv`: Analysis results of diversity scores
  - `results/temperature_reason_correlation_diversity.csv`: Correlation analysis results between temperature and diversity metrics
  - Graphs: `results/figures/temperature_reason_similarity_selected.png`, `results/figures/temperature_reason_similarity_selected.svg`
  - Graphs: `results/figures/temperature_reason_diversity_selected.png`, `results/figures/temperature_reason_diversity_selected.svg`
  - Graphs: `results/figures/temperature_reason_correlation_similarity_sorted.png`, `results/figures/temperature_reason_correlation_similarity_sorted.svg`
  - Graphs: `results/figures/temperature_reason_correlation_diversity_sorted.png`, `results/figures/temperature_reason_correlation_diversity_sorted.svg`
- **Note**: This script assumes that experimental result data exists in `data_all.csv`.

### 32. `src/create_data_sample.py`
- **Description**: Reads experimental result data (`data_all.csv`), extracts data with trial values from 1 to 3, and saves it as sample data.
- **Execution**: Run the following command from the project root directory.
  ```bash
  python ./src/create_data_sample.py
  ```
- **Generated Files**: 
  - `data_sample.csv`: Sample data extracted with trial values from 1 to 3
- **Note**: This script assumes that experimental result data exists in `data_all.csv`.
