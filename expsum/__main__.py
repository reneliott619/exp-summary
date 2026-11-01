import argparse
import sys
from pathlib import Path
from .loader import load_csv, ResultFileError
from .aggregate import summarize_results
from .formatter import format_markdown, to_latex, DEFAULT_DIGITS


def main():
    parser = argparse.ArgumentParser(
        description="读取实验结果 CSV，计算统计量并输出 Markdown 表格"
    )

    parser.add_argument(
        "csv_path",
        help="实验结果 CSV 文件路径",
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "latex"],
        default="markdown",
        help="输出格式：markdown 或 latex，默认是 markdown",
    )

    parser.add_argument(
        "--digits",
        type=int,
        default=DEFAULT_DIGITS,
        help="输出保留的小数点位数",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="把表格写入指定文件；不指定则打印到屏幕",
    )

    args = parser.parse_args()

    try:
        # 1. 读取 CSV
        results = load_csv(args.csv_path)

        # 2. 计算均值和标准差
        summary = summarize_results(results)

        if args.digits < 0:
            parser.error("--digits 必须大于或等于 0")

        if args.format == "markdown":
            output = format_markdown(summary, digits=args.digits)
        else:
            output = to_latex(summary, digits=args.digits)

        if args.output:
            args.output.write_text(output + "\n", encoding="utf-8")
            print(f"表格已写入 {args.output}", file=sys.stderr)
        else:
            print(output)
        

    except ResultFileError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
