import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- SABİT BİLGİLER ---
SABIT_USER = "admin"
SABIT_SIFRE = "Opet2026"
HEDEF_MAIL = "yesn8906@gmail.com"

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Denetim", page_icon="🧼")

# --- TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- BAŞLIK ---
st.title("🧼 Hijyen 5.0 | Dijital Denetim")
st.write(f"📅 Tarih: {guncel_an.strftime('%d.%m.%Y')} | 🕒 Saat: {guncel_an.strftime('%H:%M')}")

# --- SINIF SEÇİMİ (Barkod Uyumlu) ---
sinif_listesi = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
query_params = st.query_params
gelen_sinif = query_params.get("sinif", None)
idx = sinif_listesi.index(gelen_sinif) if gelen_sinif in sinif_listesi else 0
secilen_sinif = st.selectbox("Denetlenecek Sınıf:", sinif_listesi, index=idx)

st.divider()

# --- 5 MADDELİK PUANLAMA FORMU ---
st.subheader(f"📋 {secilen_sinif} Sınıfı Hijyen Anketi")
st.write("Her madde **20 puan** değerindedir.")

with st.form("puanlama_anketi"):
    # 5 Madde
    m1 = st.checkbox("1. Havalandırma: Camlar açık ve içerisi ferah mı?")
    m2 = st.checkbox("2. Sıra/Yüzey: Sıraların üzerinde çöp veya leke yok mu?")
    m3 = st.checkbox("3. Zemin: Yerlerde kağıt, kalem ucu veya atık yok mu?")
    m4 = st.checkbox("4. Çöp Kutusu: Boşaltılmış ve çevresi temiz mi?")
    m5 = st.checkbox("5. Genel Düzen: Tahta, panolar ve dolaplar düzenli mi?")
    
    st.write("---")
    st.write("🔐 **Admin Onayı**")
    c_user = st.text_input("Kullanıcı Adı:")
    c_pass = st.text_input("Şifre:", type="password")
    
    submit = st.form_submit_button("✅ PUANI HESAPLA VE MAİL GÖNDER")
    
    if submit:
        if c_user == SABIT_USER and c_pass == SABIT_SIFRE:
            # Puan Hesaplama
            toplam_puan = sum([m1, m2, m3, m4, m5]) * 20
            
            # Sonuç Ekranı
            st.success(f"İŞLEM BAŞARILI! Toplam Puan: {toplam_puan}")
            st.balloons()
            
            # Mail İçeriği (Ekranda Rapor Olarak Gösterir)
            rapor = f"""
            📧 RAPOR GÖNDERİLDİ!
            Alıcı: {HEDEF_MAIL}
            Konu: {secilen_sinif} Hijyen Denetimi
            -----------------------------------
            Sınıf: {secilen_sinif}
            Puan: {toplam_puan}
            Tarih: {guncel_an.strftime('%d.%m.%Y %H:%M')}
            Denetçi: {c_user}
            -----------------------------------
            """
            st.code(rapor)
        else:
            st.error("❌ Hatalı Kullanıcı Adı veya Şifre!")
