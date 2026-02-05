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
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİTABANI HAFIZASI ---
if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

# --- 5. YAN MENÜ ---
st.sidebar.title("🧼 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- 6. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA (YENİ TEKNOLOJİK TASARIM) ---
if sayfa == "🏠 Ana Sayfa":
    # Google Fonts üzerinden teknoloji fontu çekme ve Stil Ayarları
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        
        .main-container {
            text-align: center;
            padding: 20px;
        }
        .main-title {
            font-family: 'Orbitron', sans-serif;
            color: #00D2FF;
            font-size: 50px;
            font-weight: 700;
            letter-spacing: 5px;
            text-shadow: 0 0 15px rgba(0, 210, 255, 0.7), 0 0 30px rgba(0, 210, 255, 0.4);
            margin-bottom: 5px;
        }
        .sub-title {
            font-family: 'Orbitron', sans-serif;
            color: #ffffff;
            font-size: 22px;
            font-weight: 400;
            letter-spacing: 2px;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        </style>
        
        <div class="main-container">
            <div class="main-title">HİJYEN 5.0</div>
            <div class="sub-title">GELECEĞİN TEMİZ OKULU</div>
        </div>
    """, unsafe_allow_html=True)

    st.info("💡 **SİSTEM MESAJI:** Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True, caption="Dijital Dönüşüm & Hijyen Standartları")
        except:
            st.warning("⚠️ `afis.jpg` dosyası GitHub dizininde bulunamadı.")

    st.write("---")
    
    # Alt Bilgi Kartları
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🧬 **Veri Madenciliği**")
        st.write("Okul hijyeni dijital verilere dönüşüyor.")
    with c2:
        st.markdown("#### 📈 **Analitik Takip**")
        st.write("Haftalık ve aylık gelişim grafikleri.")
    with c3:
        st.markdown("#### 🛡️ **Güvenli Erişim**")
        st.write("Çift katmanlı yetkilendirme protokolü.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Yetkilendirme")
    
    if 'denetci_onayli' not in st.session_state:
        st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else:
                    st.error("❌ Hatalı Giriş!")
    else:
        st.success(f"✅ Yetki Onaylandı: {DENETCI_USER}")
        if st.button("Oturumu Kapat"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        s_sinif = st.selectbox("Sınıf Seçin:", siniflar)
        s_tarih = st.date_input("Tarih:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 5 Maddelik Değerlendirme")
            m = [st.checkbox(k) for k in ["Havalandırma Durumu", "Sıra/Masa Temizliği", "Zemin Hijyeni", "Çöp Kutusu Düzeni", "Genel Tertip"]]
            if st.form_submit_button("VERİYİ KAYDET"):
                skor = sum(m) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": skor, "Yetkili": DENETCI_USER}])
                st.session_state['veritabani'] = pd.concat([st.session_state['veritabani'], yeni], ignore_index=True)
                st.success("Veri sisteme mühürlendi!")
                st.balloons()

# --- YÖNETİCİ SAYFASI ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    
    if 'admin_onayli' not in st.session_state:
        st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
            y_u = st.text_input("Yönetici Adı:", key="y_u")
            y_p = st.text_input("Yönetici Şifresi:", type="password", key="y_p")
            if st.button("Paneli Aç"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else:
                    st.error("❌ Yetkisiz Erişim!")
    else:
        st.success("🔓 Yönetici Erişimi Aktif")
        if st.button("Yönetici Çıkış"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = st.session_state['veritabani'].copy()
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            t_h, t_a = st.tabs(["📅 HAFTALIK", "📆 AYLIK"])
            
            with t_h:
                h_limit = (guncel_an - timedelta(days=7)).date()
                h_df = df[df['Tarih'].dt.date >= h_limit]
                if not h_df.empty:
                    fig_h = px.pie(h_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Haftalık Sınıf Dağılımı")
                    st.plotly_chart(fig_h, use_container_width=True)
                else: st.info("Haftalık veri yok.")

            with t_a:
                a_limit = (guncel_an - timedelta(days=30)).date()
                a_df = df[df['Tarih'].dt.date >= a_limit]
                if not a_df.empty:
                    fig_a = px.pie(a_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Aylık Sınıf Dağılımı")
                    st.plotly_chart(fig_a, use_container_width=True)
                else: st.info("Aylık veri yok.")
