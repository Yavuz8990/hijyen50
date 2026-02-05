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
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🛡️", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 4. VERİ SİSTEMİ FONKSİYONLARI ---
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
st.sidebar.title("🧼 Hijyen 5.0")
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
    st.info("💡 **SİSTEM MESAJI:** Lütfen işlem yapmak için soldaki menüden yetki seviyenize göre giriş yapınız.")
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ `afis.jpg` bulunamadı.")

# --- DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Giriş Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Geçersiz Bilgiler!")
    else:
        st.success(f"✅ Oturum Açıldı: {DENETCI_USER}")
        if st.button("Çıkış Yap"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        s_sinif = st.selectbox("Sınıf Seçiniz:", siniflar)
        s_tarih = st.date_input("Denetim Tarihi:", guncel_an)

        with st.form("puanlama_formu"):
            st.subheader("📋 Hijyen Kriterleri")
            k1 = st.checkbox("1. Havalandırma Durumu")
            k2 = st.checkbox("2. Sıra/Masa Temizliği")
            k3 = st.checkbox("3. Zemin ve Köşeler")
            k4 = st.checkbox("4. Çöp Kutusu Düzeni")
            k5 = st.checkbox("5. Genel Tertip")
            if st.form_submit_button("ONAYLA VE GÖNDER"):
                puan = sum([k1, k2, k3, k4, k5]) * 20
                yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                veri_kaydet(yeni)
                st.success(f"Kayıt Başarılı! Veri kaydedildi.")
                st.balloons()

# --- YÖNETİCİ SAYFASI (SÜTUN GRAFİKLİ) ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Paneli")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
            y_u = st.text_input("Yönetici Adı:", key="y_u")
            y_p = st.text_input("Yönetici Şifresi:", type="password", key="y_p")
            if st.button("Sistemi Aç"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else: st.error("❌ Yetkisiz Giriş!")
    else:
        st.success("🔓 Yönetici Erişimi Onaylandı.")
        if st.button("Oturumu Kapat"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = verileri_yukle()
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            tab_h, tab_a = st.tabs(["📊 HAFTALIK PERFORMANS", "📈 AYLIK TREND"])
            
            with tab_h:
                h_limit = (guncel_an - timedelta(days=7)).date()
                h_df = df[df['Tarih'].dt.date >= h_limit]
                if not h_df.empty:
                    # Sınıf bazlı ortalama puan hesaplama
                    h_chart_data = h_df.groupby("Sınıf")["Puan"].mean().reset_index()
                    
                    # Sütun Grafiği
                    fig_h = px.bar(h_chart_data, x='Sınıf', y='Puan', 
                                   title="Sınıfların Haftalık Hijyen Ortalaması",
                                   color='Puan', # Puana göre renk değişsin
                                   color_continuous_scale='GnBu',
                                   text='Puan') # Sütun üstünde puan yazsın
                    fig_h.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                    st.plotly_chart(fig_h, use_container_width=True)
                else: st.info("Haftalık veri yok.")

            with tab_a:
                a_limit = (guncel_an - timedelta(days=30)).date()
                a_df = df[df['Tarih'].dt.date >= a_limit]
                if not a_df.empty:
                    # Sınıf bazlı toplam puan
                    a_chart_data = a_df.groupby("Sınıf")["Puan"].mean().reset_index()
                    
                    # Sütun Grafiği
                    fig_a = px.bar(a_chart_data, x='Sınıf', y='Puan', 
                                   title="Sınıfların Aylık Hijyen Ortalaması",
                                   color='Puan',
                                   color_continuous_scale='Viridis',
                                   text='Puan')
                    fig_a.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                    st.plotly_chart(fig_a, use_container_width=True)
                else: st.info("Aylık veri yok.")
            
            st.write("### 📄 Denetim Arşivi")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Kayıt bulunamadı.")
