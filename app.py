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

# --- SESSION STATE ---
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

def set_step(step):
    st.session_state.active_step = step

# ==========================================
# 1. LANDING PAGE
# ==========================================
if st.session_state.page == 'landing':
    # (Buradaki kapak kısmı aynı duruyor)
    st.button("Launch Interactive Simulator", on_click=enter_simulator, type="primary", use_container_width=True)

# ==========================================
# 2. SIMULATOR PAGE (Renamed Steps)
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

    exp_mu = st.session_state.sim_mu
    exp_Ks = st.session_state.sim_Ks

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
        st.slider("Max Growth Rate (μ_max) [1/h]", 0.10, 0.70, key="sim_mu", step=0.01)
        st.slider("Half-Saturation (Ks) [g/L]", 0.01, 1.50, key="sim_Ks", step=0.01)
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
            st.image(image_file, use_container_width=True) 
        else:
            st.error("Image file missing.")
        st.markdown('</div>', unsafe_allow_html=True)
