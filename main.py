import streamlit as st

from streamlit_searchbox import st_searchbox
from modules.database_search import get_character_list
from ui.character_stats import print_character_stats


st.write("# ONE PIECE MANGA characters stats")
st.write("Discover your favorite **ONE PIECE** character appearance statistics.")

value = st_searchbox(
    get_character_list,
    placeholder="Search any character... ",
    key="my_key",
)

if value:
    print_character_stats(value)
