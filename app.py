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

# Custom CSS for Full Page Frame & Cover Page Aesthetic
st.markdown("""
<style>
.stApp {
    border: 12px solid;
    border-image: linear-gradient(45deg, #1E3A8A, #10B981) 1;
    background-color: transparent; 
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
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
    font-size: 1.1rem;
}

/* Ok İşaretleri İçin Stil */
.process-arrow {
    text-align: center;
    font-size: 2rem;
    color: #10B981;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION & WORKFLOW ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'active_step' not in st.session_state:
    st.session_state.active_step = 'reactor'
if 'sim_mu' not in st.session_state:
    st.session_state.sim_mu = 0.45
if 'sim_Ks' not in st.session_state:
    st.session_state.sim_Ks = 0.50

def enter_simulator():
    st.session_state.page = 'simulator'

# ==========================================
# 1. LANDING PAGE (Formal Cover & Abstract)
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
# 2. SIMULATOR PAGE (Interactive Process Flow)
# ==========================================
elif st.session_state.page == 'simulator':
    
    st.markdown('<h2 style="color: var(--text-color); border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 0; text-align: center;">Interactive Bioprocess Control Panel</h2>', unsafe_allow_html=True)
    
    # --- İNTERAKTİF SÜREÇ BUTONLARI (FLOWCHART SİMÜLASYONU) ---
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, arr_col1, btn_col2, arr_col2, btn_col3 = st.columns([3, 1, 3, 1, 3])
    
    with btn_col1:
        if st.button("⚙️ STEP 1: CSTR Reactor Input", use_container_width=True, type="primary" if st.session_state.active_step == 'reactor' else "secondary"):
            st.session_state.active_step = 'reactor'
    
    with arr_col1:
        st.markdown('<div class="process-arrow">➔</div>', unsafe_allow_html=True)
        
    with btn_col2:
        if st.button("📊 STEP 2: Live Analytics", use_container_width=True, type="primary" if st.session_state.active_step == 'analytics' else "secondary"):
            st.session_state.active_step = 'analytics'
            
    with arr_col2:
        st.markdown('<div class="process-arrow">➔</div>', unsafe_allow_html=True)
        
    with btn_col3:
        if st.button("🏭 STEP 3: SuperPro Output", use_container_width=True, type="primary" if st.session_state.active_step == 'output' else "secondary"):
            st.session_state.active_step = 'output'
            
    st.markdown("---")

    # --- VERİ VE KNN ALGORİTMASI HAZIRLIĞI ---
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

    norm_mu = (df['mu_max_UserSpecified'] - st.session_state.sim_mu) / (0.70 - 0.10)
    norm_Ks = (df['Ks_K1'] - st.session_state.sim_Ks) / (1.50 - 0.01)
    
    df['Distance'] = np.sqrt(norm_mu**2 + norm_Ks**2)
    matched_idx = df['Distance'].idxmin()
    matched_row = df.loc[matched_idx]
    image_index = int(matched_row['Screenshot_Index'])
    
    worst_output_kgh = 2.17022
    best_output_kgh = 2.33290
    scale_factor = (image_index - 1) / 119.0
    efficiency_score = 1.0 + (scale_factor * 9.0)
    expected_output = worst_output_kgh + (scale_factor * (best_output_kgh - worst_output_kgh))

    # --- SEÇİLEN AŞAMAYA GÖRE EKRANI GÜNCELLEME ---
    
    # ADIM 1: REAKTÖR GİRDİLERİ
    if st.session_state.active_step == 'reactor':
        st.markdown("### Control Panel: Strain Kinetics")
        st.info("Adjust the experimental Monod parameters. The system will automatically calculate the nearest industrial scenario.")
        
        # Değerler değiştirildiğinde session_state'e kaydedilir
        new_mu = st.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 0.70, st.session_state.sim_mu, 0.01)
        new_Ks = st.slider("Half-Saturation (Ks) [g/L]", 0.01, 1.50, st.session_state.sim_Ks, 0.01)
        
        st.session_state.sim_mu = new_mu
        st.session_state.sim_Ks = new_Ks
        
        st.warning("🔒 **Fixed Constraint:** CSTR capacity mathematically bounded to 90% Working Volume.")

    # ADIM 2: CANLI ANALİZ
    elif st.session_state.active_step == 'analytics':
        st.markdown("### Process Analytics")
        col_m1, col_m2 = st.columns([1, 1])
        
        with col_m1:
            st.markdown("#### Database Matching Log")
            st.markdown(f"""<div class="knn-box">
            <b>Your Target μ_max:</b> {st.session_state.sim_mu:.2f} ➔ <i>System Matched: {matched_row['mu_max_UserSpecified']:.3f}</i><br><br>
            <b>Your Target K_s:</b> {st.session_state.sim_Ks:.2f} ➔ <i>System Matched: {matched_row['Ks_K1']:.3f}</i>
            </div>""", unsafe_allow_html=True)
            
        with col_m2:
            st.markdown("#### Projected Efficiency")
            if efficiency_score >= 8.0:
                st.success(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
            elif efficiency_score >= 4.0:
                st.warning(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
            else:
                st.error(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
                
            st.metric(label="Estimated Lactic Acid Output", value=f"~ {expected_output:.5f} kg/h")

    # ADIM 3: SUPERPRO ÇIKTISI
    elif st.session_state.active_step == 'output':
        st.markdown("### Retrieved SuperPro Designer Flowsheet")
        st.caption(f"Displaying Process File: SuperPro_{image_index}.png")
        
        image_file = f"SuperPro_{image_index}.png"
        if os.path.exists(image_file):
            img = Image.open(image_file)
            st.image(img, use_container_width=True) 
        else:
            st.error(f"Awaiting validation data: Image '{image_file}' is currently missing from the directory.")
