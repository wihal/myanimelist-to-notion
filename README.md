**Documentation/README**

### Introduction
This program is designed to automate the process of adding anime or manga entries from an XML file exported from MyAnimeList to a Notion database. It utilizes the MyAnimeList API to fetch information about anime or manga and then adds this information to a Notion database using the Notion API.

### Prerequisites
- Python 3.x installed on your system
- A MyAnimeList account with an XML file exported from your profile
- A Notion account with access to the database where you want to add the entries
- Generate a Notion integration token from [here](https://www.notion.so/my-integrations)

### Installation
1. Clone or download the repository to your local machine.
2. Install the required Python packages by running the following command:
   ```
   pip install -r requirements.txt
   ```

### Configuration
Before running the program, you need to configure the `config.py` file with your specific details:
- `DATABASE_ID`: The ID of the Notion database where you want to add the entries. You can find it in the URL of your Notion database.
- `NOTION_TOKEN`: Your Notion integration token generated from the Notion website.
- `FILE_PATH`: Path to the XML file exported from MyAnimeList.

### Usage
Once the configuration is done, you can run the program using the following command:
```
python main.py
```

### How It Works
1. The program reads the XML file containing anime or manga entries exported from MyAnimeList.
2. It extracts relevant information such as series title, link, score, and status from each entry.
3. For each entry, it fetches the cover image URL from MyAnimeList website.
4. It then constructs a data payload and sends a request to Notion API to add the entry to the specified database.
5. Concurrent threads are used to speed up the process of adding entries.

### Notes
- If the script stops working, it might be due to rate-limiting from the MyAnimeList or Notion API.
- Ensure that your integration has access to the specified Notion database.
- The program assumes that the XML file contains entries for either anime or manga, not both simultaneously.

### Example
An example of the configuration in `config.py`:
```python
# Configuration file

# Edit the following values to match your database and token.
# After that you can run the script with `python main.py`

# If the scrips stops workig it could be that you are being rate-limited.


# You can find your database ID in the search field in the browser
# https://notion.site/${DATABASE_ID}?v=********            
DATABASE_ID = "12345678-abcd-1234-abcd-1234567890ab"

# Make sure that the integration has access to the database. 
# Generate your token here: https://www.notion.so/my-integrations
NOTION_TOKEN = "my-secret-notion-token"

# Path to the XML file you can export the file from https://myanimelist.net/panel.php?go=export
FILE_PATH = "myanimelist_export.xml"
```

### Additional Information
- For more information about the Notion API, refer to the [official documentation](https://developers.notion.com/).
- For more information about the MyAnimeList API, refer to the [official documentation](https://myanimelist.net/apiconfig/references/api/v2).


### License
This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.