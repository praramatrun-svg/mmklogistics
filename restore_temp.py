import zipfile
import os

zip_path = "ai_logistics_deploy.zip"
if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print("Files in zip:")
        print(zip_ref.namelist())
        # Extract admin.html to a temp file
        zip_ref.extract("admin.html", path="temp_restore")
        print("Extracted admin.html to temp_restore/admin.html")
else:
    print("Zip file not found")
