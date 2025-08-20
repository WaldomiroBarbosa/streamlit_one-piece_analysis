import requests
import time
import json

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

retry_strategy = Retry(
    total=5,                 # tries
    backoff_factor=1,        # time for 1 try, exponential
    status_forcelist=[403, 429, 500, 502, 503, 504], # force in status
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


def get_characters_in_chapter(chapter_url: str):
    try:
        response = session.get(chapter_url, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar {chapter_url}: {e}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        char_table = soup.find('table', class_="CharTable")
        if not char_table:
            return []
        
        characters = []
        for ul in char_table.find_all('ul'):
            for li in ul.find_all('li'):
                for a in li.find_all('a', href=True):
                    href = a["href"]
                    if href.startswith("/wiki/"):
                        name = href.replace("/wiki/", "").replace("_", " ")
                        characters.append(name)
        return characters
    except Exception as e:
        print(f"❌ Erro ao processar HTML de {chapter_url}: {e}")
        return []

def get_all_chapters_url(start_url: str):
    current_url = start_url
    chapter_urls = []

    while current_url:
        try:
            time.sleep(1)
            response = session.get(current_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            chapter_urls.append(current_url)

            next_link = soup.find('a', string='Next Chapter')
            if next_link and 'href' in next_link.attrs:
                current_url = f"https://onepiece.fandom.com{next_link['href']}"
                print(f"Coletados: {len(chapter_urls)} capítulos", end="\r")
            else:
                break
        except Exception as e:
            print(f"❌ Erro ao processar {current_url}: {e}")
            break

    print(f"\n✅ Total de capítulos coletados: {len(chapter_urls)}")
    return chapter_urls

def create_json_file():
    start_url = "https://onepiece.fandom.com/wiki/Chapter_1"
    url_list = get_all_chapters_url(start_url)

    json_filename = f"one_piece_chapters_{int(time.time())}.jsonl"

    with open(json_filename, "w", encoding="utf-8") as f:
        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = {
                executor.submit(get_characters_in_chapter, url): (i, url)
                for i, url in enumerate(url_list, start=1)
            }

            for future in as_completed(futures):
                i, url = futures[future]
                try:
                    characters = future.result()
                    chapter_data = {
                        "chapter_number": str(i),
                        "chapter_url": url,
                        "characters": characters if characters else []
                    }
                    f.write(json.dumps(chapter_data, ensure_ascii=False) + "\n")
                    f.flush()

                    print(f"✅ Capítulo {i} processado ({i}/{len(url_list)})", end="\r")
                except Exception as e:
                    print(f"\n❌ Erro no capítulo {i}: {e}")

    print(f"\n🎉 Concluído! Dados salvos em {json_filename}")

if __name__ == "__main__":
    create_json_file()