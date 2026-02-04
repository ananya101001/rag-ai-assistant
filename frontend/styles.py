# frontend/styles.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* --- FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- LOGIN CARD STYLING --- */
        /* This targets the form itself to make it look like a card */
        [data-testid="stForm"] {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05); /* Soft premium shadow */
        }
        
        /* Input fields inside the form */
        .stTextInput input {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            color: #334155;
            border-radius: 8px;
        }

        /* Submit Button */
        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 10px;
        }

        /* --- DASHBOARD STYLING --- */
        section[data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Chat Bubbles */
        div[data-testid="stChatMessage"] {
            background-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)