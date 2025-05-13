import streamlit as st
import pandas as pd
import warnings

from cfg.url import (
    SHARE_LINK
)

from utils.data import (
    get_comp_details,
    get_comps_data,
    get_comps_stats,
    get_unit_items_processed,
    get_tft_version
)

from comp.card import comp_card

# ignore FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ignore UserWarning
warnings.simplefilter(action='ignore', category=UserWarning)

# Load data
@st.cache_data
def load_data():
    data = get_comps_data()
    new_data = []
    for key, value in data['results']['data']['cluster_details'].items():
        tags_for_link = '-'.join([tag['name'] for tag in value['name']])
        tags_for_name = ' '.join([tag['name'] for tag in value['name']])
        new_data.append({
            'cluster_index': key,
            'units_string': value['units_string'],
            'traits_string': value['traits_string'],
            'name': SHARE_LINK.format(tag=tags_for_link),
            'tag': tags_for_name,
            'name_string': value['name_string'],
        })
    return pd.DataFrame(new_data)

tft_version = get_tft_version()


st.title("TFT Comps Data")
st.info(f"Current TFT Version: {tft_version}")
# Data processing
meta_df = load_data()
units_split = meta_df['units_string'].str.split(',', expand=True)
cluster_id = meta_df['cluster_index']
share_link = meta_df['name']
tags = meta_df['tag']
combined_df = pd.concat([units_split, cluster_id, share_link, tags], axis=1)

# Create character menu options (all non-empty character names)
all_units_raw = pd.unique(units_split.values.ravel())
all_units = sorted(set(unit.strip() for unit in all_units_raw if pd.notna(unit)))

# Multiple keyword input
query = st.multiselect("Enter multiple character names (separated by comma)", all_units)

# Filter logic
if query:
    keywords = [kw.strip().lower() for kw in query]

    # Check if any column contains any keyword
    filtered_df = combined_df[combined_df.apply(
        lambda row: all(any(kw in str(cell).lower() for cell in row[:-1]) for kw in keywords), axis=1
    )]
else:
    filtered_df = combined_df

# Display results
# st.dataframe(filtered_df)
for index, row in filtered_df.iterrows():
    comp_card(row, tft_version)