import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import plotly.express as px

# --- 1. YETKİ VE GÜVENLİK ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİTABANI HAFIZASI ---
if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

# --- 5. YAN MENÜ ---
st.sidebar.title("🧼 Hijyen 5.0 Navigasyon")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- 6. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA (TAM İSTEDİĞİN TASARIM) ---
if sayfa == "🏠 Ana Sayfa":
    # HTML ile Başlık ve Slogan Senkronizasyonu
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0, 210, 255, 0.05); border-radius: 20px; border: 1px solid rgba(0, 210, 255, 0.1);">
            <h1 style="font-family: 'Arial Black', sans-serif; color: #00D2FF; font-size: 75px; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(0,210,255,0.6);">
                HİJYEN 5.0
            </h1>
            <p style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF; font-size: 26px; font-weight: bold; letter-spacing: 6px; margin-top: -10px; opacity: 0.9;">
                GELECEĞİN TEMİZ OKULU
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Boşluk
    st.info("💡 **DİJİTAL REHBER:** Denetim raporu girişi veya analiz takibi için lütfen sol menüyü kullanın.")
    
    st.write("---")
    
    # Afiş Bölümü
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True, caption="Okulumuzun Dijital Hijyen Standartları")
        except:
            st.warning("⚠️ Afiş görseli (afis.jpg) henüz GitHub'a yüklenmemiş.")

    st.write("---")
    
    # Teknolojik Özellik Kartları
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🧬 **Veri Mühürleme**")
        st.write("Denetimler geri dönülemez şekilde dijital arşive kaydedilir.")
    with c2:
        st.markdown("### 📊 **Anlık Analiz**")
        st.write("Pasta grafikleri ile okulun hijyen payı saniyeler içinde hesaplanır.")
    with c3:
        st.markdown("### 🛡️ **Hiyerarşik Güvenlik**")
        st.write("Denetçi ve Yönetici için ayrıştırılmış özel erişim kapıları.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetki Girişi")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("Hatalı Giriş!")
    else:
        st.success(f"Hoş geldiniz, {DENETCI_USER}. Lütfen puanlama yapın.")
        if st.button("Güvenli Çıkış"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        s_sinif = st.selectbox("Sınıf Seçiniz:", siniflar)
        s_tarih = st.date_input("Tarih:", guncel_an)

        with st.form("puan_formu"):
            k1 = st.checkbox("1. Havalandırma")
            k2 = st.checkbox("2. Sıra/Masa")
            k3 = st.checkbox("3. Zemin Hijyeni")
            k4 = st.checkbox("4. Çöp Kutusu")
            k5 = st.checkbox("5. Genel Düzen")
            if st.form_submit_button("VERİYİ KAYDET"):
                puan = sum([k1, k2, k3, k4, k5]) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                st.session_state['veritabani'] = pd.concat([st.session_state['veritabani'], yeni], ignore_index=True)
                st.success(f"Kaydedildi: {s_sinif} -> {puan} Puan")

# --- YÖNETİCİ SAYFASI ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
            y_u = st.text_input("Yönetici Adı:", key="y_u")
            y_p = st.text_input("Şifre:", type="password", key="y_p")
            if st.button("Paneli Aç"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else: st.error("Yetkisiz Erişim!")
    else:
        st.success("Yönetici Erişimi Onaylandı.")
        if st.button("Oturumu Kapat"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = st.session_state['veritabani'].copy()
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            t_h, t_a = st.tabs(["📊 HAFTALIK", "📈 AYLIK"])
            with t_h:
                h_df = df[df['Tarih'].dt.date >= (guncel_an - timedelta(days=7)).date()]
                if not h_df.empty:
                    fig = px.pie(h_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Tüm Sınıfların Haftalık Dağılımı")
                    st.plotly_chart(fig, use_container_width=True)
            with t_a:
                a_df = df[df['Tarih'].dt.date >= (guncel_an - timedelta(days=30)).date()]
                if not a_df.empty:
                    fig2 = px.pie(a_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Tüm Sınıfların Aylık Dağılımı")
                    st.plotly_chart(fig2, use_container_width=True)
        else: st.info("Kayıt bulunamadı.")
