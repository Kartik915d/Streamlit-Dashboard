# Create sample data and additional files
os.makedirs('data', exist_ok=True)

# Create sample data CSV
sample_data_content = '''email,username_x,age_x,location_x,interest_x,date_of_login_x,date_of_logout_x,followers_x,following_x,username_y,age_y,location_y,interest_y,date_of_login_y,date_of_logout_y,followers_y,following_y,username_z,age_z,location_z,interest_z,date_of_login_z,date_of_logout_z,followers_z,following_z
user1@example.com,john_x,25,New York,Technology,2024-01-01 08:00:00,2024-01-01 16:00:00,1250,850,jane_y,28,California,Sports,2024-01-01 09:00:00,2024-01-01 17:00:00,980,1200,mike_z,30,Texas,Music,2024-01-01 07:30:00,2024-01-01 15:30:00,1420,900
user2@example.com,alice_x,32,Florida,Art,2024-01-02 08:30:00,2024-01-02 16:30:00,2100,1100,bob_y,27,Nevada,Gaming,2024-01-02 09:30:00,2024-01-02 17:30:00,1800,1350,carol_z,29,Oregon,Travel,2024-01-02 08:00:00,2024-01-02 16:00:00,1650,1050
user3@example.com,david_x,24,Washington,Food,2024-01-03 07:45:00,2024-01-03 15:45:00,890,750,eva_y,31,Illinois,Fashion,2024-01-03 08:15:00,2024-01-03 16:15:00,2200,1400,frank_z,26,Colorado,Fitness,2024-01-03 09:00:00,2024-01-03 17:00:00,1300,800
user4@example.com,grace_x,28,Arizona,Photography,2024-01-04 08:00:00,2024-01-04 16:00:00,1500,950,henry_y,33,Michigan,Business,2024-01-04 07:30:00,2024-01-04 15:30:00,1750,1250,iris_z,25,Ohio,Education,2024-01-04 08:45:00,2024-01-04 16:45:00,1100,700
user5@example.com,jack_x,35,Georgia,Science,2024-01-05 09:15:00,2024-01-05 17:15:00,1320,880,kate_y,29,Virginia,Health,2024-01-05 08:30:00,2024-01-05 16:30:00,1900,1150,liam_z,27,North Carolina,Movies,2024-01-05 07:45:00,2024-01-05 15:45:00,1450,920
'''

with open('data/sample_data.csv', 'w', encoding='utf-8') as f:
    f.write(sample_data_content)

# Create data README
data_readme_content = '''# Data Directory

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
'''

with open('data/README.md', 'w', encoding='utf-8') as f:
    f.write(data_readme_content)

print("✅ Created data/sample_data.csv - Sample dataset")
print("✅ Created data/README.md - Data documentation")
print(f"Sample data size: {len(sample_data_content)} characters")
print(f"Data README size: {len(data_readme_content)} characters")