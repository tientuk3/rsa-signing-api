from fastapi import FastAPI, HTTPException
import subprocess
import base64
import os

# Initialize FastAPI app
app = FastAPI()

# helloworld
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Endpoint to sign an SHA256 hash
@app.post("/sign/")
async def sign_hash(hash_base64: str):
    try:
        # Decode the base64-encoded hash to binary
        hash_binary = base64.b64decode(hash_base64)

        # Prepare the OpenSSL command
        openssl_cmd = [
            "openssl", "pkeyutl", "-sign", "-pkeyopt", "digest:sha256", "-inkey", "privatekey.pem"
        ]

        # Start the OpenSSL process
        process = subprocess.Popen(openssl_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        signature, err = process.communicate(input=hash_binary)

        # Check for errors
        if process.returncode != 0 or err:
            raise Exception("OpenSSL error: " + err.decode('utf-8'))

        # Return the signature in base64 encoded format
        return base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))