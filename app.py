import streamlit as st
from frontend.login import render_login_page
from frontend.dashboard import render_dashboard

# --- PAGE CONFIG ---
st.set_page_config(page_title="Secure Audit Portal", layout="wide")

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- ROUTING ---
if st.session_state["logged_in"]:
    render_dashboard()
else:
    render_login_page()