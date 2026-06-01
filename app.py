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

# Custom CSS for Full Page Frame, Cover Page, RED Buttons & Lightbox
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

/* Cover Page Typography & Proper Spacing */
.cover-container {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 40px;
    color: var(--text-color);
}
.cover-uni {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.cover-dept {
    font-size: 1.3rem;
    font-weight: 600;
    opacity: 0.9;
    margin-bottom: 30px;
    text-transform: uppercase;
}
.cover-course {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 30px;
    line-height: 1.5;
}
.cover-title {
    font-size: 2.1rem; 
    font-weight: 900; 
    color: var(--text-color);
    line-height: 1.4;
    margin-bottom: 40px;
    padding: 0 10%;
}
.cover-student {
    font-size: 1.2rem;
    font-weight: 800;
    margin-bottom: 30px;
    line-height: 1.5;
}
.cover-advisor {
    font-size: 1.1rem;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: 20px;
    line-height: 1.5;
}

/* Unified Content Block for Abstract */
.content-block {
    padding: 20px 40px;
    font-size: 1.15rem; 
    line-height: 1.8; 
    color: var(--text-color); 
    text-align: justify; 
    margin: 0 auto;
    max-width: 1000px;
    border-top: 2px dashed rgba(156, 163, 175, 0.3);
}

.qr-thanks {
    text-align: center; 
    font-size: 1.15rem;
    color: var(--text-color);
    margin-top: 40px; 
    margin-bottom: 30px;
    font-weight: 700; 
    font-style: italic;
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

/* TIKLANINCA BÜYÜYEN GÖRSEL (LIGHTBOX) MANTIĞI */
.lightbox-check {
    display: none;
}
.lightbox-img {
    cursor: zoom-in;
    max-width: 1000px;
    width: 100%;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px;
    background-color: white;
    transition: all 0.3s ease;
    position: relative;
    z-index: 10;
}
.lightbox-check:checked + label .lightbox-img {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 95vw;
    max-width: 1600px; /* Geniş ekranlarda muazzam durur */
    z-index: 999999;
    cursor: zoom-out;
    box-shadow: 0 0 0 10000px rgba(0,0,0,0.85); /* Arkaplanı sinematik şekilde karartır */
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'active_step' not in st.session_state:
    st.session_state.active_step = 'reactor'

# Slider değerlerini hafızada tutuyoruz
if 'stored_mu' not in st.session_state:
    st.session_state.stored_mu = 0.45
if 'stored_Ks' not in st.session_state:
    st.session_state.stored_Ks = 0.50

def enter_simulator():
    st.session_state.page = 'simulator'

def set_step(step):
    st.session_state.active_step = step

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
Final Project Report
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
    
    # MADDELER BÖLÜM 1
    st.markdown("""<div class="content-block">
<b>Project Abstract & Evolution:</b><br>
This interactive digital twin was developed within the scope of a senior graduation project at the Bioengineering Department of Marmara University. Engineered by Mehmet Anıl Tipici, this platform bridges the gap between theoretical biological kinetics and industrial-scale chemical plant operations. 
<br><br>
<b>Project Milestones:</b>
<ul>
    <li style="margin-bottom: 10px;"><b>Foundation & Waste Valorization:</b> The study initially aimed to design a sustainable, closed-loop bioprocess for converting organic food waste into lactic acid—a crucial precursor for PLA bioplastics—using <i>Lactiplantibacillus plantarum</i>.</li>
    <li style="margin-bottom: 20px;"><b>Process Re-engineering:</b> During the early design stages, a Batch Processing topology was investigated. However, due to synchronization latency and software constraints within SuperPro Designer, the plant configuration was strategically re-engineered into a Continuous Flow (CSTR) model to ensure steady-state stability.</li>
</ul>
</div>""", unsafe_allow_html=True)

    # TIKLANINCA BÜYÜYEN SÜREÇ GÖRSELİ (CSS LIGHTBOX HİLESİ)
    process_image_path = "image_0d8649.png"
    if os.path.exists(process_image_path):
        encoded_process = base64.b64encode(open(process_image_path, 'rb').read()).decode()
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <input type="checkbox" id="zoom-img-1" class="lightbox-check">
            <label for="zoom-img-1" style="width: 100%; max-width: 1000px; text-align: center;">
                <img src="data:image/png;base64,{encoded_process}" class="lightbox-img" title="Click to enlarge">
            </label>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="text-align:center; color:red;">Process Flow image ({process_image_path}) not found. Please upload it to your folder.</p>', unsafe_allow_html=True)

    # MADDELER BÖLÜM 2
    st.markdown("""<div class="content-block">
<ul>
    <li style="margin-bottom: 10px;"><b>The Digital Twin Expansion:</b> Building upon the successful continuous process model, the project's vision significantly expanded. Instead of limiting the simulation to a single microbial strain, the scope shifted to evaluating and comparing multiple strains with distinct kinetic potentials.</li>
    <li><b>Interactive Kinetic Simulation:</b> The current platform utilizes a K-Nearest Neighbors (KNN) machine learning algorithm. It actively maps user-defined Monod kinetics (Max Growth Rate and Half-Saturation) against a comprehensive database of 120 pre-simulated industrial configurations, delivering real-time efficiency assessments and precise SuperPro Designer flowsheets.</li>
</ul>
<br>
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
    st.markdown("<br>", unsafe_allow_html=True)
    
    @st.cache_data
    def load_data():
        try:
            temp_df = pd.read_excel('120_SuperPro_Input_List.xlsx')
            return temp_df.dropna(subset=['Screenshot_Index'])
        except FileNotFoundError:
            return None

    df = load_data()
    if df is None:
        st.error("System Error: '120_SuperPro_Input_List.xlsx' database file is missing.")
        st.stop()

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
