import requests

def get_sagas ():
    response = requests.get("https://api.api-onepiece.com/v2/sagas/en")
    sagas = response.json()

    for saga in sagas:
        print(saga)

def get_chapters ():
    response = requests.get("https://api.api-onepiece.com/v2/chapters/en")
    chapters = response.json()
    
    for chapter in chapters:
        print(chapter)

def get_characters ():
    response = requests.get("https://api.api-onepiece.com/v2/characters/en")
    characters = response.json()

    return len(characters)

print(get_characters())