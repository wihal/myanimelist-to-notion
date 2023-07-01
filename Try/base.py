from datetime import datetime, timezone

import requests

NOTION_TOKEN = "SECRET_TOKEN_HERE"
DATABASE_ID = "DB_ID_HERE"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def create_page(data_db: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data_db}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res


name = "Test"
link = "https://developers.notion.com/"
typo = "Anime"
status = "In progress"
score = "⭐️⭐️⭐️⭐️⭐️"
author = "Test"
image = "https://cdn.myanimelist.net/images/anime/1107/136174.jpg"
completed_date = datetime.now().astimezone(timezone.utc).isoformat()

data = {
    "Name": {"title": [{"text": {"content": name}}]},
    "Link": {"url": link},
    "Type": {"select": {"name": typo}},
    "Status": {"status": {"name": status}},
    "Score": {"select": {"name": score}},
    "Author": {"rich_text": [{"text": {"content": author}}]},
    "Completed": {"date": {"start": completed_date, "end": None}},
}

create_page(data)
