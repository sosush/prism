import socketio
import base64
import time
import os

# Create a standard client
sio = socketio.Client()

def send_stream():
    # 1. Load image (Handle path correctly)
    img_path = "tests/me.jpg"
    if not os.path.exists(img_path):
        print(f"❌ Error: {img_path} not found! Run the curl command again.")
        return

    with open(img_path, "rb") as f:
        img_bytes = f.read()
        b64_string = base64.b64encode(img_bytes).decode('utf-8')

    print("🔌 Connecting to server...")
    
    # 2. Connect with a wait timeout
    try:
        sio.connect('http://localhost:8000', wait_timeout=10)
        print("✅ Connected!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 3. CRITICAL FIX: Wait for handshake to settle
    time.sleep(1) 

    print("🚀 Starting Stream...")

    # Spam the server
    try:
        for i in range(150):
            # Color Cycle Logic
            cycle = i % 90
            if cycle < 30:
                current_color = "RED"
            elif cycle < 60:
                current_color = "BLUE"
            else:
                current_color = "WHITE"

            sio.emit('video_frame', {
                    'image': b64_string,
                    'screenColor': current_color,
                    'timestamp': time.time() * 1000,
                    'wallet': '0xTEST_WALLET_ADDRESS_123'  
                })
            
            # Sleep to match 30 FPS
            time.sleep(0.033) 
            print(f"Sent Frame {i} | Color: {current_color}")
            
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Stream Error: {e}")
    finally:
        sio.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    send_stream()