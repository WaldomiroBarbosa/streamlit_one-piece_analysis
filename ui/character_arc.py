import pandas as pd
import plotly.express as px
import streamlit as st

from modules.database_search import get_appearances_by_arc
from data.arcs_data import StoryArcs

def by_arc_stats (character: str):
    stats = get_appearances_by_arc(character)

    if not stats:
        st.info(f"No appearances found for {character}")
        return

    data = []
    for arc in StoryArcs:
        _, title, start, end = arc.value
        if end is None:  # arco em andamento
            continue
        total_chapters = end - start + 1
        count = stats.get(title, 0)
        density = count / total_chapters if total_chapters > 0 else 0
        if count > 0:
            data.append({
                "Arc": title,
                "Appearances": count,
                "Chapters": total_chapters,
                "Density": round(density, 3)  # aparições por capítulo
            })

    df = pd.DataFrame(data)

    most = df.loc[df["Appearances"].idxmax()]
    least = df.loc[df["Appearances"].idxmin()]
    densest = df.loc[df["Density"].idxmax()]
    avg_density = df["Density"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Most appearances", most["Arc"], f"{most['Appearances']} chapters")
    col2.metric("Least appearances", least["Arc"], f"{least['Appearances']} chapters")
    col3.metric("Highest density", densest["Arc"], f"{densest['Density']:.2f}")
    col4.metric("Avg density", f"{avg_density:.2f}")

    # gráfico comparando aparições absolutas
    fig1 = px.bar(
        df,
        x="Arc",
        y="Appearances",
        title=f"Total appearances of {character} by Arc",
        text="Appearances"
    )
    fig1.update_traces(textposition="outside")

    # gráfico comparando densidade
    fig2 = px.bar(
        df,
        x="Arc",
        y="Density",
        title=f"Density of appearances of {character} by Arc",
        text="Density"
    )
    fig2.update_traces(textposition="outside")

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

    # tabela
    st.dataframe(df, use_container_width=True)