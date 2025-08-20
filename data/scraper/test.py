import requests
from bs4 import BeautifulSoup

def get_html_structure ():
    url = "https://onepiece.fandom.com/wiki/Chapter_1"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    char_table = soup.find('table', class_="CharTable")

    print(char_table)

get_html_structure()



