from model.userRepository import UserRepository
from config.auth import create_access_token
from config.connection import DBConnection
import hashlib

class UserActions:
    def __init__(self, db: DBConnection):
        self.repo = UserRepository(db)

    def checkAuth(self):
        try:
            print("[UserActions][checkAuth] -> Ejecutando proceso ")
            return {
                "flag": "OK",
                "message": "El token es valido",
                "rows": []
            }
        except Exception as e:
            print("[UserActions][checkAuth] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
        
    def fetchAllUsers(self):
        try:
            print("[UserActions][fetchAllUsers] -> Ejecutando proceso ")
            result = self.repo.fetchAllUsers()
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[UserActions][fetchAllUsers] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
        
    def fetchSpecificUser(self, params):
        try:
            print("[UserActions][fetchSpecificUser] -> Ejecutando proceso ")
            result = self.repo.fetchSpecificUser(params)
            if len(result)==0:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible identificar el registro o no existe en la base de datos",
                    "rows": []
                }
            
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[UserActions][fetchSpecificUser] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def saveUser(self, params):
        try:
            print("[UserActions][saveUser] -> Ejecutando proceso ")
            
            resultUsuario = self.repo.existeUsuario(params)
            if len(resultUsuario)>0:
                return {
                    "flag": "FAIL",
                    "message": "Este usuario ya se encuentra en uso",
                    "rows": []
                }
            
            resultCorreo = self.repo.existeCorreo(params)
            if len(resultCorreo)>0:
                return {
                    "flag": "FAIL",
                    "message": "Este correo ya se encuentra en uso",
                    "rows": []
                }

            clave = params.get("clave")
            clave_hash = hashlib.sha256(clave.encode("utf-8")).hexdigest()
            params["clave"] = clave_hash

            params.pop("idusuario", None)
            print(params)
            
            result = self.repo.saveUser(params)
            if not result:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible crear el registro",
                    "rows": []
                }

            # data["idusuario"] = result
            # "rows": [data]
            return {
                "flag": "OK",
                "message": "Se creó correctamente el registro",
                "rows": [result]
            }
        except Exception as e:
            print("[UserActions][saveUser] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def updateUser(self, params):
        try:
            print("[UserActions][updateInfoUser] -> Ejecutando proceso ")
            print(params)

            idusuario = params.get("idusuario")
            
            resultUsuario = self.repo.existeUsuario(params)
            print(" resultUsuario ::::::::::::::: ", resultUsuario)
            if len(resultUsuario)>0:
                if int(resultUsuario[0]["idusuario"]) != int(idusuario):
                    return {
                    "flag": "FAIL",
                    "message": "Este usuario ya se encuentra en uso",
                    "rows": []
                }
            
            resultCorreo = self.repo.existeCorreo(params)
            if len(resultCorreo)>0:
                if int(resultCorreo[0]["idusuario"]) != int(idusuario):
                    return {
                    "flag": "FAIL",
                    "message": "Este correo ya se encuentra en uso",
                    "rows": []
                }

            clave = params.get("clave")

            result = False
            message = ""
            if clave=="":
                # Si la clave viene vacía, no actualiza contraseña
                result = self.repo.updateInfoUser(params)
                message = "[SIN CONTRASEÑA] Se actualizó correctamente el registro" if result else "[SIN CONTRASEÑA] No fue posible actualizar el registro"
            else:
                # Si la clave viene con valor, actualiza campos de contraseña
                clave_ultima = params.get("clave_ultima")
                clave_hash = hashlib.sha256(clave.encode("utf-8")).hexdigest()
                clave_ultima_hash = hashlib.sha256(clave_ultima.encode("utf-8")).hexdigest()
                params["clave"] = clave_hash
                params["clave_ultima"] = clave_ultima_hash
                
                result = self.repo.updatePasswordUser(params)
                message = "[CON CONTRASEÑA] Se actualizó correctamente el registro" if result else "[CON CONTRASEÑA] No fue posible actualizar el registro"

            if not result:
                return {
                    "flag": "FAIL",
                    "message": message,
                    "rows": []
                }
            
            return {
                "flag": "OK",
                "message": message,
                "rows": []
            }
        except Exception as e:
            print("[UserActions][updateInfoUser] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def deleteUser(self, params):
        try:
            print("[UserActions][deleteUser] -> Ejecutando proceso ")
            result = self.repo.deleteUser(params)
            if not result:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible eliminar el registro",
                    "rows": []
                }
            
            return {
                "flag": "OK",
                "message": "Se eliminó correctamente el registro",
                "rows": []
            }
        except Exception as e:
            print("[UserActions][deleteUser] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def verifyCredentials(self, params):
        try:
            print("[UserActions][verifyCredentials] -> Ejecutando proceso ")
            
            clave = params.get("clave")
            clave_hash = hashlib.sha256(clave.encode("utf-8")).hexdigest()
            params["clave"] = clave_hash

            params.pop("idusuario", None)
            params.pop("nombre", None)

            result = self.repo.verifyCredentials(params)
            if len(result)==0:
                return {
                    "flag": "FAIL",
                    "message": "Las credenciales no son correctas",
                    "rows": []
                }
            
            # Si las credenciales son correctas, generamos JWT
            user_data = result[0]
            token_data = {"sub": user_data["idusuario"]}  # payload del token
            token = create_access_token(token_data)
            
            return {
                "flag": "OK",
                "message": "Loggeado",
                "rows": [{**result[0], "token": token}]
            }
        except Exception as e:
            print("[UserActions][verifyCredentials] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }