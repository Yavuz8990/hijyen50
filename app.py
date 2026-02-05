import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import plotly.express as px  # Pasta grafiği için gerekli

# --- 1. YETKİ TANIMLAMALARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Analiz Paneli", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİTABANI HAFIZASI ---
if 'veritabani' not in st.session_state:
    # Boş kalmaması için örnek veri seti
    st.session_state['veritabani'] = pd.DataFrame([
        {"Tarih": guncel_an.date(), "Sınıf": "9A", "Puan": 100, "Yetkili": "admin"},
        {"Tarih": guncel_an.date(), "Sınıf": "10B", "Puan": 80, "Yetkili": "admin"},
        {"Tarih": guncel_an.date(), "Sınıf": "11C", "Puan": 60, "Yetkili": "admin"}
    ])

# --- 5. YAN MENÜ ---
st.sidebar.title("🧼 Hijyen 5.0 Menü")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    st.title("🚀 Hijyen 5.0: Dijital Okul Projesi")
    st.info("💡 Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True)
        except:
            st.warning("⚠️ afis.jpg yüklenmedi.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetkilendirme")
    with st.container(border=True):
        d_u = st.text_input("Denetçi Kullanıcı Adı:", key="denetci_user")
        d_p = st.text_input("Denetçi Şifresi:", type="password", key="denetci_pass")
        if st.button("Sisteme Giriş Yap"):
            if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                st.session_state['denetci_logged_in'] = True
                st.success("✅ Yetki Onaylandı!")
            else:
                st.error("❌ Hatalı Bilgiler!")

    if st.session_state.get('denetci_logged_in'):
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        s_sinif = st.selectbox("Sınıf Seçin:", siniflar)
        s_tarih = st.date_input("Tarih:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 5 Maddelik Hijyen Kontrolü")
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

# --- YÖNETİCİ SAYFASI (PASTA GRAFİKLİ) ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    
    with st.container(border=True):
        y_u = st.text_input("Yönetici Kullanıcı Adı:", key="admin_user")
        y_p = st.text_input("Yönetici Şifresi:", type="password", key="admin_pass")
        if st.button("Yönetici Panelini Aç"):
            if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                st.session_state['admin_logged_in'] = True
            else:
                st.error("❌ Yetkisiz Erişim!")

    if st.session_state.get('admin_logged_in'):
        df = st.session_state['veritabani']
        if not df.empty:
            # Pasta grafiği için sınıfların toplam puanını hesapla
            pasta_df = df.groupby("Sınıf")["Puan"].sum().reset_index()
            
            st.subheader("🏆 Okul Hijyen Dağılım Pastası")
            st.write("Pastadaki payı büyük olan sınıf en fazla puanı toplamış demektir.")
            
            # Plotly Pasta Grafiği Oluşturma
            fig = px.pie(pasta_df, values='Puan', names='Sınıf', 
                         title='Sınıfların Toplam Puan Katkısı',
                         hole=0.3, # Ortasını boş bırakarak 'donat' görünümü verir, daha moderndir
                         color_discrete_sequence=px.colors.sequential.RdBu)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.subheader("📂 Detaylı Kayıt Listesi")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Henüz analiz edilecek veri girişi yapılmamış.")
