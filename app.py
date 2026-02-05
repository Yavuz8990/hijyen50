import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- YETKİ TANIMLAMALARI ---
DENETCI_USER = "admin"
DENETCI_PASS = "Opet2026"

YONETICI_USER = "mudur"
YONETICI_PASS = "Hijyen2026"

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Güvenli Panel", page_icon="🛡️", layout="wide")

# --- TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- VERİTABANI (SESSION STATE) ---
if 'veritabani' not in st.session_state:
    # Başlangıç için örnek veriler
    st.session_state['veritabani'] = pd.DataFrame([
        {"Tarih": guncel_an.date(), "Sınıf": "10A", "Puan": 100, "Yetkili": "admin"},
        {"Tarih": (guncel_an - timedelta(days=8)).date(), "Sınıf": "9B", "Puan": 80, "Yetkili": "admin"}
    ])

# --- ANA SAYFA NAVİGASYON ---
st.sidebar.title("🧼 Hijyen 5.0")
sayfa = st.sidebar.selectbox("Giriş Türü Seçiniz:", ["🏠 Ana Sayfa", "📝 Denetçi Puan Girişi", "📊 Yönetici Analiz Paneli"])

# --- SAYFA 1: ANA SAYFA ---
if sayfa == "🏠 Ana Sayfa":
    st.title("🚀 Hijyen 5.0 Projesine Hoş Geldiniz")
    st.write("Bu yazılım, okul hijyen standartlarını dijitalleştirmek için tasarlanmıştır.")
    st.info("Denetim yapmak için soldan **'Denetçi Girişi'**ni, analizleri görmek için **'Yönetici Paneli'**ni seçiniz.")
    
    # [Image of a clean school building interior representing digital transformation in hygiene]
    
# --- SAYFA 2: DENETÇİ GİRİŞİ ---
elif sayfa == "📝 Denetçi Puan Girişi":
    st.title("📝 Günlük Denetim Formu")
    sinif_listesi = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
    
    c1, c2 = st.columns(2)
    with c1:
        secilen_sinif = st.selectbox("Sınıf:", sinif_listesi)
    with c2:
        secilen_tarih = st.date_input("Denetim Tarihi:", guncel_an)

    with st.form("puan_formu"):
        m = [st.checkbox(k) for k in ["Havalandırma", "Sıra Temizliği", "Zemin Hijyeni", "Çöp Kutusu", "Genel Düzen"]]
        st.divider()
        u = st.text_input("Denetçi Kullanıcı Adı:")
        p = st.text_input("Denetçi Şifresi:", type="password")
        
        if st.form_submit_button("ONAYLA VE GÖNDER"):
            if u == DENETCI_USER and p == DENETCI_PASS:
                skor = sum(m) * 20
                yeni_kayit = pd.DataFrame([{"Tarih": secilen_tarih, "Sınıf": secilen_sinif, "Puan": skor, "Yetkili": u}])
                st.session_state['veritabani'] = pd.concat([st.session_state['veritabani'], yeni_kayit], ignore_index=True)
                st.success(f"Başarılı! {secilen_sinif} için {skor} puan sisteme mühürlendi.")
                st.balloons()
            else:
                st.error("Hatalı Denetçi Bilgileri!")

# --- SAYFA 3: YÖNETİCİ ANALİZ PANELİ ---
elif sayfa == "📊 Yönetici Analiz Paneli":
    st.title("📊 Yönetici Analiz ve Raporlama")
    
    st.sidebar.warning("Kısıtlı Alan: Sadece İdare Erişimi")
    y_user = st.text_input("Yönetici Kullanıcı Adı:")
    y_pass = st.text_input("Yönetici Şifresi:", type="password")
    
    if y_user == YONETICI_USER and y_pass == YONETICI_PASS:
        st.success("Yönetici Kimliği Doğrulandı.")
        df = st.session

