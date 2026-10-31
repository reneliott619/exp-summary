import argparse
import sys

from .loader import load_csv, ResultFileError
from .aggregate import summarize_results
from .formatter import format_markdown


def main():
    parser = argparse.ArgumentParser(
        description="读取实验结果 CSV，计算统计量并输出 Markdown 表格"
    )

    parser.add_argument(
        "csv_path",
        help="实验结果 CSV 文件路径",
    )

    args = parser.parse_args()

    try:
        # 1. 读取 CSV
        results = load_csv(args.csv_path)

        # 2. 计算均值和标准差
        summary = summarize_results(results)

        # 3. 格式化为 Markdown 表格
        table = format_markdown(summary)

        # 4. 输出结果
        if table:
            print(table)
        else:
            print("CSV 文件中没有实验结果。")

    except ResultFileError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()