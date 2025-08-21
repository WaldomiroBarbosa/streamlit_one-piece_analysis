import pandas as pd
import plotly.express as px
import streamlit as st

from modules.database_search import get_appearances_by_year

def by_year_stats (character: str):
    mode = st.radio("Group by:", ["Year", "Decade"], horizontal=True)

    stats = get_appearances_by_year(character, mode.lower())

    if stats:
        df = pd.DataFrame(list(stats.items()), columns=[mode, "Appearances"])

        # resumo
        most = df.loc[df["Appearances"].idxmax()]
        least = df.loc[df["Appearances"].idxmin()]
        avg = df["Appearances"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric(f"Most {mode.lower()}", most[mode], f"{most['Appearances']} chapters")
        col2.metric(f"Least {mode.lower()}", least[mode], f"{least['Appearances']} chapters")
        col3.metric("Average", f"{avg:.1f}")

        # gráfico
        fig = px.bar(df, x=mode, y="Appearances", title=f"Appearances of {character} per {mode.lower()}")
        st.plotly_chart(fig, use_container_width=True)
