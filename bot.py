import requests
import os
import json
from datetime import datetime

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TG_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    """Получаем обновления от Telegram с опциональным смещением"""
    params = {"offset": offset, "timeout": 10}
    r = requests.get(f"{API_URL}/getUpdates", params=params)
    r.raise_for_status()
    return r.json()

def load_existing_posts():
    """Загружаем уже сохраненные посты"""
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    """Сохраняем посты в файл"""
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def main():
    existing_posts = load_existing_posts()
    existing_ids = {p["id"] for p in existing_posts}

    # Берем обновления
    updates = get_updates()
    new_posts = []

    for item in updates.get("result", []):
        post = item.get("channel_post")
        if not post:
            continue

        if str(post["chat"]["id"]) != CHANNEL_ID:
            continue

        message_id = post["message_id"]

        if message_id not in existing_ids:
            text = post.get("text", "")
            date = datetime.fromtimestamp(post["date"]).strftime("%d.%m.%Y %H:%M")

            new_posts.append({
                "id": message_id,
                "text": text,
                "date": date
            })

    if new_posts:
        existing_posts.extend(new_posts)
        save_posts(existing_posts)
        print(f"Добавлено {len(new_posts)} новых постов")
    else:
        print("Новых постов нет")

if __name__ == "__main__":
    main()
