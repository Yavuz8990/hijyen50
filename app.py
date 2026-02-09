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

# --- 3. ÖZEL TASARIM (CSS) - TEKNOLOJİK VE KARANLIK TEMA ---
st.markdown("""
    <style>
    /* Slider Çizgisini Sadeleştir */
    .stSlider [data-baseweb="slider"] > div:first-child {
        background-color: #1E1E1E !important;
        height: 6px;
    }
    
    /* Metinleri ve Rakamları BEYAZ yap (Koyu Arka Planda Görünürlük) */
    .stSlider [data-testid="stWidgetLabel"] p, 
    .stSlider div[data-testid="stThumbValue"],
    .stSlider [data-baseweb="slider"] + div div {
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px #000000;
    }

    /* Expander başlıklarını BEYAZ yap */
    .st-emotion-cache-p4mowd {
        color: #FFFFFF !important;
        font-weight: bold !important;
        background-color: rgba(0, 210, 255, 0.05);
    }

    /* TEKNOLOJİK SIRALAMA KARTI (Beyaz fon içermez) */
    .rank-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        margin: 10px 0;
        border-radius: 12px;
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); /* Gece mavisi teknolojik geçiş */
        border: 1px solid rgba(0, 210, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
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
    return pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"])

def veri_listesini_guncelle(df):
    df.to_csv(DB_FILE, index=False)
    st.session_state['veritabani'] = df

if 'veritabani' not in st.session_state:
    st.session_state['veritabani'] = verileri_yukle()

def sampiyon_bul_text(veri):
    if veri.empty: return "Henüz Veri Yok"
    skorlar = veri.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

def kayit_sil(index):
    df = verileri_yukle()
    df = df.drop(index)
    veri_listesini_guncelle(df)
    st.rerun()

# --- 6. QR KOD VE YÖNLENDİRME ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

# --- 7. YAN MENÜ ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 8. SAYFA İÇERİKLERİ ---

if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    st.markdown("""<div style='text-align: center;'><h1 style='color: #00D2FF; font-size: 60px; margin-bottom: 0px;'>HİJYEN 5.0</h1></div>""", unsafe_allow_html=True)

    # --- AYLIK DEĞERLENDİRME ---
    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; border: 4px solid #CD7F32; border-radius: 20px; background: rgba(205, 127, 50, 0.15); margin-top: 20px;">
            <h2 style="color: #CD7F32; margin: 0; font-size: 35px;">🥉 AYIN HİJYEN ŞAMPİYONU</h2>
            <p style="font-size: 45px; font-weight: bold; color: #00D2FF; margin-top: 15px;">{sampiyon_bul_text(a_df)}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TEKNOLOJİK LİDERLİK TABLOSU ---
    with st.expander("🏆 AYLIK HİJYEN LİGİ SIRALAMASINI GÖR (TÜM SINIFLAR)"):
        if not a_df.empty:
            sirali_liste = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
            for i, row in sirali_liste.iterrows():
                rank = i + 1
                color = "#00D2FF"; icon = "🔹"
                if rank == 1: color = "#FFD700"; icon = "👑" # Altın
                elif rank == 2: color = "#C0C0C0"; icon = "⭐" # Gümüş
                elif rank == 3: color = "#CD7F32"; icon = "✨" # Bronz
                
                st.markdown(f"""
                    <div class="rank-card" style="border-left: 8px solid {color};">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 24px; font-weight: bold; color: {color}; margin-right: 20px;">#{rank}</span>
                            <span style="font-size: 20px; font-weight: bold; color: white;">{icon} {row['Sınıf']} Sınıfı</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 12px; color: #00D2FF; letter-spacing: 1px;">ORTALAMA SKOR</span>
                            <span style="font-size: 24px; font-weight: bold; color: white; display: block;">{row['Puan']:.1f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sıralama verisi henüz toplanmadı.")

    st.write("---")

    # --- GÜNÜN SÖZÜ ---
    sozler = [
        "🧼 'Temizlik, sağlıktan önce gelir; çünkü sağlığın koruyucusudur.'",
        "✨ 'Geleceğin temiz okulu, bugünün bilinçli adımlarıyla inşa edilir.'",
        "🧪 'Hijyen bir tercih değil, toplumun her ferdine olan sorumluluğumuzdur.'",
        "🌊 'Büyük değişimler, küçük bir temizlik alışkanlığıyla başlar.'",
        "🛡️ 'Görünmez tehlikelere karşı en güçlü kalkanımız: Hijyen.'",
        "📚 'Eğitim sadece kitaplarla değil, sağlıklı bir çevreyle hayat bulur.'",
        "💎 'Temizlik, başarının aynasıdır; parlayan bir gelecek temiz sınıflarda yetişir.'"
    ]
    st.markdown(f"<div style='text-align: center; margin-bottom: 15px;'><p style='font-size: 28px; color: #00D2FF; font-style: italic; font-weight: bold;'>{sozler[bugun.day % 7]}</p></div>", unsafe_allow_html=True)

    # --- AFİŞ ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("Afiş dosyası bulunamadı.")

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
                
                # --- Kriterler ---
                with st.expander("🌬️ 1. Havalandırma ve Hava Kalitesi"):
                    p1_1 = st.slider("Teneffüslerde sınıf havalandırılmış (0-10)", 0, 10, 0)
                    p1_2 = st.slider("Sınıfta ağır, rahatsız edici koku yok (0-10)", 0, 10, 0)
                with st.expander("🪑 2. Sınıf ve Masa Temizliği"):
                    p2_1 = st.slider("Masa yüzeyleri temiz (0-6)", 0, 6, 0)
                    p2_2 = st.slider("Sıra üstünde, altında çöp ve dağınıklık yok (0-6)", 0, 6, 0)
                    p2_3 = st.slider("Genel masa–sıra düzeni iyi (0-8)", 0, 8, 0)
                with st.expander("Sweep 3. Zemin ve Köşe Temizliği"):
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

                # Kaydet butonu tıklandığında kontrol yap
                if st.form_submit_button("💾 DEĞERLENDİRMEYİ MÜHÜRLE"):
                    df = verileri_yukle()
                    
                    # KRİTİK KONTROL: Bugün bu sınıf için kayıt var mı?
                    zaten_yapildi_mi = df[(df['Tarih'] == bugun) & (df['Sınıf'] == url_sinif)]
                    
                    if not zaten_yapildi_mi.empty:
                        st.error(f"⚠️ DİKKAT: {url_sinif} sınıfı için bugün zaten bir değerlendirme yapılmış! Günde sadece 1 kayıt girebilirsiniz.")
                    else:
                        toplam = p1_1+p1_2+p2_1+p2_2+p2_3+p3_1+p3_2+p3_3+p4_1+p4_2+p4_3+p5_1+p5_2+p5_3+p5_4
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": url_sinif, "Puan": toplam, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success(f"Kayıt Başarıyla Tamamlandı! Skor: {toplam}")
                        st.balloons()
        else:
            st.warning("⚠️ Lütfen geçerli bir sınıf QR kodu okutunuz.")

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
            # Pasta Grafiği
            st.subheader("📌 Günlük Hijyen Dağılımı")
            g_df = df[df['Tarih'] == bugun]
            if not g_df.empty:
                st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4, 
                                     color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)
            
            st.divider()
            st.subheader("📂 Sınıf Bazlı Denetim Kayıtları")
            
            # Sınıfları alfabetik sırala
            sinif_listesi = sorted(df['Sınıf'].unique())
            
            for sinif in sinif_listesi:
                with st.expander(f"🏫 {sinif} Sınıfı Kayıtları"):
                    # O sınıfa ait verileri çek ve tarihe göre yeniden eskiye sırala
                    sinif_df = df[df['Sınıf'] == sinif].sort_values(by='Tarih', ascending=False)
                    
                    # Tablo başlıkları için sütunlar
                    h_col1, h_col2, h_col3, h_col4 = st.columns([2, 2, 2, 1])
                    h_col1.write("**Tarih**")
                    h_col2.write("**Puan**")
                    h_col3.write("**Denetçi**")
                    h_col4.write("**İşlem**")
                    
                    for idx, row in sinif_df.iterrows():
                        r_col1, r_col2, r_col3, r_col4 = st.columns([2, 2, 2, 1])
                        r_col1.write(f"{row['Tarih']}")
                        r_col2.write(f"⭐ {row['Puan']}")
                        r_col3.write(f"👤 {row['Yetkili']}")
                        # Her satır için benzersiz bir anahtar (key) ile silme butonu
                        if r_col4.button("Sil", key=f"sil_{idx}"):
                            kayit_sil(idx)
                            st.success(f"Kayıt silindi!")

            st.divider()
            if st.button("🚨 Tüm Sistemi Sıfırla (Kritik)"):
                veri_listesini_guncelle(pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"]))
                st.rerun()
                
        else:
            st.info("Henüz kaydedilmiş bir veri bulunmuyor.")

        if st.button("🚪 Güvenli Çıkış"):
            st.session_state['admin_onayli'] = False; st.rerun()



