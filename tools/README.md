# FinSight 数据获取工具使用说明 🛠️

## 📋 工具概述

本工具集用于自动化获取金融数据，支持实时股票价格、财务数据、历史价格等信息的收集和更新。

---

## 🗂️ 文件结构

```
tools/
├── README.md                    # 本说明文档
├── requirements.txt             # Python依赖包
├── financial_data_fetcher.py   # 核心数据获取器
└── auto_data_update.py         # 自动化更新脚本
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd tools
pip install -r requirements.txt
```

### 2. 测试数据获取

```bash
python financial_data_fetcher.py
```

### 3. 运行自动化工具

```bash
python auto_data_update.py
```

---

## 🔧 核心工具说明

### FinancialDataFetcher 类

主要的金融数据获取器，提供以下功能：

#### 📊 获取股票信息
```python
fetcher = FinancialDataFetcher()
stock_info = fetcher.get_stock_info("PDD")
```

**返回数据包括**:
- 当前股价
- 市值
- PE、PB比率
- 成交量
- 52周高低点
- 股息率等

#### 📈 获取财务数据
```python
financial_data = fetcher.get_financial_data("PDD")
```

**返回数据包括**:
- 利润表数据
- 资产负债表数据
- 现金流量表数据
- 财务比率

#### 📊 获取历史价格
```python
history = fetcher.get_historical_prices("PDD", period="1y")
```

**支持的时间周期**:
- 1d, 5d, 1mo, 3mo, 6mo
- 1y, 2y, 5y, 10y, ytd, max

#### 🧮 计算财务比率
```python
ratios = fetcher.calculate_financial_ratios(financial_data)
```

**计算的比率包括**:
- 毛利率、净利率
- ROE、ROA
- 资产负债率
- 权益比率等

---

## 🤖 自动化工具说明

### AutoDataUpdater 类

自动化数据更新器，支持定时任务和批量更新：

#### 🔄 批量更新
```python
updater = AutoDataUpdater()
updater.update_all_companies()
```

**默认支持的公司**:
- PDD (拼多多)
- BABA (阿里巴巴)
- JD (京东)
- TME (腾讯音乐)
- NIO (蔚来)

#### ⏰ 定时更新
```python
# 每日更新
updater.schedule_daily_update("09:30")

# 每周更新
updater.schedule_weekly_update("monday", "09:00")

# 启动定时任务
updater.run_scheduler()
```

---

## 📱 交互式使用

### 运行自动化工具

```bash
python auto_data_update.py
```

**菜单选项**:
1. **立即更新所有公司数据** - 批量获取最新数据
2. **更新指定公司数据** - 获取单个公司数据
3. **设置每日自动更新** - 配置每日定时任务
4. **设置每周自动更新** - 配置每周定时任务
5. **启动定时任务** - 运行定时更新服务
6. **退出** - 退出程序

### 示例操作流程

```
选择操作 (1-6): 1
🔄 开始批量更新数据 - 2025-08-XX XX:XX:XX
============================================================
正在更新 拼多多(PDD) 的数据...
✅ 拼多多(PDD) 数据更新完成！
   JSON文件: ../data_templates/PDD_data_202508XX_XXXXXX.json
   Excel文件: ../data_templates/PDD_data_202508XX_XXXXXX.xlsx
============================================================
✅ 批量更新完成 - 2025-08-XX XX:XX:XX
```

---

## 📊 数据输出格式

### JSON格式
```json
{
  "stock_info": {
    "symbol": "PDD",
    "company_name": "Pinduoduo Inc.",
    "current_price": 140.50,
    "market_cap": 2000000000000,
    "update_time": "2025-08-XX XX:XX:XX"
  },
  "financial_data": {
    "income_statement": {
      "total_revenue": 25000000000,
      "net_income": 4000000000,
      "fiscal_year": 2024
    }
  },
  "financial_ratios": {
    "gross_margin": 80.5,
    "roe": 28.2
  }
}
```

### Excel格式
- **Stock_Info**: 股票基本信息
- **Income_Statement**: 利润表数据
- **Balance_Sheet**: 资产负债表数据
- **Cash_Flow**: 现金流量表数据
- **Financial_Ratios**: 财务比率

---

## ⚙️ 配置选项

### 自定义公司列表

在 `auto_data_update.py` 中修改 `companies` 列表：

```python
self.companies = [
    {"symbol": "PDD", "name": "拼多多"},
    {"symbol": "BABA", "name": "阿里巴巴"},
    # 添加更多公司...
]
```

### 自定义数据字段

在 `financial_data_fetcher.py` 中修改数据提取逻辑：

```python
def get_stock_info(self, symbol: str) -> Dict[str, Any]:
    # 添加或修改需要获取的字段
    stock_data = {
        'symbol': symbol,
        'custom_field': info.get('customField', 0),
        # ... 其他字段
    }
```

---

## 🔍 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 2. yfinance连接失败
```bash
# 检查网络连接
ping finance.yahoo.com

# 使用代理（如需要）
export https_proxy=http://your-proxy:port
```

#### 3. 数据获取为空
- 检查股票代码是否正确
- 确认网络连接正常
- 查看日志文件了解详细错误

### 日志文件

工具运行时会生成 `financial_data.log` 日志文件，包含详细的运行信息和错误记录。

---

## 📈 使用建议

### 1. **数据更新频率**
- **股价数据**: 每日更新（交易时间）
- **财务数据**: 季度更新（财报发布后）
- **历史数据**: 按需更新

### 2. **资源管理**
- 避免过于频繁的请求
- 合理设置定时任务间隔
- 定期清理历史数据文件

### 3. **数据质量**
- 验证获取数据的准确性
- 交叉检查多个数据源
- 记录数据来源和时间

---

## 🔗 相关链接

- **yfinance文档**: https://pypi.org/project/yfinance/
- **pandas文档**: https://pandas.pydata.org/
- **schedule文档**: https://pypi.org/project/schedule/

---

## 📞 技术支持

如有问题或需要技术支持，请联系FinSight分析团队。

---

*本工具基于开源库开发，请遵守相关使用条款和API限制。* 