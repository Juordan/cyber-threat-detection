import streamlit as st
import pandas as pd
import joblib
import json
import re
from pathlib import Path

from preprocessors.email_text_preprocessor import clean_email_text
from preprocessors.url_feature_extractor import extract_url_features


# =========================================================
# 1. CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

SMS_MODEL_PATH = BASE_DIR / "models" / "best_sms_phishing_model.pkl"
EMAIL_MODEL_PATH = BASE_DIR / "models" / "email_model.pkl"
URL_MODEL_PATH = BASE_DIR / "models" / "url_model.pkl"

EMAIL_PREPROCESSOR_PATH = (
    BASE_DIR / "preprocessors" / "email_text_preprocessor.py"
)

URL_FEATURE_NAMES_PATH = (
    BASE_DIR / "preprocessors" / "url_feature_names.json"
)

st.set_page_config(
    page_title="Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #16325c;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 25px;
    }

    .result-safe {
        background-color: #dcfce7;
        color: #166534;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #86efac;
        text-align: center;
        font-size: 23px;
        font-weight: bold;
    }

    .result-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #fca5a5;
        text-align: center;
        font-size: 23px;
        font-weight: bold;
    }

    .info-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. LOAD MODELS
# =========================================================

@st.cache_resource
def load_models():

    sms_model = joblib.load(SMS_MODEL_PATH)
    email_model = joblib.load(EMAIL_MODEL_PATH)
    url_model = joblib.load(URL_MODEL_PATH)

    with open(URL_FEATURE_NAMES_PATH, "r", encoding="utf-8") as file:
        url_feature_names = json.load(file)

    return sms_model, email_model, url_model, url_feature_names


# =========================================================
# 4. INPUT FEATURE EXTRACTION FOR SMS
# =========================================================

def extract_sms_features(text):

    # Detect URL
    url_pattern = (
        r'(?:https?://|www\.)\S+'
        r'|(?:[a-zA-Z0-9-]+\.)+'
        r'(?:com|net|org|edu|gov|co|id|info|biz|xyz)'
        r'(?:/\S*)?'
    )

    has_url = int(bool(re.search(url_pattern, text, re.IGNORECASE)))

    # Detect email address
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    has_email = int(bool(re.search(email_pattern, text)))

    # Detect phone number
    phone_pattern = r'(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)'

    has_phone = int(bool(re.search(phone_pattern, text)))

    features = pd.DataFrame([{
        "TEXT": text,
        "URL": has_url,
        "EMAIL": has_email,
        "PHONE": has_phone,
        "TEXT_LENGTH": len(text)
    }])

    return features


# =========================================================
# 5. DISPLAY PREDICTION RESULT
# =========================================================

def display_result(prediction, safe_label, danger_label):

    if int(prediction) == 0:

        st.markdown(
            f'<div class="result-safe">AMAN: {safe_label}</div>',
            unsafe_allow_html=True
        )

        st.success(
            "Model mengklasifikasikan input sebagai kategori aman. "
            "Tetap berhati-hati terhadap pesan atau tautan yang mencurigakan."
        )

    else:

        st.markdown(
            f'<div class="result-danger">BAHAYA: {danger_label}</div>',
            unsafe_allow_html=True
        )

        st.error(
            "Model mengidentifikasi input sebagai indikasi phishing. "
            "Jangan klik tautan atau memberikan informasi pribadi "
            "sebelum melakukan verifikasi."
        )


# =========================================================
# 6. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🛡️ CYBER THREAT DETECTION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Machine Learning Based Security Detection System'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 7. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.title("🛡️ CyberGuard AI")

    st.caption("Security Detection Platform")

    st.divider()

    menu = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📱 SMS Detection",
            "📧 Email Detection",
            "🌐 URL Detection",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.caption("Machine Learning Models")

    st.markdown("""
    - SMS: Multinomial Naive Bayes
    - Email: LinearSVC
    - URL: Random Forest
    """)

    st.divider()

    st.caption("Cyber Threat Detection")


# =========================================================
# 8. LOAD MODELS
# =========================================================

try:

    sms_model, email_model, url_model, url_feature_names = load_models()

except Exception as error:

    st.error("Gagal memuat model atau file pendukung.")

    st.code(str(error))

    st.info(
        "Periksa kembali lokasi file model dan preprocessor "
        "di dalam folder proyek."
    )

    st.stop()


# =========================================================
# 9. DASHBOARD PAGE
# =========================================================

if menu == "🏠 Dashboard":

    st.subheader("Welcome to Cyber Threat Detection")

    st.write(
        "Aplikasi ini menggunakan Machine Learning untuk "
        "mendeteksi potensi ancaman keamanan digital melalui "
        "pesan SMS, email, dan URL."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="SMS Detection",
            value="Active"
        )

    with col2:
        st.metric(
            label="Email Detection",
            value="Active"
        )

    with col3:
        st.metric(
            label="URL Detection",
            value="Active"
        )

    st.divider()

    st.subheader("Available Detection Services")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📱 SMS")
        st.write(
            "Mendeteksi pesan SMS yang berpotensi "
            "mengandung smishing."
        )

    with col2:
        st.markdown("### 📧 Email")
        st.write(
            "Mengklasifikasikan email menjadi "
            "Safe Email atau Phishing Email."
        )

    with col3:
        st.markdown("### 🌐 URL")
        st.write(
            "Menganalisis karakteristik URL untuk "
            "mendeteksi potensi phishing."
        )

    st.info(
        "Pilih salah satu layanan deteksi melalui menu sidebar "
        "untuk mulai melakukan pemeriksaan."
    )


# =========================================================
# 10. SMS DETECTION PAGE
# =========================================================

elif menu == "📱 SMS Detection":

    st.subheader("📱 SMS Phishing Detection")

    st.write(
        "Masukkan pesan SMS yang ingin diperiksa. "
        "Model akan mengklasifikasikan pesan menjadi "
        "Ham (Safe SMS) atau Smishing."
    )

    sms_input = st.text_area(
        "Masukkan pesan SMS:",
        height=180,
        placeholder="Contoh: Congratulations! You have won a prize..."
    )

    if st.button("🔍 Detect SMS", key="sms_button"):

        if not sms_input.strip():

            st.warning("Silakan masukkan pesan SMS terlebih dahulu.")

        else:

            try:

                sms_features = extract_sms_features(sms_input)

                prediction = sms_model.predict(sms_features)[0]

                st.divider()

                st.subheader("Detection Result")

                display_result(
                    prediction,
                    "Ham (Safe SMS)",
                    "Smishing"
                )

               
                with st.expander("Lihat fitur yang diekstraksi"):

                    st.json(sms_features.iloc[0].to_dict())

            except Exception as error:

                st.error("Terjadi kesalahan saat melakukan deteksi SMS.")

                st.code(str(error))


# =========================================================
# 11. EMAIL DETECTION PAGE
# =========================================================

elif menu == "📧 Email Detection":

    st.subheader("📧 Email Phishing Detection")

    st.write(
        "Masukkan isi email yang ingin diperiksa. "
        "Model akan mengklasifikasikan email menjadi "
        "Safe Email atau Phishing Email."
    )

    email_input = st.text_area(
        "Masukkan isi email:",
        height=250,
        placeholder=(
            "Dear Customer,\n\n"
            "Your account requires verification..."
        )
    )

    if st.button("🔍 Detect Email", key="email_button"):

        if not email_input.strip():

            st.warning("Silakan masukkan isi email terlebih dahulu.")

        else:

            try:

                cleaned_email = clean_email_text(email_input)

                prediction = email_model.predict([cleaned_email])[0]

                st.divider()

                st.subheader("Detection Result")

                display_result(
                    prediction,
                    "Safe Email",
                    "Phishing Email"
                )

            except Exception as error:

                st.error("Terjadi kesalahan saat melakukan deteksi Email.")

                st.code(str(error))


# =========================================================
# 12. URL DETECTION PAGE
# =========================================================

elif menu == "🌐 URL Detection":

    st.subheader("🌐 URL Phishing Detection")

    st.write(
        "Masukkan alamat URL yang ingin diperiksa. "
        "Model akan menganalisis 27 karakteristik URL "
        "untuk mengklasifikasikan apakah URL legitimate "
        "atau phishing."
    )

    url_input = st.text_input(
        "Masukkan URL:",
        placeholder="Contoh: https://example.com/login"
    )

    if st.button("🔍 Detect URL", key="url_button"):

        if not url_input.strip():

            st.warning("Silakan masukkan URL terlebih dahulu.")

        else:

            try:

                url_features = extract_url_features(url_input.strip())

                # Menyesuaikan urutan fitur dengan training
                missing_features = [
                    name for name in url_feature_names
                    if name not in url_features
                ]

                if missing_features:
                    raise ValueError(
                        f"Fitur tidak ditemukan: {missing_features}"
                    )

                url_input_features = pd.DataFrame(
                    [[url_features[name] for name in url_feature_names]],
                    columns=url_feature_names
                )

                prediction = url_model.predict(url_input_features)[0]

                st.divider()

                st.subheader("Detection Result")

                display_result(
                    prediction,
                    "Legitimate URL",
                    "Phishing URL"
                )

                
                with st.expander("Lihat 27 fitur URL"):

                    st.json(url_input_features.iloc[0].to_dict())


            except Exception as error:

                st.error("Terjadi kesalahan saat melakukan deteksi URL.")

                st.code(str(error))


# =========================================================
# 13. ABOUT PAGE
# =========================================================

elif menu == "ℹ️ About":

    st.subheader("About Cyber Threat Detection")

    st.write("""
    Cyber Threat Detection merupakan aplikasi berbasis
    Machine Learning yang dikembangkan untuk membantu
    mengidentifikasi potensi ancaman phishing pada
    berbagai media komunikasi digital.
    """)

    st.divider()

    st.subheader("Machine Learning Algorithms")

    st.markdown("""
    **1. SMS Phishing Detection**
    - Algorithm: Multinomial Naive Bayes
    - Features: TF-IDF dan fitur numerik
    - Classification: Ham dan Smishing

    **2. Email Phishing Detection**
    - Algorithm: Linear Support Vector Classification (LinearSVC)
    - Features: Character-level TF-IDF dan SelectKBest
    - Classification: Safe Email dan Phishing Email

    **3. URL Phishing Detection**
    - Algorithm: Random Forest
    - Features: 27 fitur karakteristik URL
    - Classification: Legitimate dan Phishing
    """)

    st.divider()

    st.caption(
        "Cyber Threat Detection"
    )


# =========================================================
# 14. FOOTER
# =========================================================

st.divider()

st.caption(
    "Cyber Threat Detection"
)
