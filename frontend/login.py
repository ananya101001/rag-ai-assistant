# frontend/login.py
import streamlit as st
from frontend.styles import load_css

def render_login_page():
    load_css()
    
    # Columns to center the card
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Header Text (Outside the form)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="font-size: 28px; margin:0; color: #0f172a;">🔐 Secure Audit</h1>
                <p style="color: #64748b; font-size: 14px; margin-top: 5px;">Enterprise Compliance Portal</p>
            </div>
        """, unsafe_allow_html=True)

        # The Form (Now automatically styled as a card by CSS)
        with st.form("login_form"):
            st.markdown("##### Credential Check")
            username = st.text_input("Username", placeholder="admin@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("##### Clearance")
            role = st.selectbox("Role", ["Junior Auditor", "Manager", "Admin"], label_visibility="collapsed")
            
            st.markdown("---")
            
            if st.form_submit_button("Access Portal", type="primary"):
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = role
                st.session_state['username'] = username if username else "Auditor"
                st.rerun()