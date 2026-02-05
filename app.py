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
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

# --- 3. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)
bugun = guncel_an.date()

# --- 4. VERİ SİSTEMİ FONKSİYONLARI ---
def verileri_yukle():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tarih'] = pd.to_datetime(df['Tarih']).dt.date
        return df
    else:
        return pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

def veri_listesini_guncelle(df):
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
            st.image("afis.jpg", use_container_width=True)
        except:
            st.warning("⚠️ `afis.jpg` bulunamadı.")

    st.write("")
    st.subheader("🎯 Proje Felsefesi")
    st.markdown("""
    * ✨ **Ölçülebilirlik Hedefi:** En büyük sorunumuz temizlik yapılmaması değil, temizliğin ölçülememesi ve sürdürülebilir bir alışkanlığa dönüşmemesidir.
    * 📊 **Veri Odaklı Yaklaşım:** Dijital olmayan bir sistemde, hijyen sadece 'şans' eseridir. Biz şansı değil, veriyi temel alıyoruz.
    """)

# --- 📝 DENETÇİ SAYFASI (GÜVENLİ VE QR UYUMLU) ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Ekranı")
    
    # URL'den sınıf bilgisini yakala (Öğrenci okutsa bile burada bir şey görmez)
    query_params = st.query_params
    url_sinif = query_params.get("sinif", None)
    
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    # GÜVENLİK KAPISI: Önce şifre sorma
    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            st.subheader("🔐 Yetkili Erişimi")
            st.write("Değerlendirme formunu açmak için lütfen bilgilerinizi giriniz.")
            d_u = st.text_input("Denetçi Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Sisteme Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else:
                    st.error("❌ Hatalı Giriş! Bu alan sadece yetkili denetçilere özeldir.")
        st.warning("⚠️ Barkod okutmuş olsanız dahi giriş yapmadan işlem yapılamaz.")
    
    # ŞİFRE DOĞRUYSA FORM AÇILIR
    else:
        st.success(f"🔓 Hoş geldiniz Yetkili: {DENETCI_USER}")
        if st.button("🚪 Oturumu Kapat"):
            st.session_state['denetci_onayli'] = False
            st.rerun()
        
        st.divider()
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        # Eğer QR okutulduysa ve şifre girildiyse o sınıfı otomatik seç
        default_idx = 0
        if url_sinif in siniflar:
            default_idx = siniflar.index(url_sinif)
            st.info(f"📱 **QR Algılandı:** {url_sinif} sınıfı formu sizin için hazırlandı.")

        col_s, col_t = st.columns(2)
        with col_s: s_sinif = st.selectbox("🏫 Denetlenecek Sınıf:", siniflar, index=default_idx)
        with col_t: s_tarih = st.date_input("📅 Denetim Tarihi:", bugun)

        with st.form("puanlama_formu"):
            st.subheader("📋 Hijyen Değerlendirme Maddeleri")
            k1 = st.checkbox("💨 Havalandırma Durumu")
            k2 = st.checkbox("🪑 Sıra ve Masa Temizliği")
            k3 = st.checkbox("🧹 Zemin ve Köşelerin Hijyeni")
            k4 = st.checkbox("🗑️ Çöp Kutusu ve Atık Yönetimi")
            k5 = st.checkbox("✨ Genel Sınıf Tertibi")
            
            if st.form_submit_button("💾 VERİYİ SİSTEME MÜHÜRLE"):
                df = verileri_yukle()
                zaten_var_mi = df[(df['Tarih'] == s_tarih) & (df['Sınıf'] == s_sinif)]
                
                if not zaten_var_mi.empty:
                    st.error(f"❌ Bu sınıf ({s_sinif}) için bugün zaten kayıt yapılmış!")
                else:
                    puan = sum([k1, k2, k3, k4, k5]) * 20
                    yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                    veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                    st.success(f"✅ Başarılı! {s_sinif} için {puan} puan arşive kaydedildi.")
                    st.balloons()

# --- 📊 YÖNETİCİ PANELİ ---
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
        st.success("🔓 Yönetim Paneli Aktif.")
        if st.button("🚪 Güvenli Çıkış"):
            st.session_state['admin_onayli'] = False
            st.rerun()

        df = verileri_yukle()
        if not df.empty:
            tab_g, tab_h, tab_a = st.tabs(["📌 Günlük", "📅 Haftalık", "📈 Aylık"])
            with tab_g:
                g_df = df[df['Tarih'] == bugun]
                if not g_df.empty:
                    st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4), use_container_width=True)
                else: st.info("Bugün veri yok.")
            
            # --- TARİH ARAMA ---
            st.divider()
            secilen_tarih = st.date_input("🔍 Tarih Sorgula:", bugun)
            t_df = df[df['Tarih'] == secilen_tarih]
            if not t_df.empty:
                st.dataframe(t_df, use_container_width=True)
                if st.button(f"🗑️ {secilen_tarih} Tarihli Tüm Verileri Sil"):
                    veri_listesini_guncelle(df[df['Tarih'] != secilen_tarih])
                    st.rerun()

            # --- SINIF BAZLI YÖNETİM ---
            st.divider()
            st.subheader("📂 Sınıf Yönetimi")
            for sinif in sorted(df['Sınıf'].unique()):
                with st.expander(f"🏫 {sinif} Kayıtları"):
                    s_df = df[df['Sınıf'] == sinif]
                    for idx, row in s_df.iterrows():
                        c1, c2 = st.columns([5, 1])
                        c1.write(f"📅 {row['Tarih']} | ⭐ {row['Puan']} Puan")
                        if c2.button("Sil", key=f"del_{sinif}_{idx}"):
                            veri_listesini_guncelle(df.drop(idx))
                            st.rerun()
        else:
            st.info("Kayıt bulunmuyor.")
