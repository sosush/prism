import base64
import numpy as np
import cv2

def decode_image(base64_string):
    try:
        # Strip the header if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode Base64 to Bytes
        img_bytes = base64.b64decode(base64_string)
        
        # Convert Bytes to NumPy Array
        np_arr = np.frombuffer(img_bytes, np.uint8)
        
        # Decode to OpenCV Image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("cv2.imdecode returned None")
            
        return img
    except Exception as e:
        print(f"[ERROR] Image Decode Failed: {e}")
        return None