from fastapi import FastAPI, Request, Depends
from config.auth import get_current_user
from config.connection import DBConnection
from actions.userActions import UserActions
from schema.userSchema import UserSchema, UserLoginSchema, UserUpdateSchema

app = FastAPI()

# Inicializamos la conexión a la BD y la capa de usuario
db = DBConnection()
userActions = UserActions(db)


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