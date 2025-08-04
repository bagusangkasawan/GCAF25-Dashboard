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

# --- Tambahkan Kolom Total Poin ---
df['# Jumlah Skill Badge yang Diselesaikan'] = df['# Jumlah Skill Badge yang Diselesaikan'].fillna(0)
df['# Jumlah Game Arcade yang Diselesaikan'] = df['# Jumlah Game Arcade yang Diselesaikan'].fillna(0)
df['# Jumlah Game Trivia yang Diselesaikan'] = df['# Jumlah Game Trivia yang Diselesaikan'].fillna(0)

df['Total Poin'] = (
    (df['# Jumlah Skill Badge yang Diselesaikan'] // 2) +
    df['# Jumlah Game Arcade yang Diselesaikan'] +
    df['# Jumlah Game Trivia yang Diselesaikan']
)

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
st.sidebar.markdown(f"---\n**Total Poin:** 🎖️ {int(peserta_data['Total Poin'])}")

# --- Judul Halaman ---
st.title("🏅 GCAF25 - Total Poin Peserta yang Difasilitasi oleh Bagus Angkasawan Sumantri Putra")
st.caption(f"Menampilkan data dari: `{os.path.basename(latest_file)}`")

# --- Custom CSS untuk styling ---
st.markdown("""
<style>
.top3-card {
    padding: 24px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    min-height: 240px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.top3-card:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
.peserta-card {
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
}
.peserta-card:hover {
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# --- Ambil Top 3 Peserta ---
top_3 = df[df['Total Poin'] > 0].sort_values(by='Total Poin', ascending=False).head(3).reset_index(drop=True)

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
                <div class="top3-card" style="background: linear-gradient(135deg, {colors[i]}, #ffffff);">
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
                    <div style="font-size: 18px; color: #444;">🏅 <b>{int(row._14)} poin</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Daftar Peserta Lain ---
st.markdown("---")
st.markdown("### 🧾 Daftar Peserta Lainnya")

# Ambil nama Top 3 (kolom pertama diasumsikan nama peserta)
top_3_names = top_3.iloc[:, 0].tolist()

# Filter peserta lain (Total Poin > 0 dan bukan Top 3)
others = df[(df['Total Poin'] > 0) & (~df.iloc[:, 0].isin(top_3_names))]
others = others.sort_values(by='Total Poin', ascending=False).reset_index(drop=True)

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
                <div class="peserta-card">
                    <div style="
                        font-size: 18px;
                        font-weight: 600;
                        color: #222;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        margin-bottom: 8px;
                    " title="{row[nama_kolom]}">{row[nama_kolom]}</div>
                    <div style="font-size: 16px; color: #444;">🏅 {int(row['Total Poin'])} poin</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Milestone Validation ---
st.markdown("---")
st.markdown("## 🏆 Pencapaian Milestone Peserta")
st.caption("Untuk detail milestone, silakan lihat [Sistem Poin](https://rsvp.withgoogle.com/events/arcade-fasilitator-id/sistem-poin).")

# Definisikan milestone
def tentukan_milestone(skill, arcade, trivia):
    if skill >= 44 and arcade >= 10 and trivia >= 8:
        return "🏆 Ultimate Milestone"
    elif skill >= 30 and arcade >= 8 and trivia >= 7:
        return "🥇 Milestone #3"
    elif skill >= 20 and arcade >= 6 and trivia >= 6:
        return "🥈 Milestone #2"
    elif skill >= 10 and arcade >= 4 and trivia >= 4:
        return "🥉 Milestone #1"
    else:
        return None

# Tambahkan kolom milestone
df['Milestone'] = df.apply(lambda row: tentukan_milestone(
    row['# Jumlah Skill Badge yang Diselesaikan'],
    row['# Jumlah Game Arcade yang Diselesaikan'],
    row['# Jumlah Game Trivia yang Diselesaikan']
), axis=1)

# Tampilkan peserta berdasarkan milestone tertinggi
milestone_order = [
    "🏆 Ultimate Milestone",
    "🥇 Milestone #3",
    "🥈 Milestone #2",
    "🥉 Milestone #1"
]

# Hitung jumlah peserta per milestone
milestone_counts = [(m, len(df[df['Milestone'] == m])) for m in milestone_order]

# Pisahkan milestone yang ada pesertanya vs yang kosong
milestone_nonempty = [m for m, count in sorted(milestone_counts, key=lambda x: -x[1]) if count > 0]
milestone_empty = [m for m, count in milestone_counts if count == 0]

# Gabungkan ulang urutannya
milestone_order_urut = milestone_nonempty + milestone_empty

# Tampilkan milestone berdasarkan urutan baru
for milestone in milestone_order_urut:
    peserta_milestone = df[df['Milestone'] == milestone]
    st.markdown(f"### {milestone}")

    if peserta_milestone.empty:
        st.info(f"Belum ada peserta yang memenuhi {milestone}.")
    else:
        st.markdown(f"<span style='color: white; font-weight: bold;'>Jumlah Peserta: {len(peserta_milestone)}</span>", unsafe_allow_html=True)

        peserta_milestone = peserta_milestone.reset_index(drop=True)
        for i in range(0, len(peserta_milestone), 3):
            baris = peserta_milestone.iloc[i:i+3]
            cols = st.columns(len(baris)) 
            for j in range(len(baris)):
                row = baris.iloc[j]
                with cols[j]:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #ffffff;
                            border-left: 6px solid #00838F;
                            border-radius: 10px;
                            padding: 14px;
                            margin-bottom: 16px;
                            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                            text-align: left;
                            color: #222;
                        ">
                            <div style="font-size: 16px; font-weight: bold; color: #004D40;">
                                {row[nama_kolom]}
                            </div>
                            <div style="font-size: 14px; margin-top: 4px;">📘 Skill Badge: <b>{int(row['# Jumlah Skill Badge yang Diselesaikan'])}</b></div>
                            <div style="font-size: 14px;">🕹️ Arcade Game: <b>{int(row['# Jumlah Game Arcade yang Diselesaikan'])}</b></div>
                            <div style="font-size: 14px;">❓ Trivia Game: <b>{int(row['# Jumlah Game Trivia yang Diselesaikan'])}</b></div>
                            <div style="font-size: 14px; margin-top: 6px;">🎯 Total Poin: <b>{int(row['Total Poin'])}</b></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
