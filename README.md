# Telegram Bot Service

Простой Telegram‑бот на PTB и Flask для routing флов в n8n:
- сохранение сообщений
- создание новостей с медиа
- health check

## Локальный запуск

```bash
git clone <repo-url>
cd telegram-bot
cp .env.example .env
pip install -r requirements.txt
python main.py
