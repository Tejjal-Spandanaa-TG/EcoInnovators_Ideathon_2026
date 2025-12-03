import os
import yaml
import torch
from google.colab import drive

# 1. MOUNT DRIVE (Just in case)
if not os.path.exists('/content/drive'):
    drive.mount('/content/drive')

# 2. INSTALL LIBRARY
print("⚙️ Checking libraries...")
try:
    from ultralytics import YOLO
except ImportError:
    !pip install ultralytics -q
    from ultralytics import YOLO

# 3. CHECK GPU
if torch.cuda.is_available():
    print(f"✅ GPU DETECTED: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ WARNING: Running on CPU. This will be slow!")

# 4. SETUP PATHS & FIND DATA
BASE_DIR = '/content/drive/MyDrive/Ideathon_2026'
DATA_DIR = os.path.join(BASE_DIR, 'datasets')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔍 Re-scanning datasets to build config...")

# Find data.yaml
yaml_files = []
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file == 'data.yaml':
            yaml_files.append(os.path.join(root, file))

if not yaml_files:
    print("❌ CRITICAL ERROR: No 'data.yaml' found in datasets folder!")
    print("   Did you run Step 1 (Unzip) successfully?")
else:
    # Use the first dataset found
    target_yaml = yaml_files[0]
    dataset_root = os.path.dirname(target_yaml)

    # Read and Fix the YAML
    with open(target_yaml, 'r') as f:
        data_config = yaml.safe_load(f)

    # Update paths for Colab
    data_config['path'] = dataset_root
    data_config['train'] = os.path.join(dataset_root, 'train', 'images')
    data_config['val'] = os.path.join(dataset_root, 'valid', 'images')

    # Save the fixed config
    fixed_config_path = os.path.join(OUTPUT_DIR, 'fixed_config.yaml')
    with open(fixed_config_path, 'w') as f:
        yaml.dump(data_config, f)

    print(f"✅ Config rebuilt at: {fixed_config_path}")

    # 5. START TRAINING
    print("\n🚀 INITIALIZING MODEL (YOLOv8 Medium)...")
    model = YOLO('yolov8m.pt')

    print("\n🔥 STARTING TRAINING NOW (10 Epochs)...")
    results = model.train(
        data=fixed_config_path,
        epochs=10,
        imgsz=640,
        batch=8,
        project=OUTPUT_DIR,
        name='Solar_Model_Medium',
        exist_ok=True
    )

    print("✅ TRAINING COMPLETE!")
    print(f"   Model saved to: {os.path.join(OUTPUT_DIR, 'Solar_Model_Medium/weights/best.pt')}")
