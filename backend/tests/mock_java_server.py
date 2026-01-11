from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# Match the endpoint the Java guy gave you
@app.post("/api/verify/human")
async def receive_data(request: Request):
    # 1. Print what your Python Backend sent
    data = await request.json()
    headers = request.headers
    
    print("\n-------- MOCK JAVA SERVER RECEIVED REQUEST --------")
    print(f"🔑 API Key: {headers.get('x-api-key')}")
    print(f"📦 Data: {data}")
    print("---------------------------------------------------\n")
    
    # 2. Return a fake success message (Like Java would)
    return {
        "success": True, 
        "tx_hash": "0xFAKE_TRANSACTION_HASH_999",
        "message": "Minting simulated successfully"
    }

if __name__ == '__main__':
    # Run on port 8080 to trick your main app
    print("☕ Mock Java Server running on port 8080...")
    uvicorn.run(app, host='0.0.0.0', port=8080)