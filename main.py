import streamlit as st
import google.generativeai as genai
import base64
import os
from PIL import Image

# --- ⚙️ PAGE CONFIGURATION ---
st.set_page_config(page_title="Swasthya Sahayak", layout="wide", initial_sidebar_state="expanded")

# --- 🔑 1. SMART ENGINE CONFIG ---
api_key = "AIzaSyC5n3cR8mQw0G2k7PBth5SczuknqJqklmk"
genai.configure(api_key=api_key)

def get_response(prompt, img=None):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        if img:
            return model.generate_content([prompt, img]), "Gemini 2.5 Flash"
        else:
            return model.generate_content(prompt), "Gemini 2.5 Flash"
    except Exception as e:
        try:
            fallback = genai.GenerativeModel('gemini-1.5-flash')
            if img:
                return fallback.generate_content([prompt, img]), "Gemini 1.5 Flash (Fallback)"
            else:
                return fallback.generate_content(prompt), "Gemini 1.5 Flash (Fallback)"
        except:
            return None, "Error"

# --- 🎨 3. UI CSS (IMAGES + BIG TEXT COMBO) ---
import base64

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return "" # Returns empty if image is missing

# Load Images
img_main = get_base64_of_bin_file("main_bg.jpg")
img_sidebar = get_base64_of_bin_file("sidebar_bg.jpg")

# Define Background Logic
if img_main:
    main_bg_css = f"""
        background-image: url("data:image/jpg;base64,{img_main}");
        background-size: cover;
        background-attachment: fixed;
    """
else:
    # Fallback to Gradient if image missing
    main_bg_css = "background: linear-gradient(to right, #eef2f3, #8e9eab);"

if img_sidebar:
    sidebar_bg_css = f"""
        background-image: url("data:image/jpg;base64,{img_sidebar}");
        background-size: cover;
    """
else:
    sidebar_bg_css = "background-color: #ffffff;"

st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{
        {main_bg_css}
    }}

    /* 2. Sidebar Background */
    [data-testid="stSidebar"] {{
        {sidebar_bg_css}
        border-right: 2px solid #d1d5db;
    }}

    /* 3. BIGGER FONTS (Global) */
    html, body, [class*="css"] {{
        font-family: 'Helvetica Neue', sans-serif;
    }}
    
    p, .stMarkdown, .stText, label {{
        font-size: 18px !important; 
        color: #000000 !important; /* Black text for contrast over images */
        font-weight: 600 !important;
    }}

    /* 4. SIDEBAR TITLE - SUPER SIZE */
    [data-testid="stSidebar"] h1 {{
        font-size: 3rem !important;
        text-align: center;
        color: #B91372 !important;
        text-transform: uppercase;
        font-weight: 900 !important;
        text-shadow: 2px 2px 0px #ffffff; /* White shadow to pop against bg */
        margin-bottom: 20px;
    }}
    
    /* 5. Headers */
    h1, h2, h3 {{
        color: #000000 !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px 0px rgba(255,255,255,0.7);
    }}

    /* 6. Glass Cards (To make text readable over images) */
    .report-card, .hospital-card {{
        background: rgba(255, 255, 255, 0.90); /* 90% Opaque White */
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }}

    /* 7. Nuclear Buttons */
    a[href="tel:108"] {{
        background-color: #DC2626 !important;
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        display: block;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
    }}
    [data-testid="stDownloadButton"] button {{
        background-color: #2563EB !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent;
        visibility: visible !important;
    }}
    </style>
""", unsafe_allow_html=True)
# --- 🏥 4. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🩺 SWASTHYA<br>SAHAYAK</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.success("🟢 System Online")
    
    st.markdown("### 📋 Patient Intake")
    role = st.selectbox("Operator Role", ["ASHA Worker", "PHC Nurse", "Emergency EMT"])
    age = st.number_input("Patient Age", 0, 120, 45)
    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    
    st.markdown("### 🌡️ Vitals")
    c1, c2 = st.columns(2)
    with c1: v_bp = st.text_input("BP", placeholder="120/80")
    with c2: v_hr = st.text_input("HR", placeholder="72")
    v_temp = st.text_input("Temp (°F)", placeholder="98.6")
    
    st.markdown("---")
    language = st.selectbox("Output Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada"])
    consent = st.checkbox("✅ I certify patient consent obtained.")

# --- 🚀 5. MAIN APP ---
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.title("Swasthya Sahayak: Elite Triage")
    st.markdown("**AI-Powered Clinical Decision Support System (CDSS) for Rural India**")

c_left, c_right = st.columns([1, 1], gap="large")

with c_left:
    st.info("🎙️ **Clinical Narrative**")
    user_text = st.text_area("Describe Symptoms", height=150, placeholder="E.g., Severe chest pain...")
    
    st.info("📸 **Visual Evidence**")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    run_btn = st.button("🔍 RUN CLINICAL ASSESSMENT", type="primary", use_container_width=True)

# --- 🧠 6. EXECUTION LOGIC ---
if run_btn:
    if not consent:
        st.error("⚠️ Compliance Error: You must certify patient consent to proceed.")
    elif not user_text and not uploaded_file:
        st.warning("⚠️ Input Error: Please provide symptoms or an image.")
    else:
        with c_right:
            with st.spinner("🔄 Analyzing Protocols..."):
                
                # --- PROMPT ---
                prompt = f"""
                ACT AS: Senior Medical Officer.
                PATIENT: {age}yo {gender}. BP: {v_bp}, HR: {v_hr}, Temp: {v_temp}.
                SYMPTOMS: {user_text}
                LANGUAGE: {language}

                TASK:
                1. ANALYZE risk severity (Red/Yellow/Green).
                2. PROVIDE a structured HTML report.

                IMPORTANT VISUAL INSTRUCTION:
                You must wrap the Triage Status word in a span with a specific color style.
                - If RED: <span style='color: #dc3545; font-weight:900;'>RED (CRITICAL)</span>
                - If YELLOW: <span style='color: #b38600; font-weight:900;'>YELLOW (URGENT)</span>
                - If GREEN: <span style='color: #28a745; font-weight:900;'>GREEN (STABLE)</span>

                OUTPUT FORMAT (HTML ONLY):
                <div style="margin-bottom:10px;">
                    <h2 style="margin:0; color:#333;">🚨 STATUS: [INSERT COLORED SPAN HERE]</h2>
                </div>
                <div style="margin-bottom:10px; color:#333;">
                      <b>🔬 Clinical Reasoning:</b><br>
                      [Bullet points]
                </div>
                <div style="background:#f9f9f9; padding:10px; border-radius:5px; color:#333;">
                      <b>🚑 ASHA Protocol:</b>
                      <ul><li>Step 1...</li></ul>
                </div>
                """
                
                img_data = Image.open(uploaded_file) if uploaded_file else None
                response, debug_info = get_response(prompt, img_data)
                
                if response:
                    clean_html = response.text.replace("```html", "").replace("```", "")
                    
                    if "RED" in clean_html.upper():
                        border_color = "#dc3545"
                        is_critical = True
                    elif "YELLOW" in clean_html.upper():
                        border_color = "#ffc107"
                        is_critical = True 
                    else:
                        border_color = "#28a745"
                        is_critical = False

                    # --- 1. EMERGENCY SECTION (TOP) ---
                    if is_critical:
                        st.error("🚨 CRITICAL PROTOCOL ACTIVATED - IMMEDIATE ACTION REQUIRED")
                        
                        b1, b2 = st.columns(2)
                        with b1:
                            st.link_button("📞 CALL 108 AMBULANCE", "tel:108", use_container_width=True)
                        with b2:
                            st.download_button("📥 DOWNLOAD REFERRAL SLIP", 
                                               data=f"REFERRAL SLIP\nPatient: {age}\nPriority: HIGH",
                                               file_name="referral.txt",
                                               use_container_width=True)
                        
                        st.markdown("### 🏥 Nearest Healthcare Facilities")
                        st.markdown(f"""
                        <div class="hospital-card">
                            <b>🏥 Govt. District Hospital (Level 1 Trauma)</b><br>
                            📍 Distance: 4.2 km (approx 12 mins)<br>
                            📞 <b>Contact:</b> +91-9988776655
                        </div>
                        <div class="hospital-card">
                            <b>🚑 Community Health Center (CHC)</b><br>
                            📍 Distance: 1.5 km (approx 5 mins)<br>
                            📞 <b>Contact:</b> +91-8877665544
                        </div>
                        """, unsafe_allow_html=True)

                    # --- 2. THE AI REPORT CARD (BOTTOM) ---
                    st.markdown(f"""
                    <div class="report-card" style="border-left: 8px solid {border_color};">
                        <div style="text-align:right; font-size:0.8rem; color:#888;">Model: {debug_info}</div>
                        {clean_html}
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error(f"❌ API Error: {debug_info}")

# --- ⚠️ SMALL FOOTER DISCLAIMER ---
st.markdown("---")
st.markdown("""
    <div style='background-color: #ffcc00; padding: 8px; border-radius: 5px; border: 2px solid #000000; text-align: center; margin-top: 25px; opacity: 0.8;'>
        <p style='color: #000000; margin: 0; font-weight: 800; font-size: 0.9rem;'>
            ⚠️ DEMO MODE: FOR RESEARCH/HACKATHON ONLY. NOT FOR MEDICAL USE.
        </p>
    </div>

""", unsafe_allow_html=True)






