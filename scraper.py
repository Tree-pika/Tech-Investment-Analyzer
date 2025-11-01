# scraper.py
import requests
import time
import json
import re # 正则表达式

# 从 config 导入URL
from config import API_DATA_URL, INITIAL_PAGE_CALLBACK


def fetch_articles_from_api(api_url, callback, page_event=1):
    """
    第二步：使用获取到的 'callback' 来请求API 
    """
    print(f"正在抓取API: {api_url} (Page: {page_event})")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/json'
    }
    
    payload = {
      "param": {
        "subnavType": 1,
        "subnavNick": "AI",
        "pageSize": 30,
        "pageEvent": page_event,
        "pageCallback": callback, #
        "platformId": 2,
        "siteId": 1
      },
      "partner_id": "web",
      "timestamp": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') != 0:
            print(f"API 逻辑错误: {data.get('msg')}")
            return [], None
            
        article_items = data.get('data', {}).get('itemList', [])
        next_callback = data.get('data', {}).get('pageCallback')
        
        if not article_items:
            print("警告：成功访问API，但未找到 'itemList'。")
            return [], next_callback

        articles = []
        base_url = "https://www.36kr.com/p/"
        
        for item in article_items:
            # 根据JSON完善解析逻辑
            material = item.get('templateMaterial', {})
            title = material.get('widgetTitle')
            summary = material.get('summary')  
            item_id = item.get('itemId')
            
            if title and summary and item_id:
                articles.append({
                    'title': title,
                    'summary': summary,
                    'link': base_url + str(item_id)
                })
        
        print(f"成功抓取 {len(articles)} 篇文章")
        return articles, next_callback

    except requests.exceptions.RequestException as e:
        print(f"抓取失败: {e}")
    except json.JSONDecodeError:
        print("API返回的不是有效的JSON数据，请检查。")
    
    return [], None

# (测试用)
if __name__ == "__main__":
    print("--- (scraper.py) DEBUG TEST ---")
    
    articles_data, next_callback = fetch_articles_from_api(API_DATA_URL, INITIAL_PAGE_CALLBACK, page_event=1)
    
    if articles_data:
        print("\n--- 抓取示例 (第一页) ---")
        print(articles_data[0]['title'])
    
    if next_callback:
        print(f"\nDEBUG: 成功获取到 'next_callback': {next_callback[:20]}...")