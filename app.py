import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.express as px

# --- 1. YETKİ VE DOSYA AYARLARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"
DB_FILE = "denetimler.csv"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

# --- 3. ÖZEL TASARIM (CSS) - SADELEŞTİRİLMİŞ BEYAZ METİN SİSTEMİ ---
st.markdown("""
    <style>
    /* 1. Tüm Yazıların Rengini BEYAZ Yap (Başlıklar, Rakamlar ve Alt Değerler) */
    .stSlider [data-testid="stWidgetLabel"] p, 
    .stSlider div[data-testid="stThumbValue"],
    .stSlider [data-baseweb="slider"] + div div {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px #000000; /* Koyu arka planda veya açık renkli çubukta okunurluk için */
    }

    /* 2. Expander (Açılır Kutu) ve Alt Başlıklar BEYAZ */
    .st-emotion-cache-p4mowd, h3, .stSubheader {
        color: #FFFFFF !important;
    }

    /* 3. Slider Düğmesini (Tutamaç) Belirgin Yap */
    .stSlider [role="slider"] {
        border: 2px solid #FFFFFF !important;
        background-color: #00D2FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)
bugun = guncel_an.date()

# --- 5. VERİ SİSTEMİ FONKSİYONLARI ---
def verileri_yukle():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tarih'] = pd.to_datetime(df['Tarih']).dt.date
        return df
    else:
        return pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

def veri_listesini_guncelle(df):
    df.to_csv(DB_FILE, index=False)
    st.session_state['veritabani'] = df

if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = verileri_yukle()

# --- 6. ŞAMPİYON HESAPLAMA ---
def sampiyon_bul_text(veri):
    if veri.empty: return "Veri bekleniyor..."
    skorlar = veri.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

# --- 7. YAN MENÜ ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 8. SAYFA İÇERİKLERİ ---

if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    st.markdown("<h1 style='text-align: center; color: #00D2FF;'>HİJYEN 5.0</h1>", unsafe_allow_html=True)
    
    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    st.markdown(f"<div style='text-align: center; border: 2px solid #CD7F32; border-radius: 15px; padding: 15px;'><h3>🥉 AYIN HİJYEN ŞAMPİYONU</h3><p style='font-size: 30px; font-weight: bold; color: #FFFFFF;'>{sampiyon_bul_text(a_df)}</p></div>", unsafe_allow_html=True)

    with st.expander("🏆 AYLIK LİDERLİK TABLOSU"):
        if not a_df.empty:
            sirali = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
            for i, row in sirali.iterrows():
                st.write(f"#{i+1} **{row['Sınıf']} Sınıfı** - {row['Puan']:.1f} Puan")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("Afiş bulunamadı.")

elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        d_u = st.text_input("Kullanıcı Adı:")
        d_p = st.text_input("Şifre:", type="password")
        if st.button("Giriş"):
            if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                st.session_state['denetci_onayli'] = True
                st.rerun()
    else:
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        if url_sinif in siniflar:
            s_sinif = url_sinif
            with st.form("hassas_form"):
                st.subheader(f"📍 Denetlenen Sınıf: {s_sinif}")
                
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0, key="h1")
                    p1_2 = st.slider("Sınıfta ağır koku yok (0-10)", 0, 10, 0, key="h2")
                with st.expander("🪑 2. Sınıf ve Masa Temizliği"):
                    p2_1 = st.slider("Masa Temizliği (0-6)", 0, 6, 0, key="h3")
                    p2_2 = st.slider("Sıra Altı/Üstü (0-6)", 0, 6, 0, key="h4")
                    p2_3 = st.slider("Genel Düzen (0-8)", 0, 8, 0, key="h5")
                with st.expander("🧹 3. Zemin ve Köşe Temizliği"):
                    p3_1 = st.slider("Dip Köşe Temizliği (0-6)", 0, 6, 0, key="h6")
                    p3_2 = st.slider("Cam Kenarları (0-6)", 0, 6, 0, key="h7")
                    p3_3 = st.slider("Zemin Temizliği (0-8)", 0, 8, 0, key="h8")
                with st.expander("🗑️ 4. Çöp Kutusu ve Atık Yönetimi"):
                    p4_1 = st.slider("Doğru Kullanım (0-6)", 0, 6, 0, key="h9")
                    p4_2 = st.slider("Doluluk Oranı (0-6)", 0, 6, 0, key="h10")
                    p4_3 = st.slider("Çevre Temizliği (0-8)", 0, 8, 0, key="h11")
                with st.expander("✨ 5. Genel Sınıf Yüzey Temizliği"):
                    p5_1 = st.slider("Duvarlar (0-5)", 0, 5, 0, key="h12")
                    p5_2 = st.slider("Panolar (0-5)", 0, 5, 0, key="h13")
                    p5_3 = st.slider("Tahta (0-5)", 0, 5, 0, key="h14")
                    p5_4 = st.slider("Genel Görünüm (0-5)", 0, 5, 0, key="h15")

                if st.form_submit_button("💾 VERİYİ SİSTEME MÜHÜRLE"):
                    toplam = p1_1+p1_2+p2_1+p2_2+p2_3+p3_1+p3_2+p3_3+p4_1+p4_2+p4_3+p5_1+p5_2+p5_3+p5_4
                    df = verileri_yukle()
                    yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": toplam, "Yetkili": DENETCI_USER}])
                    veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                    st.success(f"✅ Başarılı! Puan: {toplam}")
                    st.balloons()
        else: st.error("⚠️ Lütfen kapıdaki karekodu okutunuz.")

elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analizi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False
    if not st.session_state['admin_onayli']:
        y_u = st.text_input("Yönetici Adı:")
        y_p = st.text_input("Şifre:", type="password")
        if st.button("Giriş"):
            if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                st.session_state['admin_onayli'] = True
                st.rerun()
    else:
        df = verileri_yukle()
        if not df.empty:
            st.write(df)
            if st.button("Tüm Verileri Sil"):
                veri_listesini_guncelle(pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"]))
                st.rerun()
