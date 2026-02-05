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

# --- 4. VERİ SİSTEMİ FONKSİYONLARI ---
def verileri_yukle():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tarih'] = pd.to_datetime(df['Tarih']).dt.date
        return df
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
            st.image("afis.jpg", use_container_width=True)
        except:
            st.warning("⚠️ `afis.jpg` bulunamadı. Lütfen GitHub dizinine ekleyin.")

    st.write("")
    st.subheader("🎯 Proje Felsefesi")
    st.markdown("""
    * ✨ **Ölçülebilirlik Hedefi:** En büyük sorunumuz temizlik yapılmaması değil, temizliğin ölçülememesi ve sürdürülebilir bir alışkanlığa dönüşmemesidir.
    * 📊 **Veri Odaklı Yaklaşım:** Dijital olmayan bir sistemde, hijyen sadece 'şans' eseridir. Biz şansı değil, veriyi temel alıyoruz.
    """)

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
                mevcut_df = verileri_yukle()
                zaten_var_mi = mevcut_df[(mevcut_df['Tarih'] == s_tarih) & (mevcut_df['Sınıf'] == s_sinif)]
                
                if not zaten_var_mi.empty:
                    st.error(f"❌ HATA: {s_sinif} sınıfı için bu tarihte zaten bir kayıt var!")
                else:
                    puan = sum([k1, k2, k3, k4, k5]) * 20
                    yeni = pd.DataFrame([{"Tarih": s_tarih, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                    veri_kaydet(yeni)
                    st.success(f"✅ Başarılı! {s_sinif} için {puan} puan kaydedildi.")
                    st.balloons()

# --- YÖNETİCİ SAYFASI ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
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

        df = verileri_yukle()
        if not df.empty:
            df_filter = df.copy()
            df_filter['Tarih'] = pd.to_datetime(df_filter['Tarih']).dt.date
            
            # --- GRAFİKLER ---
            tab_h, tab_a = st.tabs(["📅 Haftalık Analiz", "📈 Aylık Trend"])
            with tab_h:
                h_df = df_filter[df_filter['Tarih'] >= (guncel_an - timedelta(days=7)).date()]
                if not h_df.empty:
                    fig_h = px.pie(h_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Haftalık Hijyen Dağılımı")
                    st.plotly_chart(fig_h, use_container_width=True)
            with tab_a:
                a_df = df_filter[df_filter['Tarih'] >= (guncel_an - timedelta(days=30)).date()]
                if not a_df.empty:
                    fig_a = px.pie(a_df.groupby("Sınıf")["Puan"].sum().reset_index(), values='Puan', names='Sınıf', hole=0.4, title="Aylık Hijyen Dağılımı")
                    st.plotly_chart(fig_a, use_container_width=True)

            # --- SINIFLARI AYRI AYRI GÖSTEREN ARŞİV ---
            st.divider()
            st.subheader("📂 Sınıf Bazlı Detaylı Denetim Arşivi")
            
            # Benzersiz sınıfları al ve sırala
            mevcut_siniflar = sorted(df['Sınıf'].unique())
            
            # Sınıfları yan yana veya alt alta göstermek için genişletilebilir kutular (expander) kullanalım
            for sinif in mevcut_siniflar:
                with st.expander(f"🏫 {sinif} Sınıfı Hijyen Geçmişi"):
                    sinif_df = df[df['Sınıf'] == sinif].sort_values(by="Tarih", ascending=False)
                    
                    # Sınıfa özel özet bilgi
                    ortalama = sinif_df['Puan'].mean()
                    kayit_sayisi = len(sinif_df)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Ortalama Puan", f"{ortalama:.1f}")
                    c2.metric("Toplam Denetim", kayit_sayisi)
                    
                    st.table(sinif_df[["Tarih", "Puan", "Yetkili"]])
        else:
            st.info("Sistemde henüz kayıtlı veri bulunmuyor.")
