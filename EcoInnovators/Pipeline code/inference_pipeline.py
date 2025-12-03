import os
import cv2
import requests
import pandas as pd
import json

# Import your custom modules
import detect
import quantify


MAPTILER_KEY = "PH73JaaZIw5SJOqDqo0f"  
INPUT_FILE = "../input_sites.xlsx"              
OUTPUT_DIR = "../Artefacts"                     
MODEL_PATH = "../Trained model file/solar_model.pt"

def fetch_image(lat, lon, sample_id):
    """Downloads satellite image using MapTiler API."""
    url = f"https://api.maptiler.com/maps/satellite/static/{lon},{lat},18/600x600.jpg?key={MAPTILER_KEY}"
    save_path = os.path.join(OUTPUT_DIR, f"{sample_id}.jpg")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return save_path
    except Exception as e:
        print(f"Fetch error: {e}")
    return None

def main():
    print("🚀 Starting EcoInnovators Pipeline...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Load Model
    model = detect.load_model(MODEL_PATH)
    if not model: return

    # 2. Read Inputs
    if not os.path.exists(INPUT_FILE):
        print("Input file not found.")
        return
    df = pd.read_excel(INPUT_FILE)
    
    results_data = []

    # 3. Process Each Site
    for _, row in df.iterrows():
        sid = row['sample_id']
        lat, lon = row['latitude'], row['longitude']
        print(f"Processing Site ID: {sid}...")
        
        # A. Fetch
        img_path = fetch_image(lat, lon, sid)
        if not img_path: continue
        
        # B. Detect
        ai_result = detect.run_detection(img_path, model)
        
        # C. Quantify & Verify
        img = cv2.imread(img_path)
        is_verified, area = quantify.process_results(ai_result, lat, img.shape)
        
        # D. Record Result
        results_data.append({
            "sample_id": sid,
            "lat": lat, "lon": lon,
            "has_solar": is_verified,
            "pv_area_sqm_est": area,
            "qc_status": "VERIFIABLE" if is_verified else "NOT_VERIFIABLE"
        })

    # 4. Save JSON Report
    json_path = "../Prediction files/submission.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(results_data, f, indent=4)
        
    print(f"✅ Pipeline Complete. Results saved to {json_path}")

if __name__ == "__main__":
    main()
