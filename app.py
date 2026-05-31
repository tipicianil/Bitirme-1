import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

# --- PAGE CONFIGURATION & ACADEMIC THEME ---
st.set_page_config(
    page_title="Lactic Acid Digital Twin | Graduation Project", 
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Giriş sayfasında yan menüyü gizleyip daha temiz bir görünüm sağlar
)

# Custom CSS for academic aesthetic
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; font-weight: 700; color: #1E3A8A; text-align: center; margin-bottom: 0px;}
    .sub-header {font-size: 1.2rem; font-weight: 400; color: #4B5563; text-align: center; margin-bottom: 30px;}
    .section-title {color: #1E3A8A; border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; margin-top: 20px;}
    .qr-thanks {text-align: center; font-style: italic; color: #10B981; margin-top: 40px; font-weight: 500;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def enter_simulator():
    st.session_state.page = 'simulator'

# ==========================================
# 1. LANDING PAGE (Academic Presentation)
# ==========================================
if st.session_state.page == 'landing':
    
    st.markdown('<p class="main-header">Predictive Digital Twin for Lactic Acid Fermentation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Marmara University • Bioengineering Department • Senior Graduation Project</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        st.info("**Developer:** Mehmet Anıl Tipici | 4th-Year Bioengineering Student")
        
        st.markdown('<h3 class="section-title">Project Evolution & Scientific Background</h3>', unsafe_allow_html=True)
        st.markdown("""
        Initially, this design project was conceptualized to optimize the bioprocess parameters for a single, specific strain of *Lactiplantibacillus plantarum*. However, to provide a more robust engineering solution, the project evolved into a dynamic, predictive digital twin.
        
        Instead of a static simulation, this interface allows users to input specific experimental Monod kinetic data—namely, the Maximum Specific Growth Rate ($\mu_{max}$) and the Half-Saturation Constant ($K_s$)—for various theoretical or newly isolated strains. 
        
        By coupling these biological parameters with a mathematically constrained Continuous Stirred-Tank Reactor (CSTR) model (operating strictly at a **90% working-to-vessel volume ratio**), the algorithm predicts how the unique kinetics of any given strain will translate into industrial-scale lactic acid yield and overall process efficiency.
        """)

        st.markdown('<h3 class="section-title">Simulation Methodology</h3>', unsafe_allow_html=True)
        st.markdown("""
        The backend utilizes a K-Nearest Neighbors (KNN) algorithm to evaluate the inputted kinetic parameters against a comprehensive MATLAB-generated database of pre-simulated industrial configurations. The system then assigns a standardized efficiency score (ranging from 1.0 to 10.0) and retrieves the exact, calibrated **SuperPro Designer** process output.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        with btn_col2:
            st.button("Launch Interactive Simulator", on_click=enter_simulator, type="primary", use_container_width=True)
            
        st.markdown('<p class="qr-thanks">Thank you for scanning the QR code and taking the time to explore my graduation project!</p>', unsafe_allow_html=True)

# ==========================================
# 2. SIMULATOR PAGE (Clean Industrial Dashboard)
# ==========================================
elif st.session_state.page == 'simulator':
    
    # Reveal sidebar inputs for the simulator
    st.sidebar.title("Kinetic Input Parameters")
    st.sidebar.markdown("Define the experimental Monod data for the target strain.")
    
    # Sliders matching the MATLAB generation ranges
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
