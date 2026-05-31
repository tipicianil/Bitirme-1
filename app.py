import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

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
    
    /* Logo için Güvenli Beyaz Rozet Stili */
    [data-testid="stImage"] img {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
        color: #10B981;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    .cover-title {
        font-size: 2.1rem; 
        font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
        color: #10B981; 
        margin-top: 40px; 
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
# 1. LANDING PAGE (Formal Cover & Abstract)
# ==========================================
if st.session_state.page == 'landing':
    
    # 1. Logo Bölümü (Temizlendi)
    col_img1, col_img2, col_img3 = st.columns([4.5, 1.2, 4.5])
    with col_img2:
        if os.path.exists("marmara.png"):
            st.image("marmara.png", use_container_width=True)
            
    # 2. Resmi Kapak Sayfası Metinleri
    st.markdown("""
    <div class="cover-container">
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
            Mehmet Anıl
