import cv2
import numpy as np
import os

# --- PATH CONFIGURATION ---
# This ensures Python finds the models folder relative to this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level (to backend) then into models
MODELS_DIR = os.path.join(CURRENT_DIR, "../models")

PROTOTXT_PATH = os.path.join(MODELS_DIR, "deploy.prototxt")
MODEL_PATH = os.path.join(MODELS_DIR, "res10_300x300_ssd_iter_140000.caffemodel")

print(f"[INFO] Loading Face Detector from: {MODELS_DIR}")
try:
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
except Exception as e:
    print(f"[ERROR] Could not load Caffe models: {e}")
    print(f"Checked path: {PROTOTXT_PATH}")
    net = None

def get_face_roi(image):
    """
    Input: OpenCV Image
    Output: (x, y, w, h) of the face bounding box OR None
    """
    if net is None:
        return None

    (h, w) = image.shape[:2]
    
    # Preprocess image for Caffe Model
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0)
    )
    
    net.setInput(blob)
    detections = net.forward()

    # Loop over detections to find the best face
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Confidence threshold (0.5 is standard)
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Ensure coordinates are within image bounds
            startX = max(0, startX)
            startY = max(0, startY)
            endX = min(w, endX)
            endY = min(h, endY)
            
            width = endX - startX
            height = endY - startY
            
            if width > 0 and height > 0:
                # Return the bounding box coordinates
                return (startX, startY, width, height)
    
    return None