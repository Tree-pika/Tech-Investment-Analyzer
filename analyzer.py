# analyzer.py
import pandas as pd
import jieba
from snownlp import SnowNLP # (可选)

jieba.load_userdict('custom_dict.txt')

def analyze_articles(articles_data, keywords):
    """分析文章数据，统计关键词并（可选）进行情绪分析"""

    # 1. 关键词统计
    keyword_counts = {keyword: 0 for keyword in keywords}

    # 2. (可选) 情绪分析
    sentiment_scores = []

    analyzed_articles = []

    for article in articles_data:
        text_to_analyze = article['title'] + " " + article['summary']

        # --- 关键词统计 ---
        # 使用jieba分词以匹配中文词
        seg_list = jieba.cut(text_to_analyze)
        article_words = set(seg_list) # 使用set提高效率

        mentions = []
        for keyword in keywords:
            # 简单的大小写不敏感匹配
            if keyword.lower() in text_to_analyze.lower() or keyword in article_words:
                keyword_counts[keyword] += 1
                mentions.append(keyword)

        # --- (可选) 情绪分析 ---
        # s = SnowNLP(article['title']) # 只分析标题的情绪
        # sentiment_scores.append(s.sentiments)
        # article['sentiment'] = s.sentiments

        article['mentions'] = ", ".join(mentions) # 记录每篇文章提到了哪些词
        analyzed_articles.append(article)

    # 3. 转换成DataFrame (Pandas)
    df_articles = pd.DataFrame(analyzed_articles)

    # 4. 创建关键词频率报告
    df_keywords = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Frequency'])
    df_keywords = df_keywords.sort_values(by='Frequency', ascending=False)

    # (可选) 计算整体情绪
    # avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    print("\n--- 分析报告 ---")
    print(df_keywords)
    # print(f"AI赛道整体情绪: {avg_sentiment:.2f}")

    return df_articles, df_keywords