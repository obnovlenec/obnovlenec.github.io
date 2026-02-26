import requests
import os
import json
from datetime import datetime

# Берем токен и ID канала из переменных окружения
TOKEN = os.getenv("TG_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # обязательно строкой

API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates():
    """Получаем все обновления бота"""
    r = requests.get(f"{API_URL}/getUpdates")
    if r.status_code == 200:
        return r.json()
    else:
        print("Ошибка при получении обновлений:", r.text)
        return {}

def load_existing_posts():
    """Загружаем уже сохраненные посты"""
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    """Сохраняем посты обратно в файл"""
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def main():
    updates = get_updates()
    existing_posts = load_existing_posts()
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
                print(f"Добавлено сообщение {message_id}")

    save_posts(existing_posts)
    print("Обновление завершено.")

if __name__ == "__main__":
    main()
