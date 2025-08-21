import json
import streamlit as st

from datetime import datetime
from collections import defaultdict

from data.arcs_data import StoryArcs
CHAPTERS_FILE = "./data/chapters.jsonl"
CHARACTERS_FILE = "./data/all_characters.json"

@st.cache_data
def load_chapters():
    with open(CHAPTERS_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

@st.cache_data
def load_characters():
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_character_list():
    return load_characters()

def get_total_chapters():
    return len(load_chapters())

def get_first_appearance(character: str):
    chapters = load_chapters()
    for ch in sorted(chapters, key=lambda c: int(c["chapter_number"])):
        if character in ch.get("characters", []):
            return ch
    return None

def get_last_appearance(character: str):
    chapters = load_chapters()
    for ch in sorted(chapters, key=lambda c: int(c["chapter_number"]), reverse=True):
        if character in ch.get("characters", []):
            return ch
    return None

def get_total_appearances(character: str):
    chapters = load_chapters()
    return sum(1 for ch in chapters if character in ch.get("characters", []))

def get_appearances_by_year(character: str):
    chapters = load_chapters()
    appearances = defaultdict(int)
    for ch in chapters:
        if character in ch.get("characters", []):
            if ch.get("date"):
                year = datetime.fromisoformat(ch["date"]).year
                appearances[year] += 1
    return dict(sorted(appearances.items()))

def get_coappearances(character: str, exclude=None):
    if exclude is None:
        exclude = []
    chapters = load_chapters()
    co_counts = defaultdict(int)
    for ch in chapters:
        if character in ch.get("characters", []):
            for co in ch.get("characters", []):
                if co != character and co not in exclude:
                    co_counts[co] += 1
    return dict(sorted(co_counts.items(), key=lambda x: -x[1]))



