# auto-val-model
Automated valuation modeling system powered by LLM. Parse financial reports, extract metrics, run DCF & comparable company analysis, and generate valuation reports automatically.

中文：基于大语言模型的自动化估值建模工具，自动解析财报PDF，提取财务指标，执行DCF与可比公司分析，输出完整估值报告。

## 功能简介
上传上市公司年度/季度财报PDF，程序自动：
1. 读取PDF文本
2. LLM抽取财务科目
3. DCF现金流折现估值计算
4. 可比公司倍数估值校验
5. 生成Markdown估值报告（包含完整计算过程、假设条件、估值逻辑、风险提示）
   
## 使用方法
1. 编辑.env 填入你的 OpenAI Key
2. 将财报 pdf 重命名为 `report.pdf`，上传到项目根目录

## GitHub Codespaces 快速启动
1. Fork本仓库，打开Codespaces
2. 在Codespace终端：
```bash
cp .env.example .env
