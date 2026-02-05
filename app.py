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
            st.warning("⚠️ Afiş görseli (afis.jpg) GitHub'a yüklenmediği için gösterilemiyor.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetkilendirme")
    
    with st.container(border=True):
        d_u = st.text_input("Denetçi Kullanıcı Adı:", key="denetci_user")
        d_p = st.text_input("Denetçi Şifresi:", type="password", key="denetci_pass")
        denetci_giris_btn = st.button("Sisteme Giriş Yap")

    if denetci_giris_btn:
        if d_u == DENETCI_USER and d_p == DENETCI_PASS:
            st.session_state['denetci_logged_in'] = True
            st.success("✅ Yetki Onaylandı!")
        else:
            st.error("❌ Hatalı Denetçi Bilgileri!")
            st.session_state['denetci_logged_in'] = False

    # Giriş Başarılıysa Maddeleri Göster
    if st.session_state.get('denetci_logged_in'):
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        # QR Kod Parametresi Takibi
        query_params = st.query_params
        gelen_sinif = query_params.get("sinif", None)
        idx = siniflar.index(gelen_sinif) if gelen_sinif in siniflar else 0
        
        c1, c2 = st.columns(2)
        with c1:
            s_sinif = st.selectbox("Sınıf Seçin:", siniflar, index=idx)
        with c2:
            s_tarih = st.date_input("Tarih:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 5 Maddelik Hijyen Kontrolü")
            st.write("*(Her madde 20 puan değerindedir)*")
            m1 = st.checkbox("1. Havalandırma Durumu")
            m2 = st.checkbox("2. Sıra ve Masa Temizliği")
            m3 = st.checkbox("3. Zemin ve Köşelerin Hijyeni")
            m4 = st.checkbox("4. Çöp Kutusu ve Atık Yönetimi")
            m5 = st.checkbox("5. Sınıf Genel Düzeni")
            
            if st.form_submit_button("ONAYLA VE VERİYİ MÜHÜRLE"):
                skor = sum([m1, m2, m3, m4, m5]) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": skor, "Yetkili": d_u}])
                st.session_state['veritabani'] = pd.concat([st.session_state['veritabani'], yeni], ignore_index=True)
                st.success(f"Kayıt Tamam: {s_sinif} sınıfına {skor} puan verildi.")
                st.balloons()

# --- YÖNETİCİ SAYFASI ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    
    with st.container(border=True):
        y_u = st.text_input("Yönetici Kullanıcı Adı:", key="admin_user")
        y_p = st.text_input("Yönetici Şifresi:", type="password", key="admin_pass")
        yönetici_giris_btn = st.button("Yönetici Panelini Aç")
    
    if yönetici_giris_btn:
        if y_u == YONETICI_USER and y_p == YONETICI_PASS:
            st.session_state['admin_logged_in'] = True
            st.success("🔓 Erişim Sağlandı!")
        else:
            st.error("❌ Yönetici Yetkisi Reddedildi!")
            st.session_state['admin_logged_in'] = False

    if st.session_state.get('admin_logged_in'):
        df = st.session_state['veritabani']
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            t1, t2 = st.tabs(["📊 HAFTALIK ANALİZ", "📈 AYLIK ANALİZ"])
            with t1:
                st.subheader("Sınıf Puan Ortalamaları")
                st.bar_chart(df.groupby("Sınıf")["Puan"].mean())
                st.dataframe(df, use_container_width=True)
            with t2:
                st.subheader("Zaman Bazlı Hijyen Trendi")
                st.line_chart(df.groupby("Tarih")["Puan"].mean())
        else:
            st.info("Henüz veri girişi yapılmamış.")
