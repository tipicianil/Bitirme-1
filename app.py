import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import base64

# --- PAGE CONFIGURATION & ACADEMIC THEME ---
st.set_page_config(
    page_title="Bioengineering Project-1 | Midterm Report", 
    page_icon="🎓", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for Full Page Frame, Cover Page & RED Buttons
st.markdown("""
<style>
.stApp {
    border: 12px solid;
    border-image: linear-gradient(45deg, #1E3A8A, #10B981) 1;
    background-color: transparent; 
}

/* KESİN KIRMIZI AKTİF BUTON (PRIMARY) STİLİ */
button[kind="primary"] {
    background-color: #EF4444 !important; 
    border-color: #EF4444 !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease;
}
button[kind="primary"]:hover {
    background-color: #DC2626 !important; 
    border-color: #DC2626 !important;
}

/* İkincil (Pasif) Buton Stili */
button[kind="secondary"] {
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

.knn-box {
    background-color: rgba(59, 130, 246, 0.05);
    border-left: 4px solid #3B82F6;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 1.1rem;
}
.step-container {
    padding: 20px;
    background-color: rgba(0,0,0,0.02);
    border-radius: 0 0 10px 10px;
    margin-bottom: 20px;
    border: 1px solid rgba(156, 163, 175, 0.2);
    border-top: none;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (GÜÇLENDİRİLMİŞ HAFIZA) ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'active_step' not in st.session_state:
    st.session_state.active_step = 'reactor'

# Değerleri saklayacağımız GİZLİ KASALAR
if 'stored_mu' not in st.session_state:
    st.session_state.stored_mu = 0.45
if 'stored_Ks' not in st.session_state:
    st.session_state.stored_Ks = 0.50

def enter_simulator():
    st.session_state.page = 'simulator'

def set_step(step):
    st.session_state.active_step = step

# Slider oynatıldığı an değerleri kasaya kaydeden fonksiyon
def update_kinetics():
    st.session_state.stored_mu = st.session_state.temp_mu
    st.session_state.stored_Ks = st.session_state.temp_Ks

# ==========================================
# 1. LANDING PAGE
# ==========================================
if st.session_state.page == 'landing':
    
    if os.path.exists("marmara.png"):
        with open("marmara.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        logo_html = f"""<div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
<img src="data:image/png;base64,{encoded_string}" style="max-width: 160px; background-color: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</div>"""
        st.markdown(logo_html, unsafe_allow_html=True)
            
    st.markdown("""<div class="cover-container">
<div class="cover-uni">MARMARA UNIVERSITY<br>FACULTY OF ENGINEERING</div>
<div class="cover-dept">BIOENGINEERING DEPARTMENT</div>
<div class="cover-course">
BIOE 4298.7<br>
Bioengineering Project-1<br>
Midterm Project Report
</div>
<div class="cover-title">
“Design and kinetic modeling of the Lactiplantibacillus plantarum:<br>
compare different strains with different kinetic parameters”
</div>
<div class="cover-student">
Mehmet Anıl Tipici<br>
150819054
</div>
<div class="cover-advisor">
Submitted to:<br>
Prof. Dr. Nihat Alpagu SAYAR
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="content-block">
<b>Project Abstract:</b><br>
This interactive digital twin was developed within the scope of a senior graduation project at the Bioengineering Department of Marmara University. The model was designed and engineered by Mehmet Anıl Tipici to bridge the gap between theoretical biological kinetics and industrial-scale chemical plant operations. 
<br><br>
Initially, the study was conceptualized to optimize the bioprocess parameters for a single, specific strain of <i>Lactiplantibacillus plantarum</i>. However, to provide a more robust and comprehensive engineering solution, the scope was significantly expanded. The current model was constructed to compare different strains possessing distinct kinetic parameters, allowing the evaluation of how varying biological potentials translate into industrial-scale lactic acid yield.
<br><br>
To achieve this objective, a Continuous Stirred-Tank Reactor (CSTR) model was utilized, strictly constrained to operate at a <b>90% working-to-vessel volume ratio</b>. Experimental Monod kinetic data—namely, the Maximum Specific Growth Rate (μ_max) and the Half-Saturation Constant (K_s)—can be inputted into the system. The backend algorithm employs a K-Nearest Neighbors (KNN) approach to evaluate these inputs against a comprehensive database of pre-simulated industrial configurations. Ultimately, the system aims to assign a standardized efficiency score and retrieve the precise, calibrated <b>SuperPro Designer</b> process output for the user.
<br><br>
<div class="qr-thanks">Special thanks are extended to the jury members and attendees for scanning the QR code and exploring the details of this graduation project.</div>
</div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.button("Launch Interactive Simulator", on_click=enter_simulator, type="primary", use_container_width=True)

# ==========================================
# 2. SIMULATOR PAGE
# ==========================================
elif st.session_state.page == 'simulator':
    
    st.markdown('<h2 style="text-align: center;">Interactive Bioprocess Control Panel</h2>', unsafe_allow_html=True)
    
    @st.cache_data
    def load_data():
        try:
            temp_df = pd.read_excel('120_SuperPro_Input_List.xlsx')
            return temp_df.dropna(subset=['Screenshot_Index'])
        except FileNotFoundError:
            return None

    df = load_data()
    if df is None:
        st.error("System Error: Database file missing.")
        st.stop()

    # Sistemin matematiği artık doğrudan GİZLİ KASADAN (stored) okuyor
    exp_mu = st.session_state.stored_mu
    exp_Ks = st.session_state.stored_Ks

    norm_mu = (df['mu_max_UserSpecified'] - exp_mu) / (0.70 - 0.10)
    norm_Ks = (df['Ks_K1'] - exp_Ks) / (1.50 - 0.01)
    df['Distance'] = np.sqrt(norm_mu**2 + norm_Ks**2)
    matched_idx = df['Distance'].idxmin()
    matched_row = df.loc[matched_idx]
    image_index = int(matched_row['Screenshot_Index'])
    
    scale_factor = (image_index - 1) / 119.0
    efficiency_score = 1.0 + (scale_factor * 9.0)
    expected_output = 2.17022 + (scale_factor * (2.33290 - 2.17022))

    # --- AKORDEON DÜZENİ ---

    # ADIM 1
    st.button("⚙️ Enter Kinetic Parameters", use_container_width=True, 
              type="primary" if st.session_state.active_step == 'reactor' else "secondary",
              on_click=set_step, args=('reactor',))
              
    if st.session_state.active_step == 'reactor':
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        # on_change ile kullanıcı sliderı bıraktığı an değerler kasaya gider
        st.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 0.70, 
                  value=st.session_state.stored_mu, 
                  key="temp_mu", step=0.01, on_change=update_kinetics)
                  
        st.slider("Half-Saturation (Ks) [g/L]", 0.01, 1.50, 
                  value=st.session_state.stored_Ks, 
                  key="temp_Ks", step=0.01, on_change=update_kinetics)
                  
        st.warning("🔒 **Fixed Constraint:** CSTR capacity mathematically bounded to 90% Working Volume.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ADIM 2
    st.button("📊 Mathematical/Theoretical Calculations", use_container_width=True, 
              type="primary" if st.session_state.active_step == 'analytics' else "secondary",
              on_click=set_step, args=('analytics',))
              
    if st.session_state.active_step == 'analytics':
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.markdown(f"""<div class="knn-box">
            <b>Target μ_max:</b> {exp_mu:.2f} ➔ <i>Matched: {matched_row['mu_max_UserSpecified']:.3f}</i><br><br>
            <b>Target K_s:</b> {exp_Ks:.2f} ➔ <i>Matched: {matched_row['Ks_K1']:.3f}</i>
            </div>""", unsafe_allow_html=True)
        with col_m2:
            st.metric(label="Estimated Lactic Acid Output", value=f"~ {expected_output:.5f} kg/h")
            if efficiency_score >= 8.0: st.success(f"**Efficiency Score:** ### ~ {efficiency_score:.1f} / 10.0")
            elif efficiency_score >= 4.0: st.warning(f"**Efficiency Score:** ### ~ {efficiency_score:.1f} / 10.0")
            else: st.error(f"**Efficiency Score:** ### ~ {efficiency_score:.1f} / 10.0")
        st.markdown('</div>', unsafe_allow_html=True)

    # ADIM 3
    st.button("🏭 SuperPro Designer Output", use_container_width=True, 
              type="primary" if st.session_state.active_step == 'output' else "secondary",
              on_click=set_step, args=('output',))
              
    if st.session_state.active_step == 'output':
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        image_file = f"SuperPro_{image_index}.png"
        if os.path.exists(image_file):
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px;">
                <img src="data:image/png;base64,{base64.b64encode(open(image_file, 'rb').read()).decode()}" width="600" style="border: 1px solid #ccc; border-radius: 5px;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Image file missing.")
        st.markdown('</div>', unsafe_allow_html=True)
