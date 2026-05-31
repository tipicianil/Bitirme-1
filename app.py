import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

# --- PAGE CONFIGURATION & ACADEMIC THEME ---
st.set_page_config(
    page_title="Design and kinetic modeling of the Lactiplantibacillus plantarum", 
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for academic aesthetic
st.markdown("""
    <style>
    .main-header {font-size: 2.2rem; font-weight: 700; color: #1E3A8A; text-align: center; margin-bottom: 10px; line-height: 1.2;}
    .sub-header {font-size: 1.2rem; font-weight: 400; color: #4B5563; text-align: center; margin-bottom: 30px;}
    .section-title {color: #1E3A8A; border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; margin-top: 25px;}
    .qr-thanks {text-align: center; font-style: italic; color: #10B981; margin-top: 50px; font-weight: 500;}
    .content-text {font-size: 1.1rem; line-height: 1.6; color: #374151; text-align: justify;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def enter_simulator():
    st.session_state.page = 'simulator'

# ==========================================
# 1. LANDING PAGE (Formal Academic Abstract)
# ==========================================
if st.session_state.page == 'landing':
    
    st.markdown('<p class="main-header">Design and kinetic modeling of the <i>Lactiplantibacillus plantarum</i>: compare different strains with different kinetic parameters</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Marmara University • Bioengineering Department • Senior Graduation Project</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        st.markdown('<h3 class="section-title">Project Overview & Development</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content-text">
        This interactive digital twin was developed within the scope of a senior graduation project at the Bioengineering Department of Marmara University. The model was designed and engineered by Mehmet Anıl Tipici to bridge the gap between theoretical biological kinetics and industrial-scale chemical plant operations. The primary objective of this system is to simulate the continuous production of lactic acid utilizing <i>Lactiplantibacillus plantarum</i>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<h3 class="section-title">Scientific Evolution</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content-text">
        Initially, the study was conceptualized to optimize the bioprocess parameters for a single, specific strain. However, to provide a more robust and comprehensive engineering solution, the scope was expanded. The current model was constructed to compare different strains possessing distinct kinetic parameters. Experimental Monod kinetic data—namely, the Maximum Specific Growth Rate ($\\mu_{max}$) and the Half-Saturation Constant ($K_s$)—can be inputted into the system to evaluate how varying biological potentials translate into industrial-scale lactic acid yield.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<h3 class="section-title">Simulation Methodology</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content-text">
        A Continuous Stirred-Tank Reactor (CSTR) model was utilized, strictly constrained to operate at a <b>90% working-to-vessel volume ratio</b>. The backend algorithm was designed using a K-Nearest Neighbors (KNN) approach to evaluate the inputted kinetic parameters against a comprehensive database of pre-simulated industrial configurations. Upon evaluation, a standardized efficiency score (ranging from 1.0 to 10.0) is assigned, and the precise, calibrated <b>SuperPro Designer</b> process output is retrieved for the user.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        with btn_col2:
            st.button("Launch Interactive Simulator", on_click=enter_simulator, type="primary", use_container_width=True)
            
        st.markdown('<p class="qr-thanks">Special thanks are extended to the jury members and attendees for scanning the QR code and exploring the details of this graduation project.</p>', unsafe_allow_html=True)

# ==========================================
# 2. SIMULATOR PAGE (Clean Industrial Dashboard)
# ==========================================
elif st.session_state.page == 'simulator':
    
    st.sidebar.title("Kinetic Input Parameters")
    st.sidebar.markdown("Define the experimental Monod data for the target strain.")
    
    exp_mu = st.sidebar.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 1.00, 0.45, 0.01)
    exp_Ks = st.sidebar.slider("Half-Saturation (Ks) [g/L]", 0.01, 2.00, 0.50, 0.01)
    
    st.sidebar.markdown("---")
    st.sidebar.warning("⚙️ **System Constraint:**\nReactor capacity is mathematically fixed at 90% Working Volume. Output varies solely based on strain kinetics.")

    st.markdown('<h2 style="color: #1E3A8A; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px;">Process Simulator & Efficiency Assessor</h2>', unsafe_allow_html=True)
    
    @st.cache_data
    def load_data():
        try:
            return pd.read_excel('120_SuperPro_Input_List.xlsx')
        except FileNotFoundError:
            return None

    df = load_data()
    
    if df is None:
        st.error("System Error: '120_SuperPro_Input_List.xlsx' database file is missing from the directory.")
        st.stop()

    # --- KNN MATCHING ALGORITHM ---
    norm_mu = (df['mu_max_UserSpecified'] - exp_mu) / (1.00 - 0.10)
    norm_Ks = (df['Ks_K1'] - exp_Ks) / (2.00 - 0.01)
    
    df['Distance'] = np.sqrt(norm_mu**2 + norm_Ks**2)
    matched_idx = df['Distance'].idxmin()
    matched_row = df.loc[matched_idx]
    
    image_index = int(matched_row['Screenshot_Index'])
    
    # --- CALIBRATED OUTPUT CALCULATIONS ---
    worst_output_kgh = 2.17022
    best_output_kgh = 2.33290
    
    scale_factor = (image_index - 1) / 119.0
    efficiency_score = 1.0 + (scale_factor * 9.0)
    expected_output = worst_output_kgh + (scale_factor * (best_output_kgh - worst_output_kgh))

    # --- DASHBOARD LAYOUT ---
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.markdown("#### Performance Metrics")
        
        if efficiency_score >= 8.0:
            st.success(f"**Efficiency Score:**\n### {efficiency_score:.1f} / 10.0")
        elif efficiency_score >= 4.0:
            st.warning(f"**Efficiency Score:**\n### {efficiency_score:.1f} / 10.0")
        else:
            st.error(f"**Efficiency Score:**\n### {efficiency_score:.1f} / 10.0")
            
        st.metric(label="Lactic Acid Production Rate", value=f"{expected_output:.5f} kg/h")
        
        st.markdown("---")
        st.markdown("#### Matched Database Profile")
        st.info(f"**Target μ_max:** {matched_row['mu_max_UserSpecified']:.3f} 1/h\n\n**Target Ks:** {matched_row['Ks_K1']:.3f} g/L")
        
    with col2:
        st.markdown("#### SuperPro Designer Process Flowsheet")
        image_file = f"SuperPro_{image_index}.png"
        
        if os.path.exists(image_file):
            img = Image.open(image_file)
            st.image(img, caption=f"System Configuration Output: {image_file}", use_container_width=True)
        else:
            st.error(f"Awaiting validation data: Image '{image_file}' is currently missing from the directory.")
