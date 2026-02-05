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
st.set_page_config(page_title="H5.0 Profesyonel Panel", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİTABANI SÜREKLİLİĞİ ---
# Verilerin oturum boyunca silinmemesi için session_state kullanılır.
if 'veritabani' not in st.session_state:
    # Başlangıçta boş kalmaması için geçmişe dönük simüle edilmiş veriler
    st.session_state['veritabani'] = pd.DataFrame([
        {"Tarih": (guncel_an - timedelta(days=2)).date(), "Sınıf": "9A", "Puan": 100, "Yetkili": "admin"},
        {"Tarih": (guncel_an - timedelta(days=10)).date(), "Sınıf": "10B", "Puan": 80, "Yetkili": "admin"},
        {"Tarih": (guncel_an - timedelta(days=15)).date(), "Sınıf": "11C", "Puan": 60, "Yetkili": "admin"},
        {"Tarih": (guncel_an - timedelta(days=1)).date(), "Sınıf": "12A", "Puan": 100, "Yetkili": "admin"}
    ])

# --- 5. YAN MENÜ ---
st.sidebar.title("🧼 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- ANA SAYFA ---
# --- ANA SAYFA TASARIMI (YENİ SLOGAN) ---
if sayfa == "🏠 Ana Sayfa":
    # Teknolojik Başlık ve Stil Ayarları
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        
        .main-title {
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            color: #00D2FF;
            font-size: 42px;
            font-weight: 700;
            letter-spacing: 3px;
            text-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .sub-title {
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            color: #ffffff;
            font-size: 18px;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 40px;
        }
        </style>
        
        <div class="main-title">HİJYEN 5.0</div>
        <div class="sub-title">GELECEĞİN TEMİZ OKULU</div>
    """, unsafe_allow_html=True)

    # Bilgilendirme Kutusu
    st.info("🚨 **SİSTEM ERİŞİMİ:** Lütfen soldaki menüden yetki seviyenize göre giriş yapınız.")
    
    st.write("---")
    
    # Afiş Görseli
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True, caption="Dijital Dönüşüm & Hijyen Standartları")
        except:
            st.warning("⚠️ `afis.jpg` bulunamadı. Lütfen GitHub deponuza yükleyin.")

    st.write("---")
    
    # Teknolojik Bilgi Kartları
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🧬 **Akıllı Veri**")
        st.write("Her denetim dijital bir imza ile kaydedilir.")
    with c2:
        st.markdown("### 📈 **Gerçek Zamanlı**")
        st.write("Haftalık ve aylık analizler anında güncellenir.")
    with c3:
        st.markdown("### 🛡️ **Tam Güvenlik**")
        st.write("Çift kademeli admin/denetçi doğrulama sistemi.")

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
        if st.button("Güvenli Çıkış"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        s_sinif = st.selectbox("Sınıf Seçin:", siniflar)
        s_tarih = st.date_input("Tarih:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 5 Maddelik Değerlendirme")
            m = [st.checkbox(f"Kriter {i+1}") for i in range(5)]
            if st.form_submit_button("VERİYİ KAYDET"):
                skor = sum(m) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": skor, "Yetkili": DENETCI_USER}])
                st.session_state['veritabani'] = pd.concat([st.session_state['veritabani'], yeni], ignore_index=True)
                st.success("Veri başarıyla arşive eklendi!")
                st.balloons()

# --- YÖNETİCİ SAYFASI (HAFTALIK/AYLIK AYRIMLI) ---
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
        if st.button("Oturumu Kapat"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = st.session_state['veritabani'].copy()
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        
        tab_h, tab_a = st.tabs(["📅 Haftalık Analiz (Son 7 Gün)", "📆 Aylık Analiz (Son 30 Gün)"])

        with tab_h:
            st.subheader("Haftalık Tüm Sınıfların Hijyen Dağılımı")
            h_limit = (guncel_an - timedelta(days=7)).date()
            h_df = df[df['Tarih'].dt.date >= h_limit]
            
            if not h_df.empty:
                h_sum = h_df.groupby("Sınıf")["Puan"].sum().reset_index()
                fig_h = px.pie(h_sum, values='Puan', names='Sınıf', hole=0.4,
                             title="Bu Hafta Tüm Sınıfların Puan Oranı",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_h, use_container_width=True)
                st.dataframe(h_df, use_container_width=True)
            else:
                st.info("Bu hafta için henüz veri girişi yok.")

        with tab_a:
            st.subheader("Aylık Tüm Sınıfların Hijyen Dağılımı")
            a_limit = (guncel_an - timedelta(days=30)).date()
            a_df = df[df['Tarih'].dt.date >= a_limit]
            
            if not a_df.empty:
                a_sum = a_df.groupby("Sınıf")["Puan"].sum().reset_index()
                fig_a = px.pie(a_sum, values='Puan', names='Sınıf', hole=0.4,
                             title="Bu Ay Tüm Sınıfların Puan Oranı",
                             color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_a, use_container_width=True)
                st.dataframe(a_df, use_container_width=True)
            else:
                st.info("Bu ay için henüz veri girişi yok.")



