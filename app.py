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

# Custom CSS for Full Page Frame & Single Content Block (Dark Mode Compatible)
st.markdown("""
    <style>
    .stApp {
        border: 12px solid;
        border-image: linear-gradient(45deg, #1E3A8A, #10B981) 1;
    }
    .main-title {
        font-size: 2.8rem; 
        font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-top: 20px;
        margin-bottom: 40px; 
        line-height: 1.2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .content-block {
        padding: 10px 40px;
        font-size: 1.15rem; 
        line-height: 1.8; 
        color: var(--text-color); 
        text-align: justify; 
        margin: 0 auto;
        max-width: 1000px;
    }
    .qr-thanks {
        text-align: center; 
        font-size: 1.15rem;
        color: #10B981; 
        margin-top: 30px; 
        margin-bottom: 30px;
        font-weight: 700; 
        font-style: italic;
    }
    .knn-box {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3B82F6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def enter_simulator():
    st.session_state.page = 'simulator'

# ==========================================
# 1. LANDING PAGE
# ==========================================
if st.session_state.page == 'landing':
    
    st.markdown('<div class="main-title">Design and kinetic modeling of the <i>Lactiplantibacillus plantarum</i>: compare different strains with different kinetic parameters</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-block">
        This interactive digital twin was developed within the scope of a senior graduation project at the Bioengineering Department of Marmara University. The model was designed and engineered by Mehmet Anıl Tipici to bridge the gap between theoretical biological kinetics and industrial-scale chemical plant operations. 
        <br><br>
        Initially, the study was conceptualized to optimize the bioprocess parameters for a single, specific strain of <i>Lactiplantibacillus plantarum</i>. However, to provide a more robust and comprehensive engineering solution, the scope was significantly expanded. The current model was constructed to compare different strains possessing distinct kinetic parameters, allowing the evaluation of how varying biological potentials translate into industrial-scale lactic acid yield.
        <br><br>
        To achieve this objective, a Continuous Stirred-Tank Reactor (CSTR) model was utilized, strictly constrained to operate at a <b>90% working-to-vessel volume ratio</b>. Experimental Monod kinetic data—namely, the Maximum Specific Growth Rate (μ_max) and the Half-Saturation Constant (K_s)—can be inputted into the system. The backend algorithm employs a K-Nearest Neighbors (KNN) approach to evaluate these inputs against a comprehensive database of pre-simulated industrial configurations. Ultimately, the system aims to assign a standardized efficiency score and retrieve the precise, calibrated <b>SuperPro Designer</b> process output for the user.
        <br><br>
        <div class="qr-thanks">Special thanks are extended to the jury members and attendees for scanning the QR code and exploring the details of this graduation project.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.button("Launch Interactive Simulator", on_click=enter_simulator, type="primary", use_container_width=True)

# ==========================================
# 2. SIMULATOR PAGE
# ==========================================
elif st.session_state.page == 'simulator':
    
    st.sidebar.title("Kinetic Input Parameters")
    st.sidebar.markdown("Define the experimental Monod data for the target strain.")
    
    exp_mu = st.sidebar.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 0.70, 0.45, 0.01)
    exp_Ks = st.sidebar.slider("Half-Saturation (Ks) [g/L]", 0.01, 1.50, 0.50, 0.01)
    
    st.sidebar.markdown("---")
    st.sidebar.warning("⚙️ **System Constraint:**\nReactor capacity is mathematically fixed at 90% Working Volume. Output varies solely based on strain kinetics.")
    st.sidebar.info("💡 **Algorithm Note:**\nThe KNN algorithm rounds your inputs to the closest pre-simulated industrial scenario in the database.")

    st.markdown('<h2 style="color: #1E3A8A; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 0;">Process Simulator & Efficiency Assessor</h2>', unsafe_allow_html=True)
    
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

    # --- KNN MATCHING ALGORITHM ---
    norm_mu = (df['mu_max_UserSpecified'] - exp_mu) / (0.70 - 0.10)
    norm_Ks = (df['Ks_K1'] - exp_Ks) / (1.50 - 0.01)
    
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
    col1, col2 = st.columns([1.2, 2.8]) 
    
    with col1:
        st.markdown("#### KNN Algorithm Matching")
        st.caption("Your custom input is dynamically mapped to the nearest neighbor scenario in the database.")
        
        # Kullanıcının girdiği değer ile algoritmanın bulduğu değeri kıyaslayan görsel kutu
        st.markdown(f"""
        <div class="knn-box">
            <b>Target μ_max:</b> {exp_mu:.2f} ➔ <i>Matched: {matched_row['mu_max_UserSpecified']:.3f}</i><br>
            <b>Target K_s:</b> {exp_Ks:.2f} ➔ <i>Matched: {matched_row['Ks_K1']:.3f}</i>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Projected Performance")
        
        if efficiency_score >= 8.0:
            st.success(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
        elif efficiency_score >= 4.0:
            st.warning(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
        else:
            st.error(f"**Efficiency Score:**\n### ~ {efficiency_score:.1f} / 10.0")
            
        # Çıktının başına 'Yaklaşık (~)' işareti eklendi
        st.metric(label="Estimated Lactic Acid Production", value=f"~ {expected_output:.5f} kg/h")
        
    with col2:
        st.markdown("#### Closest Matched Process Flowsheet (SuperPro Designer)")
        image_file = f"SuperPro_{image_index}.png"
        
        if os.path.exists(image_file):
            img = Image.open(image_file)
            st.image(img, caption=f"Approximated System Configuration Output: {image_file}", width=450)
        else:
            st.error(f"Awaiting validation data: Image '{image_file}' is currently missing from the directory.")
