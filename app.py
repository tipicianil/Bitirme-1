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
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

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
# 2. SIMULATOR PAGE (3-Step Control Panel)
# ==========================================
elif st.session_state.page == 'simulator':
    
    st.markdown('<h2 style="color: var(--text-color); border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 0; text-align: center;">Interactive Bioprocess Control Panel</h2>', unsafe_allow_html=True)
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
        st.error("System Error: '120_SuperPro_Input_List.xlsx' database file is missing from the directory.")
        st.stop()

    # Sayfayı 3 ana sütuna (Aşamalara) bölüyoruz
    col_input, col_metrics, col_output = st.columns([1.2, 1.2, 2.6]) 

    # --- ADIM 1: REAKTÖR GİRDİLERİ ---
    with col_input:
        st.markdown("### ⚙️ STEP 1\n**Reactor Kinetics**")
        st.caption("Adjust the experimental Monod data for the target strain.")
        
        exp_mu = st.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 0.70, 0.45, 0.01)
        exp_Ks = st.slider("Half-Saturation (Ks) [g/L]", 0.01, 1.50, 0.50, 0.01)
        
        st.markdown("---")
        st.warning("🔒 **Fixed Constraint:**\nCSTR capacity operates at 90% Working Volume.")

    # --- KNN MATCHING ALGORITHM ---
    norm_mu = (df['mu_max_UserSpecified'] - exp_mu) / (0.70 - 0.10)
    norm_Ks = (df['Ks_K1'] - exp_Ks) / (1.50 - 0.01)
    
    df['Distance'] = np.sqrt(norm_mu**2 + norm_Ks**2)
    matched_idx = df['Distance'].idxmin()
    matched_row = df.loc[matched_idx]
    image_index = int(matched_row['Screenshot_Index'])
    
    worst_output_kgh = 2.17022
    best_output_kgh = 2.33290
    scale_factor = (image_index - 1) / 119.0
    efficiency_score = 1.0 + (scale_factor * 9.0)
    expected_output = worst_output_kgh + (scale_factor * (best_output_kgh - worst_output_kgh))

    # --- ADIM 2: CANLI ANALİZ ---
    with col_metrics:
        st.markdown("### 📊 STEP 2\n**Live Analytics**")
        st.caption("Algorithm mapping to the nearest database scenario.")
        
        st.markdown(f"""<div class="knn-box">
<b>Target μ_max:</b> {exp_mu:.2f} ➔ <i>Matched: {matched_row['mu_max_UserSpecified']:.3f}</i><br>
<b>Target K_s:</b> {exp_Ks:.2f} ➔ <i>Matched: {matched_row['Ks_K1']:.3f}</i>
</div>""", unsafe_allow_html=True)
        
        if efficiency_score >= 8.0:
            st.success(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
        elif efficiency_score >= 4.0:
            st.warning(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
        else:
            st.error(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
            
        st.metric(label="Estimated Lactic Acid Output", value=f"~ {expected_output:.5f} kg/h")

    # --- ADIM 3: SUPERPRO ÇIKTISI ---
    with col_output:
        st.markdown("### 🏭 STEP 3\n**SuperPro Flowsheet**")
        st.caption("Calibrated industrial plant simulation output.")
        
        image_file = f"SuperPro_{image_index}.png"
        
        if os.path.exists(image_file):
            img = Image.open(image_file)
            st.image(img, width=480) # Ekranı taşırmayacak genişlik
        else:
            st.error(f"Awaiting validation data: Image '{image_file}' is currently missing from the directory.")
