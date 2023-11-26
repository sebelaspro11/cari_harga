import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
from datetime import datetime

st.set_page_config(layout="wide")

@st.cache_data  # Use st.cache to cache the data-loading function
def load_data():
    df = pd.read_parquet('data/df_price_final.parquet')
    df['Tarikh'] = pd.to_datetime(df['Tarikh'])
    df.sort_values(by='Tarikh', inplace=True)
    df['Tarikh'] = df['Tarikh'].dt.strftime('%Y-%m-%d')
    return df

def get_current_month():
    now = datetime.now()
    return calendar.month_name[now.month]

# Load data using the cached function
df = load_data()

# Filters
negeri_filter_options = sorted(df['Negeri'].unique())  # Sort the unique negeri values
negeri_filter = st.selectbox("Pilih Negeri", negeri_filter_options)

# Update Daerah filter based on selected Negeri
daerah_options = sorted(df[df['Negeri'] == negeri_filter]['Daerah'].unique())  # Sort the unique daerah values
daerah_filter = st.selectbox("Pilih Daerah", daerah_options)

# Update Kategori Item filter based on selected Negeri and Daerah
kategori_item_options = sorted(df[(df['Negeri'] == negeri_filter) & (df['Daerah'] == daerah_filter)]['Kategori Item'].unique())  # Sort the unique kategori item values
kategori_item_filter = st.selectbox("Pilih Kategori Item", kategori_item_options)

# Update available items based on selected Kategori Item
available_items = sorted(df[(df['Negeri'] == negeri_filter) & (df['Daerah'] == daerah_filter) & (df['Kategori Item'] == kategori_item_filter)]['Item'].unique())  # Sort the unique item values
item_filter = st.multiselect("Pilih Item", available_items)

# Apply filters
filtered_df = df[
    (df['Negeri'] == negeri_filter) &
    (df['Daerah'] == daerah_filter) &
    (df['Kategori Item'] == kategori_item_filter) &
    (df['Item'].isin(item_filter))
]



# Find the latest date for each Premis
latest_date_df = filtered_df.sort_values(by='Tarikh', ascending=False).drop_duplicates(subset=['Premis', 'Item'])
latest_date_df = latest_date_df.reset_index(drop=True)
latest_date_df.index += 1
# Format 'Harga' column to display two decimal places
latest_date_df['Harga (RM)'] = latest_date_df['Harga (RM)'].map('{:.2f}'.format)

# Add a gap between "Pilih Item" filter and st.dataframe
st.markdown("---")

# Display filtered DataFrame
if not latest_date_df.empty:
    st.dataframe(latest_date_df)

# Create bar chart for selected items
for selected_item in item_filter:
    item_data = latest_date_df[latest_date_df['Item'] == selected_item]

    # Get unique premises for the selected item
    selected_premises = item_data['Premis'].unique()

    # Get current month name
    current_month = get_current_month()
    
    # Get the latest date for the selected item
    latest_date = item_data.iloc[0]['Tarikh']
    unit = item_data.iloc[0]['Unit'] 

    # Plotly Express Bar Chart
    if not item_data.empty:
        # Sort the DataFrame based on 'Harga (RM)' column
        item_data_sorted = item_data.sort_values(by='Harga (RM)')

        fig_bar = px.bar(
            item_data_sorted,
            x='Premis',
            y='Harga (RM)',
            labels={'Item': 'Item', 'Tarikh': 'Tarikh', 'Harga (RM)': 'Harga (RM)', 'Unit': 'Unit', 'Premis': 'Premis'},
            title=f'Harga Semasa {unit} {selected_item} [{latest_date}]',
            text='Harga (RM)',
            hover_data={'Item': True, 'Tarikh': True, 'Harga (RM)': ':.2f', 'Unit': True, 'Premis': True}
        )

        # Manually set the order of x-axis based on sorted DataFrame
        fig_bar.update_xaxes(categoryorder='array', categoryarray=item_data_sorted['Premis'].tolist())

        st.plotly_chart(fig_bar, use_container_width=True)
        # Plotly Express Line Chart with the same set of Premis names
        fig_line = px.line(
            filtered_df[(filtered_df['Item'] == selected_item) & (filtered_df['Premis'].isin(selected_premises))],
            x='Tarikh',
            y='Harga (RM)',
            color='Premis',
            labels={'Item': 'Item', 'Tarikh': 'Tarikh', 'Harga (RM)': 'Harga (RM)', 'Unit': 'Unit', 'Premis': 'Premis'},
            title=f'Perubahan Harga Bagi {unit} {selected_item} Pada Bulan {current_month}',
            hover_data={'Item': True, 'Tarikh': True, 'Harga (RM)': ':.2f', 'Unit': True, 'Premis': True}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning(f"No data available for {selected_item}.")
            

