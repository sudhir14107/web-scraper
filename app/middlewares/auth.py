from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STATIC_TOKEN = os.getenv("STATIC_TOKEN")

async def verify_token(request: Request):
    authorization: str = request.headers.get("x-auth-token")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer" or token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
