# 搜索测试
from duckduckgo_search import DDGS

with DDGS(proxies="socks5://localhost:10806", timeout=20) as ddgs:
    for r in ddgs.text(
        "明天广州天气",
        region="cn-zh",
        timelimit="d",
        backend="api",
        max_results=1,
    ):
        print(r["body"])
