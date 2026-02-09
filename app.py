# --- ÖZEL TASARIM EKLEMESİ (CSS KISMINA EKLEYİN) ---
st.markdown("""
    <style>
    /* Şampiyonluk Paneli - Beyaz Renk Kullanılmamıştır */
    .championship-shield {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border: 2px solid #00D2FF;
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.4), inset 0 0 15px rgba(0, 210, 255, 0.2);
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }
    
    .championship-shield::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0,210,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .champion-title {
        color: #FFD700; /* Altın Sarısı */
        font-family: 'Orbitron', sans-serif;
        font-size: 24px;
        letter-spacing: 5px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .champion-class {
        color: #00D2FF; /* Siber Mavi */
        font-size: 65px;
        font-weight: 900;
        margin: 10px 0;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.8);
    }

    .champion-score {
        color: #00FFC2; /* Enerji Yeşili */
        font-size: 28px;
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# --- ANA SAYFA ŞAMPİYON GÖRÜNÜMÜ ---
if sayfa == "🏠 Ana Sayfa":
    df_genel = verileri_yukle()
    # Başlık
    st.markdown("<div style='text-align: center;'><h1 style='color: #00D2FF; font-family: sans-serif;'>HİJYEN 5.0</h1></div>", unsafe_allow_html=True)

    # Veri hesaplama
    a_df = df_genel[df_genel['Tarih'] >= (bugun - timedelta(days=30))]
    
    if not a_df.empty:
        skorlar = a_df.groupby("Sınıf")["Puan"].mean().sort_values(ascending=False)
        sampiyon_adi = skorlar.index[0]
        sampiyon_puani = int(skorlar.iloc[0])
        
        # MODERN SİBER ŞAMPİYON KUTUSU
        st.markdown(f"""
            <div class="championship-shield">
                <div class="champion-title">🏆 AYIN HİJYEN LİDERİ</div>
                <div class="champion-class">{sampiyon_adi}</div>
                <div class="champion-score">STATUS: OPTIMAL | SCORE: {sampiyon_puani}/100</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Sistem Analiz Ediliyor: Henüz Veri Girişi Saptanmadı.")
