import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass
class RunResult:
    method: str
    seed: int
    metrics: dict[str, float]

class ResultFileError(Exception):
    """实验结果 CSV 文件格式错误。"""


def parse_results(
    lines: Iterable[str],
    source: str,
) -> list[RunResult]:
    """解析 CSV 文本行，返回实验结果列表。"""
    reader = csv.DictReader(lines)

    if reader.fieldnames is None:
        raise ResultFileError(f"{source}: CSV 文件为空或缺少表头")

    required_columns = {"method", "seed"}
    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ResultFileError(
            f"{source}: 缺少必要列: {missing}"
        )

    results: list[RunResult] = []

    for row_number, row in enumerate(reader, start=2):
        try:
            method = row["method"]
            seed = int(row["seed"])

            metrics = {
                key: float(value)
                for key, value in row.items()
                if key not in {"method", "seed"}
            }

        except (ValueError, TypeError) as exc:
            raise ResultFileError(
                f"{source}: 第 {row_number} 行数据格式错误: {exc}"
            ) from exc

        results.append(
            RunResult(
                method=method,
                seed=seed,
                metrics=metrics,
            )
        )

    return results


def load_csv(path: Path) -> list[RunResult]:
    """从磁盘读取 CSV 文件。"""
    csv_path = Path(path)

    try:
        with csv_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            return parse_results(file, source=str(csv_path))

    except OSError as exc:
        raise ResultFileError(
            f"{csv_path}: 无法读取文件: {exc}"
        ) from exc
