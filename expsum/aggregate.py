import statistics
from pathlib import Path
from dataclasses import dataclass
from expsum.loader import load_csv, RunResult


@dataclass
class MetricStat:
    mean: float
    std: float


def summarize_results(results: list[RunResult]) -> dict[str, dict[str, list[MetricStat]]]:
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

