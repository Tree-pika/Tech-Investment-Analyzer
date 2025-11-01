# config.py

# API URL (to get the data)
API_DATA_URL = "https://gateway.36kr.com/api/mis/nav/ifm/subNav/flow"

# "查看网页源代码" 
INITIAL_PAGE_CALLBACK = "eyJmaXJzdElkIjo1MDg5ODY3LCJsYXN0SWQiOjUwODg0NDEsImZpcnN0Q3JlYXRlVGltZSI6MTc2MTk3MzMzMDIwNSwibGFzdENyZWF0ZVRpbWUiOjE3NjE4NjcxMjM2NjN9"


# 关心的“硬科技”公司关键词
COMPANY_KEYWORDS = [
    "OpenAI", "英伟达", "NVIDIA", "Anthropic", 
    "华为", "中芯国际", "寒武纪", "商汤", "旷视", 
    "月之暗面", "Kimi", "Sora"
]

# 输出报告的文件名
OUTPUT_FILE = "report.csv"