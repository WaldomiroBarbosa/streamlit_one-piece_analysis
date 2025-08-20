import streamlit as st

from modules.search_by_chapter import character_appearances
from modules.search_chapters import get_number_of_chapters

def arc_stats (character: str):
    

def print_character_stats(character: str):
    # get number of chapters where the character appears
    n_of_appearances = character_appearances(character) or 0
    n_of_chapters = get_number_of_chapters() or 1  # prevent division by zero

    percentage = (n_of_appearances / n_of_chapters) * 100

    st.write(
        f"**{character}** appears in **{n_of_appearances}** chapters"
        f"of the **ONE PIECE** manga. That's **{percentage:.2f}%** of the series!"
    )