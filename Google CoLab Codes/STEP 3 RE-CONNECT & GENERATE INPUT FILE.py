import os
import pandas as pd
from google.colab import drive

# 1. FORCE MOUNT DRIVE
if not os.path.exists('/content/drive'):
    print("🔌 Re-connecting to Google Drive...")
    drive.mount('/content/drive')

# 2. DEFINE & CREATE FOLDER
BASE_DIR = '/content/drive/MyDrive/Ideathon_2026'

if not os.path.exists(BASE_DIR):
    print(f"⚠️ Folder not found. Creating {BASE_DIR}...")
    os.makedirs(BASE_DIR, exist_ok=True)
else:
    print(f"✅ Found folder: {BASE_DIR}")

# 3. CREATE THE EXCEL FILE
OUTPUT_FILE = os.path.join(BASE_DIR, 'input_sites.xlsx')

real_test_data = {
    'sample_id': [1001, 1002, 1003, 1004, 1005],
    'latitude': [28.5272, 19.0445, 12.9784, 13.0827, 23.0225],
    'longitude': [77.2167, 72.8895, 77.6408, 80.2707, 72.5714]
}

df = pd.DataFrame(real_test_data)
df.to_excel(OUTPUT_FILE, index=False)

print(f"✅ SUCCESS! Created '{OUTPUT_FILE}'")
print("👉 You can now run Step 4 (The Master Pipeline).")