import zipfile
import os
from pathlib import Path

# Create a ZIP file with all the project files
def create_project_zip():
    zip_filename = 'user-database-dashboard.zip'
    
    # Files and directories to include in the ZIP
    files_to_zip = [
        'app.py',
        'requirements.txt', 
        'config.py',
        'README.md',
        '.gitignore',
        'utils/__init__.py',
        'utils/data_processing.py',
        'utils/visualizations.py',
        'pages/__init__.py',
        'pages/user_analytics.py',
        'data/README.md',
        'data/sample_data.csv'
    ]
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            if os.path.exists(file_path):
                # Add file to ZIP with proper directory structure
                zipf.write(file_path, file_path)
                print(f"✅ Added: {file_path}")
            else:
                print(f"⚠️  Missing: {file_path}")
    
    # Check ZIP file size
    zip_size = os.path.getsize(zip_filename)
    print(f"\n📦 Created ZIP file: {zip_filename}")
    print(f"📊 ZIP file size: {zip_size:,} bytes ({zip_size/1024:.1f} KB)")
    
    # List contents of ZIP file
    print(f"\n📋 ZIP file contents:")
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for info in zipf.infolist():
            print(f"   {info.filename} ({info.file_size} bytes)")
    
    return zip_filename

# Create the ZIP file
zip_file = create_project_zip()
print(f"\n🎉 SUCCESS: Your Streamlit dashboard is ready!")
print(f"📁 ZIP file created: {zip_file}")
print(f"\n📋 Next steps:")
print(f"1. Download the ZIP file")
print(f"2. Extract it to your desired location")  
print(f"3. Install dependencies: pip install -r requirements.txt")
print(f"4. Run the dashboard: streamlit run app.py")
print(f"5. Upload to GitHub by creating a new repository and pushing the extracted files")