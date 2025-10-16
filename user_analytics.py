import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import get_user_data_by_type, calculate_metrics
from utils.visualizations import create_user_comparison_chart, create_session_duration_chart

def show_user_analytics():
    st.header("👥 User Analytics")

    # Check if data is available in session state
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Please upload data from the main dashboard first.")
        return

    df = st.session_state.df

    # User selection
    users_to_analyze = st.multiselect(
        "Select users for detailed analysis:",
        ["User X", "User Y", "User Z"],
        default=["User X", "User Y", "User Z"]
    )

    if not users_to_analyze:
        st.warning("Please select at least one user for analysis.")
        return

    # Demographics section
    st.subheader("📊 Demographics Analysis")

    col1, col2 = st.columns(2)

    with col1:
        age_chart = create_user_comparison_chart(df, 'age', users_to_analyze)
        st.plotly_chart(age_chart, use_container_width=True)

    with col2:
        location_chart = create_user_comparison_chart(df, 'location', users_to_analyze)
        st.plotly_chart(location_chart, use_container_width=True)

    # Engagement analysis
    st.subheader("📈 Engagement Analysis")

    col1, col2 = st.columns(2)

    with col1:
        engagement_chart = create_user_comparison_chart(df, 'engagement', users_to_analyze)
        st.plotly_chart(engagement_chart, use_container_width=True)

    with col2:
        session_chart = create_session_duration_chart(df, users_to_analyze)
        st.plotly_chart(session_chart, use_container_width=True)

    # Interest analysis
    st.subheader("🎯 Interest Analysis")
    interest_chart = create_user_comparison_chart(df, 'interest', users_to_analyze)
    st.plotly_chart(interest_chart, use_container_width=True)

    # User summary table
    st.subheader("📋 User Summary")

    summary_data = []
    for user in users_to_analyze:
        suffix = user.split()[-1].lower()

        # Get user data
        username_col = f"username_{suffix}"
        age_col = f"age_{suffix}"
        location_col = f"location_{suffix}"
        interest_col = f"interest_{suffix}"
        followers_col = f"followers_{suffix}"
        following_col = f"following_{suffix}"

        user_summary = {"User": user}

        if username_col in df.columns:
            user_summary["Username"] = df[username_col].iloc[0] if not df[username_col].empty else "N/A"

        if age_col in df.columns:
            user_summary["Avg Age"] = f"{df[age_col].mean():.1f}" if not df[age_col].isna().all() else "N/A"

        if location_col in df.columns:
            user_summary["Top Location"] = df[location_col].mode().iloc[0] if not df[location_col].empty else "N/A"

        if interest_col in df.columns:
            user_summary["Top Interest"] = df[interest_col].mode().iloc[0] if not df[interest_col].empty else "N/A"

        if followers_col in df.columns:
            user_summary["Total Followers"] = f"{df[followers_col].sum():,}"

        if following_col in df.columns:
            user_summary["Total Following"] = f"{df[following_col].sum():,}"

        summary_data.append(user_summary)

    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)

if __name__ == "__main__":
    show_user_analytics()
