# Data Directory

This directory contains sample data and uploaded datasets for the User Database Analytics Dashboard.

## Sample Data Format

The `sample_data.csv` file shows the expected format for your database CSV file:

### Required Columns:
- **email**: User email address (unique identifier)
- **username_x/y/z**: Usernames for users X, Y, Z
- **age_x/y/z**: Ages of users X, Y, Z
- **location_x/y/z**: Geographic locations of users X, Y, Z
- **interest_x/y/z**: Interest categories of users X, Y, Z
- **date_of_login_x/y/z**: Login timestamps for users X, Y, Z
- **date_of_logout_x/y/z**: Logout timestamps for users X, Y, Z
- **followers_x/y/z**: Follower counts for users X, Y, Z
- **following_x/y/z**: Following counts for users X, Y, Z

### Data Types:
- **Numeric**: age_*, followers_*, following_*
- **Text**: email, username_*, location_*, interest_*
- **DateTime**: date_of_login_*, date_of_logout_*

### Notes:
- Date format should be: YYYY-MM-DD HH:MM:SS
- Numeric fields should contain only numbers
- Text fields can contain any valid string
- Missing values should be left empty (will be handled by the dashboard)

## Usage:
1. Replace the sample data with your actual database export
2. Ensure column names match exactly
3. Upload through the dashboard interface
