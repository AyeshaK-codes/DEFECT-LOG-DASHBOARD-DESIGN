import streamlit as st
import os

# Page Configuration
st.set_page_config(page_title="Colgate Portal", layout="wide")

# Advanced Cyber-Purple Global Theme & Header Clean-up CSS Injection
cyber_theme_css = """
<style>
    /* Hide Deploy button, Streamlit hamburger menu, and Record Screen options */
    header, [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Main Background Layout */
    .stApp {
        background-color: #0E0B1E !important;
        color: #F3F0FF !important;
    }
    
    /* Login Form Container Box */
    [data-testid="stForm"] {
        background-color: #151130 !important;
        border: 2px solid #7B2CBF !important;
        border-radius: 16px !important;
        padding: 40px !important;
        box-shadow: 0px 0px 25px rgba(123, 44, 191, 0.4) !important;
    }
    
    /* Input Fields Customization */
    div[data-testid="stTextInput"] input {
        background-color: #1C173E !important;
        color: #FFFFFF !important;
        border: 1px solid #4A3B75 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #9D4EDD !important;
        box-shadow: 0px 0px 10px #9D4EDD !important;
    }
    
    /* Login Submit Button Customization */
    button[kind="formSubmit"] {
        background: linear-gradient(135deg, #7B2CBF 0%, #9D4EDD 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 0px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 0px 4px 15px rgba(157, 78, 221, 0.4) !important;
        cursor: pointer !important;
    }
    button[kind="formSubmit"]:hover {
        background: linear-gradient(135deg, #9D4EDD 0%, #C77DFF 100%) !important;
        box-shadow: 0px 0px 20px #C77DFF !important;
    }
    
    /* Headers & Text Settings */
    h1, h2, h3, h4, label {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: #0A0718 !important;
        border-right: 1px solid #241A41 !important;
    }
</style>
"""
st.markdown(cyber_theme_css, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def show_login_page():
    st.markdown("<h1 style='text-align: center; margin-top: 80px; font-weight: 700; color: #FFFFFF;'>SIT System Gateway</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9D4EDD; margin-bottom: 40px;'>Colgate SAP Portal Verification</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter authorization key")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit_button = st.form_submit_button("Verify Credentials", use_container_width=True)
            
            if submit_button:
                if username == "admin" and password == "colgate123":
                    st.session_state["logged_in"] = True
                    st.success("Access Granted.")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials token.")

if st.session_state["logged_in"]:
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
        
    st.sidebar.markdown("---")
    
    dashboard_filename = "mnc_dashboard.py"
    if os.path.exists(dashboard_filename):
        try:
            with open(dashboard_filename, "r", encoding="utf-8") as file:
                exec(file.read(), globals())
        except Exception as e:
            st.error(f"Execution Error: {e}")
    else:
        st.error(f"System core target missing: '{dashboard_filename}'")
else:
    show_login_page()