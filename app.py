import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- SİSTEM HAFIZASI ---
if 'admin_kayitli' not in st.session_state:
    st.session_state['admin_kayitli'] = False
if 'admin_user' not in st.session_state:
    st.session_state['admin_user'] = ""
if 'admin_sifre' not in st.session_state:
    st.session_state['admin_sifre'] = ""
if 'admin_mail' not in st.session_state:
    st.session_state['admin_mail'] = ""

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Denetim Paneli", page_icon="🧼")

# --- TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 1. ADIM: İLK KURULUM ---
if not st.session_state['admin_kayitli']:
    st.title("🚀 Hijyen 5.0 | Sistem Kurulumu")
    with st.form("ilk_kurulum"):
        u_adi = st.text_input("Yönetici Kullanıcı Adı:")
        u_mail = st.text_input("Yönetici E-Posta:")
        u_sifre = st.text_input("Şifre Belirleyin:", type="password")
        if st.form_submit_button("Sistemi Başlat"):
            if u_adi and u_mail and u_sifre:
                st.session_state['admin_user'] = u_adi
                st.session_state['admin_mail'] = u_mail
                st.session_state['admin_sifre'] = u_sifre
                st.session_state['admin_kayitli'] = True
                st.rerun()
    st.stop()

# --- 2. ADIM: ANA UYGULAMA ---
st.title("🧼 Hijyen 5.0 | Dijital Denetim")

# --- TARİH VE SINIF SEÇİMİ (Form Dışında - Aktif Çalışır) ---
col1, col2 = st.columns(2)

with col1:
    secilen_tarih = st.date_input("Denetim Tarihi:", datetime.now(tr_timezone))

with col2:
    sinif_listesi = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
    
    # QR koddan gelen sınıfı kontrol et
    query_params = st.query_params
    gelen_sinif = query_params.get("sinif", None)
    
    if gelen_sinif in sinif_listesi:
        default_index = sinif_listesi.index(gelen_sinif)
    else:
        default_index = 0
        
    secilen_sinif = st.selectbox("Sınıf Seçiniz:", sinif_listesi, index=default_index)

st.divider()

# --- 3. ADIM: PUANLAMA FORMU ---
st.write(f"### 📋 {secilen_sinif} Sınıfı Kontrol Listesi")
st.write(f"📅 Tarih: {secilen_tarih.strftime('%d.%m.%Y')}")

with st.form("denetim_onay_formu"):
    m1 = st.checkbox("💨 Havalandırma (Camlar açık)")
    m2 = st.checkbox("🪑 Sıra Üstü (Temiz ve düzenli)")
    m3 = st.checkbox("🧹 Zemin (Atık yok)")
    m4 = st.checkbox("🗑️ Çöp Kutusu (Taşmamış)")
    m5 = st.checkbox("📦 Genel Düzen (Tahta/Panolar)")
    
    st.write("---")
    st.write("🔑 **Yetkili Onayı**")
    c_user = st.text_input("Kullanıcı Adı:")
    c_pass = st.text_input("Şifre:", type="password")
    
    if st.form_submit_button("KAYDI TAMAMLA VE MÜHÜRLE"):
        if c_user == st.session_state['admin_user'] and c_pass == st.session_state['admin_sifre']:
            puan = sum([m1, m2, m3
