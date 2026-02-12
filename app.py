from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-3-flash-preview")

def get_gemini_response(input_text, image, prompt):
    response = model.generate_content(
        [prompt, input_text, image],
        stream=False
    )
    return response.text


# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Civil Engineering Insight Studio",
    page_icon="🏗️",
    layout="wide"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #1f2937;
}

.sub-title {
    text-align: center;
    color: #4b5563;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-top: 20px;
}

.result-box {
    background-color: #f9fafb;
    padding: 20px;
    border-left: 6px solid #2563eb;
    border-radius: 12px;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    padding: 12px 22px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #1e40af;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown('<div class="main-title">🏗️ Civil Engineering Insight Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI-powered structural analysis & engineering insights from images</div>',
    unsafe_allow_html=True
)

# ===================== SIDEBAR =====================
st.sidebar.header("⚙️ Input Panel")

input_text = st.sidebar.text_area(
    "Additional Instructions (optional)",
    placeholder="e.g., Focus on cracks, corrosion, or load-bearing issues"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Civil Structure Image",
    type=["jpg", "jpeg", "png"]
)

submit = st.sidebar.button("🔍 Analyze Structure")

# ===================== MAIN LAYOUT =====================
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📷 Uploaded Image")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    else:
        st.info("Upload an image from the sidebar to preview it here.")

with col2:
    st.markdown("### 🧠 Engineering Analysis")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    prompt = """
    You are a civil engineer.
    Analyze the given image and explain:

    1. Type of structure
    2. Materials used
    3. Structural observations
    4. Safety or maintenance insights
    """

    if submit:
        if uploaded_file is None:
            st.warning("Please upload an image to analyze.")
        else:
            try:
                response = get_gemini_response(input_text, image, prompt)
                st.markdown(
                    f'<div class="result-box">{response}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Click **Analyze Structure** to generate insights.")

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown(
    "<hr><center>🚧 Built with Gemini AI · Streamlit · Civil Engineering Intelligence</center>",
    unsafe_allow_html=True
)
