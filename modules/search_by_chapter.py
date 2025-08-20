import json
import streamlit as st

@st.cache_data
def load_database():
    with open("./data/one_piece_chapters_1755726590.jsonl", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def character_appearances(character: str) -> int:
    database = load_database()
    n_of_appearances = 0
    for data in database:
        if character in set(data.get("characters", [])):
            n_of_appearances += 1
    return n_of_appearances
