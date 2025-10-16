# Configuration settings for the User Database Analytics Dashboard

import streamlit as st

# Dashboard configuration
DASHBOARD_CONFIG = {
    "title": "User Database Analytics Dashboard",
    "icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Color scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e", 
    "tertiary": "#2ca02c",
    "background": "#f0f2f6",
    "text": "#333333"
}

# Chart configuration
CHART_CONFIG = {
    "default_height": 400,
    "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    "background_color": "white",
    "grid_color": "#eeeeee"
}

# Data validation rules
DATA_VALIDATION = {
    "required_columns": [
        "email", "username_x", "age_x", "location_x", "interest_x",
        "date_of_login_x", "date_of_logout_x", "followers_x", "following_x",
        "username_y", "age_y", "location_y", "interest_y",
        "date_of_login_y", "date_of_logout_y", "followers_y", "following_y",
        "username_z", "age_z", "location_z", "interest_z",
        "date_of_login_z", "date_of_logout_z", "followers_z", "following_z"
    ],
    "numeric_columns": [
        "age_x", "age_y", "age_z",
        "followers_x", "followers_y", "followers_z",
        "following_x", "following_y", "following_z"
    ],
    "date_columns": [
        "date_of_login_x", "date_of_login_y", "date_of_login_z",
        "date_of_logout_x", "date_of_logout_y", "date_of_logout_z"
    ]
}

# User groups configuration
USER_GROUPS = ["User X", "User Y", "User Z"]

# Export configuration
EXPORT_CONFIG = {
    "file_formats": ["csv", "xlsx", "json"],
    "datetime_format": "%Y-%m-%d %H:%M:%S"
}
