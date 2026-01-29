import streamlit as st
import google.generativeai as genai
import base64
import os
from PIL import Image

# --- ⚙️ PAGE CONFIGURATION ---
st.set_page_config(page_title="Swasthya Sahayak | AI Triage", layout="wide", page_icon="🩺")

# --- 🔑 1. SMART ENGINE CONFIG ---
# ⚠️ PASTE YOUR NEW API KEY BELOW (Inside the quotes)
api_key = "AIzaSyBYlLb8SCMesMgzBDk67v4oCFgmZ3yJJ5k"
genai.configure(api_key=api_key)

# --- 🧠 INTELLIGENT MODEL SWITCHER (Fixed Names) ---
def get_response(prompt, img=None):
    # TIER 1: Try Gemini 1.5 Pro (High Intelligence)
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        if img:
            return model.generate_content([prompt, img]), "Gemini 2.5 Pro (High Intel)"
        else:
            return model.generate_content(prompt), "Gemini 2.5 Pro (High Intel)"
            
    except Exception as e1:
        # TIER 2: Fallback to Gemini 1.5 Flash (High Speed)
        try:
            # print(f"Pro model busy, switching to Flash: {e1}") # Debug
            fallback = genai.GenerativeModel('gemini-2.5-flash')
            if img:
                return fallback.generate_content([prompt, img]), "Gemini 2.5 Flash (Backup)"
            else:
                return fallback.generate_content(prompt), "Gemini 2.5 Flash (Backup)"
                
        except Exception as e2:
            return None, f"⚠️ Server Busy or Key Error: {str(e2)}"

# --- 🖼️ 2. ASSET LOADING ---
def get_base64_img(file_path):
    if not os.path.exists(file_path):
        if file_path.endswith(".jpg"): file_path = file_path + ".jpeg"
        elif file_path.endswith(".jpeg"): file_path = file_path.replace(".jpeg", ".jpg")
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

main_bg = get_base64_img("main_bg.jpg.jpeg")
side_bg = get_base64_img("sidebar_bg.jpg.jpeg")

# --- 🎨 3. UI CSS ---
bg_style = f'background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("data:image/jpeg;base64,{main_bg}");' if main_bg else 'background: #0e1117;'
sidebar_style = f'background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{side_bg}");' if side_bg else 'background: #161b22;'

st.markdown(f"""
    <style>
    .stApp {{
        {bg_style}
        background-size: cover;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        {sidebar_style}
        background-size: cover !important;
        border-right: 3px solid #B91372 !important;
    }}
    h1 {{
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        padding-bottom: 10px;
    }}
    h2, h3 {{ color: white !important; }}
    p, label {{ color: #e0e0e0 !important; }}

    a[href="tel:108"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ff4b4b !important;
        font-weight: 900 !important;
        text-align: center !important;
    }}
    a[href="tel:108"] > * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}
    [data-testid="stDownloadButton"] button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #4b88ff !important;
        font-weight: 900 !important;
    }}
    [data-testid="stDownloadButton"] button * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        fill: #000000 !important;
    }}
    .report-card {{
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: #333;
        margin-bottom: 20px;
    }}
    .hospital-card {{
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        color: #333;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }}
    .sidebar-brand {{
        color: #B91372;
        font-size: 1.8rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
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


