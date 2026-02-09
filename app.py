import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz

# --- 1. YETKİ VE DOSYA AYARLARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"
YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"
DB_FILE = "denetimler.csv"

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

# --- 3. DİNAMİK SLIDER RENK TASARIMI (CSS) ---
# Bu kod slider'ın içindeki doluluk rengini kırmızıdan maviye gradyan olarak değiştirir.
st.markdown("""
    <style>
    /* Slider'ın arka plan kanalını ve dolgu rengini hedefler */
    .stSlider [data-baseweb="slider"] {
        height: 12px;
    }
    .stSlider [data-baseweb="slider"] > div:first-child {
        background: linear-gradient(to right, #FF0000 0%, #00D2FF 100%) !important;
        height: 12px;
        border-radius: 6px;
    }
    /* Slider düğmesini (thumb) beyaz ve belirgin yapar */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #FFFFFF;
        border: 2px solid #00D2FF;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)
bugun = guncel_an.date()

# --- 5. VERİ SİSTEMİ FONKSİYONLARI ---
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

# --- 6. ŞAMPİYON VE SIRALAMA HESAPLAMA ---
def sampiyon_bul_text(veri):
    if veri.empty: return "Henüz veri yok"
    skorlar = veri.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

# --- 7. QR KOD VE YÖNLENDİRME ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

# --- 8. YAN MENÜ ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 9. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    st.markdown("""<div style='text-align: center; padding: 10px; background: rgba(0, 210, 255, 0.05); border-radius: 20px;'><h1 style='font-family: Arial Black; color: #00D2FF; font-size: 70px; margin-bottom: 0px;'>HİJYEN 5.0</h1></div>""", unsafe_allow_html=True)
    
    st.write("")
    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; border: 4px solid #CD7F32; border-radius: 20px; background: rgba(205, 127, 50, 0.1); margin-bottom: 20px;">
            <h2 style="color: #CD7F32; margin: 0; font-size: 35px;">🥉 AYIN HİJYEN ŞAMPİYONU</h2>
            <p style="font-size: 45px; font-weight: bold; color: white; margin-top: 15px;">{sampiyon_bul_text(a_df)}</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🏆 AYLIK HİJYEN LİGİ SIRALAMASINI GÖR (TÜM SINIFLAR)"):
        if not a_df.empty:
            sirali_liste = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
            for i, row in sirali_liste.iterrows():
                rank = i + 1
                color = "#00D2FF"
                icon = "🔹"
                if rank == 1: color = "#FFD700"; icon = "👑"
                elif rank == 2: color = "#C0C0C0"; icon = "⭐"
                elif rank == 3: color = "#CD7F32"; icon = "✨"
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; margin: 8px 0; border-radius: 12px; border-left: 8px solid {color}; background: rgba(0,210,255,0.05);">
                        <span style="font-size: 22px; font-weight: bold; color: white;">#{rank} {icon} {row['Sınıf']} Sınıfı</span>
                        <span style="font-size: 24px; font-weight: bold; color: white;">{row['Puan']:.1f}</span>
                    </div>
                """, unsafe_allow_html=True)

    st.write("---")
    sozler = ["🧼 'Temizlik, sağlıktan önce gelir.'", "✨ 'Geleceğin temiz okulu, bugünden başlar.'", "💎 'Hijyen başarının aynasıdır.'"]
    st.markdown(f"<div style='text-align: center;'><p style='font-size: 32px; color: #00D2FF; font-style: italic; font-weight: bold;'>{sozler[bugun.day % 3]}</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ Afiş Bulunamadı.")

# --- 📝 DENETÇİ SAYFASI (RENKLİ SLIDER) ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı Giriş!")
    else:
        st.success(f"🔓 Yetkili: {DENETCI_USER}")
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        if url_sinif and url_sinif in siniflar:
            s_sinif = url_sinif
            with st.form("hassas_puanlama_formu"):
                st.subheader(f"📋 {s_sinif} Değerlendirme Formu")
                
                # Form Maddeleri
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0)
                    p1_2 = st.slider("Sınıfta ağır, rahatsız edici koku yok (0-10)", 0, 10, 0)
                with st.expander("🪑 2. Sınıf ve Masa Temizliği"):
                    p2_1 = st.slider("Masa yüzeyleri temiz (0-6)", 0, 6, 0)
                    p2_2 = st.slider("Sıra üstünde, altında çöp ve dağınıklık yok (0-6)", 0, 6, 0)
                    p2_3 = st.slider("Genel masa-sıra düzeni iyi (0-8)", 0, 8, 0)
                with st.expander("🧹 3. Zemin ve Köşe Temizliği"):
                    p3_1 = st.slider("Köşe ve diplerde çöp/toz yok (0-6)", 0, 6, 0)
                    p3_2 = st.slider("Cam kenarları ve pencere dipleri temiz (0-6)", 0, 6, 0)
                    p3_3 = st.slider("Zemin genel temizliği güzel (0-8)", 0, 8, 0)
                with st.expander("🗑️ 4. Çöp Kutusu ve Atık Yönetimi"):
                    p4_1 = st.slider("Çöp kutusu doğru kullanılmış (0-6)", 0, 6, 0)
                    p4_2 = st.slider("Çöp kutusu taşmamış (0-6)", 0, 6, 0)
                    p4_3 = st.slider("Çöp kutusu çevresi temiz (0-8)", 0, 8, 0)
                with st.expander("✨ 5. Genel Sınıf Yüzey Temizliği"):
                    p5_1 = st.slider("Duvarlarda kir, yazı ve düzensizlik yok (0-5)", 0, 5, 0)
                    p5_2 = st.slider("Panolar karışık ve dağınık değil (0-5)", 0, 5, 0)
                    p5_3 = st.slider("Tahta silinmiş, gereksiz yazı yok (0-5)", 0, 5, 0)
                    p5_4 = st.slider("Sınıfın genel görünümü güzel (0-5)", 0, 5, 0)

                if st.form_submit_button("💾 VERİYİ SİSTEME MÜHÜRLE"):
                    toplam = p1_1+p1_2+p2_1+p2_2+p2_3+p3_1+p3_2+p3_3+p4_1+p4_2+p4_3+p5_1+p5_2+p5_3+p5_4
                    df = verileri_yukle()
                    if not df[(df['Tarih'] == bugun) & (df['Sınıf'] == s_sinif)].empty:
                        st.error("❌ Bu sınıf için bugün zaten kayıt yapılmış!")
                    else:
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": toplam, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success(f"✅ Başarılı! Puan: {toplam}")
                        st.balloons()
        else: st.error("⚠️ QR kod okutulmadı.")
        if st.button("🚪 Çıkış"):
            st.session_state['denetci_onayli'] = False
            st.rerun()

# --- 📊 YÖNETİCİ PANELİ ---
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
        if not df.empty:
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
