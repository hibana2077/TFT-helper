import streamlit as st
import pandas as pd
import requests

CHAMPIONS_IMG_URL = "https://cdn.metatft.com/file/metatft/champions/{hero_name}.png"
ITEM_IMG_URL = "https://cdn.metatft.com/file/metatft/items/{item_name}.png"

@st.cache_data
def fetch_image_data(image_url):
    """Fetches image data from a URL and caches it."""
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.content

def comp_card(
       row,
       tft_version,
    ):
    card = st.container(border=True, key=row['cluster_index'])
    card_title = row['tag'].replace(f"{tft_version}_","")
    card.markdown(f"## [{card_title}]({row['name']})")
    cols = card.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for i, unit in enumerate(row[:-3]):
        if pd.notna(unit):
            unit = unit.strip().lower()
            image_url = CHAMPIONS_IMG_URL.format(hero_name=unit)
            try:
                image_data = fetch_image_data(image_url)
                cols[i].image(image_data, width=40)
            except Exception as e:
                print(f"Error loading image for {unit} from {image_url}: {e}, i={i}")