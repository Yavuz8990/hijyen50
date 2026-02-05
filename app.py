import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

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

# --- ANA SAYFA (Yeni Düzen) ---
if sayfa == "🏠 Ana Sayfa":
    st.title("🚀 Hijyen 5.0: Dijital Okul Projesi")
    st.info("💡 Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            # Afişi ana sayfada ortalı şekilde gösterir
            st.image("afis.jpg", use_container_width=True, caption="Okulumuzun Hijyen Rehberi")
        except:
            st.warning("⚠️ Afiş görseli (afis.jpg) GitHub'a yüklenmediği için gösterilemiyor.")

    st.write("---")
    st.markdown("""
    ### 🌟 Sistem Özellikleri
    * **Güvenli Denetim:** Sadece yetkili denetçiler tarafından şifreli giriş.
    * **Anlık Raporlama:** Verilerin anında dijital arşive işlenmesi.
    * **Gelişmiş Analiz:** İdare için haftalık ve aylık performans grafikleri.
    """)

# --- DENETÇİ SAYFASI (Giriş Korumalı) ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetkilendirme")
    
    auth_col1, auth_col2 = st.columns(2)
    with auth_col1:
        d_u = st.text_input("Denetçi Kullanıcı Adı:")
    with auth_col2:
        d_p = st.text_input("Denetçi Şifresi:", type="password")

    if d_u == DENETCI_USER and d_p == DENETCI_PASS:
        st.success("✅ Denetçi Yetkisi Onaylandı. Formu doldurabilirsiniz.")
        st.divider()
        
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        # QR Kod Parametresi
