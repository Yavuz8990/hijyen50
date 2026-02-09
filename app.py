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

def sampiyon_bul_text(veri):
    if veri.empty: return "Veri bekleniyor..."
    skorlar = veri.groupby("Sınıf")["Puan"].mean()
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

# --- 5. QR KOD VE YÖNLENDİRME ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

# --- 6. YAN MENÜ ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 7. SAYFA İÇERİKLERİ ---

if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    st.markdown("""<div style='text-align: center; padding: 10px; background: rgba(0, 210, 255, 0.05); border-radius: 20px;'><h1 style='font-family: Arial Black; color: #00D2FF; font-size: 70px; margin-bottom: 0px;'>HİJYEN 5.0</h1></div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        h_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=7))]
        st.markdown(f"<div style='text-align: center; padding: 25px; border: 3px solid #C0C0C0; border-radius: 20px; background: rgba(192, 192, 192, 0.1);'><h2 style='color: #C0C0C0; margin: 0;'>🥈 HAFTALIK LİDER</h2><p style='font-size: 24px; font-weight: bold;'>{sampiyon_bul_text(h_df)}</p></div>", unsafe_allow_html=True)
    with c2:
        a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
        st.markdown(f"<div style='text-align: center; padding: 25px; border: 3px solid #CD7F32; border-radius: 15px; background: rgba(205, 127, 50, 0.1);'><h2 style='color: #CD7F32; margin: 0;'>🥉 AYIN ŞAMPİYONU</h2><p style='font-size: 24px; font-weight: bold;'>{sampiyon_bul_text(a_df)}</p></div>", unsafe_allow_html=True)

    st.write("---")
    sozler = [
        "🧼 'Temizlik, sağlıktan önce gelir; çünkü sağlığın koruyucusudur.'",
        "✨ 'Geleceğin temiz okulu, bugünün bilinçli adımlarıyla inşa edilir.'",
        "🛡️ 'Görünmez tehlikelere karşı en güçlü kalkanımız: Hijyen.'"
    ]
    st.markdown(f"<div style='text-align: center;'><p style='font-size: 30px; color: #00D2FF; font-style: italic;'>{sozler[bugun.day % 3]}</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("Afiş yüklenemedi.")

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
                else: st.error("Hatalı Giriş!")
    else:
        st.success(f"🔓 Hoş geldiniz: {DENETCI_USER}")
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        if url_sinif and url_sinif in siniflar:
            s_sinif = url_sinif
            st.info(f"📍 Denetlenen Sınıf: **{s_sinif}**")

            with st.form("hassas_puanlama_formu"):
                st.subheader("📋 Detaylı Hijyen Değerlendirmesi")
                
                # 1. Havalandırma ve Hava Kalitesi
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi (20 Puan)"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0)
                    p1_2 = st.slider("Sınıfta ağır, rahatsız edici koku yok (0-10)", 0, 10, 0)
                
                # 2. Sınıf ve Masa Temizliği
                with st.expander("🪑 2. Sınıf ve Masa Temizliği (20 Puan)"):
                    p2_1 = st.slider("Masa yüzeyleri temiz (0-6)", 0, 6, 0)
                    p2_2 = st.slider("Sıra üstünde, altında çöp ve dağınıklık yok (0-6)", 0, 6, 0)
                    p2_3 = st.slider("Genel masa-sıra düzeni iyi (0-8)", 0, 8, 0)
                
                # 3. Zemin ve Köşe Temizliği
                with st.expander("🧹 3. Zemin ve Köşe Temizliği (20 Puan)"):
                    p3_1 = st.slider("Köşe ve diplerde çöp/toz yok (0-6)", 0, 6, 0)
                    p3_2 = st.slider("Cam kenarları ve pencere dipleri temiz (0-6)", 0, 6, 0)
                    p3_3 = st.slider("Zemin genel temizliği güzel (0-8)", 0, 8, 0)
                
                # 4. Çöp Kutusu ve Atık Yönetimi
                with st.expander("🗑️ 4. Çöp Kutusu ve Atık Yönetimi (20 Puan)"):
                    p4_1 = st.slider("Çöp kutusu doğru kullanılmış (0-6)", 0, 6, 0)
                    p4_2 = st.slider("Çöp kutusu taşmamış (0-6)", 0, 6, 0)
                    p4_3 = st.slider("Çöp kutusu çevresi temiz (0-8)", 0, 8, 0)
                
                # 5. Genel Sınıf Yüzey Temizliği
                with st.expander("✨ 5. Genel Sınıf Yüzey Temizliği (20 Puan)"):
                    p5_1 = st.slider("Duvarlarda kir, yazı ve düzensizlik yok (0-5)", 0, 5, 0)
                    p5_2 = st.slider("Panolar karışık ve dağınık değil (0-5)", 0, 5, 0)
                    p5_3 = st.slider("Tahta silinmiş, gereksiz yazı yok (0-5)", 0, 5, 0)
                    p5_4 = st.slider("Sınıfın genel görünümü güzel (0-5)", 0, 5, 0)

                if st.form_submit_button("💾 DEĞERLENDİRMEYİ MÜHÜRLE"):
                    toplam_puan = p1_1 + p1_2 + p2_1 + p2_2 + p2_3 + p3_1 + p3_2 + p3_3 + p4_1 + p4_2 + p4_3 + p5_1 + p5_2 + p5_3 + p5_4
                    df = verileri_yukle()
                    if not df[(df['Tarih'] == bugun) & (df['Sınıf'] == s_sinif)].empty:
                        st.error("❌ Bu sınıf için bugün zaten kayıt yapılmış!")
                    else:
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": toplam_puan, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success(f"✅ Başarılı! Toplam Puan: {toplam_puan}/100")
                        st.balloons()
        else:
            st.error("⚠️ Lütfen sınıfın kapısındaki karekodu okutunuz.")
        if st.button("🚪 Çıkış"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

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
        st.success("🔓 Yönetim Paneli Aktif.")
        df = verileri_yukle()
        if not df.empty:
            tab_g, tab_h, tab_a = st.tabs(["📌 Günlük", "📅 Haftalık", "📈 Aylık"])
            with tab_g:
                g_df = df[df['Tarih'] == bugun]
                if not g_df.empty: st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4), use_container_width=True)
            
            st.divider()
            st.subheader("📂 Sınıf Kayıtları")
            for sinif in sorted(df['Sınıf'].unique()):
                with st.expander(f"🏫 {sinif} Arşivi"):
                    s_df = df[df['Sınıf'] == sinif]
                    for idx, row in s_df.iterrows():
                        c1, c2 = st.columns([5, 1])
                        c1.write(f"📅 {row['Tarih']} | ⭐ {row['Puan']} Puan")
                        if c2.button("Sil", key=f"del_{sinif}_{idx}"):
                            veri_listesini_guncelle(df.drop(idx))
                            st.rerun()
        if st.button("🚪 Güvenli Çıkış"):
            st.session_state['admin_onayli'] = False
            st.rerun()
