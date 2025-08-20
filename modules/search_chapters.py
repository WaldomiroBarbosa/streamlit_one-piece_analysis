import requests
import streamlit as st

# Cache chapter count (update every 6 hours for example)
@st.cache_data(ttl=6*60*60)
def get_number_of_chapters ():
    response = requests.get("https://api.api-onepiece.com/v2/chapters/en", timeout=10)
    response.raise_for_status()
    chapters = response.json()
    return len(chapters)