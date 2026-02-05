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

# --- 2. SAYFA AYARLARI (İstediğin gibi sadece burası Sabun 🧼) ---
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

# --- 5. YAN MENÜ (Anlamlarına Göre İkonlar) ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

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
    st.info("💡 **BİLGİLENDİRME:** Lütfen sol menüden yetki seviyenize uygun giriş alanını seçiniz.")
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ `afis.jpg` dosyası bulunamadı.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Ekranı")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            st.subheader("🔐 Kimlik Doğrulama")
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Sisteme Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı kullanıcı adı veya şifre!")
    else:
        st.success(f"🔓 Oturum Açıldı: {DENETCI_USER}")
        if st.button("🚪 Oturumu Kapat"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        st.divider()
        
        # Denetim Formu
        col_s, col_t = st.columns(2)
        with col_s:
            s_sinif = st.selectbox("🏫 Denetlenecek Sınıf:", ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"])
        with col_t:
            s_tarih = st.date_input("📅 Denetim Tarihi:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 Hijyen Değerlendirme Maddeleri")
            k1 = st.checkbox("💨 Havalandırma Durumu")
            k2 = st.checkbox("🪑 Sıra ve Masa Temizliği")
            k3 = st.checkbox("🧹 Zemin ve Köşelerin Hijyeni")
            k4 = st.checkbox("🗑️ Çöp Kutusu ve Atık Yönetimi")
            k5 = st.checkbox("✨ Genel Sınıf Tertibi")
            
            if st.form_submit_button("💾 VERİYİ SİSTEME MÜHÜRLE"):
                puan = sum([k1, k2, k3, k4, k5]) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                veri_kaydet(yeni)
                st.success(f"✅ Başarılı! {s_sinif} için {puan} puan arşive kaydedildi.")
                st.balloons()

# --- YÖNETİCİ SAYFASI ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Paneli")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
            st.subheader("🔐 Yönetici Girişi")
            y_u = st.text_input("Yönetici Adı:", key="y_u")
            y_p = st.text_input("Yönetici Şifresi:", type="password", key="y_p")
            if st.button("Paneli Kilidini Aç"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else: st.error("❌ Yetkisiz Erişim Denemesi!")
    else:
        st.success("🔓 Yönetim Paneline Erişim Onaylandı.")
        if st.button("🚪 Çıkış Yap"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = verileri_yukle()
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            tab_h, tab_a = st.tabs(["📅 Haftalık Analiz", "📈 Aylık Trend"])
            
            with tab_h:
                h_limit = (guncel_an - timedelta(days=7)).date()
                h_df = df[df['Tarih'].dt.date >= h_limit]
                if not h_df.empty:
                    h_data = h_df.groupby("Sınıf")["Puan"].mean().reset_index()
                    fig_h = px.bar(h_data, x='Sınıf', y='Puan', color='Puan', color_continuous_scale='Blues', text_auto='.1f')
                    st.plotly_chart(fig_h, use_container_width=True)
                else: st.info("Bu hafta için henüz kayıt bulunmuyor.")

            with tab_a:
                a_limit = (guncel_an - timedelta(days=30)).date()
                a_df = df[df['Tarih'].dt.date >= a_limit]
                if not a_df.empty:
                    a_data = a_df.groupby("Sınıf")["Puan"].mean().reset_index()
                    fig_a = px.bar(a_data, x='Sınıf', y='Puan', color='Puan', color_continuous_scale='GnBu', text_auto='.1f')
                    st.plotly_chart(fig_a, use_container_width=True)
                else: st.info("Son 30 gün için kayıt bulunmuyor.")
            
            st.write("### 📂 Dijital Denetim Arşivi")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Sistemde henüz kayıtlı veri bulunmuyor.")
