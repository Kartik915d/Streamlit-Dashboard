import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from utils.data_processing import get_user_data_by_type, get_location_distribution, get_interest_distribution, calculate_session_duration

def create_user_comparison_chart(df, chart_type, users_to_analyze):
    """
    Create comparison charts for different data types
    """
    try:
        if chart_type == 'age':
            return create_age_comparison(df, users_to_analyze)
        elif chart_type == 'location':
            return create_location_comparison(df, users_to_analyze)
        elif chart_type == 'interest':
            return create_interest_comparison(df, users_to_analyze)
        elif chart_type == 'engagement':
            return create_engagement_comparison(df, users_to_analyze)
        else:
            return create_default_chart()
    except Exception as e:
        st.error(f"Error creating {chart_type} chart: {str(e)}")
        return create_default_chart()

def create_age_comparison(df, users_to_analyze):
    """
    Create age distribution comparison chart
    """
    age_data = get_user_data_by_type(df, 'age', users_to_analyze)

    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, (user, ages) in enumerate(age_data.items()):
        if ages:
            fig.add_trace(go.Histogram(
                x=ages,
                name=user,
                opacity=0.7,
                marker_color=colors[i % len(colors)],
                nbinsx=15
            ))

    fig.update_layout(
        title="Age Distribution Comparison",
        xaxis_title="Age",
        yaxis_title="Count",
        barmode='overlay',
        height=400
    )

    return fig

def create_location_comparison(df, users_to_analyze):
    """
    Create location distribution comparison chart
    """
    location_data = get_location_distribution(df, users_to_analyze)

    # Prepare data for plotting
    plot_data = []
    for user, locations in location_data.items():
        for location, count in locations.items():
            plot_data.append({
                'User': user,
                'Location': location,
                'Count': count
            })

    if not plot_data:
        return create_default_chart("No location data available")

    plot_df = pd.DataFrame(plot_data)

    fig = px.bar(
        plot_df,
        x='Location',
        y='Count',
        color='User',
        title="Location Distribution Comparison",
        barmode='group',
        height=400
    )

    fig.update_layout(xaxis_title="Location", yaxis_title="Count")

    return fig

def create_interest_comparison(df, users_to_analyze):
    """
    Create interest distribution comparison chart
    """
    interest_data = get_interest_distribution(df, users_to_analyze)

    # Prepare data for plotting
    plot_data = []
    for user, interests in interest_data.items():
        for interest, count in interests.items():
            plot_data.append({
                'User': user,
                'Interest': interest,
                'Count': count
            })

    if not plot_data:
        return create_default_chart("No interest data available")

    plot_df = pd.DataFrame(plot_data)

    fig = px.bar(
        plot_df,
        x='Interest',
        y='Count',
        color='User',
        title="Interest Distribution Comparison",
        barmode='group',
        height=400
    )

    fig.update_layout(xaxis_title="Interest Category", yaxis_title="Count")

    return fig

def create_engagement_comparison(df, users_to_analyze):
    """
    Create followers vs following comparison chart
    """
    engagement_data = []

    for user in users_to_analyze:
        suffix = user.split()[-1].lower()
        followers_col = f"followers_{suffix}"
        following_col = f"following_{suffix}"

        if followers_col in df.columns and following_col in df.columns:
            followers = df[followers_col].fillna(0).sum()
            following = df[following_col].fillna(0).sum()

            engagement_data.append({
                'User': user,
                'Followers': followers,
                'Following': following
            })

    if not engagement_data:
        return create_default_chart("No engagement data available")

    engagement_df = pd.DataFrame(engagement_data)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Followers',
        x=engagement_df['User'],
        y=engagement_df['Followers'],
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Bar(
        name='Following',
        x=engagement_df['User'],
        y=engagement_df['Following'],
        marker_color='#ff7f0e'
    ))

    fig.update_layout(
        title="Followers vs Following Comparison",
        xaxis_title="Users",
        yaxis_title="Count",
        barmode='group',
        height=400
    )

    return fig

def create_activity_timeline(df, users_to_analyze):
    """
    Create user activity timeline
    """
    try:
        timeline_data = []

        for user in users_to_analyze:
            suffix = user.split()[-1].lower()
            login_col = f"date_of_login_{suffix}"
            logout_col = f"date_of_logout_{suffix}"

            if login_col in df.columns and logout_col in df.columns:
                user_df = df[[login_col, logout_col]].dropna()

                for _, row in user_df.iterrows():
                    timeline_data.append({
                        'User': user,
                        'Login': row[login_col],
                        'Logout': row[logout_col],
                        'Duration': (row[logout_col] - row[login_col]).total_seconds() / 3600
                    })

        if not timeline_data:
            return create_default_chart("No activity timeline data available")

        timeline_df = pd.DataFrame(timeline_data)

        fig = px.timeline(
            timeline_df,
            x_start='Login',
            x_end='Logout',
            y='User',
            color='User',
            title="User Activity Timeline",
            height=400
        )

        fig.update_layout(xaxis_title="Time", yaxis_title="Users")

        return fig

    except Exception as e:
        return create_default_chart(f"Error creating timeline: {str(e)}")

def create_engagement_heatmap(df, users_to_analyze):
    """
    Create engagement heatmap
    """
    try:
        # Create engagement metrics matrix
        metrics = []
        user_names = []

        for user in users_to_analyze:
            suffix = user.split()[-1].lower()

            # Get user metrics
            age_col = f"age_{suffix}"
            followers_col = f"followers_{suffix}"
            following_col = f"following_{suffix}"

            user_metrics = []
            user_names.append(user)

            # Age (normalized)
            if age_col in df.columns:
                avg_age = df[age_col].mean()
                user_metrics.append(avg_age if not pd.isna(avg_age) else 0)
            else:
                user_metrics.append(0)

            # Followers (normalized)
            if followers_col in df.columns:
                total_followers = df[followers_col].sum()
                user_metrics.append(total_followers / 1000 if total_followers > 0 else 0)  # Scale down
            else:
                user_metrics.append(0)

            # Following (normalized)
            if following_col in df.columns:
                total_following = df[following_col].sum()
                user_metrics.append(total_following / 1000 if total_following > 0 else 0)  # Scale down
            else:
                user_metrics.append(0)

            # Engagement ratio
            if len(user_metrics) >= 2 and user_metrics[2] > 0:
                engagement_ratio = user_metrics[1] / user_metrics[2]
                user_metrics.append(engagement_ratio)
            else:
                user_metrics.append(0)

            metrics.append(user_metrics)

        if not metrics:
            return create_default_chart("No data for heatmap")

        fig = go.Figure(data=go.Heatmap(
            z=metrics,
            x=['Avg Age', 'Followers (K)', 'Following (K)', 'Engagement Ratio'],
            y=user_names,
            colorscale='Viridis',
            showscale=True
        ))

        fig.update_layout(
            title="User Engagement Metrics Heatmap",
            height=400
        )

        return fig

    except Exception as e:
        return create_default_chart(f"Error creating heatmap: {str(e)}")

def create_session_duration_chart(df, users_to_analyze):
    """
    Create session duration analysis chart
    """
    session_data = calculate_session_duration(df, users_to_analyze)

    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, (user, durations) in enumerate(session_data.items()):
        if durations:
            fig.add_trace(go.Box(
                y=durations,
                name=user,
                marker_color=colors[i % len(colors)]
            ))

    fig.update_layout(
        title="Session Duration Distribution",
        yaxis_title="Duration (hours)",
        height=400
    )

    return fig

def create_default_chart(message="No data available"):
    """
    Create a default chart when data is not available
    """
    fig = go.Figure()

    fig.add_annotation(
        x=0.5, y=0.5,
        text=message,
        showarrow=False,
        font=dict(size=16),
        xref="paper", yref="paper"
    )

    fig.update_layout(
        title="Chart Placeholder",
        height=400,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False)
    )

    return fig
