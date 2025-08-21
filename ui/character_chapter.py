import streamlit as st

import pandas as pd
import plotly.express as px

from modules.database_search import get_first_appearance, get_last_appearance, get_all_appearances, get_total_chapters

def by_chapters(character: str):
    first = get_first_appearance(character)
    last = get_last_appearance(character)
    total = get_total_chapters()
    since = total - int(last.get("chapter_number"))
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="First Appearance",
            value=f"Ch. {first.get('chapter_number')}",
            help=f"{first.get('title')} ({first.get('date')})"
        )

    with col2:
        st.metric(
            label="Last Appearance",
            value=f"Ch. {last.get('chapter_number')}",
            help=f"{last.get('title')} ({last.get('date')})"
        )

    with col3:
        st.metric(
            label="Chapters Since",
            value=since
        )

    appearances = get_all_appearances(character)
    df = pd.DataFrame({"Chapter": appearances, "Appearance": [1]*len(appearances)})

    fig = px.scatter(df, x="Chapter", y="Appearance",
                    title="Appearances over time",
                    labels={"Appearance": ""})
    st.plotly_chart(fig, use_container_width=True)