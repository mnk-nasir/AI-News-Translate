# AI-News-Translate
A Telegram bot delivering daily AI news summaries with multilingual support.# 🗞️ Daily AI News Bot (Python v2)

Modern Python version of your n8n workflow **“Daily AI News Translation & Summary with GPT-4 and Telegram Delivery”**

---

## ⚙️ What It Does
1. Fetches AI news from **NewsAPI** and **GNews**
2. Summarizes and translates top stories into **Traditional Chinese**
3. Sends results to **Telegram**
4. Runs daily (or manually)

---

## 🚀 Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
Then add your keys to .env and run:

bash
Copy code
python daily_ai_news.py
If keys are missing, it automatically runs in MOCK mode for safe testing.

🕒 Automating Daily Delivery
You can automate daily sending at 8 AM using:

bash
Copy code
0 8 * * * /usr/bin/python /path/to/daily_ai_news.py
or a GitHub Action with a cron schedule.

🧩 APIs Used
NewsAPI.org

GNews.io

OpenAI API

Telegram Bot API

🪪 License
MIT License © 2025

markdown
Copy code

---

✅ **All 5 files complete and upgraded to v2**:
1. `daily_ai_news.py`  
2. `config.py`  
3. `requirements.txt`  
4. `.env.example`  
5. `README.md`  

Would you like me to add a **GitHub Actions workflow (`.github/workflows/daily.yml`)** so it auto-po
