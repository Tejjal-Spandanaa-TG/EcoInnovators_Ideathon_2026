
import cv2
from ultralytics import YOLO
from google.colab.patches import cv2_imshow
import os

# 1. Load your trained brain
model_path = '/content/drive/MyDrive/Ideathon_2026/outputs/Solar_Model_Medium/weights/best.pt'
if not os.path.exists(model_path):
    model_path = '/content/drive/MyDrive/Ideathon_2026/outputs/Solar_Model_Medium/weights/last.pt'

model = YOLO(model_path)

# 2. Run on your uploaded image
img_path = 'YOUR_IMAGE_HERE'  

if os.path.exists(img_path):
    print(f"🚀 Testing model on {img_path}...")

    # Run Inference
    results = model.predict(img_path, conf=0.15)

    # Show results
    for result in results:
        # Plot the result (draw boxes)
        im_array = result.plot()
        cv2_imshow(im_array) # Display image in Colab

        if len(result.boxes) > 0:
            print("\n✅ SUCCESS! Solar Panel Detected.")
        else:
            print("\n❌ No detection. (Try a clearer image or lower confidence)")
else:
    print("⚠️ Error: Please upload 'test_solar.jpg' to the files sidebar first.")