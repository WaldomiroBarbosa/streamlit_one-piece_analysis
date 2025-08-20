import json
import streamlit as st

with open("./data/all_characters.json", "r", encoding="utf-8") as f:
    database = json.load(f) 

@st.cache_data
def get_characters_list():
    return database

def search_term(query: str):
    characters = get_characters_list()
    if not query:
        return []
    return [c for c in characters if query.lower() in c.lower()][:20]