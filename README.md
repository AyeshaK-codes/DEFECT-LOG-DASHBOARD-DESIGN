# DEFECT-LOG-DASHBOARD-DESIGN
A premium, dark-themed SAP Testing &amp; Quality Gate Portal built with Streamlit and Altair. Features role-based access, multi-phase workspace environments (SIT-IT1, SIT-IT2, UAT), real-time interactive tracking metrics, and data filtering capabilities.

# 📊 Colgate SAP Quality Gate & Defect Tracking Portal

An executive-level, production-ready interactive dashboard designed to streamline, visualize, and monitor SAP integration test runs and User Acceptance Testing (UAT) cycles. 

---

## 📑 About the Project

This application serves as a centralized operational hub for tracking integration defects across multiple core SAP modules (including **SD, MM, FI, PP, and QM**). It provides clear visibility for executive visitors while granting system administrators tools to manage data environments dynamically.

### 🌟 Key Features
* **Dual-Mode Access Gateway:** Secure authentication logic dividing users into read-only **Executive Visitors** and control-enabled **System Administrators**.
* **Multi-Phase Environment Switching:** Admin dashboard to swap between **SIT-IT1 Baseline Logs**, **SIT-IT2 Active Testing Environments**, and live **UAT Defect Registries**.
* **Advanced Visual Analytics:** High-fidelity tracking charts powered by Altair, detailing total defect volume, resolution clean rates, status breakdowns, and priority allocations.
* **Contextual UI Optimization:** Premium dark theme layout with smart, context-aware scrolling (automatically locked on the landing page for a perfect fit, and enabled during metric reviews).

### 🛠️ Built With
* [Streamlit](https://streamlit.io/) - For the rapid development of the interactive web interface.
* [Altair](https://altair-viz.github.io/) - For declarative statistical data visualizations.
* [Pandas](https://pandas.pydata.org/) - For downstream data parsing and matrix manipulation.
