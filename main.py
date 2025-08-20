import streamlit as st

from streamlit_searchbox import st_searchbox
from modules.search_characters import search_term
from ui.character_stats import print_character_stats


st.write("# ONE PIECE MANGA characters stats")
st.write("Discover your favorite **ONE PIECE** character appearance statistics.")

value = st_searchbox(
    search_term,
    placeholder="Search any character... ",
    key="my_key",
)

if value:
    print_character_stats(value)
