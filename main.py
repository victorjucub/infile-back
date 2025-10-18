from fastapi import FastAPI, Request, Depends
from config.auth import get_current_user
from config.connection import DBConnection
# ------------ users
from actions.userActions import UserActions
from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema

# ------------ users
from actions.newsActions import NewsActions
# from actions.userActions import UserActions
# from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema

app = FastAPI()

# Inicializamos la conexión a la BD y la capa de usuario
db = DBConnection()
userActions = UserActions(db)
newsActions = NewsActions(db)


# ------------------------------------------------- USERS
@app.get("/")
def fetchAllUsers(current_user: dict = Depends(get_current_user)):
    result = userActions.fetchAllUsers()
    return result

@app.get("/fetch-specific-user/{idusuario}")
def fetchSpecificUser(req: Request, current_user: dict = Depends(get_current_user)):
    result = userActions.fetchSpecificUser({**req.path_params})
    return result

@app.post("/create-user")
def saveUser(body:UserSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.saveUser({**body.model_dump()})
    return result

@app.put("/update-user/{idusuario}")
def updateUser(req: Request, body:UserUpdateSchema, current_user: dict = Depends(get_current_user)):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.updateUser({**body.model_dump(), **req.path_params})
    return result

@app.delete("/delete-user/{idusuario}")
def deleteUser(req: Request, current_user: dict = Depends(get_current_user)):
    result = userActions.deleteUser({**req.path_params})
    return result

@app.post("/login-user")
def verifyCredentials(body:UserLoginSchema):
    # Se parsea a un objeto {} (body.model_dump)
    result = userActions.verifyCredentials({**body.model_dump()})
    return result


# ------------------------------------------------- NOTICES

@app.get("/fetch-categories")
def fetchCategories(req: Request, current_user: dict = Depends(get_current_user)):
    result = newsActions.fetchCategories()
    return result

@app.get("/fetch-all-news/{categoria}")
def fetchAllNews(req: Request, current_user: dict = Depends(get_current_user)):
    result = newsActions.fetchAllNews({**req.path_params})
    return result

@app.get("/fetch-specific-new/{idnoticia}")
def fetchSpecificNew(req: Request, current_user: dict = Depends(get_current_user)):
    result = newsActions.fetchSpecificNew({**req.path_params})
    return result

@app.get("/fetch-recomended-news/{categoria}/{idnoticia}")
def fetchRecomendedNews(req: Request, current_user: dict = Depends(get_current_user)):
    result = newsActions.fetchRecomendedNews({**req.path_params})
    return result

@app.get("/migrate-news/{category}")
def migrateNews(req: Request, current_user: dict = Depends(get_current_user)):
    result = newsActions.migrateNews({**req.path_params})
    return result