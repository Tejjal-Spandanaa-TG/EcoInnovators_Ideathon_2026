import os
import requests
from google.colab import drive
import zipfile
from IPython.display import Image, display

# 1. Mount Google Drive
print("MOUNTING GOOGLE DRIVE...")
drive.mount('/content/drive')

MAPTILER_KEY = 'PH73JaaZIw5SJOqDqo0f'

# 2. Install The "Brain" Libraries 
print("INSTALLING AI LIBRARIES... (This takes 1 min)")
pip install -q transformers datasets rasterio shapely geopandas

# 3. Setup Project Folders
BASE_DIR = '/content/drive/MyDrive/Ideathon_2026'
DATA_DIR = os.path.join(BASE_DIR, 'datasets')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

if not os.path.exists(BASE_DIR):
    print(f"❌ ERROR: Folder {BASE_DIR} not found. Did you create 'Ideathon_2026' in your Drive?")
else:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✅ Workspace ready at: {BASE_DIR}")

# 4. Auto-Unzip Data
print("CHECKING FOR DATASETS...")
zip_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.zip')]

if not zip_files:
    print("⚠️ WARNING: No ZIP files found in Ideathon_2026 folder!")
    print("Please upload the 3 downloaded ZIP files to the 'Ideathon_2026' folder in Google Drive.")
else:
    for zf in zip_files:
        folder_name = zf.replace('.zip', '')
        if not os.path.exists(os.path.join(DATA_DIR, folder_name)):
            print(f"   -> Unzipping {zf}...")
            with zipfile.ZipFile(os.path.join(BASE_DIR, zf), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(DATA_DIR, folder_name))
        else:
            print(f"   -> {zf} already unzipped.")
    print(f"✅ Data processing complete.")

# 5. Test MapTiler API 
print("\nTESTING SATELLITE CONNECTION...")
# We request a test image of New Delhi
lat, lon = 28.6139, 77.2090
url = f"https://api.maptiler.com/maps/satellite/static/{lon},{lat},18/400x400.jpg?key={MAPTILER_KEY}"

response = requests.get(url)
if response.status_code == 200:
    with open('test_map.jpg', 'wb') as f:
        f.write(response.content)
    print("✅ API SUCCESS! Here is a test satellite image of New Delhi:")
    display(Image('test_map.jpg'))
else:
    print("❌ API ERROR. Please check your Key.")
    print("Server said:", response.text)

print("IF YOU SEE THE IMAGE ABOVE, WE ARE READY FOR PHASE 3.")
