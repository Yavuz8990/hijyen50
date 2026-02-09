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
SESSION_FILE = "gunluk_denetci.txt"  # İsim hafızası için dosya

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 | Geleceğin Temiz Okulu", page_icon="🧼", layout="wide")

# --- 3. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stSlider [data-baseweb="slider"] > div:first-child { background-color: #1E1E1E !important; height: 6px; }
    .stSlider [data-testid="stWidgetLabel"] p, .stSlider div[data-testid="stThumbValue"], .stSlider [data-baseweb="slider"] + div div {
        color: #FFFFFF !important; font-weight: bold !important; text-shadow: 1px 1px 3px #000000;
    }
    .streamlit-expanderHeader { color: #FFFFFF !important; font-weight: bold !important; background-color: rgba(0, 210, 255, 0.05); }
    .rank-card {
        display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; margin: 10px 0;
        border-radius: 12px; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        border: 1px solid rgba(0, 210, 255, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ZAMAN VE YARDIMCI FONKSİYONLAR ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)
bugun = guncel_an.date()

def verileri_yukle():
    sutunlar = ["Tarih", "Sınıf", "Puan", "Yetkili", "K1_Hava", "K2_Masa", "K3_Zemin", "K4_Cop", "K5_Genel"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Eğer eski dosya varsa ve yeni sütunlar eksikse onları 0 olarak ekle
            for col in sutunlar:
                if col not in df.columns:
                    df[col] = 0
            
            df['Tarih'] = pd.to_datetime(df['Tarih']).dt.date
            return df
        except: return pd.DataFrame(columns=sutunlar)
    return pd.DataFrame(columns=sutunlar)

def veri_listesini_guncelle(df):
    df.to_csv(DB_FILE, index=False)
    st.session_state['veritabani'] = df

# --- GÜNLÜK DENETÇİ HAFIZA SİSTEMİ (YENİ) ---
def gunluk_denetci_getir():
    """Bugün için kaydedilmiş bir denetçi varsa ismini döndürür, yoksa None döner."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                icerik = f.read().strip().split("|")
                if len(icerik) == 2:
                    kayitli_tarih = icerik[0]
                    kayitli_isim = icerik[1]
                    # Eğer dosyadaki tarih bugüne eşitse ismi kullan
                    if kayitli_tarih == str(bugun):
                        return kayitli_isim
        except: pass
    return None

def gunluk_denetci_kaydet(isim):
    """Denetçi ismini bugünün tarihiyle dosyaya yazar."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"{bugun}|{isim}")

# Session State Başlatma
if 'veritabani' not in st.session_state: st.session_state['veritabani'] = verileri_yukle()
if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False
if 'denetci_adi' not in st.session_state: st.session_state['denetci_adi'] = None

# --- DİĞER FONKSİYONLAR ---
def sampiyon_bul_text(veri):
    if veri.empty: return "Henüz Veri Yok"
    skorlar = veri.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
    if skorlar.empty: return "Henüz Veri Yok"
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

    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; border: 4px solid #CD7F32; border-radius: 20px; background: rgba(205, 127, 50, 0.15); margin-top: 20px;">
            <h2 style="color: #CD7F32; margin: 0; font-size: 35px;">🥉 AYIN HİJYEN ŞAMPİYONU</h2>
            <p style="font-size: 45px; font-weight: bold; color: #00D2FF; margin-top: 15px;">{sampiyon_bul_text(a_df)}</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🏆 AYLIK HİJYEN LİGİ SIRALAMASINI GÖR"):
        if not a_df.empty:
            sirali_liste = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
            for i, row in sirali_liste.iterrows():
                rank = i + 1
                color = "#00D2FF"; icon = "🔹"
                if rank == 1: color = "#FFD700"; icon = "👑"
                elif rank == 2: color = "#C0C0C0"; icon = "⭐"
                elif rank == 3: color = "#CD7F32"; icon = "✨"
                st.markdown(f"""
                   <div class="rank-card" style="border-left: 8px solid {color};">
                       <div style="display: flex; align-items: center;">
                           <span style="font-size: 24px; font-weight: bold; color: {color}; margin-right: 20px;">#{rank}</span>
                           <span style="font-size: 20px; font-weight: bold; color: white;">{icon} {row['Sınıf']} Sınıfı</span>
                       </div>
                        <div style="text-align: right;">
                           <span style="font-size: 12px; color: #00D2FF;">ORTALAMA SKOR</span>
                           <span style="font-size: 24px; font-weight: bold; color: white; display: block;">{row['Puan']:.1f}</span>
                       </div>
                   </div>
               """, unsafe_allow_html=True)
        else: st.info("Sıralama verisi henüz toplanmadı.")
    
    st.write("---")
    sozler = ["🧼 Temizlik sağlıktır.", "✨ Gelecek temiz sınıflarda başlar.", "🧪 Hijyen sorumluluktur.", "🌊 Değişim temizlikle başlar.", "🛡️ Mikroplara karşı kalkan ol.", "📚 Temiz okul, temiz zihin.", "💎 Parlayan bir gelecek için."]
    st.markdown(f"<div style='text-align: center; margin-bottom: 15px;'><p style='font-size: 28px; color: #00D2FF; font-style: italic; font-weight: bold;'>{sozler[bugun.day % 7]}</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: pass

elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    
    # --- 1. SİSTEM GİRİŞİ (Şifre) ---
    if not st.session_state['denetci_onayli']:
        d_u = st.text_input("Kullanıcı Adı:")
        d_p = st.text_input("Şifre:", type="password")
        if st.button("Sisteme Bağlan"):
            if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                st.session_state['denetci_onayli'] = True
                st.rerun()
            else: st.error("Hatalı giriş.")
    else:
        # --- 2. İSİM KONTROLÜ (OTOMATİK HAFIZA) ---
        
        # Önce dosyadan bugünün ismini çekmeyi dene
        if st.session_state['denetci_adi'] is None:
            kayitli_isim = gunluk_denetci_getir()
            if kayitli_isim:
                st.session_state['denetci_adi'] = kayitli_isim
                st.success(f"🗓️ Bugünün nöbetçi denetçisi **{kayitli_isim}** olarak tanımlandı.")
        
        # Hâlâ isim yoksa (dosyada yoksa) sor ve kaydet
        if st.session_state['denetci_adi'] is None:
            st.info("👋 Merhaba! Bugünün denetimlerini kim yapacak?")
            with st.form("isim_formu"):
                girilen_isim = st.text_input("Adınız Soyadınız:")
                if st.form_submit_button("✅ Görevi Başlat"):
                    if len(girilen_isim) > 2:
                        gunluk_denetci_kaydet(girilen_isim) # Dosyaya yaz (Bugün için hatırla)
                        st.session_state['denetci_adi'] = girilen_isim
                        st.rerun()
                    else: st.warning("Lütfen geçerli bir isim giriniz.")
            st.stop() # İsim girilmeden aşağı geçme
            
        # --- 3. ADIM: DENETİM FORMU ---
        st.success(f"👤 Aktif Denetçi: **{st.session_state['denetci_adi']}**")
        
        siniflar = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
        
        # Eğer URL'den sınıf gelmediyse seçim kutusu göster
        secilen_sinif = url_sinif
        if not secilen_sinif:
            secilen_sinif = st.selectbox("Lütfen Denetlenecek Sınıfı Seçiniz:", ["Seçiniz..."] + siniflar)

        if secilen_sinif and secilen_sinif != "Seçiniz...":
            if secilen_sinif in siniflar:
                with st.form("denetim_formu"):
                    st.subheader(f"📍 Denetlenen Alan: {secilen_sinif}")
                    
                    # --- Kriterler ---
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

                    # Kaydet butonu
                    if st.form_submit_button("💾 DEĞERLENDİRMEYİ MÜHÜRLE"):
                        df = verileri_yukle()
                        
                        # KRİTİK KONTROL: Bugün bu sınıf için kayıt var mı?
                        zaten_yapildi_mi = df[(df['Tarih'] == bugun) & (df['Sınıf'] == secilen_sinif)]
                        
                        if not zaten_yapildi_mi.empty:
                            st.error(f"⚠️ DİKKAT: {secilen_sinif} sınıfı için bugün zaten bir değerlendirme yapılmış!")
                        else:
                            # 5 Ana Maddenin Puanlarını Ayrı Ayrı Hesapla (Hepsi 20 Üzerinden)
                            k1 = p1_1 + p1_2                 # Havalandırma
                            k2 = p2_1 + p2_2 + p2_3          # Masa
                            k3 = p3_1 + p3_2 + p3_3          # Zemin
                            k4 = p4_1 + p4_2 + p4_3          # Çöp
                            k5 = p5_1 + p5_2 + p5_3 + p5_4   # Genel
                            
                            toplam = k1 + k2 + k3 + k4 + k5
                            
                            yeni = pd.DataFrame([{
                                "Tarih": bugun, 
                                "Sınıf": secilen_sinif, 
                                "Puan": toplam, 
                                "Yetkili": st.session_state['denetci_adi'],
                                "K1_Hava": k1,
                                "K2_Masa": k2,
                                "K3_Zemin": k3,
                                "K4_Cop": k4,
                                "K5_Genel": k5
                            }])
                            
                            veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                            st.success(f"Kayıt Başarıyla Tamamlandı! Skor: {toplam}")
                            st.balloons()
            else:
                st.warning("Geçersiz Sınıf Seçimi")
        else:
            st.info("Lütfen bir sınıf seçiniz veya QR kodu okutunuz.")

elif sayfa == "📊 Yönetici Paneli":
    st.title("📊 Yönetici Analiz Merkezi")
    if 'admin_onayli' not in st.session_state: st.session_state['admin_onayli'] = False
    
    if not st.session_state['admin_onayli']:
        y_u = st.text_input("Yetkili ID:")
        y_p = st.text_input("Şifre:", type="password")
        if st.button("Veri Erişimini Aç"):
            if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                st.session_state['admin_onayli'] = True; st.rerun()
    else:
        df = verileri_yukle()
        if not df.empty:
            
            # --- 1. AYLIK DURUM ÖZETİ (YENİ EKLENEN KISIM) ---
            st.subheader("🏆 Aylık Performans Özeti")
            
            # Son 30 günün verisini filtrele
            a_df = df[df['Tarih'] >= (bugun - timedelta(days=30))]
            
            col_ozet1, col_ozet2 = st.columns([1, 2])
            
            with col_ozet1:
                # Şampiyon Kutusu
                st.markdown(f"""
                    <div style="text-align: center; padding: 20px; border: 2px solid #CD7F32; border-radius: 15px; background: rgba(205, 127, 50, 0.1); height: 100%;">
                        <h3 style="color: #CD7F32; margin: 0; font-size: 20px;">🥉 AYIN ŞAMPİYONU</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #00D2FF; margin-top: 15px;">{sampiyon_bul_text(a_df)}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_ozet2:
                # Sıralama Listesi (Expander içinde)
                with st.expander("📊 AYLIK HİJYEN LİGİ SIRALAMASI", expanded=True):
                    if not a_df.empty:
                        sirali_liste = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False).reset_index()
                        # Sadece ilk 3'ü değil, hepsini ufak liste halinde gösterelim
                        st.dataframe(
                            sirali_liste.style.format({"Puan": "{:.2f}"}), 
                            column_config={
                                "Sınıf": st.column_config.TextColumn("Sınıf"),
                                "Puan": st.column_config.ProgressColumn("Ortalama Puan", format="%.2f", min_value=0, max_value=85)
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.info("Son 30 güne ait veri yok.")

            st.divider()

            # --- 2. PASTA GRAFİĞİ ---
            st.subheader("📌 Günlük Hijyen Dağılımı")
            g_df = df[df['Tarih'] == bugun]
            if not g_df.empty:
                st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4, 
                                    color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)
            else:
                st.info("Bugün henüz giriş yapılmadı.")
            
            st.divider()

            # --- 3. SINIF BAZLI KAYITLAR ---
            st.subheader("📂 Sınıf Bazlı Detaylı Kayıtlar")
            
            sinif_listesi = sorted(df['Sınıf'].unique())
            
            for sinif in sinif_listesi:
                with st.expander(f"🏫 {sinif} Sınıfı Kayıtları"):
                    sinif_df = df[df['Sınıf'] == sinif].sort_values(by='Tarih', ascending=False)
                    
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
                        if r_col4.button("Sil", key=f"sil_{idx}"):
                            kayit_sil(idx)
                            st.success(f"Kayıt silindi!")

            st.divider()
            
            # --- 4. YÖNETİM ARAÇLARI ---
            st.subheader("⚙️ Yönetim Araçları")
            
            col_Arac1, col_Arac2 = st.columns(2)
            
            with col_Arac1:
                if st.button("🔄 Günlük Denetçi İsmini Sıfırla"):
                    if os.path.exists(SESSION_FILE):
                        os.remove(SESSION_FILE)
                        st.session_state['denetci_adi'] = None
                        st.success("✅ Denetçi hafızası silindi! İsim tekrar sorulacak.")
                        st.rerun()
                    else:
                        st.info("ℹ️ Zaten kayıtlı bir günlük denetçi ismi yok.")

            with col_Arac2:
                if st.button("🚨 Tüm Veritabanını Sıfırla (Kritik)"):
                    veri_listesini_guncelle(pd.DataFrame(columns=["Tarih", "Sınıf", "Puan", "Yetkili"]))
                    st.rerun()
                
        else:
            st.info("Henüz kaydedilmiş bir veri bulunmuyor.")

        if st.button("🚪 Güvenli Çıkış"):
            st.session_state['admin_onayli'] = False; st.rerun()


