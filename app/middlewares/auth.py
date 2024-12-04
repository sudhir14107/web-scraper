from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv


load_dotenv()
STATIC_TOKEN = os.getenv("STATIC_TOKEN")

async def verify_token(request: Request):
    token = request.headers.get("x-auth-token")
    
    # Check if the token is missing or incorrect
    # haven't applied scheme check
    if not token or token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return token
