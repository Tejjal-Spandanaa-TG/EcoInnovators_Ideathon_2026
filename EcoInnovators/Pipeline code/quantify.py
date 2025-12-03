import math
import numpy as np
from shapely.geometry import Polygon, Point

def calculate_gsd(lat, zoom_level=18):
    """Calculates Ground Sample Distance (meters per pixel)."""
    # Standard Web Mercator formula
    return 156543.03 * math.cos(math.radians(lat)) / (2 ** zoom_level)

def process_results(result, lat, image_shape):
    """
    Analyzes detection results against Buffer Zone rules.
    Returns: (is_verified, total_area_sqm)
    """
    h, w = image_shape[:2]
    
    # 1. Calculate Scale
    gsd = calculate_gsd(lat)
    pixel_area_m2 = gsd ** 2
    
    # 2. Define Buffer Zones (1200 sq.ft & 2400 sq.ft)
    # 1200 sq.ft ~= 5.95m radius
    # 2400 sq.ft ~= 8.42m radius
    radius_1200_px = int(5.95 / gsd)
    radius_2400_px = int(8.42 / gsd)
    
    center = Point(w // 2, h // 2)
    circle_1200 = center.buffer(radius_1200_px)
    circle_2400 = center.buffer(radius_2400_px)
    
    # 3. Extract Polygons from AI Result
    polygons = []
    if result.boxes:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            # Convert bounding box to polygon points
            pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], np.int32)
            polygons.append(pts)
    elif result.masks:
        polygons = [np.array(x, np.int32) for x in result.masks.xy]

    # 4. Verification Logic
    verified = False
    total_area = 0.0
    
    for pts in polygons:
        if len(pts) < 3: continue
        poly = Polygon(pts)
        
        # Rule: Check intersections with buffer zones
        if poly.intersects(circle_1200) or poly.intersects(circle_2400):
            verified = True
            total_area += poly.area * pixel_area_m2

    return verified, round(total_area, 2)