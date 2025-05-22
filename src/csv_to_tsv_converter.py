import os
import sys
import pandas as pd
import glob


def convert_csv_to_tsv(input_dir):
    """
    CSVファイルをTSVファイルに変換する。

    Args:
        input_dir (str): CSVファイルが格納されているディレクトリのパス
    """
    # CSVファイルを検索
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    if not csv_files:
        print(f"CSVファイルが {input_dir} に見つかりませんでした。")
        return

    for csv_file in csv_files:
        try:
            # CSVファイルを読み込み
            df = pd.read_csv(csv_file)

            # 出力ファイル名を生成（.csvを.tsvに置換）
            tsv_file = csv_file.replace('.csv', '.tsv')

            # TSVファイルとして保存
            df.to_csv(tsv_file, sep='\t', index=False)
            print(f"変換完了: {os.path.basename(csv_file)} → {os.path.basename(tsv_file)}")

        except Exception as e:
            print(f"エラー: {os.path.basename(csv_file)} の変換中にエラーが発生しました。")
            print(f"エラー詳細: {str(e)}")


def main():
    """
    メイン関数。コマンドライン引数からディレクトリパスを受け取り、変換処理を実行する。
    """
    if len(sys.argv) != 2:
        print("使用方法: python csv_to_tsv_converter.py <CSVファイルのディレクトリパス>")
        sys.exit(1)

    input_dir = sys.argv[1]

    if not os.path.isdir(input_dir):
        print(f"エラー: {input_dir} はディレクトリではありません。")
        sys.exit(1)

    convert_csv_to_tsv(input_dir)


if __name__ == "__main__":
    main()
