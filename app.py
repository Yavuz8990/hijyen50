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

# --- 3. ÖZEL TASARIM (CSS) - SİBER VE TEKNOLOJİK TEMA ---
st.markdown("""
    <style>
    /* Ana Arka Plan Ayarı */
    .stApp {
        background-color: #050505;
    }

    /* Slider (Puanlama Çubuğu) Tasarımı */
    .stSlider [data-baseweb="slider"] > div:first-child {
        background-color: #1a1a1a !important;
        height: 8px;
    }
    .stSlider [data-testid="stWidgetLabel"] p, 
    .stSlider div[data-testid="stThumbValue"],
    .stSlider [data-baseweb="slider"] + div div {
        color: #00D2FF !important; /* Rakamlar Siber Mavi */
        font-weight: bold !important;
    }

    /* ŞAMPİYONLUK PANELİ (Beyaz Renk Yok) */
    .championship-shield {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border: 2px solid #00D2FF;
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.4);
        margin: 20px 0;
    }
    .champion-title {
        color: #FFD700; /* Altın */
        font-size: 22px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .champion-class {
        color: #00D2FF;
        font-size: 70px;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.8);
        margin: 10px 0;
    }
    .champion-score {
        color: #00FFC2; /* Neon Yeşil */
        font-size: 26px;
        font-family: monospace;
    }

    /* TEKNOLOJİK SIRALAMA KARTLARI */
    .rank-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        margin: 10px 0;
        border-radius: 12px;
        background: rgba(48, 43, 99, 0.3);
        border: 1px solid rgba(0, 210, 255, 0.2);
    }

    /* Metin Renkleri */
    h1, h2, h3, p, span {
        color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)
bugun = guncel_an.date()

# --- 5. VERİ FONKSİYONLARI ---
def verileri_yukle():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tarih'] = pd.to_datetime(df['Tarih']).dt.date
        return df
    return pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

def veri_listesini_guncelle(df):
    df.to_csv(DB_FILE, index=False)
    st.session_state['veritabani'] = df

if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = verileri_yukle()

# --- 6. SAYFA SEÇİMİ ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 7. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    st.markdown("<div style='text-align: center;'><h1 style='color: #00D2FF; font-size: 60px;'>HİJYEN 5.0</h1></div>", unsafe_allow_html=True)

    # Aylık Veri Filtreleme
    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    
    # ŞAMPİYON PANELİ
    if not a_df.empty:
        skorlar = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
        sampiyon_adi = skorlar.index[0]
        sampiyon_puani = int(skorlar.iloc[0])
        
        st.markdown(f"""
            <div class="championship-shield">
                <div class="champion-title">🏆 AYIN HİJYEN LİDERİ</div>
                <div class="champion-class">{sampiyon_adi}</div>
                <div class="champion-score">STATUS: OPTIMAL | SCORE: {sampiyon_puani}/100</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Sistem Analiz Ediliyor: Henüz Veri Girişi Saptanmadı.")

    # TEKNOLOJİK SIRALAMA LİSTESİ
    with st.expander("🏆 AYLIK HİJYEN LİGİ SIRALAMASINI GÖR (TÜM SINIFLAR)"):
        if not a_df.empty:
            sirali_liste = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
            for i, row in sirali_liste.iterrows():
                rank = i + 1
                color = "#00D2FF"; icon = "🔹"
                if rank == 1: color = "#FFD700"; icon = "👑"
                elif rank == 2: color = "#C0C0C0"; icon = "⭐"
                elif rank == 3: color = "#CD7F32"; icon = "✨"
                
                st.markdown(f"""
                    <div class="rank-card" style="border-left: 6px solid {color};">
                        <span style="font-size: 18px; font-weight: bold;">#{rank} {icon} {row['Sınıf']} Sınıfı</span>
                        <span style="font-size: 18px; font-weight: bold; color: {color};">{row['Puan']:.1f} Puan</span>
                    </div>
                """, unsafe_allow_html=True)

    st.write("---")

    # GÜNÜN SÖZÜ (AFİŞİN ÜSTÜNDE)
    sozler = [
        "🧼 'Temizlik, sağlıktan önce gelir; çünkü sağlığın koruyucusudur.'",
        "✨ 'Geleceğin temiz okulu, bugünün bilinçli adımlarıyla inşa edilir.'",
        "🧪 'Hijyen bir tercih değil, toplumun her ferdine olan sorumluluğumuzdur.'",
        "🌊 'Büyük değişimler, küçük bir temizlik alışkanlığıyla başlar.'",
        "🛡️ 'Görünmez tehlikelere karşı en güçlü kalkanımız: Hijyen.'",
        "📚 'Eğitim sadece kitaplarla değil, sağlıklı bir çevreyle hayat bulur.'",
        "💎 'Temizlik, başarının aynasıdır; parlayan bir gelecek temiz sınıflarda yetişir.'"
    ]
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><p style='font-size: 28px; color: #00D2FF; font-style: italic; font-weight: bold;'>{sozler[bugun.day % 7]}</p></div>", unsafe_allow_html=True)

    # AFİŞ
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("Afiş dosyası bulunamadı.")

# --- DENETÇİ GİRİŞİ ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False
    
    if not st.session_state['denetci_onayli']:
        d_u = st.text_input("Kullanıcı Adı:"); d_p = st.text_input("Şifre:", type="password")
        if st.button("Sisteme Bağlan"):
            if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                st.session_state['denetci_onayli'] = True; st.rerun()
    else:
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        if url_sinif and url_sinif in siniflar:
            with st.form("denetim_formu"):
                st.subheader(f"📍 Denetlenen Alan: {url_sinif}")
                # Kriterler (Sliderlar siber mavi rakamlı)
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0)
                    p1_2 = st.slider("Sınıfta ağır, rahatsız edici koku yok (0-10)", 0, 10, 0)
                with st.expander("🪑 2. Sınıf ve Masa Temizliği"):
                    p2_1 = st.slider("Masa yüzeyleri temiz (0-6)", 0, 6, 0)
                    p2_2 = st.slider("Sıra üstünde, altında çöp ve dağınıklık yok (0-6)", 0, 6, 0)
                    p2_3 = st.slider("Genel masa–sıra düzeni iyi (0-8)", 0, 8, 0)
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

                if st.form_submit_button("💾 DEĞERLENDİRMEYİ MÜHÜRLE"):
                    toplam = p1_1+p1_2+p2_1+p2_2+p2_3+p3_1+p3_2+p3_3+p4_1+p4_2+p4_3+p5_1+p5_2+p5_3+p5_4
                    df = verileri_yukle()
                    yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": url_sinif, "Puan": toplam, "Yetkili": DENETCI_USER}])
                    veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                    st.success(f"Kayıt Tamamlandı! Skor: {toplam}"); st.balloons()
        else: st.warning("⚠️ Lütfen geçerli bir sınıf QR kodu okutunuz.")
        if st.button("🚪 Bağlantıyı Kes"):
            st.session_state['denetci_onayli'] = False; st.rerun()

# --- YÖNETİCİ PANELİ ---
elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False
    
    if not st.session_state['admin_onayli']:
        y_u = st.text_input("Yetkili ID:"); y_p = st.text_input("Şifre:", type="password")
        if st.button("Veri Erişimini Aç"):
            if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                st.session_state['admin_onayli'] = True; st.rerun()
    else:
        df = verileri_yukle()
        if not df.empty:
            # PASTA GRAFİĞİ (SADECE BURADA)
            st.subheader("📌 Günlük Hijyen Dağılımı")
            g_df = df[df['Tarih'] == bugun]
            if not g_df.empty:
                st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4, 
                                     color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)
            
            st.divider()
            st.subheader("📂 Veritabanı")
            st.dataframe(df, use_container_width=True)
            if st.button("Sistemi Sıfırla (Kritik)"):
                veri_listesini_guncelle(pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"]))
                st.rerun()
        if st.button("🚪 Çıkış"):
            st.session_state['admin_onayli'] = False; st.rerun()
