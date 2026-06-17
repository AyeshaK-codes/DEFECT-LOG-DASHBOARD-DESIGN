import streamlit as st
import pandas as pd
import altair as alt
import os

# 1. INITIALIZE APPLICATION ENVIRONMENT WITH UPDATED COLGATE IMAGE
st.set_page_config(
    page_title="Colgate SAP Testing Portal", 
    layout="wide"
)

# 2. APPLICATION CORE STYLES & LAYOUT ENFORCEMENT
ui_theme_styles = """
<style>
    /* NATURAL SCROLLING ACTIVATED */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #070412 !important;
        background-image: radial-gradient(circle at 50% 45%, #2D124D 0%, #070412 70%) !important;
        color: #FFFFFF !important;
        overflow-y: auto !important;
    }
    
    .stApp { background: transparent !important; }
    [data-testid="stHeader"], footer { display: none !important; visibility: hidden !important; }
    
    [data-testid="stMainBlockContainer"] {
        max-height: none !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        overflow-y: auto !important; 
    }

    /* REMOVED CONTAINER BOX: CLEAN PLAIN LAYOUT */
    .login-plain-wrapper {
        max-width: 500px !important; 
        margin: 5% auto !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        text-align: center;
    }

    .custom-input-label {
        display: block !important;
        color: #BDB9D0 !important;
        font-size: 14px !important; 
        font-weight: 500 !important;
        margin-bottom: 6px !important;
        text-align: left;
    }

    /* BIG BUTTON CARD IMPLEMENTATION */
    .big-role-card {
        padding: 24px !important;
        border-radius: 16px !important;
        margin-bottom: 8px !important;
        text-align: left !important;
    }
    
    .big-role-card.active {
        background: linear-gradient(135deg, #E11B22 0%, #9B0F14 100%) !important;
        border: 2px solid #FF4D52 !important;
        box-shadow: 0 6px 25px rgba(225, 27, 34, 0.4) !important;
    }
    
    .big-role-card.inactive {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 2px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* ADMIN HUB SYMMETRICAL CARDS */
    .hub-card {
        background: rgba(25, 18, 54, 0.7) !important;
        border: 1px solid rgba(157, 78, 221, 0.3) !important;
        border-radius: 20px !important; 
        padding: 24px !important;
        height: 180px !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 15px !important;
    }
    
    .hub-card h3 {
        margin: 0 0 8px 0 !important;
        font-size: 18px !important;
        color: #C77DFF !important;
    }
    
    .hub-card p {
        margin: 0 !important;
        font-size: 13px !important;
        color: #BDB9D0 !important;
        line-height: 1.4;
    }

    /* STANDARD PREMIUM BUTTON ACTION */
    div.stButton > button {
        background: linear-gradient(90deg, #7B2CBF 0%, #9D4EDD 100%) !important;
        border: none !important; border-radius: 12px !important; color: #FFFFFF !important;
        padding: 10px 20px !important; font-size: 14px !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.3) !important;
        transition: all 0.2s ease !important;
        height: 44px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(157, 78, 221, 0.5) !important;
    }
    
    .table-scroll-container {
        max-height: 60vh !important;
        overflow-y: auto !important;
        border: 1px solid rgba(157, 78, 221, 0.2);
        border-radius: 12px;
        background-color: rgba(20, 15, 38, 0.6) !important;
    }
</style>
"""
st.markdown(ui_theme_styles, unsafe_allow_html=True)

# 3. GLOBAL VARIABLES & SAP CONFIGURATION
MASTER_SAP_MODULES = ["SD", "MM", "FI", "PP", "QM"]
LOGO_PATH = "Colgate.svg.png"

def display_colgate_logo(centered=True):
    """Safely displays the locally uploaded Colgate logo layout block."""
    if os.path.exists(LOGO_PATH):
        if centered:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(LOGO_PATH, width=180, use_container_width=True)
        else:
            st.image(LOGO_PATH, width=150)
    else:
        align = "center" if centered else "left"
        st.markdown(f"<h2 style='text-align: {align}; color: #E11B22; font-weight: 800; letter-spacing: 1px;'>Colgate</h2>", unsafe_allow_html=True)

# 4. DATA ENGINE PIPELINE
@st.cache_data
def load_testing_phase_data(phase_id):
    file_mapping = {1: "SIT_IT1.csv", 2: "SIT_IT2.csv", 3: "UAT.csv"}
    filename = file_mapping.get(phase_id, "SIT_IT1.csv")
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            df = pd.read_csv(filename)
        except Exception:
            df = pd.DataFrame(columns=["Defect ID", "Module", "Description", "Priority", "Status"])
    else:
        if phase_id == 1:
            df = pd.DataFrame([
                {"Defect ID": "SIT1-SD-01", "Module": "SD", "Description": "Pricing interface drop", "Priority": "High", "Status": "Closed"},
                {"Defect ID": "SIT1-MM-01", "Module": "MM", "Description": "PO confirmation delay", "Priority": "Critical", "Status": "Open"},
                {"Defect ID": "SIT1-FI-01", "Module": "FI", "Description": "Tax posting dump", "Priority": "High", "Status": "Closed"},
                {"Defect ID": "SIT1-PP-01", "Module": "PP", "Description": "BOM batch drop error", "Priority": "Medium", "Status": "Open"},
                {"Defect ID": "SIT1-QM-01", "Module": "QM", "Description": "Inspection hang status", "Priority": "Low", "Status": "Closed"}
            ])
        elif phase_id == 2:
            df = pd.DataFrame([
                {"Defect ID": "SIT2-SD-01", "Module": "SD", "Description": "Delivery block bypass", "Priority": "Medium", "Status": "Open"},
                {"Defect ID": "SIT2-MM-01", "Module": "MM", "Description": "Inventory sync looping", "Priority": "High", "Status": "Open"}
            ])
        else:
            df = pd.DataFrame([
                {"Defect ID": "UAT-SD-01", "Module": "SD", "Description": "End-user billing invoice reject", "Priority": "High", "Status": "Open"}
            ])

    df.columns = df.columns.str.strip()
    cleaned = pd.DataFrame()
    
    id_col = [c for c in df.columns if "ID" in c.upper()]
    cleaned["Defect ID"] = df[id_col[0]].fillna("N/A").astype(str).str.strip() if id_col else [f"DFT-{i+1000}" for i in range(len(df))]
    
    mod_col = [c for c in df.columns if "MODULE" in c.upper()]
    cleaned["Module"] = df[mod_col[0]].fillna("GENERAL").astype(str).str.strip().str.upper() if mod_col else "GENERAL"

    desc_col = [c for c in df.columns if "DESCRIPTION" in c.upper() or "SCRIPT" in c.upper()]
    cleaned["Description"] = df[desc_col[0]].fillna("No description provided.") if desc_col else "No description provided."
    
    priority_col = [c for c in df.columns if "PRIORITY" in c.upper() or "TYPE" in c.upper()]
    cleaned["Priority"] = df[priority_col[0]].fillna("Medium").astype(str).str.strip().str.capitalize() if priority_col else "Medium"
    
    status_col = [c for c in df.columns if "STATUS" in c.upper()]
    cleaned["Status"] = df[status_col[0]].fillna("Open").astype(str).str.strip().str.capitalize() if status_col else "Open"
    
    return cleaned

# 5. STATE ENGINE CONFIGURATION
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None 
if "app_view_state" not in st.session_state:
    st.session_state["app_view_state"] = "HUB_SCREEN"  
if "active_dataset_scope" not in st.session_state:
    st.session_state["active_dataset_scope"] = 1  
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard Metrics"
if "prelogin_role" not in st.session_state:
    st.session_state["prelogin_role"] = "user" 

def trigger_logout():
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["app_view_state"] = "HUB_SCREEN"
    st.rerun()

# ==========================================
# PHASE A: LANDING SCREEN GATEWAY
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown('<div class="login-plain-wrapper">', unsafe_allow_html=True)
    display_colgate_logo(centered=True)
    st.markdown("<h2 style='text-align: center; margin: 15px 0 25px 0; font-size: 24px; font-weight: 600; color: #FFFFFF;'>User Login and Admin Login Portal</h2>", unsafe_allow_html=True)
    
    # BIG BUTTON 1: EXECUTIVE VISITOR DASHBOARD
    u_state = "active" if st.session_state["prelogin_role"] == "user" else "inactive"
    st.markdown(f"""
    <div class="big-role-card {u_state}">
        <h4 style="margin:0; font-size:17px; color:#FFF; font-weight:600;">📋 Executive User Mode</h4>
        <p style="margin:4px 0 0 0; font-size:12px; color:rgba(255,255,255,0.75);">Instant read-only access to primary integration tracking dashboards.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Executive Dashboard View", key="act_set_user", use_container_width=True):
        st.session_state["prelogin_role"] = "user"
        st.session_state["logged_in"] = True
        st.session_state["user_role"] = "user"
        st.session_state["active_dataset_scope"] = 1 
        st.session_state["app_view_state"] = "PORTAL_DASHBOARD"
        st.session_state["current_page"] = "Dashboard Metrics"
        st.rerun()
        
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    
    # BIG BUTTON 2: ADMINISTRATIVE CONTROLLER MODE
    a_state = "active" if st.session_state["prelogin_role"] == "admin" else "inactive"
    st.markdown(f"""
    <div class="big-role-card {a_state}">
        <h4 style="margin:0; font-size:17px; color:#FFF; font-weight:600;">🛠️ System Administrator</h4>
        <p style="margin:4px 0 0 0; font-size:12px; color:rgba(255,255,255,0.75);">Unlock phase workspace switching and UAT control panel.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Select System Admin Mode", key="act_set_admin", use_container_width=True):
        st.session_state["prelogin_role"] = "admin"
        st.rerun()

    # SHOW ADMIN FORM IF SELECTED
    if st.session_state["prelogin_role"] == "admin":
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0 20px 0;'>", unsafe_allow_html=True)
        with st.form(key="admin_credential_lock_form"):
            st.markdown('<label class="custom-input-label">Admin Username</label>', unsafe_allow_html=True)
            user = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username", key="adm_user")
            st.markdown('<label class="custom-input-label">Security Password</label>', unsafe_allow_html=True)
            pwd = st.text_input("Password", label_visibility="collapsed", type="password", placeholder="Enter password", key="adm_pwd")
            
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            if st.form_submit_button("Log In as Administrator", use_container_width=True):
                if user == "admin" and pwd == "colgate123":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "admin"
                    st.session_state["app_view_state"] = "HUB_SCREEN"
                    st.rerun()
                else:
                    st.error("Invalid Administrative Credentials.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PHASE B: PLATFORM SWITCHING HUB (ADMIN ONLY)
# ==========================================
elif st.session_state["logged_in"] and st.session_state["app_view_state"] == "HUB_SCREEN" and st.session_state["user_role"] == "admin":
    col_l, col_r = st.columns([8, 2])
    with col_l:
        display_colgate_logo(centered=False)
    with col_r:
        if st.button("🚪 Log Out", key="hub_top_logout", use_container_width=True):
            trigger_logout()

    st.markdown("<h1 style='font-size: 26px; font-weight: 700; margin-top:10px;'>SAP Environment Quality Gate (Admin Control Panel)</h1>", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    hub_col1, hub_col2, hub_col3 = st.columns(3)
    with hub_col1:
        st.markdown('<div class="hub-card"><div><h3>📊 Phase 1: SIT-IT1 Baseline</h3><p>Original core integration log sheet. View verified historical IT execution cycles.</p></div></div>', unsafe_allow_html=True)
        if st.button("Open SIT-IT1 Log", key="btn_load_scope_1", use_container_width=True):
            st.session_state["active_dataset_scope"] = 1
            st.session_state["app_view_state"] = "PORTAL_DASHBOARD"
            st.session_state["current_page"] = "Dashboard Metrics"
            st.rerun()

    with hub_col2:
        st.markdown('<div class="hub-card"><div><h3>⚠️ Phase 2: SIT-IT2 Testing</h3><p>Active regression test copy currently being utilized by validation engineers.</p></div></div>', unsafe_allow_html=True)
        if st.button("Open SIT-IT2 Log", key="btn_load_scope_2", use_container_width=True):
            st.session_state["active_dataset_scope"] = 2
            st.session_state["app_view_state"] = "PORTAL_DASHBOARD"
            st.session_state["current_page"] = "Dashboard Metrics"
            st.rerun()

    with hub_col3:
        st.markdown('<div class="hub-card"><div><h3>✅ Phase 3: UAT Sign-off</h3><p>User Acceptance Tracking zone where business users attach live operational defects.</p></div></div>', unsafe_allow_html=True)
        if st.button("Open UAT Registry", key="btn_load_scope_3", use_container_width=True):
            st.session_state["active_dataset_scope"] = 3
            st.session_state["app_view_state"] = "PORTAL_DASHBOARD"
            st.session_state["current_page"] = "Dashboard Metrics"
            st.rerun()

# ==========================================
# PHASE C: LIVE INTEGRATION METRICS PORTAL
# ==========================================
else:
    working_df = load_testing_phase_data(st.session_state["active_dataset_scope"])
    filter_options = ["Show All Sub-modules"] + MASTER_SAP_MODULES
    workspace_names = {1: "SIT-IT1 Baseline Log", 2: "SIT-IT2 Testing Environment", 3: "UAT Defect Registry"}

    # CONTEXT-AWARE NAVIGATION HEADER
    if st.session_state["user_role"] == "admin":
        top_nav_col1, top_nav_col2, top_nav_col3, top_nav_col4 = st.columns([2, 3, 3, 2])
        with top_nav_col1:
            display_colgate_logo(centered=False)
        with top_nav_col2:
            if st.button("🎛️ Back to Phase Hub", key="global_back_to_hub_action", use_container_width=True):
                st.session_state["app_view_state"] = "HUB_SCREEN"
                st.rerun()
        with top_nav_col3:
            if st.session_state["current_page"] == "Dashboard Metrics":
                if st.button("📋 View Phase Data Table", key="toggle_reg", use_container_width=True):
                    st.session_state["current_page"] = "Master Defect Registry"
                    st.rerun()
            else:
                if st.button("📊 Return to Phase Dashboard", key="toggle_dash", use_container_width=True):
                    st.session_state["current_page"] = "Dashboard Metrics"
                    st.rerun()
        with top_nav_col4:
            if st.button("🚪 Log Out", key="top_header_logout", use_container_width=True):
                trigger_logout()
    else:
        top_user_left, top_user_right = st.columns([8, 2])
        with top_user_left:
            display_colgate_logo(centered=False)
        with top_user_right:
            if st.button("🚪 Exit Dashboard", key="user_exit_action", use_container_width=True):
                trigger_logout()
        st.session_state["current_page"] = "Dashboard Metrics"

    st.markdown("<hr style='margin: 8px 0px;'>", unsafe_allow_html=True)

    selected_mod = st.selectbox(
        "🎯 Filter Phase Data by SAP Module", 
        options=filter_options, 
        key="dashboard_engine_filter_widget"
    )

    if selected_mod == "Show All Sub-modules":
        filtered_df = working_df.copy()
    else:
        filtered_df = working_df[working_df['Module'].str.upper() == selected_mod.upper()].copy()

    total_records = len(filtered_df)
    closed_count = filtered_df['Status'].astype(str).str.lower().str.contains('closed|fixed|resolved', na=False).sum()
    open_count = total_records - closed_count
    completion_rate = round((closed_count / total_records * 100), 1) if total_records > 0 else 0.0

    if st.session_state["current_page"] == "Dashboard Metrics":
        st.markdown(f"<h3 style='margin:0 0 5px 0;'>Dashboard View: {workspace_names[st.session_state['active_dataset_scope']]}</h3>", unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Logged Items", str(total_records))
        m_col2.metric("Closed/Resolved", str(closed_count))
        m_col3.metric("Remaining Open", str(open_count))
        m_col4.metric("Phase Clean Rate", f"{completion_rate}%")
        
        st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)
        
        row1_ch1, row1_ch2 = st.columns(2)
        row2_ch1, row2_ch2 = st.columns(2)
        
        with row1_ch1:
            st.markdown("#### 📈 Chart 1: Total Volume by Sub-Module")
            if not filtered_df.empty:
                counts = filtered_df['Module'].value_counts().reset_index()
                counts.columns = ['Module', 'Logs']
                chart1 = alt.Chart(counts).mark_bar(color="#7B2CBF", cornerRadiusEnd=6).encode(
                    x=alt.X('Module:N', title='Module ID', sort=MASTER_SAP_MODULES),
                    y=alt.Y('Logs:Q', title='Count'),
                    tooltip=['Module', 'Logs']
                ).properties(height=180)
                st.altair_chart(chart1, use_container_width=True)

        with row1_ch2:
            st.markdown("#### 🍩 Chart 2: Operational Status Breakdown")
            if total_records > 0:
                donut_data = pd.DataFrame({"Status": ["Closed Items", "Open Items"], "Count": [closed_count, open_count]})
                chart2 = alt.Chart(donut_data).mark_arc(innerRadius=40).encode(
                    theta=alt.Theta(field="Count", type="quantitative"),
                    color=alt.Color(field="Status", type="nominal", scale=alt.Scale(range=["#9D4EDD", "#FF5A5F"])),
                    tooltip=['Status', 'Count']
                ).properties(height=180)
                st.altair_chart(chart2, use_container_width=True)

        with row2_ch1:
            st.markdown("#### 📊 Chart 3: Distribution of Priority Levels")
            if not filtered_df.empty:
                p_counts = filtered_df['Priority'].value_counts().reset_index()
                p_counts.columns = ['Priority', 'Logs']
                chart3 = alt.Chart(p_counts).mark_bar(color="#C77DFF", cornerRadiusEnd=4).encode(
                    x=alt.X('Priority:N', title='Priority'),
                    y=alt.Y('Logs:Q', title='Count'),
                    tooltip=['Priority', 'Logs']
                ).properties(height=180)
                st.altair_chart(chart3, use_container_width=True)

        with row2_ch2:
            st.markdown("#### 🚨 Chart 4: Active Open Defects Remaining by Module")
            if not filtered_df.empty:
                open_only = filtered_df[filtered_df['Status'].astype(str).str.lower().str.contains('open', na=False)]
                if not open_only.empty:
                    open_counts = open_only['Module'].value_counts().reset_index()
                    open_counts.columns = ['Module', 'Open Logs']
                    chart4 = alt.Chart(open_counts).mark_bar(color="#FF5A5F", cornerRadiusEnd=4).encode(
                        x=alt.X('Module:N', title='SAP Module'),
                        y=alt.Y('Open Logs:Q', title='Unresolved Count'),
                        tooltip=['Module', 'Open Logs']
                    ).properties(height=180)
                    st.altair_chart(chart4, use_container_width=True)
                else:
                    st.success("Clean Run Status! 0 Active open defects left.")
    else:
        st.markdown(f"<h3 style='margin:0 0 5px 0;'>📋 {workspace_names[st.session_state['active_dataset_scope']]} Log Table</h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="table-scroll-container">', unsafe_allow_html=True)
        if not filtered_df.empty:
            st.table(filtered_df.reset_index(drop=True))
        else:
            st.warning("No records found.")
        st.markdown('</div>', unsafe_allow_html=True)