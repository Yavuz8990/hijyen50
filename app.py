import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go

# --- 1. YETKİ VE DOSYA AYARLARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"
DB_FILE = "denetimler.csv"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

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
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"])

# --- 6. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0, 210, 255, 0.05); border-radius: 20px;">
            <h1 style="font-family: 'Arial Black', sans-serif; color: #00D2FF; font-size: 65px; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(0,210,255,0.6);">
                HİJYEN 5.0
            </h1>
            <p style="font-family: 'Trebuchet MS', sans-serif; color: #FFFFFF; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin-top: -10px; opacity: 0.9;">
                GELECEĞİN TEMİZ OKULU
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **BİLGİLENDİRME:** Lütfen sol menüden yetki seviyenize uygun giriş alanını seçiniz.")
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("afis.jpg", use_container_width=True, caption="Dijital Dönüşüm & Hijyen Standartları")
        except:
            st.warning("⚠️ `afis.jpg` bulunamadı. Lütfen GitHub'a yükleyin.")

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
                else: st.error("❌ Hatalı Denetçi Bilgileri!")
    else:
        st.success(f"🔓 Oturum Açıldı: {DENETCI_USER}")
        if st.button("🚪 Oturumu Kapat"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        col_s, col_t = st.columns(2)
        with col_s: s_sinif = st.selectbox("🏫 Denetlenecek Sınıf:", siniflar)
        with col_t: s_tarih = st.date_input("📅 Denetim Tarihi:", guncel_an)

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
    st.title("📊 Yönetici Analiz Merkezi")
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
                else: st.error("❌ Yetkisiz Erişim!")
    else:
        st.success("🔓 Yönetim Paneline Erişim Onaylandı.")
        if st.button("🚪 Çıkış Yap"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        # Mum Grafiği Fonksiyonu
        def ciz_teknolojik_mum(veri, baslik):
            if veri.empty: return None
            stats = veri.groupby("Sınıf")["Puan"].agg(['mean', 'max', 'min']).reset_index()
            fig = go.Figure(data=[go.Candlestick(
                x=stats['Sınıf'],
                open=stats['mean'], high=stats['max'],
                low=stats['min'], close=stats['mean'],
                increasing_line_color='#00D2FF', decreasing_line_color='#00D2FF'
            )])
            fig.update_layout(title=baslik, template="plotly_dark", xaxis_rangeslider_visible=False,
                            yaxis_title="Puan", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#00D2FF"))
            return fig

        df = verileri_yukle()
        if not df.empty:
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            tab_h, tab_a = st.tabs(["📅 Haftalık Analiz", "📈 Aylık Trend"])
            
            with tab_h:
                h_df = df[df['Tarih'].dt.date >= (guncel_an - timedelta(days=7)).date()]
                fig_h = ciz_teknolojik_mum(h_df, "Haftalık Sınıf Hijyen Endeksi")
                if fig_h: st.plotly_chart(fig_h, use_container_width=True)
                else: st.info("Haftalık veri yok.")

            with tab_a:
                a_df = df[df['Tarih'].dt.date >= (guncel_an - timedelta(days=30)).date()]
                fig_a = ciz_teknolojik_mum(a_df, "Aylık Hijyen Trend Analizi")
                if fig_a: st.plotly_chart(fig_a, use_container_width=True)
                else: st.info("Aylık veri yok.")
            
            st.write("### 📂 Dijital Denetim Arşivi")
            st.dataframe(df, use_container_width=True)
        else: st.info("Sistemde henüz kayıtlı veri bulunmuyor.")
