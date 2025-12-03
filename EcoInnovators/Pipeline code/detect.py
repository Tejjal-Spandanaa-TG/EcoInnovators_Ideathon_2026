from ultralytics import YOLO

def load_model(model_path):
    """Loads the YOLOv8 model."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def run_detection(image_path, model):
    """
    Runs inference on a single image.
    Returns the raw result object from YOLO.
    """
    # conf=0.15 is the optimized threshold for solar panels
    results = model.predict(image_path, conf=0.15, verbose=False)
    return results[0]