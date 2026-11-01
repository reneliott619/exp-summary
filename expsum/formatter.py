import statistics
from pathlib import Path
from dataclasses import dataclass
from expsum.aggregate import MetricStat
from expsum.loader import RunResult



def summarize_results(results: list[RunResult]) -> dict[str, dict[str, MetricStat]]:
    values_by_method = {}
    for result in results:
        if result.method not in values_by_method:
            values_by_method[result.method] = {}
        values_by_metric = values_by_method[result.method]
        for name, value in result.metrics.items():
            if name not in values_by_metric:
                values_by_metric[name] = []
            values_by_metric[name].append(value)

    summary = {}
    for method, metric_values in values_by_method.items():
        summary[method] = {}
        for name, values in metric_values.items():
            mean = statistics.mean(values)
            std = statistics.stdev(values) if len(values) > 1 else 0.0
            summary[method][name] = MetricStat(mean=mean, std=std)
    return summary

def format_markdown(
    summary: dict[str, dict[str, MetricStat]]
) -> str:
    # 获取所有指标名称
    first_method_stats = list(summary.values())[0]
    metric_names = list(first_method_stats.keys())

    # 第一行：表头
    header = ["Method"] + metric_names
    lines = ["| " + " | ".join(header) + " |"]

    # 第二行：分隔行
    separator = [" --- "] * len(header)
    lines.append("|" + "|".join(separator) + "|")

    # 后续行：每种方法的统计结果
    for method, values in summary.items():
        row = [method]

        for metric in metric_names:
            stats = values[metric]
            row.append(f"{stats.mean:.2f} ± {stats.std:.2f}")

        lines.append("| " + " | ".join(row) + " |")

    # 将所有行拼接成完整字符串
    return "\n".join(lines)

def _escape_latex(text: str) -> str:
    """转义 LaTeX 表格中的特殊字符。"""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }

    return "".join(replacements.get(char, char) for char in text)


def to_latex(summary: dict[str, dict[str, MetricStat]]) -> str:
    """将实验结果格式化为 LaTeX 表格。"""
    if not summary:
        return ""

    # 收集所有指标名称，避免不同方法的指标不完全一致时漏列
    metrics = list(
        dict.fromkeys(
            metric
            for values in summary.values()
            for metric in values
        )
    )

    # 第一列是 Method，其他列是实验指标。
    columns = "l" + "c" * len(metrics)

    header = ["Method"] + metrics
    lines = [
        rf"\begin{{tabular}}{{{columns}}}",
        r"\hline",
        " & ".join(_escape_latex(name) for name in header) + r" \\",
        r"\hline",
    ]

    for method, values in summary.items():
        row = [_escape_latex(method)]

        for metric in metrics:
            if metric not in values:
                row.append("--")
                continue

            stats = values[metric]
            row.append(rf"${stats.mean:.2f} \pm {stats.std:.2f}$")

        lines.append(" & ".join(row) + r" \\")

    lines.extend([
        r"\hline",
        r"\end{tabular}",
    ])

    return "\n".join(lines)