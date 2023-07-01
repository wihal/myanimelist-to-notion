import lxml.etree as ET
import requests
from datetime import datetime, timezone

from bs4 import BeautifulSoup

NOTION_TOKEN = "SECRET_TOKEN_HERE"
DATABASE_ID = "DB_ID_HERE"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Path to the XML file
file_path = 'animelist.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

typo = "Anime"
author = "MyAnimeList"
completed_date = datetime.now().astimezone(timezone.utc).isoformat()


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": data,
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": image_url
                    }
                }
            }
        ]
    }

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res


# Extract and print the desired information
for anime_elem in root.findall('.//anime'):

    series_animedb_id = anime_elem.find('series_animedb_id').text

    link = f"https://myanimelist.net/anime/{series_animedb_id}"
    print(link)

    series_title = anime_elem.find('series_title').text

    my_score = anime_elem.find('my_score').text
    if my_score in ['1', '2']:
        my_score = '⭐️'
    elif my_score in ['3', '4']:
        my_score = '⭐️⭐️'
    elif my_score in ['5', '6']:
        my_score = '⭐️⭐️⭐️'
    elif my_score in ['7', '8']:
        my_score = '⭐️⭐️⭐️⭐️'
    elif my_score in ['9', '10']:
        my_score = '⭐️⭐️⭐️⭐️⭐️'
    else:
        my_score = 'TBD'

    my_status = anime_elem.find('my_status').text
    if my_status == 'Completed':
        my_status = 'Done'
    elif my_status == 'Plan to Watch':
        my_status = 'Not started'

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    cover_image = soup.find("img", class_="ac")
    image_url = cover_image["data-src"]
    print(image_url)

    data = {
        "Name": {"title": [{"text": {"content": series_title}}]},
        "Link": {"url": link},
        "Type": {"select": {"name": typo}},
        "Status": {"status": {"name": my_status}},
        "Score": {"select": {"name": my_score}},
        "Author": {"rich_text": [{"text": {"content": author}}]},
        "Completed": {"date": {"start": completed_date, "end": None}},
    }

    create_page(data)
