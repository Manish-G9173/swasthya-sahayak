import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Swasthya Sahayak", page_icon="🏥")

# --- API KEY SETUP ---
# Tries to get the key from Streamlit Secrets.
# If running locally without secrets, replace "PASTE_YOUR_KEY_HERE" with your actual key.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        # REPLACE THIS STRING WITH YOUR ACTUAL API KEY IF NOT USING SECRETS
        api_key = "PASTE_YOUR_GOOGLE_API_KEY_HERE" 
    
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key Error: Please set your GOOGLE_API_KEY.")
    st.stop()


# --- 2. CSS & UI STYLING (RESTORED CLEAN VERSION) ---
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
    /* 1. Base Dark Backgrounds */
    .stApp {{ {main_bg_css} }}
    [data-testid="stSidebar"] {{ {sidebar_bg_css} border-right: 2px solid #B91372; }}

    /* 2. Global Text -> WHITE (For Dark Theme) */
    html, body, p, .stMarkdown, .stText, label, div, li, span, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
    }}

    /* 3. Title Style */
    h1 {{
        color: #B91372 !important; /* Brand Pink */
        font-weight: 900 !important;
        text-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        text-transform: uppercase;
    }}

    /* --- 4. VISIBILITY FIXES (CLEAN WHITE BOXES) --- */

    /* A. Call 108 Button (White Box + Black Text) */
    a[href="tel:108"] {{
        background-color: #ffffff !important;
        color: #000000 !important; /* BLACK TEXT */
        border: 3px solid #ff0000 !important;
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        text-align: center !important;
        display: block;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    /* B. Report Cards & Hospitals (White Box + Black Text) */
    .report-card, .hospital-card {{
        background-color: #ffffff !important; /* CLEAN WHITE */
        border: 2px solid #333 !important;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}

    /* Force text INSIDE cards to be BLACK (Like a paper report) */
    .report-card p, .report-card h1, .report-card h2, .report-card h3, .report-card li, .report-card span,
    .hospital-card p, .hospital-card h1, .hospital-card h2, .hospital-card h3, .hospital-card li, .hospital-card span {{
        color: #000000 !important; /* BLACK TEXT */
        font-weight: bold !important;
        text-shadow: none !important;
    }}

    /* --- 5. INPUT BARS (White Box + Black Text) --- */
    
    /* Select Boxes */
    .stSelectbox > div > div {{
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
    }}
    .stSelectbox > div > div div {{
        color: #000000 !important; /* BLACK TEXT */
        font-weight: bold !important;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] section {{
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
    }}
    [data-testid="stFileUploader"] section span, 
    [data-testid="stFileUploader"] section small {{
        color: #000000 !important; /* BLACK TEXT */
        font-weight: bold !important;
    }}

    /* Text Area */
    .stTextArea textarea {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
    }}

    /* Dropdown Options */
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
    
    role = st.selectbox("Operator Role", ["ASHA Worker", "Community Volunteer", "Nurse"])
    language = st.selectbox("Output Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada"])
    
    st.markdown("---")
    st.markdown("### **Emergency**")
    st.markdown('<a href="tel:108">📞 CALL 108 (AMBULANCE)</a>', unsafe_allow_html=True)
    
    if st.button("🏥 Find Nearest Hospitals"):
        hospital_list = """
        ### 🏥 Nearest Medical Centers Found:
        1. **District Civil Hospital** - 5km (Trauma Center Available)
        2. **Primary Health Center (PHC) Rampur** - 2km
        3. **LifeCare Private Clinic** - 8km
        
        *Ambulance ETA: ~15 Mins*
        """
        st.markdown(f'<div class="hospital-card">{hospital_list}</div>', unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title("Swasthya Sahayak: Elite Triage")
st.markdown("**AI-Powered Clinical Decision Support System (CDSS) for Rural India**")

# Inputs
symptoms = st.text_area("Describe Symptoms (Voice Input Supported)", placeholder="E.g., Severe chest pain radiating to left arm, sweating...")

uploaded_file = st.file_uploader("📸 Upload Visual Evidence (Wound/Skin/Eyes)", type=["jpg", "png", "jpeg"])

# --- 5. AI LOGIC ---
if st.button("🔍 RUN CLINICAL ASSESSMENT"):
    if not symptoms and not uploaded_file:
        st.warning("⚠️ Please provide symptoms or upload an image.")
    else:
        with st.spinner("⚡ Analyzing Symptoms & Vitals..."):
            
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

            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    image_data = uploaded_file.getvalue()
                    image_parts = [{"mime_type": uploaded_file.type, "data": image_data}]
                    response = model.generate_content([prompt, image_parts[0]])
                else:
                    response = model.generate_content(prompt)
                
                # Display Result in CLEAN WHITE CARD
                st.markdown(f'<div class="report-card">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
