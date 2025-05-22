# LLM文学分析ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English version here](README.md)

## 概要

このリポジトリ「**LLM文学分析ツール**」は、複数の大規模言語モデル（LLM）を用いて日本語文学作品の感情次元を分析するための包括的なツールセットを提供します。このプロジェクトは、異なるモデル、ペルソナ、パラメータ間で面白さ、驚き、悲しみ、怒りなどの感情を自動評価し、結果を比較することを目的としています。文学研究、教育、感情ベースの対話システムの開発に、自動化された感情分析を通じて貢献することを目指しています。

この研究は、2025年5月30日までに準備を完了し、国際学術ジャーナルへの投稿を予定しています。

## 目的と背景

文学における感情分析の自動化は、文学研究、教育ツール、感情駆動型の対話システムの進歩に大きな可能性を秘めています。複数のLLMを活用することで、このプロジェクトは感情評価の差異と一貫性を明らかにし、モデル性能や感情分析のための最適な設定に関する洞察を提供することを目指しています。

## 機能

- **複数の感情次元での分析**：日本語文学作品（「懐中時計」「お金とピストル」「ぼろぼろな駝鳥」）を4つの感情次元（面白さ、驚き、悲しみ、怒り）で評価。
- **比較研究**：異なるモデル、ペルソナ、温度設定が感情評価に与える影響を分析。
- **視覚化ツール**：PNGおよびSVG形式で出版に適したグラフを生成し、`japanize_matplotlib`を使用して適切な日本語フォントをサポート。
- **モジュール式分析スクリプト**：`model_emotion`、`text_emotion`、`persona_emotion`、`temperature_emotion`などのシリーズを含み、データの特定の側面に焦点を当てた分析が可能。

## インストール

これらのツールを使用するには、Python 3.xと必要なライブラリがインストールされている必要があります。以下の手順で環境を設定してください：

1. **リポジトリのクローン**：
   ```bash
   git clone https://github.com/nshrhm/llm-literary-analysis-tools.git
   cd llm-literary-analysis-tools
   ```

2. **依存関係のインストール**：
   ```bash
   pip install -r requirements.txt
   ```
   `requirements.txt`ファイルが提供されていない場合は、以下のコマンドでコアライブラリを手動でインストールしてください：
   ```bash
   pip install pandas numpy scipy matplotlib seaborn japanize-matplotlib
   ```

## 使用方法

すべての分析スクリプトを実行し、結果を生成するには：

```bash
bash make_result.sh
```

このスクリプトはすべての分析および視覚化スクリプトを実行し、CSVファイルを`results/`ディレクトリに、グラフを`results/figures/`に保存します。`src/`ディレクトリ内の個々のスクリプトを特定の分析のために個別に実行することも可能です。

各スクリプトの詳細な情報については、[データ分析スクリプト ガイド](docs/analysis_scripts_guide_ja.md)をご参照ください。

- **CSV出力**：統計結果やデータ抽出は`results/`に保存されます。
- **図表**：グラフは`results/figures/`にPNG（Microsoft Word用）およびSVG（LaTeX用）形式で保存されます。

## ディレクトリ構造

- **`src/`**：すべての分析および視覚化スクリプトを含む。
- **`results/`**：統計分析のCSV出力を保存。
- **`results/figures/`**：生成されたグラフをPNGおよびSVG形式で保存。
- **`memory-bank/`**：プロジェクト管理およびCline指示のためのドキュメントとコンテキストファイル。

## 貢献方法

文学の感情分析をLLMを使用して進めることに興味を持つ研究者や開発者からの貢献を歓迎します。貢献するには：

1. リポジトリをフォークしてください。
2. 機能追加やバグ修正のための新しいブランチを作成してください。
3. 変更内容の詳細な説明とともにプルリクエストを提出してください。

問題や機能リクエストは、[GitHub Issuesページ](https://github.com/nshrhm/llm-literary-analysis-tools/issues)を通じて報告してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 連絡先

お問い合わせや詳細情報については、[GitHub Issuesページ](https://github.com/nshrhm/llm-literary-analysis-tools/issues)を使用してプロジェクトのメンテナーに連絡してください。
