from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from config.auth import getCurrentUser, verifyRefreshToken, createAccessToken
from config.connection import DBConnection
# ------------ users
from actions.userActions import UserActions
from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema, UserUpdateSchemaWhitPass, GoogleLoginSchema, ForgotPasswordSchema, RestorePasswordSchema, RefreshTokenSchema, RevokeSchema

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


@app.post("/refresh-token")
def refreshToken(body:RefreshTokenSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.refreshToken({**body.model_dump()})
    return result

@app.post("/logout")
def logout(body:RevokeSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.logout({**body.model_dump()})
    return result

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