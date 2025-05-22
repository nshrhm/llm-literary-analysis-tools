# LLM Literary Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[日本語版はこちら](README_ja.md)

## Overview

This repository, **LLM Literary Analysis Tools**, provides a comprehensive set of tools for analyzing emotional dimensions in Japanese literary works using multiple Large Language Models (LLMs). The project aims to automatically evaluate emotions such as amusement, surprise, sadness, and anger across different models, personas, and parameters, and to compare the results for academic research purposes. Our goal is to contribute to literary studies, education, and the development of emotion-based dialogue systems through automated sentiment analysis.

This work is intended for submission to an international academic journal, with a deadline for preparation by May 30, 2025.

## Purpose and Background

The automation of sentiment analysis in literature holds significant potential for advancing literary research, educational tools, and emotion-driven dialogue systems. By leveraging multiple LLMs, this project seeks to uncover differences and consistencies in emotional evaluations, providing insights into model performance and optimal configurations for sentiment analysis.

## Features

- **Emotion Analysis Across Multiple Dimensions**: Evaluates Japanese literary works ("Kaichu Tokei", "Okane to Pistol", "Boroboro na Dachou") on four emotional dimensions (amusement, surprise, sadness, anger).
- **Comparative Studies**: Analyzes the impact of different models, personas, and temperature settings on emotional evaluations.
- **Visualization Tools**: Generates publication-ready graphs in PNG and SVG formats, with proper Japanese font support using `japanize_matplotlib`.
- **Modular Analysis Scripts**: Includes series such as `model_emotion`, `text_emotion`, `persona_emotion`, `temperature_emotion`, and more, each focusing on specific aspects of the data.

## Installation

To use these tools, you'll need to have Python 3.x installed along with the required libraries. Follow these steps to set up the environment:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nshrhm/llm-literary-analysis-tools.git
   cd llm-literary-analysis-tools
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If a `requirements.txt` file is not provided, install the core libraries manually:
   ```bash
   pip install pandas numpy scipy matplotlib seaborn japanize-matplotlib
   ```

## Usage

To run the full suite of analysis scripts and generate results:

```bash
bash make_result.sh
```

This script executes all analysis and visualization scripts, saving CSV files to the `results/` directory and graphs to `results/figures/`. Individual scripts in the `src/` directory can also be run separately for specific analyses.

For detailed information on each script, refer to the [Data Analysis Scripts Guide](docs/analysis_scripts_guide.md).

- **CSV Outputs**: Statistical results and data extracts are saved in `results/`.
- **Figures**: Graphs are saved in `results/figures/` in both PNG (for Microsoft Word) and SVG (for LaTeX) formats.

## Directory Structure

- **`src/`**: Contains all analysis and visualization scripts.
- **`results/`**: Stores CSV outputs of statistical analyses.
- **`results/figures/`**: Stores generated graphs in PNG and SVG formats.
- **`memory-bank/`**: Documentation and context files for project management and Cline instructions.

## Contributing

We welcome contributions from researchers and developers interested in advancing sentiment analysis of literature using LLMs. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

Please report any issues or feature requests via the [GitHub Issues page](https://github.com/nshrhm/llm-literary-analysis-tools/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For inquiries or further information, please use the [GitHub Issues page](https://github.com/nshrhm/llm-literary-analysis-tools/issues) to reach out to the project maintainers.
