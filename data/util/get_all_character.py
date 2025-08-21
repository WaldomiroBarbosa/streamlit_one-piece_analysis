import json

with open("../onepiece_data.jsonl", "r", encoding="utf-8") as f:
    database = [json.loads(line) for line in f]

def create_json_file():
    all_characters = set()
    
    for data in database:
        character_list = data.get("characters", [])
        # remove todos que tenham "(cover)" no nome
        clean_list = [c for c in character_list if "(cover)" not in c]
        all_characters.update(clean_list)
    
    all_characters_list = sorted(all_characters)

    with open("../all_characters.json", "w", encoding="utf-8") as json_file:
        json.dump(all_characters_list, json_file, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo salvo com {len(all_characters_list)} personagens únicos.")

if __name__ == "__main__":
    create_json_file()