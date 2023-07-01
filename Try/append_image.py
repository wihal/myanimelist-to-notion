import requests

NOTION_TOKEN = "SECRET_TOKEN_HERE"
DATABASE_ID = "DB_ID_HERE"
BLOCK_ID = "BLOCK_ID_HERE"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",

}

url = "https://api.notion.com/v1/blocks/" + BLOCK_ID + "/children"

data = {
    "children": [
        {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": "https://cdn.myanimelist.net/images/anime/1107/136174.jpg"
                }
            }
        }

    ]
}

response = requests.patch(url, headers=headers, json=data)

print(response.text)
