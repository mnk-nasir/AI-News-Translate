import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    GNEWS_API_KEY: str
    NEWSAPI_KEY: str
    OPENAI_API_KEY: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    mock: bool

    @staticmethod
    def load_from_env() -> "Config":
        g = os.getenv("GNEWS_API_KEY", "")
        n = os.getenv("NEWSAPI_KEY", "")
        o = os.getenv("OPENAI_API_KEY", "")
        t = os.getenv("TELEGRAM_BOT_TOKEN", "")
        c = os.getenv("TELEGRAM_CHAT_ID", "")
        mock = not (g and n and o and t and c)
        return Config(g, n, o, t, c, mock)
