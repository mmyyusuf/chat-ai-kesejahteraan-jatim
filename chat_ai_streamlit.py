import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Konfigurasi & Load data
# -------------------------
st.set_page_config(page_title="Chat AI Kesejahteraan Jatim",
                   page_icon="💬",
                   layout="wide")

DATAFILE = "hasil_kesejahteraan_agglo.xlsx"

try:
    df = pd.read_excel(DATAFILE)
except Exception as e:
    st.error(f"Error membaca file data: {e}")
    st.stop()

# Nama kolom (pastikan sesuai)
COL_KAB = "Kabupaten/Kota"
COL_CLUSTER = "Agglo_Kesejahteraan"
COL_IPM = "Indeks Pembangunan Manusia"
COL_PENGELUARAN = "Pengeluaran Per Kapita Riil"
COL_TPT = "Tingkat Pengangguran Terbuka (TPT)"

required = [COL_KAB, COL_CLUSTER, COL_IPM, COL_PENGELUARAN, COL_TPT]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Kolom required tidak ditemukan di file: {missing}. Pastikan file benar.")
    st.stop()

# -------------------------
# Deskripsi Cluster
# -------------------------
cluster_descriptions = {
    'Rendah': """**Cluster 0 – Kesejahteraan Rendah**
IPM dan pengeluaran cukup tinggi, namun TPT juga tinggi.
Umumnya di kota besar seperti Surabaya, Malang, dan Sidoarjo.
Faktor: urbanisasi cepat, biaya hidup tinggi, persaingan kerja.""",

    'Sedang': """**Cluster 2 – Kesejahteraan Sedang**
Indikator kesejahteraan menengah seperti Kediri, Blitar, Jember, Banyuwangi.
Faktor: pemerataan pembangunan mulai terlihat, UMKM tumbuh, namun lapangan kerja formal terbatas.""",

    'Tinggi': """**Cluster 1 – Kesejahteraan Tinggi**
Wilayah seperti Pacitan, Sumenep, dan Bangkalan.
Ciri: IPM tinggi, pengeluaran stabil, TPT rendah.
Faktor: stabilitas sosial, sektor produktif kuat, dan pembangunan merata."""
}

# -------------------------
# Sidebar info
# -------------------------
with st.sidebar:
    st.markdown("### 📘 Info Proyek")
    st.write("**Proyek:** Analisis Kesejahteraan Daerah — Jawa Timur")
    st.write("**Metode:** Agglomerative Hierarchical Clustering")
    st.write("**Output:** Chat AI + Visualisasi interaktif")
    st.markdown("---")
    st.caption("© Proyek Sains Data 2025")

# -------------------------
# Layout utama
# -------------------------
st.title("💬 Chat AI Kesejahteraan Daerah Jawa Timur")
st.write("Tanyakan nama kabupaten/kota atau gunakan perintah seperti:")
st.code("kabupaten tinggi | kota rendah | daftar sedang | jelaskan cluster sedang", language="markdown")

col1, col2 = st.columns([1.2, 1])

# =====================================================
# Kolom 1: Chat AI (fitur utama)
# =====================================================
with col1:
    user_input = st.text_input("Masukkan pertanyaan di sini 👇").strip()

    if user_input:
        ui = user_input.lower()

        # ---- Jelaskan cluster ----
        if any(x in ui for x in ["jelaskan", "penjelasan", "deskripsi"]) and "cluster" in ui:
            for k in cluster_descriptions.keys():
                if k.lower() in ui:
                    st.subheader(f"📖 Penjelasan Cluster {k}")
                    st.write(cluster_descriptions[k])
                    break
            else:
                st.warning("Tentukan cluster: rendah / sedang / tinggi")

        # ---- Daftar daerah per kategori (kabupaten/kota) ----
        elif any(k in ui for k in ["daftar rendah", "kabupaten rendah", "kota rendah"]):
            subset = df[df[COL_CLUSTER] == "Rendah"]
            if "kabupaten" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kabupaten", case=False, na=False)]
                st.subheader("📍 Kabupaten Kategori Rendah")
            elif "kota" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kota", case=False, na=False)]
                st.subheader("🏙️ Kota Kategori Rendah")
            else:
                st.subheader("📍 Semua Daerah Kategori Rendah")
            st.write(", ".join(subset[COL_KAB].tolist()))

        elif any(k in ui for k in ["daftar sedang", "kabupaten sedang", "kota sedang"]):
            subset = df[df[COL_CLUSTER] == "Sedang"]
            if "kabupaten" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kabupaten", case=False, na=False)]
                st.subheader("📍 Kabupaten Kategori Sedang")
            elif "kota" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kota", case=False, na=False)]
                st.subheader("🏙️ Kota Kategori Sedang")
            else:
                st.subheader("📍 Semua Daerah Kategori Sedang")
            st.write(", ".join(subset[COL_KAB].tolist()))

        elif any(k in ui for k in ["daftar tinggi", "kabupaten tinggi", "kota tinggi"]):
            subset = df[df[COL_CLUSTER] == "Tinggi"]
            if "kabupaten" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kabupaten", case=False, na=False)]
                st.subheader("📍 Kabupaten Kategori Tinggi")
            elif "kota" in ui:
                subset = subset[subset[COL_KAB].str.contains("Kota", case=False, na=False)]
                st.subheader("🏙️ Kota Kategori Tinggi")
            else:
                st.subheader("📍 Semua Daerah Kategori Tinggi")
            st.write(", ".join(subset[COL_KAB].tolist()))

        # ---- Pertanyaan umum seperti “Kota Kediri cluster apa” ----
        elif any(x in ui for x in ["cluster apa", "masuk cluster apa", "kategori apa", "masuk kategori apa"]):
            found = None
            for daerah in df[COL_KAB].str.lower():
                if daerah in ui:
                    found = daerah
                    break
            if found:
                row = df[df[COL_KAB].str.lower() == found]
                if not row.empty:
                    daerah_nama = row[COL_KAB].values[0]
                    kategori = row[COL_CLUSTER].values[0]
                    st.success(f"🏙️ {daerah_nama} termasuk dalam kategori **{kategori}**")
                    st.write(cluster_descriptions[kategori])
            else:
                st.warning("Nama daerah tidak ditemukan di database.")

        # ---- Cari langsung nama kabupaten/kota ----
        else:
            match = df[df[COL_KAB].str.lower() == ui]
            if not match.empty:
                kategori = match[COL_CLUSTER].values[0]
                st.success(f"🏙️ {match[COL_KAB].values[0]} → kategori **{kategori}**")
                st.write(cluster_descriptions.get(kategori, "Deskripsi tidak tersedia."))
            else:
                st.error("Nama daerah tidak ditemukan. Coba 'daftar tinggi/sedang/rendah' atau 'kabupaten rendah'.")

# =====================================================
# Kolom 2: Visualisasi interaktif
# =====================================================
with col2:
    st.header("📊 Distribusi Kategori")
    counts = df[COL_CLUSTER].value_counts().reset_index()
    counts.columns = ["Kategori", "Jumlah"]
    counts["Persentase"] = (counts["Jumlah"] / counts["Jumlah"].sum() * 100).round(1)

    fig_pie = px.pie(counts, names="Kategori", values="Jumlah",
                     color="Kategori",
                     color_discrete_map={'Rendah': '#ff6b6b', 'Sedang': '#feca57', 'Tinggi': '#1dd1a1'},
                     hole=0.4,
                     title="Distribusi Daerah per Kategori (persentase)")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# =====================================================
# Rata-rata indikator
# =====================================================
st.markdown("---")
st.header("📈 Rata-Rata Indikator per Kategori")

avg_df = df.groupby(COL_CLUSTER).agg({
    COL_IPM: "mean",
    COL_PENGELUARAN: "mean",
    COL_TPT: "mean"
}).round(2).reset_index()

st.dataframe(avg_df.rename(columns={
    COL_IPM: "Rata-rata IPM",
    COL_PENGELUARAN: "Rata-rata Pengeluaran Per Kapita Riil",
    COL_TPT: "Rata-rata TPT"
}), height=220)

melt = avg_df.melt(id_vars=[COL_CLUSTER], value_vars=[COL_IPM, COL_PENGELUARAN, COL_TPT],
                   var_name="Indikator", value_name="Rata2")
fig_bar = px.bar(melt, x=COL_CLUSTER, y="Rata2", color="Indikator", barmode="group",
                 title="Perbandingan Rata-Rata Indikator per Kategori",
                 color_discrete_map={
                     COL_IPM: "#00a8e8",
                     COL_PENGELUARAN: "#48cae4",
                     COL_TPT: "#0077b6"
                 })
st.plotly_chart(fig_bar, use_container_width=True)
