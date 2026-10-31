import csv
from pathlib import Path
from dataclasses import dataclass

class ResultFileError(Exception):
    pass

@dataclass
class RunResult:
    method: str
    seed: int
    metrics: dict[str, float]

def load_csv(path: Path) -> list[RunResult]:
    path = Path(path)
    results = []
    try:
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            missing = {"method", "seed"} - set(reader.fieldnames or [])
            if missing:
                raise ResultFileError(f"文件 {path} 第 1 行（表头）缺少必需的列: "
                    f"{', '.join(sorted(missing))}")
            for line_no, row in enumerate(reader, start=2):
                try:
                    method = row["method"]
                    seed = int(row["seed"])
                    metrics = {k: float(v) for k, v in row.items() if k not in ("method", "seed")}

                except (ValueError, TypeError) as e:
                    raise ResultFileError(f"{path} 第 {line_no} 行数据无法解析: {e}") from e
                result = RunResult(
                    method=method,
                    seed=seed,
                    metrics=metrics
                )
                results.append(result)
    except OSError as e:
        raise ResultFileError(f"文件读取失败{path}：{e}") from e
    return results

if __name__ == "__main__":
    try:
        path = Path(__file__).parent / "result.csv"
        results = load_csv(path)
        for result in results:
            print(result.method, result.seed, result.metrics)
    except ResultFileError as e:
        print(f"读取失败：{e}")