from io import StringIO
from statistics import mean, pstdev

from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel

from expsum.loader import parse_results, ResultFileError
from expsum.aggregate import summarize_results
from expsum.formatter import format_markdown, to_latex

app = FastAPI(
    title="exp-summary API",
    description="实验结果统计工具的 Web API",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """检查 API 服务是否正常运行"""
    return {"status": "ok"}

@app.get("/add")
async def add(a: int, b: int) -> dict[str, int]:
    """计算两个整数之和"""
    return {"result": a + b}

class StatsRequest(BaseModel):
    values: list[float]

class StatsResponse(BaseModel):
    mean: float
    std: float

@app.post("/stats", response_model=StatsResponse)
async def calculate_stats(request: StatsRequest) -> StatsResponse:
    """计算一组数据的均值和总体标准差。"""
    values = request.values

    if not values:
        raise ValueError("values 不能为空")

    return StatsResponse(
        mean=mean(values),
        std=pstdev(values),
    )

@app.post("/summarize")
async def summarize(
    file: UploadFile,
    digits: int = 3,
    format: str = "markdown",
) -> dict[str, str]:
    """上传 CSV，返回指定格式的统计报告。"""

    # 1. 校验查询参数
    if digits < 0:
        raise HTTPException(
            status_code=422,
            detail="digits 必须大于或等于 0",
        )

    if format not in {"markdown", "latex"}:
        raise HTTPException(
            status_code=422,
            detail="format 必须是 markdown 或 latex",
        )

    # 2. 读取上传文件
    content = await file.read()

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="文件编码错误，请上传 UTF-8 编码的 CSV",
        ) from exc

    # 3. 解析 CSV
    try:
        results = parse_results(
            StringIO(text),
            source=file.filename or "上传的文件",
        )
    except ResultFileError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # 4. 计算统计结果
    summary = summarize_results(results)

    # 5. 根据 format 选择输出格式
    if format == "markdown":
        output = format_markdown(summary, digits=digits)
    else:
        output = to_latex(summary, digits=digits)

    # 6. 返回结果
    return {
        "format": format,
        "markdown" if format == "markdown" else "latex": output,
    }
