from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.auth import getCurrentUser, verifyRefreshToken, createAccessToken
from config.connection import DBConnection
# ------------ users
from actions.userActions import UserActions
from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema, UserUpdateSchemaWhitPass, GoogleLoginSchema, ForgotPasswordSchema, RestorePasswordSchema

# ------------ users
from actions.newsActions import NewsActions
# from actions.userActions import UserActions
# from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializamos la conexión a la BD y la capa de usuario
db = DBConnection()
userActions = UserActions(db)
newsActions = NewsActions(db)


# ------------------------------------------------- USERS
@app.get("/check-auth")
def checkAuth(current_user: dict = Depends(getCurrentUser)):
    result = userActions.checkAuth()
    return result

@app.get("/fetch-all-users")
def fetchAllUsers(current_user: dict = Depends(getCurrentUser)):
    result = userActions.fetchAllUsers()
    return result

@app.get("/fetch-specific-user/{idusuario}")
def fetchSpecificUser(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = userActions.fetchSpecificUser({**req.path_params})
    return result

@app.post("/create-user")
def saveUser(body:UserSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.saveUser({**body.model_dump()})
    return result

@app.put("/update-info-user/{idusuario}")
def updateInfoUser(req: Request, body:UserUpdateSchema, current_user: dict = Depends(getCurrentUser)):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.updateInfoUser({**body.model_dump(), **req.path_params})
    return result

@app.put("/update-password-user/{idusuario}")
def updatePasswordUser(req: Request, body:UserUpdateSchemaWhitPass, current_user: dict = Depends(getCurrentUser)):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.updatePasswordUser({**body.model_dump(), **req.path_params})
    return result

@app.delete("/delete-user/{idusuario}")
def deleteUser(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = userActions.deleteUser({**req.path_params})
    return result

@app.post("/login-user")
def verifyCredentials(body:UserLoginSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.verifyCredentials({**body.model_dump()})
    return result

@app.post("/login-google")
def loginGoogle(body: GoogleLoginSchema):
    result = userActions.loginWithGoogle({**body.model_dump()})
    return result

@app.post("/forgot-password")
def forgotPassword(body:ForgotPasswordSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.forgotPassword({**body.model_dump()})
    return result

@app.post("/restore-password")
def restorePassword(body:RestorePasswordSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.restorePassword({**body.model_dump()})
    return result


class RefreshTokenSchema(BaseModel):
    refresh_token: str

@app.post("/refresh-token")
def refresh_token(body: RefreshTokenSchema):
    payload = verifyRefreshToken(body.refresh_token)
    if not payload:
        return {"flag": "FAIL", "message": "Refresh token inválido", "rows": []}

    tokens = userActions.repo.getRefreshToken(body.refresh_token)
    if len(tokens) == 0 or not tokens[0]["estado"]:
        return {"flag": "FAIL", "message": "Refresh token revocado", "rows": []}

    idusuario = payload["sub"]
    new_access = createAccessToken(idusuario)
    return {"flag": "OK", "message": "Token renovado", "rows": [{"access_token": new_access}]}

class RevokeSchema(BaseModel):
    refresh_token: str

@app.post("/logout")
def logout(body: RevokeSchema):
    ok = userActions.repo.revokeRefreshToken(body.refresh_token)
    if not ok:
        return {"flag": "FAIL", "message": "No se pudo revocar el token", "rows": []}
    return {"flag": "OK", "message": "Sesión cerrada", "rows": []}

# ------------------------------------------------- NOTICES

@app.get("/fetch-categories")
def fetchCategories(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.fetchCategories()
    return result

@app.get("/fetch-all-news")
def fetchAllNews(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.fetchAllNews()
    return result

@app.get("/fetch-news-by-category/{categoria}")
def fetchNewsByCategory(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.fetchNewsByCategory({**req.path_params})
    return result

@app.get("/fetch-specific-new/{idnoticia}")
def fetchSpecificNew(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.fetchSpecificNew({**req.path_params})
    return result

@app.get("/fetch-recomended-news/{categoria}/{idnoticia}")
def fetchRecomendedNews(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.fetchRecomendedNews({**req.path_params})
    return result

@app.get("/migrate-news/{category}")
def migrateNews(req: Request, current_user: dict = Depends(getCurrentUser)):
    result = newsActions.migrateNews({**req.path_params})
    return result