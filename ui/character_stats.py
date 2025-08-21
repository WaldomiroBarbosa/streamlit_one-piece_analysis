import streamlit as st

from modules.database_search import get_total_chapters, get_total_appearances, get_first_appearance, get_last_appearance
from ui.character_chapter import by_chapters
from ui.character_year import by_year_stats
from ui.character_arc import by_arc_stats

def print_character_stats(character: str):
    # get number of chapters where the character appears
    n_appearances = get_total_appearances(character) or 0
    n_chapters = get_total_chapters() or 1  # prevent division by zero

    percentage = (n_appearances / n_chapters) * 100

    st.write(
        f"**{character}** appears in **{n_appearances}** chapters "
        f"of the **ONE PIECE** manga. That's **{percentage:.2f}%** of the series!"
    )

    st.write("# BY CHAPTER")
    by_chapters(character)
    st.write("# BY YEAR")
    by_year_stats(character)
    st.write("# BY ARC")
    by_arc_stats(character)