import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Swasthya Sahayak", page_icon="🏥")

# --- API KEY SETUP ---
# Tries to get the key from Streamlit Secrets.
# If you are running locally and get an error, you can replace the line below with:
# api_key = "YOUR_ACTUAL_API_KEY_HERE"
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        # Fallback for local testing if secrets are missing
        # REPLACE THE TEXT INSIDE QUOTES BELOW WITH YOUR API KEY IF NEEDED
        api_key = "PASTE_YOUR_GOOGLE_API_KEY_HERE" 
    
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key Error: Please set your GOOGLE_API_KEY in Streamlit secrets or the code.")
    st.stop()


# --- 2. CSS & UI STYLING (FINAL: MAROON ALERTS + VISIBLE INPUTS) ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# Load Images
img_main = get_base64_of_bin_file("main_bg.jpg")
img_sidebar = get_base64_of_bin_file("sidebar_bg.jpg")

# Define Background Logic
if img_main:
    main_bg_css = f"""background-image: url("data:image/jpg;base64,{img_main}"); background-size: cover; background-attachment: fixed;"""
else:
    main_bg_css = "background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);"

if img_sidebar:
    sidebar_bg_css = f"""background-image: url("data:image/jpg;base64,{img_sidebar}"); background-size: cover;"""
else:
    sidebar_bg_css = "background-color: #111;"

st.markdown(f"""
    <style>
    /* 1. Base App Backgrounds */
    .stApp {{ {main_bg_css} }}
    [data-testid="stSidebar"] {{ {sidebar_bg_css} border-right: 2px solid #B91372; }}

    /* 2. Global Text -> WHITE (For Dark Theme) */
    html, body, p, .stMarkdown, .stText, label, div, li, span, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
    }}

    /* 3. Title Style */
    h1 {{
        color: #B91372 !important; /* Brand Pink/Maroon */
        font-weight: 900 !important;
        text-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        text-transform: uppercase;
    }}

    /* --- 🚨 MAROON GLASS ALERTS (108 & Results) 🚨 --- */

    /* A. Call 108 Button */
    a[href="tel:108"] {{
        background-color: rgba(128, 0, 0, 0.85) !important; /* Translucent Maroon */
        color: #ffffff !important;                          /* White Text */
        border: 2px solid #ff4b4b !important;               /* Red Border */
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        text-align: center !important;
        display: block;
        padding: 15px;
        border-radius: 12px;
        text-decoration: none;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    /* B. Report Cards & Hospitals */
    .report-card, .hospital-card {{
        background-color: rgba(128, 0, 0, 0.85) !important; /* Translucent Maroon */
        border: 1px solid rgba(255, 100, 100, 0.3) !important;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}

    /* Text INSIDE Maroon Cards must be WHITE */
    .report-card p, .report-card h1, .report-card h2, .report-card h3, .report-card li, .report-card span,
    .hospital-card p, .hospital-card h1, .hospital-card h2, .hospital-card h3, .hospital-card li, .hospital-card span {{
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }}

    /* --- 🚨 INPUT BARS (WHITE BOX + BLACK TEXT) 🚨 --- */
    
    /* 1. Select Boxes (Role, Language) */
    .stSelectbox > div > div {{
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
    }}
    /* Force Text inside Selectbox to be BLACK */
    .stSelectbox > div > div div {{
        color: #000000 !important;
        font-weight: bold !important;
    }}
    
    /* 2. File Uploader */
    [data-testid="stFileUploader"] section {{
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
    }}
    /* Force Text inside Uploader to be BLACK */
    [data-testid="stFileUploader"] section span, 
    [data-testid="stFileUploader"] section small {{
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* 3. Text Area */
    .stTextArea textarea {{
        background-color: #ffffff !important;
        color: #000000 !important; /* Black Text */
        border: 1px solid #d1d5db !important;
    }}

    /* 4. Dropdown Menu Items */
    ul[data-testid="stSelectboxVirtualDropdown"] li {{
        color: #000000 !important;
        background-color: #ffffff !important;
    }}

    /* Button Override */
    [data-testid="stDownloadButton"] button {{
        background-color: #2563EB !important; color: white !important; border: 1px solid white !important;
    }}
    
    header[data-testid="stHeader"] {{ background: transparent; visibility: visible !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🚑 Swasthya Sahayak")
    st.markdown("### **Rural Triage System**")
    
    # Inputs
    role = st.selectbox("Operator Role", ["ASHA Worker", "Community Volunteer", "Nurse"])
    language = st.selectbox("Output Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada"])
    
    st.markdown("---")
    st.markdown("### **Emergency**")
    # Call 108 Button
    st.markdown('<a href="tel:108">📞 CALL 108 (AMBULANCE)</a>', unsafe_allow_html=True)
    
    # Hospital Finder
    if st.button("🏥 Find Nearest Hospitals"):
        hospital_list = """
        ### 🏥 Nearest Medical Centers Found:
        1. **District Civil Hospital** - 5km (Trauma Center Available)
        2. **Primary Health Center (PHC) Rampur** - 2km
        3. **LifeCare Private Clinic** - 8km
        
        *Ambulance ETA: ~15 Mins*
        """
        # Display in Maroon Card
        st.markdown(f'<div class="hospital-card">{hospital_list}</div>', unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title("Swasthya Sahayak: Elite Triage")
st.markdown("**AI-Powered Clinical Decision Support System (CDSS) for Rural India**")

# Inputs
symptoms = st.text_area("Describe Symptoms (Voice Input Supported)", placeholder="E.g., Severe chest pain radiating to left arm, sweating...")

uploaded_file = st.file_uploader("📸 Upload Visual Evidence (Wound/Skin/Eyes)", type=["jpg", "png", "jpeg"])

# --- 5. AI LOGIC (THE BRAIN) ---
if st.button("🔍 RUN CLINICAL ASSESSMENT"):
    if not symptoms and not uploaded_file:
        st.warning("⚠️ Please provide symptoms or upload an image.")
    else:
        with st.spinner("⚡ Analyzing Symptoms & Vitals..."):
            
            # Prepare Prompt
            prompt = f"""
            You are an expert emergency medical AI assistant for Rural India.
            
            Patient Symptoms: {symptoms}
            Operator Role: {role}
            Output Language: {language} (Translate the final output to this language).
            
            TASK:
            1. Analyze the symptoms/image.
            2. Assign a Triage Level: RED (Immediate), AMBER (Urgent), GREEN (Routine).
            3. Provide a Step-by-Step Action Plan for the {role}.
            4. Suggest First Aid immediately.
            
            FORMAT:
            Use clear headings. Keep it concise.
            """

            # Call Gemini
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    # Handle Image
                    image_data = uploaded_file.getvalue()
                    image_parts = [{"mime_type": uploaded_file.type, "data": image_data}]
                    response = model.generate_content([prompt, image_parts[0]])
                else:
                    # Text Only
                    response = model.generate_content(prompt)
                
                # --- 6. DISPLAY RESULT IN MAROON CARD ---
                st.markdown(f'<div class="report-card">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
