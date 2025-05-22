import pandas as pd

def create_sample_data(input_file, output_file, trial_limit=3):
    """
    data_all.csvからtrial値が1から指定された値までのデータを抽出し、サンプルデータとして保存する。
    
    Parameters:
    input_file (str): 入力CSVファイルのパス
    output_file (str): 出力CSVファイルのパス
    trial_limit (int): 抽出するtrialの最大値
    """
    # CSVファイルの読み込み
    df = pd.read_csv(input_file)
    
    # trial値が1からtrial_limitまでのデータを抽出
    sample_df = df[df['trial'] <= trial_limit]
    
    # サンプルデータをCSVとして保存
    sample_df.to_csv(output_file, index=False)
    print(f"サンプルデータを {output_file} に保存しました。抽出された行数: {len(sample_df)}")

if __name__ == "__main__":
    input_file = "data_all.csv"
    output_file = "data_sample.csv"
    create_sample_data(input_file, output_file)
