# frontend/dashboard.py
import streamlit as st
from frontend.styles import load_css
from backend.database import process_file_upload, query_documents, reset_database
from backend.llm import generate_rag_response
from backend.audit_log import get_audit_logs
from frontend.graph_viz import render_rbac_graph

def render_dashboard():
    load_css()

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🛡️ Audit Workspace")
        st.caption(f"Logged in as **{st.session_state['user_role']}**")
        st.markdown("---")
        
        with st.expander("📂 **Upload Documents**", expanded=True):
            uploaded_file = st.file_uploader("Select PDF/TXT", type=["pdf", "txt"], label_visibility="collapsed")
            security_level = st.selectbox("Security Level", ["low", "medium", "high"], 
                                          format_func=lambda x: {"low": "🟢 Public", "medium": "🟡 Internal", "high": "🔴 Secret"}[x])
            
            if uploaded_file:
                if st.button("Encrypt & Upload"):
                    with st.spinner("Processing..."):
                        if process_file_upload(uploaded_file, security_level):
                            st.success("Uploaded!")

        with st.expander("⚙️ **System**"):
            if st.button("Clear Database"):
                reset_database()
                st.cache_resource.clear()
                st.toast("Database Cleared")
            
            if st.button("Log Out"):
                st.session_state['logged_in'] = False
                st.session_state['messages'] = []
                st.rerun()

    # --- MAIN CONTENT ---
    st.title("🛡️ Secure Audit AI")
    
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🕸️ RBAC Graph", "📜 Audit Logs"])

    # --- TAB 1: CHAT ---
    with tab1:
        # 1. DISPLAY HISTORY (Always moves messages to top)
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Ready. Access limited by your role."}]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 2. HANDLE INPUT
        if prompt := st.chat_input("Type your audit query here..."):
            
            # A. Add User Message to State
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # B. Generate Response (Logic only, no UI printing yet)
            results, status = query_documents(prompt, st.session_state['user_role'], st.session_state['username'])
            full_response = ""
            
            if status == "success":
                stream_or_error, sources = generate_rag_response(prompt, results)
                # Handle stream vs string
                if isinstance(stream_or_error, str):
                    full_response = stream_or_error
                else:
                    # Collect the stream into a single string
                    for chunk in stream_or_error:
                        if 'message' in chunk and 'content' in chunk['message']:
                            full_response += chunk['message']['content']
                    
                    if sources:
                        source_str = "  \n".join([f"- *{s}*" for s in sources])
                        full_response += "\n\n**Sources:**\n" + source_str
            
            elif status == "denied":
                full_response = f"⛔ **ACCESS BLOCKED:** Documents exist, but they are classified above your level (**{st.session_state['user_role']}**)."
            
            else:
                full_response = "I searched the documents but found no relevant information."

            # C. Add Assistant Message to State
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # D. THE FIX: Force Reload
            # This restarts the script, so the new messages are printed in Step 1 (above the input bar)
            st.rerun()

    # --- TAB 2: GRAPH ---
    with tab2:
        st.markdown("### Access Control Architecture")
        render_rbac_graph()

    # --- TAB 3: LOGS ---
    with tab3:
        st.markdown("### System Activity Log")
        logs = get_audit_logs()
        if not logs.empty:
            def color_status(val):
                color = '#ffcdd2' if 'DENIED' in val else '#c8e6c9'
                return f'background-color: {color}'
            st.dataframe(logs.style.applymap(color_status, subset=['Status']), use_container_width=True)
        else:
            st.info("No activity recorded yet.")