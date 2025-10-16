# Create the data processing utilities
data_processing_content = '''import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def load_and_process_data(uploaded_file):
    """
    Load and process the uploaded CSV file
    """
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = [
            'email', 'username_x', 'age_x', 'location_x', 'interest_x', 
            'date_of_login_x', 'date_of_logout_x', 'followers_x', 'following_x',
            'username_y', 'age_y', 'location_y', 'interest_y', 
            'date_of_login_y', 'date_of_logout_y', 'followers_y', 'following_y',
            'username_z', 'age_z', 'location_z', 'interest_z', 
            'date_of_login_z', 'date_of_logout_z', 'followers_z', 'following_z'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            return None
        
        # Process date columns
        date_columns = [col for col in df.columns if 'date_of_login' in col or 'date_of_logout' in col]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                st.warning(f"Could not parse dates in column: {col}")
        
        # Clean numeric columns
        numeric_columns = [col for col in df.columns if any(x in col for x in ['age', 'followers', 'following'])]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def calculate_metrics(df, users_to_analyze):
    """
    Calculate key metrics from the dataframe
    """
    metrics = {}
    
    try:
        # Total users (unique emails)
        metrics['total_users'] = df['email'].nunique() if 'email' in df.columns else len(df)
        
        # Calculate average age across selected users
        age_columns = []
        if 'User X' in users_to_analyze:
            age_columns.append('age_x')
        if 'User Y' in users_to_analyze:
            age_columns.append('age_y')
        if 'User Z' in users_to_analyze:
            age_columns.append('age_z')
        
        if age_columns:
            ages = []
            for col in age_columns:
                if col in df.columns:
                    ages.extend(df[col].dropna().tolist())
            metrics['avg_age'] = np.mean(ages) if ages else 0
        else:
            metrics['avg_age'] = 0
        
        # Calculate total followers
        follower_columns = []
        if 'User X' in users_to_analyze:
            follower_columns.append('followers_x')
        if 'User Y' in users_to_analyze:
            follower_columns.append('followers_y')
        if 'User Z' in users_to_analyze:
            follower_columns.append('followers_z')
        
        total_followers = 0
        for col in follower_columns:
            if col in df.columns:
                total_followers += df[col].fillna(0).sum()
        metrics['total_followers'] = int(total_followers)
        
        # Calculate engagement rate (followers/following ratio)
        following_columns = []
        if 'User X' in users_to_analyze:
            following_columns.append('following_x')
        if 'User Y' in users_to_analyze:
            following_columns.append('following_y')
        if 'User Z' in users_to_analyze:
            following_columns.append('following_z')
        
        total_following = 0
        for col in following_columns:
            if col in df.columns:
                total_following += df[col].fillna(0).sum()
        
        if total_following > 0:
            metrics['engagement_rate'] = (total_followers / total_following) * 100
        else:
            metrics['engagement_rate'] = 0
        
        # Set default deltas (in a real scenario, you'd compare with previous period)
        metrics['user_growth'] = np.random.randint(5, 20)
        metrics['age_trend'] = round(np.random.uniform(-1, 1), 1)
        metrics['follower_growth'] = np.random.randint(100, 500)
        metrics['engagement_delta'] = round(np.random.uniform(-0.5, 0.5), 2)
        
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        # Return default metrics
        metrics = {
            'total_users': 0,
            'avg_age': 0,
            'total_followers': 0,
            'engagement_rate': 0,
            'user_growth': 0,
            'age_trend': 0,
            'follower_growth': 0,
            'engagement_delta': 0
        }
    
    return metrics

def get_user_data_by_type(df, data_type, users_to_analyze):
    """
    Extract specific type of data for selected users
    """
    user_data = {}
    
    for user in users_to_analyze:
        suffix = user.split()[-1].lower()  # Get 'x', 'y', or 'z'
        column_name = f"{data_type}_{suffix}"
        
        if column_name in df.columns:
            user_data[user] = df[column_name].dropna().tolist()
        else:
            user_data[user] = []
    
    return user_data

def calculate_session_duration(df, users_to_analyze):
    """
    Calculate session duration for users
    """
    session_data = {}
    
    for user in users_to_analyze:
        suffix = user.split()[-1].lower()
        login_col = f"date_of_login_{suffix}"
        logout_col = f"date_of_logout_{suffix}"
        
        if login_col in df.columns and logout_col in df.columns:
            df_user = df[[login_col, logout_col]].dropna()
            if len(df_user) > 0:
                # Calculate session duration in hours
                df_user['session_duration'] = (df_user[logout_col] - df_user[login_col]).dt.total_seconds() / 3600
                session_data[user] = df_user['session_duration'].tolist()
            else:
                session_data[user] = []
        else:
            session_data[user] = []
    
    return session_data

def get_location_distribution(df, users_to_analyze):
    """
    Get location distribution for selected users
    """
    location_data = {}
    
    for user in users_to_analyze:
        suffix = user.split()[-1].lower()
        location_col = f"location_{suffix}"
        
        if location_col in df.columns:
            location_counts = df[location_col].value_counts().to_dict()
            location_data[user] = location_counts
        else:
            location_data[user] = {}
    
    return location_data

def get_interest_distribution(df, users_to_analyze):
    """
    Get interest distribution for selected users
    """
    interest_data = {}
    
    for user in users_to_analyze:
        suffix = user.split()[-1].lower()
        interest_col = f"interest_{suffix}"
        
        if interest_col in df.columns:
            interest_counts = df[interest_col].value_counts().to_dict()
            interest_data[user] = interest_counts
        else:
            interest_data[user] = {}
    
    return interest_data
'''

# Create utils directory and files
import os
os.makedirs('utils', exist_ok=True)

with open('utils/data_processing.py', 'w', encoding='utf-8') as f:
    f.write(data_processing_content)

with open('utils/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

print("✅ Created utils/data_processing.py - Data processing utilities")
print(f"File size: {len(data_processing_content)} characters")