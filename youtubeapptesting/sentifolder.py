import os

def create_flask_project_structure(project_name):
    folders = [
        f"{project_name}/app",
        f"{project_name}/app/templates",
        f"{project_name}/app/static",
        f"{project_name}/migrations"
    ]
    files = {
        f"{project_name}/app/__init__.py": "# Flask app initialization\n",
        f"{project_name}/app/routes.py": "# Flask routes\n",
        f"{project_name}/app/models.py": "# Database models\n",
        f"{project_name}/app/analysis.py": "# YouTube analysis functions\n",
        f"{project_name}/config.py": "# Flask configuration\n",
        f"{project_name}/run.py": "# Entry point to run Flask app\n",
        f"{project_name}/requirements.txt": "flask\nflask_sqlalchemy\nflask_migrate\ntransformers\ngoogle-api-python-client\npandas\ntqdm\n"
    }

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    for file_path, content in files.items():
        with open(file_path, "w") as file:
            file.write(content)
            print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_flask_project_structure("flask_youtube_analysis")
