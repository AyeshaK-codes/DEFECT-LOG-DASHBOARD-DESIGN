import streamlit as st
import pandas as pd

# Advanced UI Custom Layout Injector & Header Cleaner
dashboard_styles = """
<style>
    /* Force drop top navigation menus, rerun logs, and screen recording options */
    header, [data-testid="stHeader"], #MainMenu, footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Global Content Reskinning */
    .stApp { background-color: #0E0B1E !important; color: #F3F0FF !important; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; }
    
    /* Navigation Dropdowns Style Rules */
    [data-testid="stSidebar"] { background-color: #0A0718 !important; border-right: 1px solid #241A41 !important; }
    div[data-testid="stExpander"] {
        background-color: #151130 !important;
        border: 1px solid #32255E !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }
    
    /* Glowing Neon Data Metrics Blocks Layout */
    .metric-container {
        background-color: #151130 !important;
        border: 1px solid #7B2CBF !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0px 0px 15px rgba(123, 44, 191, 0.3) !important;
    }
    .metric-title { font-size: 15px !important; color: #C77DFF !important; font-weight: 500 !important; margin-bottom: 10px; }
    .metric-value { font-size: 32px !important; font-weight: 700 !important; color: #FFFFFF !important; margin: 5px 0px; }
    .metric-subtitle { font-size: 12px !important; color: #9D4EDD !important; }
</style>
"""
st.markdown(dashboard_styles, unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dynamic Metrics Summary"

# --- 1. SIDEBAR NAVIGATION PANELS ---
st.sidebar.markdown("### Navigation Options")

with st.sidebar.expander("📊 Summary Panel", expanded=True):
    if st.button("Dynamic Metrics & Summary", use_container_width=True, key="btn_sum"):
        st.session_state["current_page"] = "Dynamic Metrics Summary"
        st.rerun()

with st.sidebar.expander("🔍 Registry Panel", expanded=True):
    if st.button("Master Defect Registry", use_container_width=True, key="btn_reg"):
        st.session_state["current_page"] = "Master Defect Registry"
        st.rerun()

with st.sidebar.expander("⚡ Pipeline Panel", expanded=True):
    if st.button("Automatic Sync Pipeline", use_container_width=True, key="btn_pipe"):
        st.session_state["current_page"] = "Automatic Sync Pipeline"
        st.rerun()

st.sidebar.markdown("---")

# --- 2. LAYOUT ROUTING FLOW CONTROLLER ---

# PAGE 1: DYNAMIC METRICS & SUMMARY VIEW
if st.session_state["current_page"] == "Dynamic Metrics Summary":
    st.markdown("<h1 style='margin-bottom:0px;'>SIT Defect Dashboard</h1>", unsafe_allow_html=True)
    
    col_title, col_date = st.columns([4, 1])
    with col_title:
        st.markdown("<p style='color: #C77DFF; font-size:18px;'>Key Metrics</p>", unsafe_allow_html=True)
    with col_date:
        st.markdown("<p style='text-align: right; color: #A0A0A0; padding-top:5px;'>05-June-2026</p>", unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown('<div class="metric-container"><div class="metric-title">Total Defects Logged</div><div class="metric-value">💥 117</div><div class="metric-subtitle">&nbsp;</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-container"><div class="metric-title">Closed / Fixed Defects</div><div class="metric-value">🛡️ 114</div><div class="metric-subtitle">97.4% fixed</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown('<div class="metric-container"><div class="metric-title">Active Open Defects</div><div class="metric-value">🚨 3</div><div class="metric-subtitle">-3 remaining</div></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown('<div class="metric-container"><div class="metric-title">Defect Resolution Rate</div><div class="metric-value">🚀 97.4%</div><div class="metric-subtitle">&nbsp;</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-top:0px;'>📊 Defects by Module and Status (Closed vs. Open)</h3>", unsafe_allow_html=True)
    
    chart_data = pd.DataFrame({
        "Fixed": [36, 24, 20, 16, 9, 5, 4],
        "Remaining": [1, 0, 2, 0, 0, 0, 0]
    }, index=["SD", "FI", "MM", "PP", "CO", "PM", "QM"])
    
    st.bar_chart(chart_data, color=["#9D4EDD", "#FF5A5F"])

# PAGE 2: REGISTRY RECORD LIST VIEW
elif st.session_state["current_page"] == "Master Defect Registry":
    st.title("📋 Master Defect Registry")
    st.caption("Active cycle logs and filters mapping systems")
    
    master_df = pd.DataFrame({
        "Defect ID": ["SD-SIT-D-0021", "MM-SIT-D-0009", "MM-SIT-D-0021"],
        "Module": ["SD", "MM", "MM"],
        "SIT Script Description": ["Customer Workflow", "Material creation apps", "HS Code, Comm Code changed"],
        "Priority": ["High", "Critical", "High"],
        "Defect Description": ["Customer WF Tables issues", "Fiori app system grid connection blocks", "All Material HS code fields altered"],
        "Status (Colgate)": ["Open", "Open", "Open"],
        "Status (EY)": ["In-Progress", "Fixed", "In-Progress"]
    })
    
    c1, c2 = st.columns(2)
    with c1: selected_mod = st.selectbox("Filter Module Context", ["All", "SD", "FI", "MM", "PP", "CO"])
    with c2: selected_stat = st.selectbox("Filter Status Block", ["All", "Fixed", "In-Progress"])
    
    f_df = master_df.copy()
    if selected_mod != "All": f_df = f_df[f_df["Module"] == selected_mod]
    if selected_stat != "All": f_df = f_df[f_df["Status (EY)"] == selected_stat]
        
    st.dataframe(f_df, use_container_width=True)

# PAGE 3: SYNC PIPELINE OPERATIONS CONTROL
elif st.session_state["current_page"] == "Automatic Sync Pipeline":
    st.title("🔄 Automatic Sync Pipeline")
    st.info("System Sync Module Status: Connected ✅")
    if st.button("Trigger Global Environment Sync", use_container_width=True):
        with st.spinner("Processing local tracking assets..."):
            import time; time.sleep(1)
            st.success("Environment state synchronized.")