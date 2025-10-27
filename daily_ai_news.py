#!/usr/bin/env python3
"""
Daily AI News - Python v2
-------------------------
Rebuilt from n8n workflow:
“Daily AI News Translation & Summary with GPT-4 and Telegram Delivery”

This script:
1. Fetches AI-related articles from NewsAPI & GNews
2. Merges & deduplicates articles
3. Uses OpenAI GPT model to summarize & translate them into Traditional Chinese
4. Sends results via Telegram message

Runs automatically in MOCK mode if API keys are not set.
"""

import os
import logging
import requests
from datetime import datetime
from openai import OpenAI
from config import Config

log = logging.getLogger("daily_ai_news")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
cfg = Config.load_from_env()


# --- MOCK HELPERS ---
def mock_articles():
    return [
        {"title": "AI beats humans at chess again", "url": "https://example.com/ai1"},
        {"title": "New GPT model released by OpenAI", "url": "https://example.com/ai2"},
    ]


# --- FETCH NEWS ---
def fetch_gnews():
    if cfg.mock:
        log.info("[MOCK] Fetching GNews articles")
        return mock_articles()

    url = "https://gnews.io/api/v4/search"
    params = {"q": "AI", "lang": "en", "apikey": cfg.GNEWS_API_KEY}
    res = requests.get(url, params=params)
    return res.json().get("articles", [])


def fetch_newsapi():
    if cfg.mock:
        log.info("[MOCK] Fetching NewsAPI articles")
        return mock_articles()

    url = "https://newsapi.org/v2/everything"
    headers = {"X-Api-Key": cfg.NEWSAPI_KEY}
    params = {"q": "AI", "language": "en", "pageSize": 20, "sortBy": "publishedAt"}
    res = requests.get(url, headers=headers, params=params)
    return res.json().get("articles", [])


# --- MERGE & CLEAN ---
def merge_articles(a1, a2):
    seen, merged = set(), []
    for article in (a1 + a2):
        title = article.get("title", "").strip()
        if title and title not in seen:
            seen.add(title)
            merged.append({"title": title, "url": article.get("url", "")})
    return merged


# --- AI SUMMARIZER ---
def summarize_and_translate(articles):
    today = datetime.now().strftime("%Y/%m/%d")
    text = f"早安，這是 {today} 的 AI 新聞：\n\n"
    if cfg.mock:
        log.info("[MOCK] Summarizing and translating articles")
        for a in articles:
            text += f"• {a['title']} ({a['url']})\n"
        return text

    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    prompt = (
        "You are an AI news assistant. Your tasks:\n"
        "1. Select the 15 most relevant AI technology news items from the list below.\n"
        "2. Translate them into Traditional Chinese but do not translate technical English terms.\n"
        "3. Include URLs.\n"
        f"Articles: {articles}"
    )
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a multilingual AI news summarizer."},
            {"role": "user", "content": prompt},
        ],
    )
    return text + res.choices[0].message.content.strip()


# --- TELEGRAM SEND ---
def send_telegram(message):
    if cfg.mock:
        log.info("[MOCK] Telegram message:\n" + message)
        return

    url = f"https://api.telegram.org/bot{cfg.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": cfg.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    res = requests.post(url, data=data)
    if res.status_code != 200:
        log.error(f"Failed to send message: {res.text}")
    else:
        log.info("Message sent to Telegram successfully!")


# --- MAIN WORKFLOW ---
def main():
    log.info("🗞️ Starting Daily AI News Workflow")

    gnews = fetch_gnews()
    newsapi = fetch_newsapi()
    merged = merge_articles(gnews, newsapi)
    log.info(f"Fetched and merged {len(merged)} articles.")

    summary = summarize_and_translate(merged)
    send_telegram(summary)

    log.info("✅ Daily news summary completed.")


if __name__ == "__main__":
    main()
