# main.py
from config import API_DATA_URL, COMPANY_KEYWORDS, OUTPUT_FILE, INITIAL_PAGE_CALLBACK
from scraper import fetch_articles_from_api
from analyzer import analyze_articles
import pandas as pd

def run():
    
    if not INITIAL_PAGE_CALLBACK:
        print("错误: 'INITIAL_PAGE_CALLBACK' 未在 config.py 中设置。")
        return

    print(f"DEBUG: 正在使用硬编码的 'pageCallback' 开始抓取: {INITIAL_PAGE_CALLBACK[:20]}...")
    
    # 1. 抓取第一页
    articles_data, next_callback = fetch_articles_from_api(API_DATA_URL, INITIAL_PAGE_CALLBACK, page_event=1)
    
    # 2. 自动抓取第二页
    if next_callback:
        print("DEBUG: 正在抓取第二页...")
        page_2_articles, _ = fetch_articles_from_api(API_DATA_URL, next_callback, page_event=2)
        if page_2_articles:
            articles_data.extend(page_2_articles) # 把第二页数据合并
            print(f"DEBUG: 成功合并第二页，总文章数: {len(articles_data)}")
        else:
            print("DEBUG: 第二页没有更多文章了。")
    
    if not articles_data:
        print("没有抓取到数据，程序退出。")
        return

    # 3. 分析数据
    df_articles, df_keywords = analyze_articles(articles_data, COMPANY_KEYWORDS)
    
    # 4. 保存报告
    df_articles.to_csv("detailed_articles.csv", index=False, encoding='utf-8-sig')
    df_keywords.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print(f"\n--- 任务完成 ---")
    print(f"关键词热度报告已保存到: {OUTPUT_FILE}")
    print(f"详细文章列表已保存到: detailed_articles.csv (共 {len(articles_data)} 篇)")

if __name__ == "__main__":
    run()