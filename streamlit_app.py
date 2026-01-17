import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ------------------------------
# Configuration & Data Setup
# ------------------------------
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "applications.csv")
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(
    page_title="Internship & Job Application Tracker",
    layout="wide"
)

st.title("📌 Internship & Job Application Tracker")
st.write("Manage, track, and analyze your internship and job applications efficiently.")

# ==================================================
# ➕ Add Application | 🔄 Update Status (Side by Side)
# ==================================================
left_col, right_col = st.columns(2)

# ---------- ADD APPLICATION ----------
with left_col:
    st.subheader("➕ Add New Application")

    with st.form("add_application_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Role Applied For")
        applied_date = st.date_input("Application Date")

        status = st.selectbox(
            "Application Status",
            ["Applied", "Interview", "Selected", "Rejected", "On Hold"]
        )

        source = st.text_input("Application Source (LinkedIn, Referral, etc.)")
        follow_up_date = st.date_input("Follow-up Date")

        submit = st.form_submit_button("Add Application")

    if submit:
        if company.strip() == "" or role.strip() == "":
            st.error("Company name and Role are required.")
        else:
            new_record = {
                "company": company.strip(),
                "role": role.strip(),
                "applied_date": applied_date.strftime("%Y-%m-%d"),
                "status": status,
                "source": source.strip(),
                "follow_up_date": follow_up_date.strftime("%Y-%m-%d")
            }

            df_new = pd.DataFrame([new_record])
            file_exists = os.path.exists(DATA_FILE)
            df_new.to_csv(DATA_FILE, mode="a", header=not file_exists, index=False)

            st.success("Application added successfully!")

# ---------- UPDATE STATUS ----------
with right_col:
    st.subheader("🔄 Update Application Status")

    if os.path.exists(DATA_FILE):
        df_update = pd.read_csv(DATA_FILE)
    else:
        df_update = pd.DataFrame()

    if df_update.empty:
        st.info("No applications available to update.")
    else:
        # Use company name for display, but keep index mapping
        company_list = df_update["company"].tolist()

        selected_company = st.selectbox(
            "Select Company",
            company_list
        )

        selected_index = df_update[df_update["company"] == selected_company].index[0]

        current_status = df_update.at[selected_index, "status"]

        st.write(f"**Current Status:** {current_status}")

        new_status = st.selectbox(
            "Update Status To",
            ["Applied", "Interview", "Selected", "Rejected", "On Hold"],
            index=["Applied", "Interview", "Selected", "Rejected", "On Hold"].index(current_status)
        )

        if st.button("Update Status"):
            df_update.at[selected_index, "status"] = new_status
            df_update.drop(columns=["selector"], inplace=True)

            try:
                df_update.to_csv(DATA_FILE, index=False)
                st.success("Status updated successfully!")
            except PermissionError:
                st.error("Please close the CSV file and try again.")

# ==================================
# 📋 View & Filter Applications
# ==================================
st.subheader("📋 View & Filter Applications")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame()

if df.empty:
    st.info("No applications available yet.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + sorted(df["status"].unique().tolist())
        )

    with col2:
        company_filter = st.selectbox(
            "Filter by Company",
            ["All"] + sorted(df["company"].unique().tolist())
        )

    with col3:
        role_filter = st.selectbox(
            "Filter by Role",
            ["All"] + sorted(df["role"].unique().tolist())
        )

    filtered_df = df.copy()

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    if company_filter != "All":
        filtered_df = filtered_df[filtered_df["company"] == company_filter]

    if role_filter != "All":
        filtered_df = filtered_df[filtered_df["role"] == role_filter]

    st.dataframe(filtered_df, use_container_width=True)

# ==================================
# 📊 Application Summary Dashboard
# ==================================
st.subheader("📊 Application Summary")

if df.empty:
    st.info("No data available for summary.")
else:
    df["follow_up_date"] = pd.to_datetime(df["follow_up_date"], errors="coerce")

    total_apps = len(df)
    applied = (df["status"] == "Applied").sum()
    interview = (df["status"] == "Interview").sum()
    selected = (df["status"] == "Selected").sum()
    rejected = (df["status"] == "Rejected").sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", total_apps)
    c2.metric("Applied", applied)
    c3.metric("Interview", interview)
    c4.metric("Selected", selected)
    c5.metric("Rejected", rejected)

    st.markdown("### 📌 Status Distribution")
    st.bar_chart(df["status"].value_counts())

    st.markdown("### ⏰ Pending Follow-ups")
    today = pd.to_datetime("today").normalize()
    pending_df = df[df["follow_up_date"] >= today]

    if pending_df.empty:
        st.success("No pending follow-ups 🎉")
    else:
        st.dataframe(
            pending_df[["company", "role", "status", "follow_up_date"]],
            use_container_width=True
        )
