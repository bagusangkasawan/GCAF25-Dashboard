import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="🏆 GCAF25 Dashboard", layout="wide")

# --- Sidebar: Pilih file CSV terbaru otomatis ---
st.sidebar.title("📁 File Data")
csv_files = sorted(
    glob.glob("data/GCAF25-ID-VQN-DWK [*.csv"),
    key=os.path.getmtime,
    reverse=True
)

if not csv_files:
    st.warning("❗ Tidak ada file CSV ditemukan di folder /data")
    st.stop()

latest_file = csv_files[0]
file_date = latest_file.split("[")[-1].replace("].csv", "").strip()
st.sidebar.markdown(f"**📅 Data Tanggal:** `{file_date}`")

# --- Load Data ---
df = pd.read_csv(latest_file)

# --- Tambahkan Kolom Total Badge ---
if all(col in df.columns for col in [
    '# Jumlah Skill Badge yang Diselesaikan',
    '# Jumlah Game Arcade yang Diselesaikan',
    '# Jumlah Game Trivia yang Diselesaikan'
]):
    df['Total Badge'] = (
        df['# Jumlah Skill Badge yang Diselesaikan'].fillna(0) +
        df['# Jumlah Game Arcade yang Diselesaikan'].fillna(0) +
        df['# Jumlah Game Trivia yang Diselesaikan'].fillna(0)
    )
else:
    st.warning("❗ Kolom-kolom penghitungan Total Badge tidak lengkap.")
    st.stop()

# --- Sidebar: Lihat detail peserta ---
st.sidebar.markdown("---")
st.sidebar.header("👤 Lihat Detail Peserta")

nama_kolom = df.columns[0]  # diasumsikan kolom pertama adalah nama peserta
nama_peserta = st.sidebar.selectbox("Pilih Peserta", df[nama_kolom].dropna().unique().tolist())

peserta_data = df[df[nama_kolom] == nama_peserta].iloc[0]

st.sidebar.markdown("### 🎯 Rincian Badge")
st.sidebar.markdown(f"- **Skill Badge:** {int(peserta_data['# Jumlah Skill Badge yang Diselesaikan'])}")
st.sidebar.markdown(f"- **Game Arcade:** {int(peserta_data['# Jumlah Game Arcade yang Diselesaikan'])}")
st.sidebar.markdown(f"- **Game Trivia:** {int(peserta_data['# Jumlah Game Trivia yang Diselesaikan'])}")
st.sidebar.markdown(f"---\n**Total Badge:** 🎖️ `{int(peserta_data['Total Badge'])}`")

# --- Judul Halaman ---
st.title("🏅 GCAF25 - Total Badge Peserta yang Difasilitasi oleh Bagus Angkasawan Sumantri Putra")
st.caption(f"Menampilkan data dari: `{os.path.basename(latest_file)}`")

# --- Ambil Top 3 Peserta ---
top_3 = df[df['Total Badge'] > 0].sort_values(by='Total Badge', ascending=False).head(3).reset_index(drop=True)

if top_3.empty:
    st.warning("Belum ada peserta yang memiliki badge.")
else:
    medals = ["🥇", "🥈", "🥉"]
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze

    st.markdown("---")
    st.markdown("### 👑 Tiga Peserta Terbaik Hari Ini")

    col1, col2, col3 = st.columns(3)

    for i, (col, row) in enumerate(zip([col1, col2, col3], top_3.itertuples())):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, {colors[i]}, #ffffff);
                    padding: 24px;
                    border-radius: 18px;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    cursor: default;
                    min-height: 240px;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                " onmouseover="this.style.transform='scale(1.03)'; this.style.boxShadow='0 6px 18px rgba(0,0,0,0.15)';"
                  onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)';"
                >
                    <div style="font-size: 52px; margin-bottom: 12px;">{medals[i]}</div>
                    <div style="
                        font-size: 20px;
                        font-weight: 700;
                        margin-bottom: 8px;
                        max-width: 95%;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        color: #333;
                    " title="{row._1}">{row._1}</div>
                    <div style="font-size: 18px; color: #444;">🏅 <b>{int(row._14)} badge</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Daftar Peserta Lain ---
st.markdown("---")
st.markdown("### 🧾 Daftar Peserta Lainnya")

# Ambil nama Top 3 (kolom pertama diasumsikan nama peserta)
top_3_names = top_3.iloc[:, 0].tolist()

# Filter peserta lain (Total Badge > 0 dan bukan Top 3)
others = df[(df['Total Badge'] > 0) & (~df.iloc[:, 0].isin(top_3_names))]
others = others.sort_values(by='Total Badge', ascending=False).reset_index(drop=True)

if others.empty:
    st.info("Tidak ada peserta lain dengan badge > 0.")
else:
    # Tampilkan dalam bentuk grid card, 3 per baris
    nama_kolom = df.columns[0]  # kolom nama peserta
    cols = st.columns(3)
    for idx, row in others.iterrows():
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: #f5f5f5;
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 16px;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
                    text-align: center;
                    height: 140px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    transition: transform 0.2s;
                " onmouseover="this.style.transform='scale(1.02)';"
                  onmouseout="this.style.transform='scale(1)';"
                >
                    <div style="
                        font-size: 18px;
                        font-weight: 600;
                        color: #222;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        margin-bottom: 8px;
                    " title="{row[nama_kolom]}">{row[nama_kolom]}</div>
                    <div style="font-size: 16px; color: #444;">🏅 {int(row['Total Badge'])} badge</div>
                </div>
                """,
                unsafe_allow_html=True
            )
