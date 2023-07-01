import requests
from bs4 import BeautifulSoup

NOTION_TOKEN = "SECRET_TOKEN_HERE"
DATABASE_ID = "DB_ID_HERE"

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json"
}

response = requests.post(url, headers=headers)
data = response.json()

# Iterate over each item in the database
for item in data["results"]:
    properties = item["properties"]

    # Assuming the link property is named "Link", extract its value
    link = properties["Link"]["url"]

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    cover_image = soup.find("img", class_="ac")
    image_url = cover_image["data-src"]

    print(properties)
    print(link)
    print(image_url)
