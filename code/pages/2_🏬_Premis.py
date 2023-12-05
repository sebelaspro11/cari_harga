import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # URLs for data
    URL_DATA_premise = 'https://storage.data.gov.my/pricecatcher/lookup_premise.parquet'
    URL_DATA_item = 'https://storage.data.gov.my/pricecatcher/lookup_item.parquet'
    URL_DATA_price = 'https://storage.data.gov.my/pricecatcher/pricecatcher_2023-12.parquet'

    # Load premise data
    df_premise = pd.read_parquet(URL_DATA_premise)
    if 'date' in df_premise.columns:
        df_premise['date'] = pd.to_datetime(df_premise['date'])
    df_premise.drop(index=0, inplace=True)

    # Load item data
    df_item = pd.read_parquet(URL_DATA_item)
    if 'date' in df_item.columns:
        df_item['date'] = pd.to_datetime(df_item['date'])
    df_item.drop(index=0, inplace=True)

    # Load price data for November
    df_price_nov = pd.read_parquet(URL_DATA_price)
    if 'date' in df_price_nov.columns:
        df_price_nov['date'] = pd.to_datetime(df_price_nov['date'])

    # Merge premise and price datasets
    df_price_premise = pd.merge(df_price_nov, df_premise, left_on="premise_code", right_on="premise_code")

    # Merge item data with the merged premise and price dataset
    df_price_final = pd.merge(df_price_premise, df_item, left_on="item_code", right_on="item_code")

    # Select relevant columns
    df_price_final = df_price_final[['date', 'price', 'premise', 'address', 'premise_type', 'state', 'district', 'item', 'unit', 'item_group', 'item_category']]

    # Rename columns
    new_names = {
        "date": "Tarikh",
        "price": "Harga (RM)",
        "premise": "Premis",
        "address": "Alamat",
        "premise_type": "Jenis Premis",
        "item": "Item",
        "state": "Negeri",
        "district": "Daerah",
        "unit": "Unit",
        "item_group": "Kumpulan Item",
        "item_category": "Kategori Item"
    }

    df_price_final = df_price_final.rename(columns=new_names)

    return df_price_final

# Usage
df = load_data()

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.markdown(
   ' #### Pilih Negeri, Daerah dan Nama Premis untuk melihat senarai Item dan Harga'
)


# Filters
negeri_filter_options = sorted(df['Negeri'].unique())
negeri_filter = st.selectbox("Pilih Negeri", negeri_filter_options)

# Update Daerah filter based on selected Negeri
daerah_options = sorted(df[df['Negeri'] == negeri_filter]['Daerah'].unique())
daerah_filter = st.selectbox("Pilih Daerah", daerah_options)

# Update Premis filter based on selected Negeri and Daerah
premis_options = sorted(df[(df['Negeri'] == negeri_filter) & (df['Daerah'] == daerah_filter)]['Premis'].unique())
premis_filter = st.selectbox("Pilih Premis", premis_options)

# Apply filters
filtered_df = df[
    (df['Negeri'] == negeri_filter) &
    (df['Daerah'] == daerah_filter) &
    (df['Premis'] == premis_filter)
]


# Display filtered DataFrame
if not filtered_df.empty:
    #st.dataframe(filtered_df)

    # Show only the latest Tarikh for each unique combination of Item, Unit, and Harga
    latest_date_df = filtered_df.sort_values(by='Tarikh', ascending=False).drop_duplicates(subset=['Premis', 'Item'])
    latest_date_df = latest_date_df.reset_index(drop=True)
    latest_date_df.index += 1
    latest_date_df['Harga (RM)'] = latest_date_df['Harga (RM)'].map('{:.2f}'.format)
    alamat = latest_date_df.iloc[0]['Alamat'] 

    # Calculate the total number of items available
    total_items = len(latest_date_df)

    # Show available items based on Premis with the latest Tarikh
    st.markdown("---")
    st.markdown('### Alamat')
    st.write(alamat)
    st.markdown('### Jumlah Item')
    st.write(f'<div style="font-weight: bold; font-size: 20px;">{total_items}</div>', unsafe_allow_html=True)
    # Add a gap between "Pilih Item" filter and st.dataframe
    st.markdown("---")
    st.markdown("### Senarai Item yang tersedia:")
    st.dataframe(latest_date_df[['Tarikh', 'Kategori Item', 'Item', 'Unit', 'Harga (RM)', 'Jenis Premis']], width=1500)
    
else:
    st.warning("No data available for the selected filters.")
