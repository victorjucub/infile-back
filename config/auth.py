from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, Depends
import jwt  # pyjwt

SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
PASSWORD_RESTORE_TOKEN_EXPIRE_MINUTES = 120

REFRESH_TOKEN_EXPIRE_DAYS = 30  # duración estándar
NEVER_EXPIRE = 10*365  # 10 años para "recordarme"

def createAccessToken(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # identificador del usuario
        "exp": expire         # fecha de expiración
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verifyAccessToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # token expirado
    except jwt.InvalidTokenError:
        return None  # token inválido

def getCurrentUser(request: Request):
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
    
    payload = verifyAccessToken(token)
    if payload is None:
        # raise HTTPException(status_code=401, detail="Token inválido o expirado")
        raise HTTPException(status_code=401, detail={
            "flag": "FAIL",
            "message": "Token inválido o expirado",
            "rows": []
        })
    
    return payload  # por ejemplo {"sub": "7"}

def createPasswordRestoreToken(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=PASSWORD_RESTORE_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # identificador del usuario
        "exp": expire         # fecha de expiración
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def createRefreshToken(user_id: int, remember_me: str = 'no'):
    print('[auth][createRefreshToken] remember_me ::::::::::::: ', remember_me)
    if remember_me == 'si':
        print('marco si recordar NEVER_EXPIRE ::::::::::::: ', NEVER_EXPIRE)
        expire = datetime.utcnow() + timedelta(days=NEVER_EXPIRE)
    else:
        print('marco no recordar ACCESS_TOKEN_EXPIRE_MINUTES ::::::::::::: ', ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verifyRefreshToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None