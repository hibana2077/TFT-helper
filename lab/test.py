import streamlit as st
import pandas as pd

# 載入資料
@st.cache_data
def load_data():
    data = pd.read_csv('./tft.csv')
    return data

st.title("TFT Comps Data")

# 資料處理
meta_df = load_data()
units_split = meta_df['units_string'].str.split(',', expand=True)
cluster_id = meta_df['cluster_id']
combined_df = pd.concat([units_split, cluster_id], axis=1)

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