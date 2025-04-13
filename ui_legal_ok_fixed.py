import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
from PIL import Image

# Data user login (username dan password)
valid_users = {
    "admin": "password123",  # Username: admin, Password: password123
    "legal": "legalpass"     # Username: legal, Password: legalpass
}

# Halaman Login
def login():
    st.title("Login ke Aplikasi Legal Ticketing")

    # Tampilkan Logo Starcom
    logo = Image.open("starcom_logo.png")  # Pastikan file logo ada di direktori yang sesuai
    st.image(logo, width=180)  # Ganti dengan ukuran yang sesuai

    # Masukkan username dan password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in valid_users and valid_users[username] == password:
            # Simpan status login di session_state
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["login_error"] = False  # Reset error flag
            st.success("Login berhasil!")
        else:
            st.session_state["login_error"] = True
            st.error("Username atau password salah. Coba lagi!")

# Cek apakah sudah login
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()  # Kalau belum login, tampilkan halaman login
else:
    # Kalau sudah login, tampilkan dashboard aplikasi
    # Load daftar karyawan dari file Excel
    karyawan_list = ["-"]
    if os.path.exists("karyawan.xlsx"):
        df_karyawan = pd.read_excel("karyawan.xlsx")
        if "Nama" in df_karyawan.columns:
            karyawan_list += df_karyawan["Nama"].dropna().unique().tolist()

    FILE_PATH = "LEGAL_2024_updated.xlsx"
    st.set_page_config(page_title="Legal Officer Ticketing", layout="wide")

    # Custom styling
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .stMetric {
                text-align: center;
                font-size: 1.2rem;
            }
            .highlight-card {
                padding: 12px;
                background-color: #f1f3f6;
                border-radius: 10px;
                border-left: 5px solid #6c63ff;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo & Judul
    logo = Image.open("logo.png")
    st.image(logo, width=180)
    st.title("📋 Legal Officer Ticketing System")

    # Load Data
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
    else:
        df = pd.DataFrame(columns=[
            "Divisi", "Bulan", "Kode Dokumen", "Nomor Tiket", "Deskripsi", "PIC",
            "Kategori", "Nilai", "Status", "Tanggal Input", "Tanggal Update", "Due Date", "Assign To", "Dokumen Upload"
        ])

    # Edit Mode
    edit_index = st.session_state.get("edit_index", None)
    if edit_index is not None:
        st.markdown("## ✏️ Edit Tiket")
        row = df.iloc[edit_index]
        with st.form("form_edit"):
            divisi = st.selectbox("Divisi", ['HR', 'GA', 'Legal', 'Finance', 'Marketing', 'Sales', 'Prodev', 'Ops', 'Other'], index=['HR', 'GA', 'Legal', 'Finance', 'Marketing', 'Sales', 'Prodev', 'Ops', 'Other'].index(row["Divisi"]))
            bulan = st.selectbox("Bulan", ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'], index=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'].index(row["Bulan"]) if row["Bulan"] in ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'] else 0)
            kode_dok = st.text_input("Kode Dokumen", value=row["Kode Dokumen"])
            nomor = st.text_input("Nomor Tiket", value=row["Nomor Tiket"])
            desk = st.text_area("Deskripsi", value=row["Deskripsi"])
            pic = st.text_input("PIC", value=row["PIC"])
            kategori = st.selectbox("Kategori", ["PERIJINAN", "KONTRAK", "LITIGASI", "LAINNYA"], index=["PERIJINAN", "KONTRAK", "LITIGASI", "LAINNYA"].index(row["Kategori"]))
            nilai = st.number_input("Nilai", min_value=0.0, value=float(row["Nilai"]))
            status = st.selectbox("Status", ["Proses", "Progress", "Info", "Closed"], index=["Proses", "Progress", "Info", "Closed"].index(row["Status"]))
            due_date = st.date_input("Tanggal Due Date", value=pd.to_datetime(row["Due Date"]).date())
            assign_to = st.selectbox("Assign ke", ["-", "Legal 1", "Legal 2", "Legal 3"], index=["-", "Legal 1", "Legal 2", "Legal 3"].index(str(row["Assign To"])))
            submit_edit = st.form_submit_button("Simpan Perubahan")

            if submit_edit:
                df.loc[edit_index] = [
                    divisi, bulan, kode_dok, nomor, desk, pic,
                    kategori, nilai, status, row["Tanggal Input"],
                    datetime.today().date(), due_date, assign_to, row["Dokumen Upload"]
                ]
                df.to_excel(FILE_PATH, index=False)
                st.success("✅ Tiket berhasil diperbarui!")
                st.session_state.edit_index = None
                st.experimental_rerun()

        st.stop()

    # Form Tambah Tiket
    st.sidebar.header("➕ Tambah Ticket Baru")
    with st.sidebar.form("form_tiket"):
        divisi = st.selectbox("Divisi", ['HR', 'GA', 'Legal', 'Finance', 'Marketing', 'Sales', 'Prodev', 'Ops', 'Other'])
        bulan = st.selectbox("Bulan", ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
        kode_dok = st.text_input("Kode Dokumen")
        nomor = st.text_input("Nomor Tiket")
        desk = st.text_area("Deskripsi")
        pic = st.text_input("PIC")
        kategori = st.selectbox("Kategori", ["PERIJINAN", "KONTRAK", "LITIGASI", "LAINNYA"])
        nilai = st.number_input("Nilai", min_value=0.0)
        status = st.selectbox("Status", ["Proses", "Progress", "Info", "Closed"])
        due_date = st.date_input("Tanggal Due Date", value=datetime.today() + timedelta(days=7))
        assign_to = st.selectbox("Assign ke", karyawan_list)
        uploaded_files = st.file_uploader("📎 Upload Dokumen (boleh lebih dari 1)", type=["pdf", "docx", "jpg", "jpeg", "png"], accept_multiple_files=True)
        submit = st.form_submit_button("Kirim")

        if submit:
            file_list = []
            if uploaded_files:
                os.makedirs("uploads", exist_ok=True)
                for file in uploaded_files:
                    save_path = os.path.join("uploads", file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                    file_list.append(file.name)

            new_data = pd.DataFrame([{
                "Divisi": divisi,
                "Bulan": bulan,
                "Kode Dokumen": kode_dok,
                "Nomor Tiket": nomor,
                "Deskripsi": desk,
                "PIC": pic,
                "Kategori": kategori,
                "Nilai": nilai,
                "Status": status,
                "Tanggal Input": datetime.today().date(),
                "Tanggal Update": None,
                "Due Date": due_date,
                "Assign To": assign_to,
                "Dokumen Upload": ", ".join(file_list)
            }])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_excel(FILE_PATH, index=False)
            st.sidebar.success("✅ Ticket berhasil ditambahkan!")
