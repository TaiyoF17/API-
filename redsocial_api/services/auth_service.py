import uuid, hashlib, time
from typing import Optional

# Tokens en memoria (suficiente para práctica)
TOKENS = {}  # token -> {"user_id":..., "iat":...}

def hash_password(p:str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def create_token(user_id:int) -> str:
    token = uuid.uuid4().hex
    TOKENS[token] = {"user_id": user_id, "iat": int(time.time())}
    return token

def verify_token(token:str) -> Optional[int]:
    info = TOKENS.get(token)
    if not info:
        return None
    return info["user_id"]
