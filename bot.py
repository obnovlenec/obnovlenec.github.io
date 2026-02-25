import requests
import os
import json
from datetime import datetime

TOKEN = os.getenv("TG_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates():
    r = requests.get(f"{API_URL}/getUpdates")
    return r.json()

def load_existing_posts():
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def generate_html(posts):
    posts_html = ""
    for p in reversed(posts):
        posts_html += f"""
        <div class="post">
            <div class="date">{p['date']}</div>
            <div class="text">{p['text']}</div>
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Не(о)обновленец</title>
<style>
body {{ font-family: sans-serif; max-width: 700px; margin: auto; }}
.post {{ border-bottom: 1px solid #ddd; padding: 15px 0; }}
.date {{ color: gray; font-size: 12px; margin-bottom: 5px; }}
</style>
</head>
<body>
<h1>Не(о)обновленец</h1>
{posts_html}
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    updates = get_updates()
    existing_posts = load_existing_posts()

    existing_ids = {p["id"] for p in existing_posts}

    for item in updates.get("result", []):
        post = item.get("channel_post")
        if post and str(post["chat"]["id"]) == CHANNEL_ID:
            if post["message_id"] not in existing_ids:
                text = post.get("text", "")
                date = datetime.fromtimestamp(post["date"]).strftime("%d.%m.%Y %H:%M")

                existing_posts.append({
                    "id": post["message_id"],
                    "text": text,
                    "date": date
                })

    save_posts(existing_posts)
    generate_html(existing_posts)

if __name__ == "__main__":
    main()
