import requests
import os
import json
from datetime import datetime

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TG_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Получаем новые сообщения
def get_updates():
    r = requests.get(f"{API_URL}/getUpdates")
    r.raise_for_status()
    return r.json()

# Загружаем уже сохранённые посты
def load_existing_posts():
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохраняем посты в файл
def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def main():
    updates = get_updates()
    existing_posts = load_existing_posts()

    # Чтобы не добавлять повторно
    existing_ids = {p["id"] for p in existing_posts}

    for item in updates.get("result", []):
        post = item.get("channel_post")
        if post and str(post["chat"]["id"]) == CHANNEL_ID:
            message_id = post["message_id"]
            if message_id not in existing_ids:
                text = post.get("text", "")
                date = datetime.fromtimestamp(post["date"]).strftime("%d.%m.%Y %H:%M")

                existing_posts.append({
                    "id": message_id,
                    "text": text,
                    "date": date
                })

    save_posts(existing_posts)

if __name__ == "__main__":
    main()
