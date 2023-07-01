import requests
from bs4 import BeautifulSoup

url = "https://myanimelist.net/anime/51009/Jujutsu_Kaisen_2nd_Season"

# Send an HTTP GET request to the MyAnimeList page
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the cover image element using its HTML class or ID
cover_image = soup.find("img", class_="ac")

# Extract the URL attribute of the cover image
image_url = cover_image["data-src"]

# Print the cover image URL
print(image_url)
