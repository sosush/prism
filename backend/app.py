import socketio
import uvicorn
from core.image_utils import decode_image
from core.mock_ml import get_face_data_mock, get_bio_score_mock

# Initialize Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

print("🚀 PRISM Backend is Alive")

@sio.event
async def connect(sid, environ):
    print(f"Client Connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client Disconnected: {sid}")

@sio.event
async def video_frame(sid, data):
    """
    Expects: {'image': 'base64...', 'timestamp': 123}
    """
    # 1. DECODE
    raw_b64 = data.get('image')
    img = decode_image(raw_b64)
    
    if img is None:
        await sio.emit('error', {'msg': 'Bad Image'}, room=sid)
        return

    # 2. DETECT FACE (Mocked for now)
    has_face, roi = get_face_data_mock(img)
    
    if not has_face:
        print(f"[{sid}] No Face Detected")
        return

    # 3. ANALYZE BIO (Mocked for now)
    score = get_bio_score_mock(img, roi)

    # 4. DECIDE
    if score > 0.85:
        print(f"✅ PASSED (Score: {score:.2f})")
        # TODO: Add Java Integration Call Here
        await sio.emit('result', {'status': 'success', 'score': score}, room=sid)
    else:
        print(f"❌ FAILED (Score: {score:.2f})")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)