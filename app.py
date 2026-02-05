import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="H5.0 Denetim", page_icon="🧼")

# --- BARKODDAN GELEN SINIF BİLGİSİ ---
# URL yapısı: https://hijyen50.app/?sinif=10A
query_params = st.query_params
sinif_adi = query_params.get("sinif", "Sınıf Seçilmedi")

# --- LOGO VE BAŞLIK ---
st.title("🧼 Hijyen 5.0")
st.subheader(f"📍 Denetlenen Alan: {sinif_adi}")
st.write("Nöbetçi Öğretmen Hızlı Kontrol Paneli")

st.divider()

# --- 5 MADDELİK HIZLI FORM ---
with st.form("hizli_denetim"):
    st.write("🔍 **Lütfen Gözleminizi Onaylayın:**")
    
    # Maddeler (Her 'Evet' 20 Puan)
    m1 = st.checkbox("💨 Havalandırma (Camlar açık/Hava ferah)")
    m2 = st.checkbox("🪑 Sıra Üstü (Çöp veya beslenme artığı yok)")
    m3 = st.checkbox("🧹 Zemin (Kağıt, maske veya atık yok)")
    m4 = st.checkbox("🗑️ Çöp Kutusu (Taşma yok/Etrafı temiz)")
    m5 = st.checkbox("📦 Genel Düzen (Tahta, askılık ve dolaplar toplu)")

    st.divider()
    
    # Notlar
    notlar = st.text_input("Varsa eklemek istediğiniz not:")

    # Kaydet Butonu
    submit = st.form_submit_button("✅ DENETİMİ TAMAMLA VE KAYDET")

    if submit:
        # Puan Hesaplama
        skor = sum([m1, m2, m3, m4, m5]) * 20
        
        if sinif_adi == "Sınıf Seçilmedi":
            st.error("Hata: Sınıf bilgisi barkoddan alınamadı!")
        else:
            st.success(f"Başarılı! {sinif_adi} için {skor} puan sisteme işlendi.")
            st.balloons() # Şampiyonluk havası!

# --- YÖNETİCİ GÖRÜNÜMÜ (OPSİYONEL) ---
if st.checkbox("📊 Güncel Liderlik Tablosunu Gör"):
    st.write("Haftalık Şampiyonluk Yarışı")
    tablo = pd.DataFrame({
        "Sınıf": ["10-B", "9-A", "11-C"],
        "Puan": [100, 80, 60]
    })
    st.dataframe(tablo, hide_index=True)