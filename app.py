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

# --- 2. SAYFA AYARLARI (İkon Değişti: 🧼) ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİ SİSTEMİ ---
def verileri_yukle():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

def veri_kaydet(yeni_veri):
    df = verileri_yukle()
    df = pd.concat([df, yeni_veri], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    st.session_state['veritabani'] = df

if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = verileri_yukle()

# --- 5. YAN MENÜ ---
st.sidebar.title("🫧 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "🧼 Denetçi Girişi", "📈 Yönetici Paneli"])

# --- 6. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="font-family: 'Arial Black', sans-serif; color: #00D2FF; font-size: 60px; margin-bottom: 0px; text-shadow: 2px 2px 10px rgba(0,210,255,0.5);">
                HİJYEN 5.0
            </h1>
            <h2 style="font-family: 'Trebuchet MS', sans-serif; color: #FFFFFF; font-size: 28px; font-weight: normal; letter-spacing: 4px; margin-top: 0px; opacity: 0.9;">
                GELECEĞİN TEMİZ OKULU
            </h2>
        </div>
    """, unsafe_allow_html=True)
    st.info("💡 **SİSTEM MESAJI:** Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ `afis.jpg` bulunamadı.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "🧼 Denetçi Girişi":
    st.title("🧼 Denetçi Giriş Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("🧼 Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Geçersiz Bilgiler!")
    else:
        st.success(f"✨ Oturum Açıldı: {DENETCI_USER}")
        if st.button("🏃 Çıkış Yap"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        st.divider()
        siniflar = ["9
