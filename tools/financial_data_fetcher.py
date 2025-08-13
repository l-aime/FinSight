#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金融数据获取工具
用于获取股票价格、财务数据等实时信息
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_data.log'),
        logging.StreamHandler()
    ]
)

class FinancialDataFetcher:
    """金融数据获取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码 (如: PDD, BABA, JD)
            
        Returns:
            股票基本信息字典
        """
        try:
            logging.info(f"正在获取 {symbol} 的股票信息...")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 提取关键信息
            stock_data = {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'current_price': info.get('regularMarketPrice', 0),
                'previous_close': info.get('regularMarketPreviousClose', 0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'year_high': info.get('fiftyTwoWeekHigh', 0),
                'year_low': info.get('fiftyTwoWeekLow', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logging.info(f"成功获取 {symbol} 股票信息")
            return stock_data
            
        except Exception as e:
            logging.error(f"获取 {symbol} 股票信息失败: {str(e)}")
            return {}
    
    def get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """
        获取财务数据
        
        Args:
            symbol: 股票代码
            
        Returns:
            财务数据字典
        """
        try:
            logging.info(f"正在获取 {symbol} 的财务数据...")
            stock = yf.Ticker(symbol)
            
            # 获取财务报表
            income_stmt = stock.income_stmt
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cash_flow
            
            financial_data = {
                'symbol': symbol,
                'income_statement': self._process_income_statement(income_stmt),
                'balance_sheet': self._process_balance_sheet(balance_sheet),
                'cash_flow': self._process_cash_flow(cash_flow),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logging.info(f"成功获取 {symbol} 财务数据")
            return financial_data
            
        except Exception as e:
            logging.error(f"获取 {symbol} 财务数据失败: {str(e)}")
            return {}
    
    def _process_income_statement(self, income_stmt: pd.DataFrame) -> Dict[str, Any]:
        """处理利润表数据"""
        if income_stmt.empty:
            return {}
        
        try:
            # 获取最新年度数据
            latest_year = income_stmt.columns[0]
            
            return {
                'total_revenue': income_stmt.loc['Total Revenue', latest_year] if 'Total Revenue' in income_stmt.index else 0,
                'gross_profit': income_stmt.loc['Gross Profit', latest_year] if 'Gross Profit' in income_stmt.index else 0,
                'operating_income': income_stmt.loc['Operating Income', latest_year] if 'Operating Income' in income_stmt.index else 0,
                'net_income': income_stmt.loc['Net Income', latest_year] if 'Net Income' in income_stmt.index else 0,
                'ebitda': income_stmt.loc['EBITDA', latest_year] if 'EBITDA' in income_stmt.index else 0,
                'fiscal_year': latest_year.year
            }
        except Exception as e:
            logging.error(f"处理利润表数据失败: {str(e)}")
            return {}
    
    def _process_balance_sheet(self, balance_sheet: pd.DataFrame) -> Dict[str, Any]:
        """处理资产负债表数据"""
        if balance_sheet.empty:
            return {}
        
        try:
            latest_year = balance_sheet.columns[0]
            
            return {
                'total_assets': balance_sheet.loc['Total Assets', latest_year] if 'Total Assets' in balance_sheet.index else 0,
                'total_liabilities': balance_sheet.loc['Total Liabilities', latest_year] if 'Total Liabilities' in balance_sheet.index else 0,
                'total_equity': balance_sheet.loc['Total Equity', latest_year] if 'Total Equity' in balance_sheet.index else 0,
                'cash_and_equivalents': balance_sheet.loc['Cash and Cash Equivalents', latest_year] if 'Cash and Cash Equivalents' in balance_sheet.index else 0,
                'total_debt': balance_sheet.loc['Total Debt', latest_year] if 'Total Debt' in balance_sheet.index else 0,
                'fiscal_year': latest_year.year
            }
        except Exception as e:
            logging.error(f"处理资产负债表数据失败: {str(e)}")
            return {}
    
    def _process_cash_flow(self, cash_flow: pd.DataFrame) -> Dict[str, Any]:
        """处理现金流量表数据"""
        if cash_flow.empty:
            return {}
        
        try:
            latest_year = cash_flow.columns[0]
            
            return {
                'operating_cash_flow': cash_flow.loc['Operating Cash Flow', latest_year] if 'Operating Cash Flow' in cash_flow.index else 0,
                'investing_cash_flow': cash_flow.loc['Investing Cash Flow', latest_year] if 'Investing Cash Flow' in cash_flow.index else 0,
                'financing_cash_flow': cash_flow.loc['Financing Cash Flow', latest_year] if 'Financing Cash Flow' in cash_flow.index else 0,
                'free_cash_flow': cash_flow.loc['Free Cash Flow', latest_year] if 'Free Cash Flow' in cash_flow.index else 0,
                'fiscal_year': latest_year.year
            }
        except Exception as e:
            logging.error(f"处理现金流量表数据失败: {str(e)}")
            return {}
    
    def get_historical_prices(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        获取历史价格数据
        
        Args:
            symbol: 股票代码
            period: 时间周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            历史价格DataFrame
        """
        try:
            logging.info(f"正在获取 {symbol} 的历史价格数据...")
            stock = yf.Ticker(symbol)
            history = stock.history(period=period)
            
            logging.info(f"成功获取 {symbol} 历史价格数据")
            return history
            
        except Exception as e:
            logging.error(f"获取 {symbol} 历史价格数据失败: {str(e)}")
            return pd.DataFrame()
    
    def calculate_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算财务比率"""
        try:
            income = financial_data.get('income_statement', {})
            balance = financial_data.get('balance_sheet', {})
            
            if not income or not balance:
                return {}
            
            ratios = {}
            
            # 盈利能力比率
            if income.get('total_revenue') and income.get('gross_profit'):
                ratios['gross_margin'] = (income['gross_profit'] / income['total_revenue']) * 100
            
            if income.get('total_revenue') and income.get('net_income'):
                ratios['net_margin'] = (income['net_income'] / income['total_revenue']) * 100
            
            if balance.get('total_equity') and income.get('net_income'):
                ratios['roe'] = (income['net_income'] / balance['total_equity']) * 100
            
            if balance.get('total_assets') and income.get('net_income'):
                ratios['roa'] = (income['net_income'] / balance['total_assets']) * 100
            
            # 财务健康比率
            if balance.get('total_assets') and balance.get('total_liabilities'):
                ratios['debt_to_assets'] = (balance['total_liabilities'] / balance['total_assets']) * 100
            
            if balance.get('total_equity') and balance.get('total_assets'):
                ratios['equity_ratio'] = (balance['total_equity'] / balance['total_assets']) * 100
            
            return ratios
            
        except Exception as e:
            logging.error(f"计算财务比率失败: {str(e)}")
            return {}
    
    def save_data_to_json(self, data: Dict[str, Any], filename: str):
        """保存数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            logging.info(f"数据已保存到 {filename}")
        except Exception as e:
            logging.error(f"保存数据失败: {str(e)}")
    
    def save_data_to_excel(self, data: Dict[str, Any], filename: str):
        """保存数据到Excel文件"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 股票信息
                if 'stock_info' in data:
                    pd.DataFrame([data['stock_info']]).to_excel(writer, sheet_name='Stock_Info', index=False)
                
                # 财务数据
                if 'financial_data' in data:
                    financial = data['financial_data']
                    if 'income_statement' in financial:
                        pd.DataFrame([financial['income_statement']]).to_excel(writer, sheet_name='Income_Statement', index=False)
                    if 'balance_sheet' in financial:
                        pd.DataFrame([financial['balance_sheet']]).to_excel(writer, sheet_name='Balance_Sheet', index=False)
                    if 'cash_flow' in financial:
                        pd.DataFrame([financial['cash_flow']]).to_excel(writer, sheet_name='Cash_Flow', index=False)
                
                # 财务比率
                if 'financial_ratios' in data:
                    pd.DataFrame([data['financial_ratios']]).to_excel(writer, sheet_name='Financial_Ratios', index=False)
            
            logging.info(f"数据已保存到 {filename}")
        except Exception as e:
            logging.error(f"保存Excel文件失败: {str(e)}")

def main():
    """主函数 - 示例用法"""
    fetcher = FinancialDataFetcher()
    
    # 获取拼多多数据
    symbol = "PDD"
    
    print(f"正在获取 {symbol} 的完整数据...")
    
    # 获取股票信息
    stock_info = fetcher.get_stock_info(symbol)
    
    # 获取财务数据
    financial_data = fetcher.get_financial_data(symbol)
    
    # 计算财务比率
    financial_ratios = fetcher.calculate_financial_ratios(financial_data)
    
    # 整合所有数据
    all_data = {
        'stock_info': stock_info,
        'financial_data': financial_data,
        'financial_ratios': financial_ratios
    }
    
    # 保存数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_filename = f"../data_templates/{symbol}_data_{timestamp}.json"
    excel_filename = f"../data_templates/{symbol}_data_{timestamp}.xlsx"
    
    fetcher.save_data_to_json(all_data, json_filename)
    fetcher.save_data_to_excel(all_data, excel_filename)
    
    print(f"数据获取完成！")
    print(f"JSON文件: {json_filename}")
    print(f"Excel文件: {excel_filename}")

if __name__ == "__main__":
    main() 