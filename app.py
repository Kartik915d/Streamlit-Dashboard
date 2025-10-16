import streamlit as st
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('location_x_label_encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return model, encoder

model, encoder = load_model()
st.title("User Analytics & Model Explainability Dashboard")

with st.sidebar:
    selected_tab = option_menu(
        menu_title="Navigation",
        options=[
            "Problem", "Dataset", "EDA", "ML Experiments", "SHAP"
        ],
        icons=[
            "puzzle", "folder", "bar-chart-line", "bezier", "search"
        ],
        default_index=0,
        orientation="vertical"
    )
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

SAMPLE_SIZE = 1000

if selected_tab == "Problem":
    st.header("Project Problem Statement")
    st.markdown("""
    **In today’s hyper-connected digital ecosystem, users actively engage across multiple social media platforms, often switching between networks like Instagram, Facebook, and X (formerly Twitter).**
    These interactions collectively reflect an individual’s online behavior — their interests, demographics, engagement levels, and activity patterns. However, most social media analytics focus on isolated platforms, missing the broader view of cross-platform dynamics and user migration patterns.

    ---
    ### Project Goals
    - **Bridge the gap** in analytics by exploring multi-platform user behavior using a consolidated dataset.
    - The dataset includes:
        - User demographics (age, location)
        - Interests across platforms (interest_x, interest_y, interest_z)
        - Social connections (followers and following)
        - Temporal engagement metrics (date_of_login, date_of_logout, for each platform x, y, z)
        - A target variable to enable behavioral modeling (predicting influence, engagement propensity, churn likelihood)
    - **Analysis Focus:**
        - Discover patterns of user engagement across platforms
        - Detect interest overlaps
        - Identify key factors driving platform preference or switching
        - Examine how user demographics relate to engagement frequency

    ---
    ### Methods Used
    - Exploratory Data Analysis (EDA)
    - Comparative trend analysis
    - Behavioral modeling

    **Outcome:**
    Develop a unified understanding of social media user behavior across platforms. The project aims to guide businesses, marketers, and policymakers in creating integrated strategies, improving retention, and fostering data-driven decisions in the digital landscape.
    """)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    sample_df = df.sample(SAMPLE_SIZE, random_state=42) if len(df) > SAMPLE_SIZE else df

    if selected_tab == "EDA":
        N = 10
        users = sample_df['username_x'].value_counts().head(N).index.tolist() if 'username_x' in sample_df else []
        selected_users = st.sidebar.multiselect("Select users (top 10)", users)

        st.header("User Database Analytics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Users", len(sample_df['username_x'].unique()) if 'username_x' in sample_df else 0)
        col2.metric("Avg Age", round(sample_df['age_x'].mean(), 1) if 'age_x' in sample_df else 0)
        col3.metric("Followers", int(sample_df['followers_x'].sum()) if 'followers_x' in sample_df else 0)
        engagement_rate = (
            sample_df['followers_x'].sum() / sample_df['following_x'].sum() * 100
            if ('followers_x' in sample_df and 'following_x' in sample_df and sample_df['following_x'].sum() > 0) else 0
        )
        col4.metric("Engagement Rate", f"{engagement_rate:.2f}%")

        st.subheader("Location & Interest Distribution")
        left, right = st.columns(2)
        with left:
            if 'location_x' in sample_df:
                top_locs = sample_df['location_x'].value_counts().nlargest(10).index
                loc_data = sample_df[sample_df['location_x'].isin(top_locs)]
                st.bar_chart(loc_data['location_x'].value_counts())
        with right:
            if 'interest_x' in sample_df:
                top_intr = sample_df['interest_x'].value_counts().nlargest(10).index
                intr_data = sample_df[sample_df['interest_x'].isin(top_intr)]
                st.bar_chart(intr_data['interest_x'].value_counts())

        st.subheader("Age Distribution & Engagement")
        left_age, right_eng = st.columns(2)
        with left_age:
            if 'age_x' in sample_df and selected_users:
                for user in selected_users:
                    user_data = sample_df[sample_df['username_x'] == user]
                    st.bar_chart(user_data['age_x'].value_counts().sort_index())
            elif 'age_x' in sample_df:
                st.bar_chart(sample_df['age_x'].value_counts().sort_index())
        with right_eng:
            if 'followers_x' in sample_df and 'following_x' in sample_df and selected_users:
                agg = sample_df[sample_df['username_x'].isin(selected_users)].groupby('username_x')[['followers_x', 'following_x']].sum()
                st.bar_chart(agg)
            elif 'followers_x' in sample_df and 'following_x' in sample_df:
                agg = sample_df.groupby('username_x')[['followers_x', 'following_x']].sum()
                st.bar_chart(agg.head(N))

    elif selected_tab == "Dataset":
        st.subheader("Uploaded Dataset Preview")
        st.info("Below is the data from your uploaded CSV file.")
        st.dataframe(df, use_container_width=True)

    elif selected_tab == "ML Experiments":
        st.markdown("""
        ### ML Modeling & Experiment Tracking

        #### Validation comparison (per model)
        |model|pr_auc_pos|f1_pos|roc_auc|accuracy|cm_TN|cm_FP|cm_FN|cm_TP|
        |---|---|---|---|---|---|---|---|---|
        |RandomForest|0.600866|0.611765|0.579416|0.561620|13|26|
        |LogisticRegression|0.583544|0.5|0.512821|0.466667|15|21|19|20|
        |LinearSVC+Calibrated|0.524325|0.641509|0.480769|0.493333|33|35|34|
        |RBF SVC (prob=True)|0.469474|0.583333|0.418803|0.466667|7|29|11|28|

        #### Test metrics (best model from validation)
        |model (TEST)|f1_pos|pr_auc_pos|roc_auc|accuracy|cm_TN|cm_FP|cm_FN|cm_TP|
        |---|---|---|---|---|---|---|---|---|
        |RandomForest|0.522727|0.460990|0.357143|0.441025|17|23|

        #### Threshold tuning
        Threshold @ max F1 (validation)
        **0.44**  
        Threshold @ min cost (FP=1, FN=5)
        **0.32**  
        Chosen operating threshold  
        **0.44**

        #### Validation leaderboard (picked by PR-AUC)
        |model|pr_auc_pos|roc_auc|f1_pos@0.5|accuracy@0.5|cm_TN|cm_FP|cm_FN|cm_TP|
        |---|---|---|---|---|---|---|---|---|
        |stockout_randomforest.pkl|0.600866|0.579416|0.611765|0.561620|13|26|
        |stockout_logisticregression.pkl|0.583544|0.512821|0.5|0.466667|15|21|19|20|
        |stockout_linearsvcpluscalibrated.pkl|0.524325|0.480769|0.641509|0.493333|33|35|34|
        Chosen winner: **stockout_randomforest.pkl** Tuned threshold on validation: **0.44**

        #### Test metrics (winner @ tuned threshold)
        |model|threshold|PR-AUC_test|ROC-AUC_test|F1_pos_test|Accuracy_test|TN|FP|FN|TP|
        |---|---|---|---|---|---|---|---|---|---|
        |stockout_randomforest.pkl|0.44|0.46099|0.357143|0.594059|0.453333|43|11|0|30|

        ### Plots & explanations

        **Precision–Recall (Validation)**
        - X (Recall): of all real stockouts, how many did we catch?
        - Y (Precision): of all predicted stockouts, how many were correct?
        - Takeaway: moderate ability to identify stockouts (AP ≈ 0.584).

        **Precision–Recall (Test)**
        - Same interpretation as validation.
        - Takeaway: reasonable but weaker (AP ≈ 0.461).

        **Validation Confusion Matrix**
        - Correctly predicted ∼33 stockouts; missed ∼6 (FN).
        - ∼25 In-Stock cases flagged as stockouts (FP) → more false alarms.
        - Model leans toward predicting OutOfStock to catch more true stockouts.

        **Test Confusion Matrix**
        - Catches most stockouts (e.g., ∼32 TP) but ∼28 FP on In-Stock items.
        - Similar to validation: good recall for stockouts, weaker on In-Stock.
        - Threshold tuning balances early alerts vs false alarms.
        """)

    elif selected_tab == "SHAP":
        st.header("Model Prediction & SHAP")
        st.markdown("""
        **Explainable AI (XAI) — SHAP**
        
        SHAP (SHapley Additive exPlanations) helps us interpret the predictions of our model for social media user analytics.

        **Model Used for SHAP:** RandomForestClassifier

        - We use TreeExplainer in interventional mode for Random Forest models.
        - SHAP summary plots visualize which features most drive engagement or behavioral predictions.
        - Feature dependence plots (optional) show how specific values impact the target.

        **How to read the plot:**  
        Features with the largest average SHAP values contribute most to the model decisions (e.g., followers, age, location).  
        If all SHAP values are zero, check for data/feature mismatch or out-of-distribution values.

        **Notes:**  
        If features have no spread, SHAP explanations may be unstable. Ensure your input data matches what the model expects!

        ### SHAP Feature Contributions (RandomForestClassifier Result)
        """)
        st.image("WhatsApp Image 2025-10-16 at 23.39.12_a6885adf.jpg", caption="SHAP Feature Contributions (RandomForestClassifier Result)", use_container_width=True)

else:
    if selected_tab != "Problem":
        st.info("Please upload your dataset CSV to start.")
