import random


def get_face_data_mock(image):
    # Simulate finding a face at x=100, y=100
    # Returns: (FaceDetected_Bool, ROI_Coordinates)
    return True, {"x": 100, "y": 100, "w": 200, "h": 200}


def get_bio_score_mock(image, roi):
    # Simulate a score between 0.0 and 1.0
    # Randomly fail sometimes to test your logic
    return random.uniform(0.7, 0.99)