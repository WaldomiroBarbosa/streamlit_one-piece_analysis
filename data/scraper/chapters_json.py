import requests
import time
import json
import re

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
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


def extrair_texto(elemento, tag, atributos):
    if elemento:
        found = elemento.find(tag, atributos)
        return found.text.strip() if found else None
    return None

def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        pass

    pattern = r"^(?P<month>\w+)\s+(?P<day>\d{1,2}),\s+(?P<year>\d{4})$"
    match = re.match(pattern, date_str)
    if match:
        month_str = match.group("month")
        day = int(match.group("day"))
        year = int(match.group("year"))

        try:
            month = datetime.strptime(month_str, "%B").month
            return datetime(year, month, day)
        except ValueError:
            pass
    
    return None

def extract_chapter_data(chapter_url: str):
    
    try:
        response = session.get(chapter_url, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar {chapter_url}: {e}")
        return {}

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = extrair_texto(soup, 'h2', {'data-source': 'title'})

        data_element = soup.find('div', {'data-source': 'date2'})
        date_value = None
        if data_element:
            div_val = data_element.find('div', {'class': 'pi-data-value'})
            if div_val:
                # remove spans/sup que atrapalham
                for tag in div_val.find_all(['sup', 'span']):
                    tag.decompose()
                date_value = div_val.get_text(strip=True)

        date_format = parse_date(date_value) if date_value else None

        characters = []
        char_table = soup.find('table', class_="CharTable")
        if char_table:
            for ul in char_table.find_all('ul'):
                for li in ul.find_all('li'):
                    for a in li.find_all('a', href=True):
                        if a["href"].startswith("/wiki/"):
                            raw_name = a["href"].replace("/wiki/", "").replace("_", " ")

                            if "%" in raw_name:
                                name = unquote(raw_name)
                            else:
                                name = raw_name

                            # Verificar no <li> inteiro se tem "(cover)"
                            li_text = li.get_text(" ", strip=True).lower()
                            if "(cover)" in li_text:
                                name += " (cover)"

                            characters.append(name)

        return {
            'title': title,
            'date': date_format,
            'characters': characters
        }

    except Exception as e:
        print(f"❌ Erro ao processar HTML de {chapter_url}: {e}")
        return {}

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
                current_url = f"one piece wiki{next_link['href']}"
                print(f"Coletados: {len(chapter_urls)} capítulos", end="\r")
            else:
                break
        except Exception as e:
            print(f"❌ Erro ao processar {current_url}: {e}")
            break

    print(f"\n✅ Total de capítulos coletados: {len(chapter_urls)}")
    return chapter_urls

def load_database():
    with open("one_piece_chapters_1755749489.jsonl", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]
    
def create_json_file():
    start_url = "one piece wiki"
    url_list = get_all_chapters_url(start_url)

    json_filename = f"one_piece_chapters_{int(time.time())}.jsonl"

    with open(json_filename, "w", encoding="utf-8") as f:
        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = {
                executor.submit(extract_chapter_data, url): (i, url)
                for i, url in enumerate(url_list, start=1)
            }

            for future in as_completed(futures):
                i, url = futures[future]
                try:
                    data = future.result() or {}
                    characters = data.get("characters", [])
                    # remover duplicatas mantendo ordem
                    characters = list(dict.fromkeys(characters))
                    chapter_data = {
                        "chapter_number": str(i),
                        "chapter_url": url,
                        "title": data.get("title"),
                        "date": data.get("date").strftime("%Y-%m-%d") if data.get("date") else None,
                        "characters": characters
                    }
                    f.write(json.dumps(chapter_data, ensure_ascii=False) + "\n")
                    f.flush()

                    print(f"✅ Capítulo {i} processado ({i}/{len(url_list)})", end="\r")
                except Exception as e:
                    print(f"\n❌ Erro no capítulo {i}: {e}")

    print(f"\n🎉 Concluído! Dados salvos em {json_filename}")

if __name__ == "__main__":
    create_json_file()