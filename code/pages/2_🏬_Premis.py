import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
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
# def page2_content():
#     st.title("Page 1 Content")
#     st.write("This is the content for Page 1.")
    #@st.cache_data  # Use st.cache to cache the data-loading function
@st.cache_data  # Use st.cache to cache the data-loading function
def load_data():
    df = pd.read_parquet('D:/streamlit/pricecatch/df_price_final.parquet')
    df['Tarikh'] = pd.to_datetime(df['Tarikh'])
    df.sort_values(by='Tarikh', inplace=True)
    df['Tarikh'] = df['Tarikh'].dt.strftime('%Y-%m-%d')
    return df

# Load data using the cached function
df = load_data()

# Filters
negeri_filter_options = sorted(df['Negeri'].unique())
negeri_filter = st.selectbox("Pilih Negeri", negeri_filter_options)

# Update Daerah filter based on selected Negeri
daerah_options = sorted(df[df['Negeri'] == negeri_filter]['Daerah'].unique())
daerah_filter = st.selectbox("Pilih Daerah", daerah_options)

# Update Premis filter based on selected Negeri and Daerah
premis_options = sorted(df[(df['Negeri'] == negeri_filter) & (df['Daerah'] == daerah_filter)]['Premis'].unique())
premis_filter = st.multiselect("Pilih Premis", premis_options)

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
