import os

# Create directory structure for the Streamlit dashboard project
project_structure = {
    'app.py': '',
    'requirements.txt': '',
    'config.py': '',
    'utils/': {
        'data_processing.py': '',
        'visualizations.py': '',
        '__init__.py': ''
    },
    'pages/': {
        'user_analytics.py': '',
        'engagement_metrics.py': '',
        'comparative_analysis.py': '',
        '__init__.py': ''
    },
    'data/': {
        'sample_data.csv': '',
        'README.md': ''
    },
    'README.md': '',
    '.gitignore': ''
}

print("Project structure created:")
for item in project_structure:
    if isinstance(project_structure[item], dict):
        print(f"📁 {item}")
        for subitem in project_structure[item]:
            print(f"   📄 {subitem}")
    else:
        print(f"📄 {item}")