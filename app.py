import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- SİSTEM HAFIZASI (SESSION STATE) ---
# Sistemde kayıtlı yönetici yoksa kurulum modunu açar
if 'admin_kayitli' not in st.session_state:
    st.session_state['admin_kayitli'] = False
if 'admin_user' not in st.session_state:
    st.session_state['admin_user'] = ""
if 'admin_sifre' not in st.session_state:
    st.session_state['admin_sifre'] = ""
if 'admin_mail' not in st.session_state:
    st.session_state['admin_mail'] = ""

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Admin Yönetimi", page_icon="🛡️")

# --- TÜRKİYE SAATİ ---
tr_timezone = pytz.timezone('Europe/Istanbul')
guncel_an = datetime.now(tr_timezone)

# --- 1. ADIM: İLK KURULUM EKRANI ---
if not st.session_state['admin_kayitli']:
    st.title("🚀 Hijyen 5.0 | Sistem Kurulumu")
    st.info("Sistem ilk kez başlatılıyor. Lütfen yönetici bilgilerinizi belirleyin.")
    
    with st.form("kurulum_formu"):
        u_adi = st.text_input("Yönetici Kullanıcı Adı:")
        u_mail = st.text_input("Yönetici E-Posta Adresi (Kurtarma için):")
        u_sifre = st.text_input("Yönetici Şifresi:", type="password")
        u_sifre_onay = st.text_input("Şifreyi Tekrar Girin:", type="password")
        
        if st.form_submit_button("Sistemi Kur ve Başlat"):
            if u_adi and u_mail and u_sifre:
                if u_sifre == u_sifre_onay:
                    st.session_state['admin_user'] = u_adi
                    st.session_state['admin_mail'] = u_mail
                    st.session_state['admin_sifre'] = u_sifre
                    st.session_state['admin_kayitli'] = True
                    st.success("✅ Sistem başarıyla kuruldu! Artık giriş yapabilirsiniz.")
                    st.rerun()
                else:
                    st.error("❌ Şifreler birbiriyle uyuşmuyor!")
            else:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    st.stop() # Kurulum bitmeden ana sayfayı göstermez

# --- 2. ADIM: ANA UYGULAMA (KURULUMDAN SONRA) ---
st.title("🧼 Hijyen 5.0 | Yetkili Paneli")
st.write(f"📅 {guncel_an.strftime('%d.%m.%Y')} | 🕒 {guncel_an.strftime('%H:%M')}")

# --- YÖNETİCİ AYARLARI (SIDEBAR) ---
st.sidebar.title("⚙️ Yönetim Merkezi")
admin_modu = st.sidebar.checkbox("Yönetici Ayarları")

if admin_modu:
    st.sidebar.subheader("Bilgileri Güncelle")
    g_mail = st.sidebar.text_input("Doğrulama E-Postası:")
    g_sifre = st.sidebar.text_input("Mevcut Şifre:", type="password")
    
    if g_mail == st.session_state['admin_mail'] and g_sifre == st.session_state['admin_sifre']:
        st.sidebar.success(f"Hoş geldin, {st.session_state['admin_user']}")
        with st.sidebar.expander("📝 Bilgileri Değiştir"):
            y_user = st.text_input("Yeni Kullanıcı Adı:", value=st.session_state['admin_user'])
            y_mail = st.text_input("Yeni E-Posta:", value=st.session_state['admin_mail'])
            y_sifre = st.text_input("Yeni Şifre:", type="password")
            if st.button("Güncelle ve Kaydet"):
                st.session_state['admin_user'] = y_user
                st.session_state['admin_mail'] = y_mail
                st.session_state['admin_sifre'] = y_sifre
                st.success("Bilgiler güncellendi!")
                st.rerun()
    elif g_mail != "" or g_sifre != "":
        st.sidebar.error("❌ Kimlik doğrulama başarısız.")

st.divider()

# --- SINIF DENETİM FORMU ---
sinif_listesi = ["9A", "9B", "9C", "10A", "10B", "10C", "11A", "11B", "11C", "12A", "12B", "12C"]
query_params = st.query_params
gelen_sinif = query_params.get("sinif", None)

if gelen_sinif in sinif_listesi:
    secilen_sinif = gelen_sinif
