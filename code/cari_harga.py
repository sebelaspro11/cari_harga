import streamlit as st

st.set_page_config(
    page_title="Cari Harga",
    page_icon="💰",
)

st.write("# Selamat Datang ke C Harga! 👋")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Web Aplikasi ini bertujuan untuk memudahkan pengguna membuat perbandingan harga kepada barangan-barangan asas dan keperluan harian.\n
    Data akan dikemaskini setiap hari bergantung kepada data daripada 
    Kementerian Perdagangan Dalam Negeri Dan Kos Sara Hidup (KPDN).
    
    ### 🛒 Item
    - Pilih dan bandingkan harga item di premis-premis di negeri dan daerah anda
    
     ### 🏬 Premis
    - Pilih Premis yang berdaftar dengan KPDN untuk melihat item-item dan harga.
    
    ### Sumber Data
    - [data.gov.my](https://data.gov.my/data-catalogue)
"""
)

st.header(":mailbox: Maklum Balas!")
st.markdown('##### ***:keyboard: Komen dan Cadangan anda untuk sebarang penambahbaikan amat dihargai***')


contact_form = """
    <form action="https://formsubmit.co/sebelaspro11@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Nama" required>
        <input type="email" name="email" placeholder="Email (Optional)">
        <textarea name="message" placeholder="Komen/Cadangan" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("css/style.css")
