from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, Depends
import jwt  # pyjwt

SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # identificador del usuario
        "exp": expire         # fecha de expiración
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # token expirado
    except jwt.InvalidTokenError:
        return None  # token inválido


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # raise HTTPException(status_code=401, detail="No autorizado")
        raise HTTPException(status_code=401, detail={
            "flag": "FAIL",
            "message": "No autorizado",
            "rows": []
        })
    
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        # raise HTTPException(status_code=401, detail="Formato de token inválido")
        raise HTTPException(status_code=401, detail={
            "flag": "FAIL",
            "message": "Formato de token inválido",
            "rows": []
        })
    
    payload = verify_access_token(token)
    if payload is None:
        # raise HTTPException(status_code=401, detail="Token inválido o expirado")
        raise HTTPException(status_code=401, detail={
            "flag": "FAIL",
            "message": "Token inválido o expirado",
            "rows": []
        })
    
    return payload  # por ejemplo {"sub": "7"}