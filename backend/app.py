import socketio
import uvicorn
from core.image_utils import decode_image
from core.java_client import send_to_java

# --- IMPORT REAL ENGINES ---
try:
    from core.face_engine import get_face_roi
    print("✅ Face Engine Loaded")
except ImportError as e:
    print(f"❌ Face Engine Error: {e}")

try:
    from core.bio_engine import process_pipeline, init_session, remove_session
    print("✅ Bio Engine Loaded")
except ImportError as e:
    print(f"❌ Bio Engine Error: {e}")

# --- SETUP SERVER ---
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

print("🚀 PRISM PIPELINE: READY")

@sio.event
async def connect(sid, environ):
    print(f"Client Connected: {sid}")
    # Initialize the ML Engine for this specific user
    init_session(sid)

@sio.event
async def disconnect(sid):
    print(f"Client Disconnected: {sid}")
    # Clean up memory
    remove_session(sid)

@sio.event
async def video_frame(sid, data):
    """
    Payload: {'image': 'base64...', 'screenColor': 'RED', 'timestamp': 123}
    """
        # 1. GET DATA FROM FRONTEND
    raw_img = data.get('image')
    screen_color = data.get('screenColor', 'WHITE')
    
    # --- THIS IS NEW ---
    # The frontend MUST send this. If they don't, we can't mint.
    user_wallet = data.get('wallet') 
    
    if user_wallet is None:
        # Just print a warning but keep running for testing
        # print(f"[{sid}] Warning: No Wallet Address in packet")
        pass

    # ... [DECODE IMAGE CODE STAYS THE SAME] ...
    img = decode_image(raw_img)
    if img is None: return

    # ... [GET ROI CODE STAYS THE SAME] ...
    roi = get_face_roi(img)
    if roi is None: return

    # ... [ML PIPELINE CODE STAYS THE SAME] ...
    # This runs your bio_engine and gets the result object
    result = process_pipeline(sid, img, roi, screen_color)

    # 4. DECISION & JAVA CALL
    if result.confidence > 0: # We have data
        
        # Log to console
        print(f"[{sid}] Human: {result.is_human} | Conf: {result.confidence}%")

        # Emit back to Frontend so they see the score
        await sio.emit('result', {
            'status': 'verified' if result.is_human else 'analyzing',
            'score': result.confidence,
            'details': result.details
        }, room=sid)

        # 5. CALL JAVA (Only if Human + We have a Wallet)
        if result.is_human and user_wallet:
            print(f"🚀 Triggering Mint for {user_wallet}...")
            
            success = send_to_java(user_wallet, result)
            
            if success:
                # Tell Frontend: "STOP SCANNING, YOU ARE DONE"
                await sio.emit('mint_status', {'status': 'success'}, room=sid)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)