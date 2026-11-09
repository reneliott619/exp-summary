# exp-summary

`exp-summary` 是一个基于 Python 标准库的实验结果统计工具，可以读取 CSV 格式的实验数据，计算不同方法的指标均值和标准差，并生成 Markdown 或 LaTeX 表格。

## 功能列表

- **CSV 数据读取**：读取实验结果，并将每条记录转换为结构化对象。
- **数据校验**：检查必要的字段和数值格式，报告文件读取及数据错误。
- **统计分析**：按照实验方法分组，计算各项指标的均值和总体标准差。
- **Markdown 输出**：生成适合 GitHub、Markdown 文档和实验记录的表格。
- **LaTeX 输出**：生成可以放入论文的 LaTeX 表格。
- **精度控制**：通过 `--digits` 指定均值和标准差的小数位数。
- **命令行使用**：通过一条命令完成数据读取、统计和表格生成。

## 环境要求

- Python 3.10 或更高版本。
- 无第三方运行时依赖，使用 Python 标准库完成数据处理。
- Ruff 仅用于开发阶段的代码检查和格式化，不是程序运行的必要依赖。

## 快速开始

### 1. 获取项目

克隆仓库后进入项目目录：

```bash
git clone 
cd exp-summary
```

如果你已经下载或克隆了项目，可以直接进入项目根目录。

### 2. 准备示例数据

项目提供了示例文件：

```text
examples/result.csv
```

CSV 文件包含实验方法、随机种子和评价指标。

### 3. 运行程序

默认输出 Markdown 表格：

```bash
python -m expsum examples/result.csv
```

指定 Markdown 格式并保留两位小数：

```bash
python -m expsum examples/result.csv --format markdown --digits 2
```

输出 LaTeX 表格并保留四位小数：

```bash
python -m expsum examples/result.csv --format latex --digits 4
```

查看命令行帮助：

```bash
python -m expsum --help
```

### 4. 输出示例

假设示例数据中包含 MethodA、MethodB 和 MethodC，执行：

```bash
python -m expsum examples/result.csv --format markdown --digits 2
```

输出示例：

```text
| Method | EN | SSIM |
| --- | --- | --- |
| MethodA | 7.12 ± 0.04 | 0.81 ± 0.01 |
| MethodB | 6.95 ± 0.04 | 0.84 ± 0.01 |
| MethodC | 7.06 ± 0.04 | 0.79 ± 0.01 |
```

实际结果取决于 CSV 文件中的数据。

LaTeX 输出示例：

```latex
\begin{tabular}{lcc}
\hline
Method & EN & SSIM \\
\hline
MethodA & $7.12 \pm 0.04$ & $0.81 \pm 0.01$ \\
MethodB & $6.95 \pm 0.04$ & $0.84 \pm 0.01$ \\
MethodC & $7.06 \pm 0.04$ & $0.79 \pm 0.01$ \\
\hline
\end{tabular}
```

生成的 LaTeX `tabular` 内容可以复制到论文的 `table` 环境中。

## 输入 CSV 格式

CSV 文件的第一行为表头，必须包含以下两个字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `method` | 字符串 | 实验方法名称 |
| `seed` | 整数 | 实验随机种子 |

除上述两个字段外，其他列均作为评价指标读取，并转换为浮点数。

例如：

```csv
method,seed,EN,SSIM
MethodA,42,7.10,0.80
MethodA,43,7.14,0.82
MethodA,44,7.12,0.81
MethodB,42,6.91,0.83
MethodB,43,6.95,0.84
MethodB,44,6.99,0.85
MethodC,42,7.02,0.78
MethodC,43,7.06,0.79
MethodC,44,7.10,0.80
```

注意事项：

- `method` 和 `seed` 是必需字段。
- `seed` 必须能够转换为整数。
- 评价指标必须能够转换为浮点数。
- 每条数据记录应具有完整且正确的字段。
- 同一方法的多次实验结果会被合并统计。

## 命令行参数

```text
python -m expsum <csv_path> [--format {markdown,latex}] [--digits DIGITS]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `csv_path` | 无 | 输入 CSV 文件路径 |
| `--format` | `markdown` | 输出格式，可选 `markdown` 或 `latex` |
| `--digits` | 由 `DEFAULT_DIGITS` 决定 | 均值和标准差保留的小数位数 |

示例：

```bash
python -m expsum examples/result.csv --format markdown --digits 4
python -m expsum examples/result.csv --format latex --digits 2
```

## 项目结构

```text
exp-summary/
├── expsum/
│   ├── __init__.py
│   ├── __main__.py
│   ├── loader.py
│   ├── aggregate.py
│   └── formatter.py
├── examples/
│   └── result.csv
├── .gitignore
└── README.md
```

模块说明：

- `loader.py`：定义实验结果数据结构、读取 CSV 并进行数据校验。
- `aggregate.py`：按照实验方法分组，计算指标的均值和总体标准差。
- `formatter.py`：将统计结果转换为 Markdown 或 LaTeX 表格。
- `__main__.py`：解析命令行参数并调用其他模块。
- `examples/result.csv`：可直接运行的示例输入文件。

## 开发检查

安装 Ruff：

```bash
python -m pip install ruff
```

检查代码问题：

```bash
ruff check .
```

检查缺失的类型注解：

```bash
ruff check --select ANN .
```

格式化 Python 代码：

```bash
ruff format .
```
## 安装

需要 Python 3.10 及以上。

```bash
pip install -r requirements.txt
```

命令行功能只使用 Python 标准库；API 服务依赖 FastAPI。

## API 用法

启动服务：

```bash
uvicorn expsum.api:app --reload
```

启动后访问 http://127.0.0.1:8000/docs 可在网页上直接测试接口。

### 接口说明

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查，返回 `{"status": "ok"}` |
| POST | `/summarize` | 上传 CSV，返回统计表格 |

`/summarize` 的参数：

- `file`（必填）：实验结果 CSV 文件，格式同命令行
- `digits`（可选，默认 3）：保留的小数位数
- `format`（可选，默认 `markdown`）：输出格式，`markdown` 或 `latex`

### 示例

```bash
curl -F "file=@examples/results.csv" "http://127.0.0.1:8000/summarize?digits=2"
```

返回：

```json
{
  "format": "markdown",
  "table": "| Method | EN | SSIM |\n| --- | --- | --- |\n| MethodA | 7.12 ± 0.04 | 0.81 ± 0.01 |\n..."
}
```

### 错误码

| 状态码 | 含义 |
|--------|------|
| 400 | 文件内容有误（缺列、数值无法解析、编码不是 UTF-8） |
| 422 | 参数不合法（如 `digits` 为负数、`format` 不在可选范围内） |