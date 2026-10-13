# -*- coding: utf-8 -*-
"""Dashboard Streamlit — Regresi OLS Belanja Modal Pendidikan & Kesehatan terhadap IPM.

Jalankan dengan:  streamlit run app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import statsmodels.formula.api as smf
import streamlit as st

BASE = Path(__file__).resolve().parent
URL_DATA = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/main/dataset_fiskal_97_hipoFull.csv"
PATH_LOKAL = BASE / "data" / "dataset_fiskal_97_hipoFull.csv"
KOTA_DEFAULT = "Kota Jambi"

st.set_page_config(
    page_title="Regresi OLS — Belanja Modal vs IPM",
    page_icon="📈",
    layout="wide",
)


# --------------------------------------------------------------------- data
@st.cache_data(show_spinner=False)
def muat_data() -> pd.DataFrame:
    """Muat dataset panel: coba URL GitHub, fallback ke berkas lokal."""
    try:
        df = pd.read_csv(URL_DATA)
    except Exception:
        df = pd.read_csv(PATH_LOKAL)
    df = df[["Kota", "Tahun", "bm_pendidikan", "bm_kesehatan", "IPM"]].dropna().copy()
    df["Kota"] = df["Kota"].astype(str).str.strip()
    return df


def estimasi(df: pd.DataFrame):
    """Estimasi OLS: IPM ~ bm_pendidikan + bm_kesehatan."""
    return smf.ols("IPM ~ bm_pendidikan + bm_kesehatan", data=df).fit()


# ------------------------------------------------------------------ layout
def gaya_layout(judul: str, tinggi: int = 420) -> dict:
    return dict(
        title=dict(text=f"<b>{judul}</b>", font=dict(size=15, color="#0f172a")),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=12, color="#334155"),
        margin=dict(l=60, r=20, t=56, b=52),
        height=tinggi,
        hoverlabel=dict(bgcolor="#0f172a", font=dict(color="#fff", size=12)),
    )


def fig_sebaran(df: pd.DataFrame, kolom: str, judul: str, warna: str, model) -> go.Figure:
    """Scatter + garis regresi (variabel bebas lain ditahan pada nilai rata-ratanya)."""
    rata_x1 = df["bm_pendidikan"].mean()
    rata_x2 = df["bm_kesehatan"].mean()

    x_garis = np.linspace(df[kolom].min(), df[kolom].max(), 60)
    if kolom == "bm_pendidikan":
        y_garis = (model.params["Intercept"] + model.params["bm_pendidikan"] * x_garis
                   + model.params["bm_kesehatan"] * rata_x2)
    else:
        y_garis = (model.params["Intercept"] + model.params["bm_pendidikan"] * rata_x1
                   + model.params["bm_kesehatan"] * x_garis)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[kolom], y=df["IPM"], mode="markers+text", text=df["Tahun"].astype(str),
        textposition="top center", textfont=dict(size=10, color="#475569"),
        marker=dict(color=warna, size=12, line=dict(width=1.5, color="#ffffff")),
        name="Data aktual",
        hovertemplate="<b>Tahun %{text}</b><br>%{x:.2f}<br>IPM: %{y:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x_garis, y=y_garis, mode="lines", name="Garis regresi",
        line=dict(color="#e65100", width=3), hoverinfo="skip",
    ))
    fig.update_layout(**gaya_layout(judul))
    fig.update_layout(
        xaxis=dict(title="Indeks belanja modal", gridcolor="#eef2f7", zeroline=False),
        yaxis=dict(title="IPM", gridcolor="#eef2f7", zeroline=False),
        showlegend=False,
    )
    return fig


def fig_3d(df: pd.DataFrame, model) -> go.Figure:
    g1 = np.linspace(df["bm_pendidikan"].min(), df["bm_pendidikan"].max(), 25)
    g2 = np.linspace(df["bm_kesehatan"].min(), df["bm_kesehatan"].max(), 25)
    zg = np.array([
        [model.params["Intercept"] + model.params["bm_pendidikan"] * a
         + model.params["bm_kesehatan"] * b for a in g1]
        for b in g2
    ])

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=df["bm_pendidikan"], y=df["bm_kesehatan"], z=df["IPM"],
        mode="markers+text", text=df["Tahun"].astype(str), textposition="top center",
        textfont=dict(size=11, color="#334155"),
        marker=dict(size=7, color="#2e7d32", opacity=0.95), name="Data aktual",
        hovertemplate="<b>Tahun %{text}</b><br>Belanja pendidikan: %{x:.2f}<br>"
                      "Belanja kesehatan: %{y:.2f}<br>IPM: %{z:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Surface(
        x=g1, y=g2, z=zg, opacity=0.60, colorscale="Viridis",
        showscale=False, name="Bidang regresi",
        hovertemplate="Belanja pendidikan: %{x:.2f}<br>Belanja kesehatan: %{y:.2f}<br>"
                      "Prediksi IPM: %{z:.2f}<extra></extra>",
    ))
    fig.update_layout(**gaya_layout("Bidang Regresi 3D", tinggi=650))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Belanja Modal Pendidikan (X1)", gridcolor="#eef2f7",
                       backgroundcolor="#fbfdff", showbackground=True),
            yaxis=dict(title="Belanja Modal Kesehatan (X2)", gridcolor="#eef2f7",
                       backgroundcolor="#fbfdff", showbackground=True),
            zaxis=dict(title="IPM (Y)", gridcolor="#eef2f7",
                       backgroundcolor="#fbfdff", showbackground=True),
            camera=dict(eye=dict(x=1.65, y=1.65, z=1.05)),
        ),
        legend=dict(x=0.02, y=0.98),
    )
    return fig


# -------------------------------------------------------------------- main
df_semua = muat_data()
daftar_kota = sorted(df_semua["Kota"].unique())

with st.sidebar:
    st.header("Pengaturan")
    indeks_default = daftar_kota.index(KOTA_DEFAULT) if KOTA_DEFAULT in daftar_kota else 0
    kota = st.selectbox("Pilih kota", daftar_kota, index=indeks_default)
    st.divider()
    st.caption(
        f"**Dataset:** panel fiskal 97 kota Indonesia\n\n"
        f"- {len(df_semua):,} observasi\n"
        f"- {len(daftar_kota)} kota\n"
        f"- Tahun {int(df_semua['Tahun'].min())}–{int(df_semua['Tahun'].max())}"
    )

st.title("Pengaruh Belanja Modal Pendidikan & Kesehatan terhadap IPM")
st.caption(
    "Dashboard interaktif — Regresi Linier Berganda (*Ordinary Least Squares*). "
    "Pilih kota di panel kiri untuk menghitung ulang seluruh analisis."
)

df = df_semua[df_semua["Kota"] == kota].sort_values("Tahun").reset_index(drop=True)

st.subheader(f"Studi Kasus: {kota}")
if len(df) < 4:
    st.error(f"Data {kota} hanya {len(df)} observasi — tidak cukup untuk estimasi OLS.")
    st.stop()

model = estimasi(df)
b = model.params
se = model.bse
tv = model.tvalues
pv = model.pvalues
jumlah_sig = int(sum(pv[k] < 0.05 for k in ["bm_pendidikan", "bm_kesehatan"]))

# --------------------------------------------------------------------- KPI
k1, k2, k3, k4 = st.columns(4)
k1.metric("Observasi", f"{len(df)}", f"tahun {int(df['Tahun'].min())}–{int(df['Tahun'].max())}",
          delta_color="off")
k2.metric("R-squared", f"{model.rsquared:.3f}", f"Adj. R² {model.rsquared_adj:.3f}",
          delta_color="off")
k3.metric("F-statistic", f"{model.fvalue:.3f}", f"p = {model.f_pvalue:.4f}", delta_color="off")
k4.metric("Variabel signifikan", f"{jumlah_sig} / 2", "pada alpha 5%", delta_color="off")

# --------------------------------------------------------------- persamaan
st.subheader("Model Penelitian")
st.latex(
    r"\widehat{\text{IPM}} = "
    + f"{b['Intercept']:.4f}".replace(".", "{,}")
    + (" + " if b["bm_pendidikan"] >= 0 else " - ")
    + f"{abs(b['bm_pendidikan']):.4f}".replace(".", "{,}")
    + r"\cdot X_1"
    + (" + " if b["bm_kesehatan"] >= 0 else " - ")
    + f"{abs(b['bm_kesehatan']):.4f}".replace(".", "{,}")
    + r"\cdot X_2"
)

# ------------------------------------------------------------------- tabel
st.subheader("Hasil Estimasi Koefisien")

label = ["Konstanta", "Belanja Modal Pendidikan", "Belanja Modal Kesehatan"]
kode = ["—", "bm_pendidikan", "bm_kesehatan"]
baris = []
for i, nama in enumerate(["Intercept", "bm_pendidikan", "bm_kesehatan"]):
    signifikan = pv[nama] < 0.05
    baris.append({
        "Variabel": label[i],
        "Kolom": kode[i],
        "Koefisien": round(float(b[nama]), 4),
        "Std. Error": round(float(se[nama]), 4),
        "t-statistik": round(float(tv[nama]), 3),
        "p-value": round(float(pv[nama]), 4),
        "Keputusan": "Signifikan" if signifikan else "Tidak signifikan",
    })

tabel = pd.DataFrame(baris)
st.dataframe(
    tabel,
    hide_index=True,
    width="stretch",
    column_config={
        "Koefisien": st.column_config.NumberColumn(format="%.4f"),
        "Std. Error": st.column_config.NumberColumn(format="%.4f"),
        "t-statistik": st.column_config.NumberColumn(format="%.3f"),
        "p-value": st.column_config.NumberColumn(format="%.4f"),
    },
)
st.caption(
    f"R² = {model.rsquared:.4f} · Adj. R² = {model.rsquared_adj:.4f} · "
    f"F = {model.fvalue:.4f} (p = {model.f_pvalue:.4f})"
)

# ------------------------------------------------------------------ grafik
st.subheader("Visualisasi")

kol1, kol2 = st.columns(2)
with kol1:
    st.plotly_chart(
        fig_sebaran(df, "bm_pendidikan", "Belanja Modal Pendidikan vs IPM", "#2e7d32", model),
        width="stretch",
    )
with kol2:
    st.plotly_chart(
        fig_sebaran(df, "bm_kesehatan", "Belanja Modal Kesehatan vs IPM", "#1e88e5", model),
        width="stretch",
    )

fig_bar = go.Figure(go.Bar(
    x=["Belanja Modal Pendidikan", "Belanja Modal Kesehatan"],
    y=[b["bm_pendidikan"], b["bm_kesehatan"]],
    marker_color=["#15803d" if b["bm_pendidikan"] >= 0 else "#b91c1c",
                  "#15803d" if b["bm_kesehatan"] >= 0 else "#b91c1c"],
    text=[f"{b['bm_pendidikan']:.4f}", f"{b['bm_kesehatan']:.4f}"],
    textposition="outside",
    cliponaxis=False,
    hovertemplate="%{x}<br>Koefisien: %{y:.4f}<extra></extra>",
))
fig_bar.update_layout(**gaya_layout("Nilai Koefisien Regresi OLS", tinggi=390))
fig_bar.update_layout(
    yaxis=dict(title="Koefisien", gridcolor="#eef2f7", zeroline=True, zerolinecolor="#94a3b8"),
    xaxis=dict(title=""),
    showlegend=False,
)
st.plotly_chart(fig_bar, width="stretch")

fig_tren = go.Figure(go.Scatter(
    x=df["Tahun"], y=df["IPM"], mode="lines+markers",
    line=dict(color="#2563eb", width=3), marker=dict(size=9, color="#1e3a8a"),
    hovertemplate="Tahun %{x}<br>IPM: %{y:.2f}<extra></extra>",
))
fig_tren.update_layout(**gaya_layout(f"Perkembangan IPM {kota}", tinggi=390))
fig_tren.update_layout(
    xaxis=dict(title="Tahun", dtick=1, gridcolor="#eef2f7", zeroline=False),
    yaxis=dict(title="IPM", gridcolor="#eef2f7", zeroline=False),
    showlegend=False,
)
st.plotly_chart(fig_tren, width="stretch")

st.plotly_chart(fig_3d(df, model), width="stretch")

# ------------------------------------------------------------- data mentah
with st.expander(f"Lihat data {kota} ({len(df)} baris)"):
    st.dataframe(
        df.rename(columns={
            "Tahun": "Tahun",
            "bm_pendidikan": "Belanja Modal Pendidikan",
            "bm_kesehatan": "Belanja Modal Kesehatan",
            "IPM": "IPM",
        })[["Tahun", "Belanja Modal Pendidikan", "Belanja Modal Kesehatan", "IPM"]],
        hide_index=True,
        width="stretch",
    )
    st.download_button(
        "Unduh CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"data_{kota.replace(' ', '_')}.csv",
        mime="text/csv",
    )

# -------------------------------------------------------------- kesimpulan
st.subheader("Kesimpulan")

arah_x1 = "positif" if b["bm_pendidikan"] >= 0 else "negatif"
arah_x2 = "positif" if b["bm_kesehatan"] >= 0 else "negatif"

st.markdown(
    f"""
1. **Belanja Modal Pendidikan** {"berpengaruh **signifikan**" if pv["bm_pendidikan"] < 0.05
   else "**tidak berpengaruh signifikan**"} terhadap IPM
   (koefisien {b['bm_pendidikan']:+.4f}; p = {pv['bm_pendidikan']:.4f}; arah {arah_x1}).

2. **Belanja Modal Kesehatan** {"berpengaruh **signifikan**" if pv["bm_kesehatan"] < 0.05
   else "**tidak berpengaruh signifikan**"} terhadap IPM
   (koefisien {b['bm_kesehatan']:+.4f}; p = {pv['bm_kesehatan']:.4f}; arah {arah_x2}).

3. **Daya penjelas model**: R² = {model.rsquared:.4f} (Adj. R² = {model.rsquared_adj:.4f}) —
   {"cukup kuat" if model.rsquared >= 0.3 else "terbatas"}. Secara simultan kedua variabel
   {"berpengaruh signifikan" if model.f_pvalue < 0.05 else "tidak berpengaruh signifikan"}
   (F = {model.fvalue:.4f}; p = {model.f_pvalue:.4f}).
"""
)

st.info(
    "**Catatan interpretasi:** koefisien negatif pada belanja modal kesehatan umumnya bukan berarti "
    "belanja tersebut merugikan IPM, melainkan mencerminkan pola *alokasi berbasis kebutuhan* "
    "(kota dengan IPM rendah menganggarkan belanja modal kesehatan lebih besar) dan sifat belanja "
    "modal sebagai investasi jangka panjang yang dampaknya baru terasa beberapa tahun kemudian.",
    icon="ℹ️",
)

st.divider()
st.caption(
    "Sumber data: `dataset_fiskal_97_hipoFull.csv` — panel fiskal 97 kota Indonesia (2014–2024). "
    "Dibangun dengan Python · Pandas · Statsmodels · Plotly · Streamlit."
)
