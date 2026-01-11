import requests
import uuid
import json
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

# Get values (with defaults just in case)
JAVA_URL = os.getenv("JAVA_API_URL", "http://localhost:8080/api/verify/human")
API_KEY = os.getenv("API_SECRET", "prism-python-secret")

def send_to_java(wallet_address, ml_result):
    """
    Takes the ML result and sends it to Java exactly how he asked.
    """
    
    # 1. Extract details from your bio_engine result
    # (If a score is missing, default to 0.0 to prevent crash)
    details = ml_result.details
    
    payload = {
        "sessionId": str(uuid.uuid4()),  # Generate a random ID
        "eye_score": float(details.get('sss_ratio', 0.0)), # Map SSS/Eye stats here
        "skin_score": float(details.get('signal_variance', 0.0)),
        "pulse_score": float(ml_result.signal_quality), # Use signal quality
        "flash_score": float(details.get('chroma_contribution', 0.0)),
        "wallet": wallet_address  # <--- CRITICAL: Must come from Frontend
    }

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    print(f"🔗 Sending to Java: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(JAVA_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Java Success:", response.text)
            return True
        else:
            print(f"❌ Java Failed [{response.status_code}]: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False