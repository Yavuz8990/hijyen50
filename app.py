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

# --- 5. ŞAMPİYON HESAPLAMA FONKSİYONU ---
def sampiyon_bul_text(veri):
    if veri.empty: return "Henüz veri yok"
    skorlar = veri.groupby("Sınıf")["Puan"].mean()
    en_yuksek = skorlar.max()
    sampiyonlar = skorlar[skorlar == en_yuksek].index.tolist()
    return f"{', '.join(sampiyonlar)} ({int(en_yuksek)} Puan)"

# --- 6. QR KOD VE YÖNLENDİRME ---
query_params = st.query_params
url_sinif = query_params.get("sinif", None)
default_index = 1 if url_sinif else 0 

# --- 7. YAN MENÜ ---
st.sidebar.title("💎 Hijyen 5.0")
sayfa = st.sidebar.radio("Giriş Türü:", ["🏠 Ana Sayfa", "📝 Denetçi Girişi", "📊 Yönetici Paneli"], index=default_index)

# --- 8. SAYFA İÇERİKLERİ ---

# --- ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    
    st.markdown("""
        <div style="text-align: center; padding: 10px; background: rgba(0, 210, 255, 0.05); border-radius: 20px;">
            <h1 style="font-family: 'Arial Black', sans-serif; color: #00D2FF; font-size: 70px; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(0,210,255,0.6);">
                HİJYEN 5.0
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # --- ŞAMPİYONLAR KÜRSÜSÜ (YENİ) ---
    st.write("")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        g_df = df_genel[df_genel['Tarih'] == bugun]
        st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid #FFD700; border-radius: 15px; background: rgba(255, 215, 0, 0.1);">
                <h3 style="color: #FFD700; margin: 0;">🥇 GÜNÜN LİDERİ</h3>
                <p style="font-size: 20px; font-weight: bold; color: white; margin-top: 10px;">{sampiyon_bul_text(g_df)}</p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        h_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=7))]
        st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid #C0C0C0; border-radius: 15px; background: rgba(192, 192, 192, 0.1);">
                <h3 style="color: #C0C0C0; margin: 0;">🥈 HAFTANIN EN TEMİZİ</h3>
                <p style="font-size: 20px; font-weight: bold; color: white; margin-top: 10px;">{sampiyon_bul_text(h_df)}</p>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
        st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid #CD7F32; border-radius: 15px; background: rgba(205, 127, 50, 0.1);">
                <h3 style="color: #CD7F32; margin: 0;">🥉 AYIN ŞAMPİYONU</h3>
                <p style="font-size: 20px; font-weight: bold; color: white; margin-top: 10px;">{sampiyon_bul_text(a_df)}</p>
            </div>
        """, unsafe_allow_html=True)

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
    secilen_soz = sozler[bugun.day % 7]

    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px; padding: 20px; border-bottom: 3px solid #00D2FF; background-color: rgba(0, 210, 255, 0.05); border-radius: 15px;">
            <p style="font-family: 'Georgia', serif; font-size: 32px; color: #00D2FF; font-style: italic; font-weight: bold; line-height: 1.4; text-shadow: 1px 1px 2px black;">
                {secilen_soz}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- AFİŞ ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("afis.jpg", use_container_width=True)
        except: st.warning("⚠️ `afis.jpg` bulunamadı.")

# --- 📝 DENETÇİ SAYFASI ---
elif sayfa == "📝 Denetçi Girişi":
    st.title("📝 Denetçi Kayıt Paneli")
    if 'denetci_onayli' not in st.session_state: st.session_state['denetci_onayli'] = False

    if not st.session_state['denetci_onayli']:
        with st.container(border=True):
            d_u = st.text_input("Kullanıcı Adı:", key="d_u")
            d_p = st.text_input("Şifre:", type="password", key="d_p")
            if st.button("Sisteme Giriş Yap"):
                if d_u == DENETCI_USER and d_p == DENETCI_PASS:
                    st.session_state['denetci_onayli'] = True
                    st.rerun()
                else: st.error("❌ Hatalı Giriş!")
    else:
        st.success(f"🔓 Yetkili: {DENETCI_USER}")
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
                        st.error(f"❌ {s_sinif} için bugün kayıt yapılmış!")
                    else:
                        puan = sum([k1, k2, k3, k4, k5]) * 20
                        yeni = pd.DataFrame([{"Tarih": bugun, "Sınıf": s_sinif, "Puan": puan, "Yetkili": DENETCI_USER}])
                        veri_listesini_guncelle(pd.concat([df, yeni], ignore_index=True))
                        st.success(f"✅ Başarılı!")
                        st.balloons()
        else: st.error("⚠️ Lütfen sınıf karekodunu okutunuz.")
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
            if st.button("Paneli Kilidini Aç"):
                if y_u == YONETICI_USER and y_p == YONETICI_PASS:
                    st.session_state['admin_onayli'] = True
                    st.rerun()
                else: st.error("❌ Yetkisiz Erişim!")
    else:
        st.success("🔓 Yönetim Paneli Aktif.")
        df = verileri_yukle()
        if not df.empty:
            tab_g, tab_h, tab_a = st.tabs(["📌 Günlük", "📅 Haftalık", "📈 Aylık"])
            with tab_g:
                g_df = df[df['Tarih'] == bugun]
                if not g_df.empty: st.plotly_chart(px.pie(g_df, values='Puan', names='Sınıf', hole=0.4), use_container_width=True)
            
            st.divider()
            st.subheader("📂 Sınıf Yönetimi")
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
