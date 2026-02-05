import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import plotly.express as px

# --- 1. YETKİ TANIMLAMALARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Güvenli Panel", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİTABANI HAFIZASI ---
if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

# --- 5. YAN MENÜ ---
st.sidebar.title("🧼 Hijyen 5.0 Menü")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- 6. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    st.title("🚀 Hijyen 5.0: Dijital Okul Projesi")
    st.info("💡 Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True, caption="Okulumuzun Hijyen Rehberi")
        except:
            st.warning("⚠️ afis.jpg yüklenmedi.")

# --- DENETÇİ SAYFASI (Şifre Olmadan Form Açılmaz) ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetkilendirme")
    
    # Giriş Durumu Kontrolü
    if 'denetci_onayli' not in st.session_state:
        st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Denetçi Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Denetçi Şifresi:", type="password", key="d_p")
            if st.button("Sisteme Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun() # Sayfayı yenileyerek formu açar
                else:
                    st.error("❌ Hatalı Denetçi Bilgileri!")
        st.warning("⚠️ Değerlendirme formuna erişmek için önce giriş yapmalısınız.")
    
    else:
        # GİRİŞ YAPILDIKTAN SONRA GÖRÜNECEK KISIM
        st.success(f"✅ Yetki Onaylandı! Denetçi: {DENETCI_USER}")
        if st.button("Oturumu Kapat"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "
