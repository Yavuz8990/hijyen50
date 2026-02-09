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

# --- 3. DİNAMİK TASARIM VE SİYAH RAKAM DÜZENLEMESİ (CSS) ---
st.markdown("""
    <style>
    /* Slider doluluk rengini kırmızıdan maviye gradyan yapar */
    .stSlider [data-baseweb="slider"] > div:first-child {
        background: linear-gradient(to right, #FF0000 0%, #00D2FF 100%) !important;
        height: 12px;
        border-radius: 6px;
    }
    
    /* Slider üzerindeki ana başlıkları SİYAH ve KALIN yapar */
    .stSlider [data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* Slider'ın o anki değerini (rakamı) SİYAH ve KALIN yapar */
    .stSlider div[data-testid="stThumbValue"] {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* Slider'ın altındaki sınır rakamlarını (0, 10 vb.) SİYAH yapar */
    .stSlider [data-baseweb="slider"] + div div {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Genel metinlerin okunabilirliği */
    .stMarkdown p {
        font-weight: 500;
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
    if veri.empty: return "Veri bekleniyor..."
    skorlar = veri.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

# --- 7. QR KOD VE OTOMATİK YÖNLENDİRME ---
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
    st.markdown("""<div style='text-align: center; padding: 10px; background: rgba(0, 210, 255, 0.05); border-radius: 20px;'><h1 style='font-family: Arial Black; color: #00D2FF; font-size: 70px; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(0,210,255,0.6);'>HİJYEN 5.0</h1></div>""", unsafe_allow_html=True)
    
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
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; margin: 8px 0; border-radius: 12px; border-left: 8px solid {color}; background: rgba(0,210,255,0.05); border: 1px solid {color};">
                        <span style="font-size: 20px; font-weight: bold; color: white;">#{rank} {icon} {row['Sınıf']} Sınıfı</span>
                        <span style="font-size: 22px; font-weight: bold; color: white;">{row['Puan']:.1f}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sıralama için henüz yeterli veri toplanmadı.")

    st.write("---")
    
    # GÜNÜN SÖZÜ (FOTOĞRAFIN ÜSTÜNDE)
    sozler = [
        "🧼 'Temizlik, sağlıktan önce gelir; çünkü sağlığın koruyucusudur.'",
        "✨ 'Geleceğin temiz okulu, bugünün bilinçli adımlarıyla inşa edilir.'",
        "🧪 'Hijyen bir tercih değil, toplumun her ferdine olan sorumluluğumuzdur.'",
        "💎 'Temizlik, başarının aynasıdır; parlayan bir gelecek temiz sınıflarda yetişir.'"
    ]
    secilen_soz = sozler[bugun.day % 4]
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><p style='font-size: 32px; color: #00D2FF; font-style: italic; font-weight: bold;'>{secilen_soz}</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ Afiş Bulunamadı.")

# --- 📝 DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            if url_sinif: st.success(f"📱 QR Okutuldu: {url_sinif} sınıfı için giriş yapınız.")
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Sisteme Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı Giriş!")
    else:
        st.success(f"🔓 Yetkili Girişi Başarılı: {DENETCI_USER}")
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        if url_sinif and url_sinif in siniflar:
            s_sinif = url_sinif
            st.info(f"📍 Denetlenen Sınıf: **{s_sinif}**")

            with st.form("hassas_puanlama_formu"):
                st.subheader("📋 Hijyen Değerlendirme Formu")
                
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0)
                    p1_2 = st.slider("Sınıfta ağır koku yok (0-10)", 0, 10, 0)
                
                with st.expander("🪑 2. Sınıf ve Masa Temizliği"):
                    p2_1 = st.slider("Masa yüzeyleri temiz (0-6)", 0, 6, 0)
                    p2_2 = st.slider("Sıra altı/üstü çöp yok (0-6)", 0, 6, 0)
                    p2_3 = st.slider("Genel masa-sıra düzeni (0-8)", 0, 8, 0)
                
                with st.expander("🧹 3. Zemin ve Köşe Temizliği"):
                    p3_1 = st.slider("Köşe ve diplerde toz yok (0-6)", 0, 6, 0)
                    p3_2 = st.slider("Cam kenarları temiz (0-6)", 0, 6, 0)
                    p3_3 = st.slider("Zemin genel temizliği (0-8)", 0, 8, 0)
                
                with st.expander("🗑️ 4. Çöp Kutusu ve Atık Yönetimi"):
                    p4_1 = st.slider("Çöp kutusu doğru kullanım (0-6)", 0, 6, 0)
                    p4_2 = st.slider("Çöp kutusu taşmamış (0-6)", 0, 6, 0)
                    p4_3 = st.slider("Çöp kutusu çevresi temiz (0-8)", 0, 8, 0)
                
                with st.expander("✨ 5. Genel Sınıf Yüzey Temizliği"):
                    p5_1 = st.slider("Duvarlar ve yazı durumu (0-5)", 0, 5, 0)
                    p5_2 = st.slider("Panoların düzeni (0-5)", 0, 5, 0)
                    p5_3 = st.slider("Tahta temizliği (0-5)", 0, 5, 0)
                    p5_4 = st.slider("Genel sınıf görünümü (0-5)", 0, 5, 0)

                if st.form_submit_button("💾 VERİYİ SİSTEME MÜHÜRLE"):
                    toplam = p1_1+p1_2+p2_1+p2_2+p2_3+p3_1+p3_2+p3_3+p4_1+p4_2+p4_3+p5_1+p5_2+p5_3+p5_4
                    df = verileri_yukle()
                    if not df[(df['Tarih'] == bugun) & (df['Sınıf'] == s_sinif)].empty:
                        st.error("❌ HATA: Bugün zaten kayıt yapılmış!")
                    else:
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": toplam, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success(f"✅ Başarılı! Toplam Puan: {toplam}")
                        st.balloons()
        else:
            st.error("⚠️ HATA: Lütfen kapıdaki karekodu okutarak giriş yapınız.")

        if st.button("🚪 Oturumu Kapat"):
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
                else: st.error("❌ Hatalı Giriş!")
    else:
        st.success("🔓 Yönetim Paneli Aktif.")
        df = verileri_yukle()
        if not df.empty:
            tab_g, tab_h, tab_a = st.tabs(["📌 Günlük", "📅 Haftalık", "📈 Aylık"])
            with tab_g:
                g_df = df[df['Tarih'] == bugun]
                if not g_df.empty: st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4), use_container_width=True)
            
            st.divider()
            st.subheader("📂 Sınıf Kayıt Yönetimi")
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
