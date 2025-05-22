"""Unified script for analyzing missing values in model responses."""

import pandas as pd
from config import (
    OUTPUT_DIR, ANALYSIS_COLUMNS, DATA_PATHS,
    ensure_output_directories, safe_read_csv
)

def generate_missing_values_report(input_csv, output_csv):
    """
    Read a CSV file, count results per model, identify models with fewer than 120 results,
    and save a report as CSV.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path where the output CSV report will be saved.
    """
    df, error = safe_read_csv(input_csv)
    if error:
        print(error)
        return False

    # Count results per model
    model_counts = df['model'].value_counts().sort_values()

    # Identify models with fewer than 120 results
    missing_value_models = model_counts[model_counts < 120]

    # Save the results to CSV
    missing_value_models.to_csv(output_csv, header=['count'])
    print(f"結果が120に満たないモデルのレポートを '{output_csv}' に保存しました。")
    return True

def calculate_missing_values_by_model(input_csv, output_csv):
    """
    Calculate the proportion of missing values per model and save to CSV.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path where the output CSV will be saved.
    """
    df, error = safe_read_csv(input_csv)
    if error:
        print(error)
        return None

    # Calculate missing value proportions per model
    missing_values = df.groupby('model').apply(lambda x: x.isnull().mean(), include_groups=False)
    missing_values.to_csv(output_csv)
    print(f"欠損値分析が完了しました。結果は '{output_csv}' に保存されています。")
    return missing_values

def generate_detailed_missing_summary(input_csv, output_csv):
    """
    Generate a detailed summary of missing values with percentages and averages.

    Args:
        input_csv (str): Path to the CSV file with missing value proportions.
        output_csv (str): Path where the summary CSV report will be saved.
    """
    df, error = safe_read_csv(input_csv)
    if error:
        print(error)
        return False

    # Use the values as-is in a new DataFrame
    result_df = df[['model'] + ANALYSIS_COLUMNS['all']].copy()

    # Calculate and add average missing value rate
    result_df['Average'] = result_df[ANALYSIS_COLUMNS['all']].mean(axis=1)

    # Exclude models with no missing values
    result_df = result_df[result_df['Average'] > 0]

    # Sort by average missing value rate in descending order
    result_df = result_df.sort_values('Average', ascending=False)

    # Convert to percentage with one decimal place
    for col in ANALYSIS_COLUMNS['all'] + ['Average']:
        result_df[col] = (result_df[col] * 100).round(1).astype(str) + '%'

    # Save with specified column order
    columns = ['model', 'Average'] + ANALYSIS_COLUMNS['all']
    result_df[columns].to_csv(output_csv, index=False)
    print(f"詳細な欠損値サマリーを '{output_csv}' に保存しました。")
    return True

if __name__ == "__main__":
    # Ensure necessary directories exist
    ensure_output_directories()

    # Step 1: Generate report of models with fewer than 120 results
    generate_missing_values_report(DATA_PATHS['input'], DATA_PATHS['missing_report'])

    # Step 2: Calculate missing value proportions per model
    calculate_missing_values_by_model(DATA_PATHS['input'], DATA_PATHS['missing_by_model'])

    # Step 3: Generate detailed summary with percentages
    generate_detailed_missing_summary(DATA_PATHS['missing_by_model'], DATA_PATHS['missing_summary'])
