import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- YETKİLİ ERİŞİM BİLGİLERİ (Burayı Değiştirebilirsin) ---
SABIT_USER = "admin"
SABIT_SIFRE = "Opet2026"
SABIT_MAIL = "hijyen50@okulunuz.edu.tr"

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Denetim Paneli", page_icon="🧼")

# --- TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- ANA BAŞLIK ---
st.title("🧼 Hijyen 5.0 | Dijital Denetim")
st.info(f"📅 Tarih: {guncel_an.strftime('%d.%m.%Y')} | 🕒 Saat: {guncel_an.strftime('%H:%M')}")

# --- TARİH VE SINIF SEÇİMİ (Aktif Çalışır) ---
col1, col2 = st.columns(2)

with col1:
    secilen_tarih = st.date_input("Denetim Tarihi:", guncel_an)

with col2:
    sinif_listesi = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
    
    # URL'den gelen sınıfı yakala
    query_params = st.query_params
    gelen_sinif = query_params.get("sinif", None)
    
    index_secimi = 0
    if gelen_sinif in sinif_listesi:
        index_secimi = sinif_listesi.index(gelen_sinif)
        
    secilen_sinif = st.selectbox("Sınıf Seçiniz:", sinif_listesi, index=index_secimi)

st.divider()

# --- PUANLAMA FORMU ---
st.write(f"### 📋 {secilen_sinif} Kontrol Listesi")

with st.form("denetim_formu"):
    m1 = st.checkbox("💨 Havalandırma (Camlar açık)")
    m2 = st.checkbox("🪑 Sıra Üstü (Temiz ve düzenli)")
    m3 = st.checkbox("🧹 Zemin (Atık yok)")
    m4 = st.checkbox("🗑️ Çöp Kutusu (Taşmamış)")
    m5 = st.checkbox("📦 Genel Düzen (Tahta/Panolar)")
    
    st.write("---")
    st.write("🔐 **Yetkili Doğrulaması**")
    c_user = st.text_input("Kullanıcı Adı:", placeholder="Örn: admin")
    c_pass = st.text_input("Şifre:", type="password", placeholder="****")
    
    submit = st.form_submit_button("✅ KAYDI SİSTEME MÜHÜRLE")
    
    if submit:
        # Sabit bilgilerle kontrol
        if c_user == SABIT_USER and c_pass == SABIT_SIFRE:
            puan = sum([m1, m2, m3, m4, m5]) * 20
            st.success(f"BAŞARILI! {secilen_sinif} için {puan} puan sisteme mühürlendi.")
            st.balloons()
            # Özet Veri Çıktısı
            st.code(f"Kayıt No: H50-{guncel_an.strftime('%y%m%d%H%M')}\nSınıf: {secilen_sinif}\nOnaylayan: {c_user}\nE-Posta: {SABIT_MAIL}")
        else:
            st.error("❌ Yetkisiz Giriş! Kullanıcı adı veya şifre hatalı.")

# --- YAN MENÜ (BİLGİ PANEL
