import socketio
import base64
import time

sio = socketio.Client()

def send_stream():
    # Load image once
    with open("tests/me.jpg", "rb") as f:
        img_bytes = f.read()
        b64_string = base64.b64encode(img_bytes).decode('utf-8')

    print("Connecting to server...")
    sio.connect('http://localhost:8000')

    # Spam the server (Simulate 30 FPS)
    for i in range(100):
        sio.emit('video_frame', {'image': b64_string, 'timestamp': time.time()})
        time.sleep(0.033) 
        print(f"Sent Frame {i}")

    sio.disconnect()

if __name__ == "__main__":
    send_stream()