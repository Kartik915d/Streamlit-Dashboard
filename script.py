# First, let me analyze the column structure you provided
columns = [
    "email",
    "username_x", "age_x", "location_x", "interest_x", "date_of_login_x", "date_of_logout_x", "followers_x", "following_x",
    "username_y", "age_y", "location_y", "interest_y", "date_of_login_y", "date_of_logout_y", "followers_y", "following_y", 
    "username_z", "age_z", "location_z", "interest_z", "date_of_login_z", "date_of_logout_z", "followers_z", "following_z"
]

# Analyze the structure
print("Database columns structure:")
print("Total columns:", len(columns))
print("\nColumn categories:")
print("- Email: 1 column")
print("- User X data: 8 columns")
print("- User Y data: 8 columns") 
print("- User Z data: 8 columns")

print("\nData types inferred:")
print("- Identifiers: email, username_x/y/z")
print("- Numeric: age_x/y/z, followers_x/y/z, following_x/y/z")
print("- Categorical: location_x/y/z, interest_x/y/z")
print("- Datetime: date_of_login_x/y/z, date_of_logout_x/y/z")