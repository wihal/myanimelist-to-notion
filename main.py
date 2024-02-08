import lxml.etree as ET
import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import sys
import os
import threading
from config import *

LOG_FILE_NAME = "error_log.txt"

def get_file_path(file_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    file_path = os.path.join(base_path, file_path)
    
    if os.path.exists(file_path) and os.path.isfile(file_path) and file_path.lower().endswith('.xml'):
        try:
            print("XML file found:", file_path)
            ET.parse(file_path)
            return file_path
        except ET.ParseError:
            print("XML file is not valid. Please enter a valid path.")
    else:
        print("Please enter a valid XML file path.")

def add_item_to_notion(DATABASE_ID: str, headers: dict, image_url: str, data: dict, series_title: str):
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

        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)

        if res.status_code != 200:
            print("Failed to add item.")

        if None == image_url:
            return

        cover_properties = {
            "cover": {
                "external": {
                    "url": image_url
                }
            }
        }
        response_cover = requests.patch(f"https://api.notion.com/v1/pages/{res.json().get('id')}", headers=headers, json=cover_properties)
            
        if response_cover.status_code != 200: 
            print(f"Failed to update cover image for {series_title}.")
            return
        print(series_title + " added to your database!")
        

def main():
    file_path, database_id, notion_token = get_file_path(FILE_PATH), DATABASE_ID, NOTION_TOKEN

    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    root = ET.parse(file_path).getroot()


    completed_date = datetime.now().astimezone(timezone.utc).isoformat()

    new_count = 0

    if root.findall('.//anime'):
        for anime_elem in root.findall('.//anime'):
            
            print(f"Processing {new_count} of {len(root.findall('.//anime'))}...")

            series_title = anime_elem.find('series_title').text

            link = f"https://myanimelist.net/anime/{anime_elem.find('series_animedb_id').text}"

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

            try:
                my_status = anime_elem.find('my_status').text
                if my_status == 'Completed':
                    my_status = 'Done'
                elif my_status == 'Plan to Watch':
                    my_status = 'Not started'
            except:
                my_status = 'TBD'

            image_url = BeautifulSoup(requests.get(link).text, "html.parser").find("img", class_="ac")["data-src"]

            data = {
                "Name": {"title": [{"text": {"content": series_title}}]},
                "Link": {"url": link},
                "Status": {"select": {"name": my_status}},
                "Score": {"select": {"name": my_score}},
                "Completed": {"date": {"start": completed_date, "end": None}},
            }
            new_count += 1
            threading.Thread(target=add_item_to_notion, args=(database_id, headers, image_url, data, series_title)).start()
    
    else:
        for manga_elem in root.findall('.//manga'):

            print(f"Processing {new_count} of {len(root.findall('.//anime'))}...")

            link = f"https://myanimelist.net/manga/{manga_elem.find('manga_mangadb_id').text}"

            series_title = manga_elem.find('manga_title').text

            my_score = manga_elem.find('my_score').text
            
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

            try:
                my_status = anime_elem.find('my_status').text
                if my_status == 'Completed':
                    my_status = 'Done'
                elif my_status == 'Plan to Watch':
                    my_status = 'Not started'
            except:
                my_status = 'TBD'
            
            image_url = BeautifulSoup(requests.get(link).text, "html.parser").find("img", class_="ac")["data-src"]

            data = {
                "Name": {"title": [{"text": {"content": series_title}}]},
                "Link": {"url": link},
                "Status": {"select": {"name": my_status}},
                "Score": {"select": {"name": my_score}},
                "Completed": {"date": {"start": completed_date, "end": None}},
            }

            new_count += 1
            threading.Thread(target=add_item_to_notion, args=(database_id, headers, image_url, data, series_title)).start()
    
if __name__ == '__main__':
    main()