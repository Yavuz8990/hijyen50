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

# --- 5. QR KOD KONTROLÜ ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0

# --- 6. YAN MENÜ ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 7. SAYFA İÇERİKLERİ ---

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
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ `afis.jpg` bulunamadı.")

elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            if url_sinif: st.success(f"📱 QR Okutuldu: {url_sinif}")
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı Giriş!")
    else:
        st.success(f"🔓 Hoş geldiniz: {DENETCI_USER}")
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        if url_sinif and url_sinif in siniflar:
            s_sinif = url_sinif
            with st.form("puanlama_formu"):
                st.subheader(f"📋 {s_sinif} Değerlendirme Formu")
                k1 = st.checkbox("💨 Havalandırma Durumu")
                k2 = st.checkbox("🪑 Sıra ve Masa Temizliği")
                k3 = st.checkbox("🧹 Zemin ve Köşelerin Hijyeni")
                k4 = st.checkbox("🗑️ Çöp Kutusu ve Atık Yönetimi")
                k5 = st.checkbox("✨ Genel Sınıf Tertibi")
                if st.form_submit_button("💾 VERİYİ MÜHÜRLE"):
                    df = verileri_yukle()
                    if not df[(df['Tarih'] == bugun) & (df['Sınıf'] == s_sinif)].empty:
                        st.error("❌ Bu sınıf için bugün zaten kayıt yapılmış!")
                    else:
                        puan = sum([k1, k2, k3, k4, k5]) * 20
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success("✅ Kaydedildi!")
                        st.balloons()
        else:
            st.error("⚠️ Lütfen sınıf karekodunu okutunuz.")
        if st.button("🚪 Çıkış"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

# --- 📊 YÖNETİCİ PANELİ (ŞAMPİYONLAR NOTU EKLENDİ) ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False

    if not st.session_state['admin_onayli']:
        with st.container(border=True):
            y_u = st.text_input("Yönetici Adı:", key="y_u")
            y_p = st.text_input("Şifre:", type="password", key="y_p")
            if st.button("Giriş"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı!")
    else:
        df = verileri_yukle()
        
        # --- ŞAMPİYONLARI HESAPLAMA ---
        def sampiyon_bul(veri, baslik):
            if not veri.empty:
                skorlar = veri.groupby("Sınıf")["Puan"].mean()
                en_yuksek = skorlar.max()
                sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
                return f"{baslik}: **{', '.join(sampiyonlar)}** ({int(en_yuksek)} Puan)"
            return f"{baslik}: Veri bulunamadı."

        st.subheader("🏆 Hijyen Şampiyonları")
        with st.container(border=True):
            # Günlük
            g_df = df[df['Tarih'] == bugun]
            # Haftalık
            h_df = df[df['Tarih'] >= (bugun - timedelta(days=7))]
            # Aylık
            a_df = df[df['Tarih'] >= (bugun - timedelta(days=30))]

            st.write(f"🥇 **1. Bugünün Şampiyonu:** {sampiyon_bul(g_df, '').replace(': ', '')}")
            st.write(f"🥈 **2. Haftanın Şampiyonu:** {sampiyon_bul(h_df, '').replace(': ', '')}")
            st.write(f"🥉 **3. Ayın Şampiyonu:** {sampiyon_bul(a_df, '').replace(': ', '')}")

        st.divider()
        
        # Grafik Sekmeleri
        tab_g, tab_h, tab_a = st.tabs(["📌 Günlük", "📅 Haftalık", "📈 Aylık"])
        with tab_g:
            if not g_df.empty: st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4, title="Bugünkü Dağılım"), use_container_width=True)
        
        # Arşiv ve Silme
        st.subheader("📂 Kayıt Yönetimi")
        for sinif in sorted(df['Sınıf'].unique()):
            with st.expander(f"🏫 {sinif} Kayıtları"):
                s_df = df[df['Sınıf'] == sinif]
                for idx, row in s_df.iterrows():
                    c1, c2 = st.columns([5, 1])
                    c1.write(f"📅 {row['Tarih']} | ⭐ {row['Puan']} Puan")
                    if c2.button("Sil", key=f"del_{sinif}_{idx}"):
                        veri_listesini_guncelle(df.drop(idx))
                        st.rerun()

        if st.button("🚪 Çıkış"):
            st.session_state['admin_onayli'] = False
            st.rerun()
