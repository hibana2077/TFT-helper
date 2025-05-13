import streamlit as st
import pandas as pd
from cfg.url import (
    SHARE_LINK
)
from utils.data import (
    get_comp_details,
    get_comps_data,
    get_comps_stats,
    get_unit_items_processed,
)

# 載入資料
@st.cache_data
def load_data():
    data = get_comps_data()
    new_data = []
    for key, value in data['results']['data']['cluster_details'].items():
        new_data.append({
            'cluster_index': key,
            'units_string': value['units_string'],
            'traits_string': value['traits_string'],
            'name': SHARE_LINK.format(tag=f"{value['name'][0]['name']}-{value['name'][1]['name']}"),
            'name_string': value['name_string'],
        })
    return pd.DataFrame(new_data)

st.title("TFT Comps Data")

# 資料處理
meta_df = load_data()
units_split = meta_df['units_string'].str.split(',', expand=True)
cluster_id = meta_df['cluster_index']
share_link = meta_df['name']
combined_df = pd.concat([units_split, cluster_id, share_link], axis=1)

# 建立角色選單選項（所有非空角色名稱）
all_units_raw = pd.unique(units_split.values.ravel())
all_units = sorted(set(unit.strip() for unit in all_units_raw if pd.notna(unit)))

# 多關鍵字輸入
query = st.multiselect("輸入多個角色名稱（以逗號分隔）", all_units)

# 篩選邏輯
if query:
    keywords = [kw.strip().lower() for kw in query]

    # 檢查任一欄位是否包含任一關鍵字
    filtered_df = combined_df[combined_df.apply(
        lambda row: all(any(kw in str(cell).lower() for cell in row[:-1]) for kw in keywords), axis=1
    )]
else:
    filtered_df = combined_df

# 顯示結果
st.dataframe(filtered_df)