#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化数据更新脚本
定期运行获取最新金融数据并更新报告
"""

import schedule
import time
import os
import sys
from datetime import datetime
from financial_data_fetcher import FinancialDataFetcher

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AutoDataUpdater:
    """自动化数据更新器"""
    
    def __init__(self):
        self.fetcher = FinancialDataFetcher()
        self.companies = [
            {"symbol": "PDD", "name": "拼多多"},
            {"symbol": "BABA", "name": "阿里巴巴"},
            {"symbol": "JD", "name": "京东"},
            {"symbol": "TME", "name": "腾讯音乐"},
            {"symbol": "NIO", "name": "蔚来"}
        ]
    
    def update_single_company(self, symbol: str, name: str):
        """更新单个公司的数据"""
        try:
            print(f"正在更新 {name}({symbol}) 的数据...")
            
            # 获取股票信息
            stock_info = self.fetcher.get_stock_info(symbol)
            
            # 获取财务数据
            financial_data = self.fetcher.get_financial_data(symbol)
            
            # 计算财务比率
            financial_ratios = self.fetcher.calculate_financial_ratios(financial_data)
            
            # 整合所有数据
            all_data = {
                'stock_info': stock_info,
                'financial_data': financial_data,
                'financial_ratios': financial_ratios
            }
            
            # 保存数据
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data_dir = "../data_templates"
            
            # 确保目录存在
            os.makedirs(data_dir, exist_ok=True)
            
            json_filename = f"{data_dir}/{symbol}_data_{timestamp}.json"
            excel_filename = f"{data_dir}/{symbol}_data_{timestamp}.xlsx"
            
            self.fetcher.save_data_to_json(all_data, json_filename)
            self.fetcher.save_data_to_excel(all_data, excel_filename)
            
            print(f"✅ {name}({symbol}) 数据更新完成！")
            print(f"   JSON文件: {json_filename}")
            print(f"   Excel文件: {excel_filename}")
            
        except Exception as e:
            print(f"❌ {name}({symbol}) 数据更新失败: {str(e)}")
    
    def update_all_companies(self):
        """更新所有公司的数据"""
        print(f"\n🔄 开始批量更新数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        for company in self.companies:
            self.update_single_company(company["symbol"], company["name"])
            time.sleep(2)  # 避免请求过于频繁
        
        print("=" * 60)
        print(f"✅ 批量更新完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_specific_company(self, symbol: str):
        """更新指定公司的数据"""
        company = next((c for c in self.companies if c["symbol"] == symbol), None)
        if company:
            self.update_single_company(company["symbol"], company["name"])
        else:
            print(f"❌ 未找到公司代码: {symbol}")
    
    def schedule_daily_update(self, time_str: str = "09:30"):
        """设置每日定时更新"""
        schedule.every().day.at(time_str).do(self.update_all_companies)
        print(f"📅 已设置每日 {time_str} 自动更新数据")
    
    def schedule_weekly_update(self, day: str = "monday", time_str: str = "09:00"):
        """设置每周定时更新"""
        if day == "monday":
            schedule.every().monday.at(time_str).do(self.update_all_companies)
        elif day == "friday":
            schedule.every().friday.at(time_str).do(self.update_all_companies)
        else:
            schedule.every().week.at(time_str).do(self.update_all_companies)
        
        print(f"📅 已设置每周 {day} {time_str} 自动更新数据")
    
    def run_scheduler(self):
        """运行定时任务"""
        print("🚀 启动定时任务调度器...")
        print("按 Ctrl+C 停止")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n⏹️ 定时任务已停止")

def main():
    """主函数"""
    updater = AutoDataUpdater()
    
    print("🔧 FinSight 自动化数据更新工具")
    print("=" * 40)
    print("1. 立即更新所有公司数据")
    print("2. 更新指定公司数据")
    print("3. 设置每日自动更新")
    print("4. 设置每周自动更新")
    print("5. 启动定时任务")
    print("6. 退出")
    print("=" * 40)
    
    while True:
        try:
            choice = input("\n请选择操作 (1-6): ").strip()
            
            if choice == "1":
                updater.update_all_companies()
                
            elif choice == "2":
                symbol = input("请输入公司代码 (如: PDD): ").strip().upper()
                updater.update_specific_company(symbol)
                
            elif choice == "3":
                time_str = input("请输入每日更新时间 (格式: HH:MM, 默认: 09:30): ").strip()
                if not time_str:
                    time_str = "09:30"
                updater.schedule_daily_update(time_str)
                
            elif choice == "4":
                day = input("请输入每周更新日期 (monday/friday, 默认: monday): ").strip()
                if not day:
                    day = "monday"
                time_str = input("请输入每周更新时间 (格式: HH:MM, 默认: 09:00): ").strip()
                if not time_str:
                    time_str = "09:00"
                updater.schedule_weekly_update(day, time_str)
                
            elif choice == "5":
                updater.run_scheduler()
                
            elif choice == "6":
                print("👋 再见！")
                break
                
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 操作失败: {str(e)}")

if __name__ == "__main__":
    proxy = 'http://127.0.0.1:8118'
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    main() 