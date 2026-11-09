from io import StringIO
from statistics import mean, pstdev

from fastapi import FastAPI, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import Literal

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

class SummarizeResponse(BaseModel):
    format: str
    table: str

@app.post("/summarize",response_model= SummarizeResponse)
async def summarize(
    file: UploadFile,
    digits: int = Query(default=3, ge=0),
    format: Literal["markdown", "latex"] = "markdown",
):
    """上传 CSV，返回指定格式的统计报告。"""

    content = await file.read()

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="文件编码错误，请上传 UTF-8 编码的 CSV",
        ) from exc

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

    summary = summarize_results(results)

    if format == "markdown":
        output = format_markdown(summary, digits=digits)
    else:
        output = to_latex(summary, digits=digits)

    return SummarizeResponse(format=format, table=output)
