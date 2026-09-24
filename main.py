import os
import dotenv
import pdfplumber
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def extract_pdf_text(pdf_path: str) -> str:
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text

valuation_prompt = ChatPromptTemplate.from_template("""
你是资深金融分析师。下面是上市公司财报/研报文本。
任务：
1. 提取核心财务数据：营业收入、净利润、EBIT、折旧摊销、资本开支、营运资本变动、税率。区分是年报还是季报。
2. 做DCF估值：计算自由现金流FCF；设定永续增长率、WACC；计算企业价值EV、股权价值、每股价值。
3. 做可比公司相对估值：选取同行业可比标的，用PE、EV/EBITDA做估值校验。
4. 输出完整估值报告：
- 公司&报告基础信息
- 提取的财务数据表格
- DCF估值完整计算过程（每一步公式+数值）
- 相对估值结果
- 估值结论：当前估算内在价值，上涨/下跌空间，估值逻辑与风险点
要求：
- 严格写明每一步计算过程，不要跳步骤
- 区分假设参数（WACC、永续增长率），标注哪些是人为假设
- 报告中文，结构清晰

【研报/财报文本】
{report_text}
""")

def run_valuation(pdf_file_path: str):
    print(f"开始读取PDF：{pdf_file_path}")
    text = extract_pdf_text(pdf_file_path)
    print("PDF文本提取完成，开始调用大模型进行估值建模...")
    chain = valuation_prompt | llm
    result = chain.invoke({"report_text": text[:12000]})
    report_content = result.content

    out_file = "valuation_result.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"✅ 估值报告已生成：{out_file}")
    return report_content

if __name__ == "__main__":
    pdf_path = "report.pdf"
    markdown_report = run_valuation(pdf_path)
    print("\n===== 估值报告预览 =====")
    print(markdown_report[:2000])
