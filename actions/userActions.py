from model.userRepository import UserRepository
from config.auth import create_access_token
from config.connection import DBConnection
from service.emailService import EmailService
from utils.generalUtils import GeneralUtils
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

import hashlib

generalUtils = GeneralUtils()
# emailService = EmailService()
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
            
            # verifica si el usuario ya existe
            resultUsuario = self.repo.existeUsuario(params)
            if len(resultUsuario)>0:
                return {
                    "flag": "FAIL",
                    "message": "Este usuario ya se encuentra en uso",
                    "rows": []
                }
            
            # verifica si el correo ya existe
            resultCorreo = self.repo.existeCorreo(params)
            if len(resultCorreo)>0:
                return {
                    "flag": "FAIL",
                    "message": "Este correo ya se encuentra en uso",
                    "rows": []
                }

            # encripta la clave
            clave = params.get("clave")
            clave_hash = hashlib.sha256(clave.encode("utf-8")).hexdigest()
            params["clave"] = clave_hash

            # remueve idusuario para el insert
            params.pop("idusuario", None)

            # crea un token para activar el usuario
            token_activate = generalUtils.randToken(10)
            print('token_activate :::::::::::::: ', token_activate)

            params["token_activate"] = token_activate
            print(params)
            
            result = self.repo.saveUser(params)
            if not result:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible crear el registro",
                    "rows": []
                }

            # ✅ Enviar correo de bienvenida
            EmailService.send_welcome_email(params["correo"], params["nombre"], params["token_activate"])

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
    
    def updateInfoUser(self, params):
        try:
            print("[UserActions][updateInfoUser] -> Ejecutando proceso ")
            print(params)

            idusuario = params.get("idusuario")
            
            resultUsuario = self.repo.existeUsuario(params)
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

            result = self.repo.updateInfoUser(params)

            if not result:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible actualizar el registro",
                    "rows": []
                }
            
            return {
                "flag": "OK",
                "message": "Se actualizó correctamente el registro",
                "rows": []
            }
        
        except Exception as e:
            print("[UserActions][updateInfoUser] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def updatePasswordUser(self, params):
        try:
            print("[UserActions][updatePasswordUser] -> Ejecutando proceso ")
            
            # Obtenemos la clave actual
            resultCurrent = self.repo.getCurrentPassword(params)
            print("resultCurrent ::::::::::::::::::::::::::: ", resultCurrent)
            
            currentPass = resultCurrent[0]["clave"]
            lastPass = resultCurrent[0]["clave_ultima"]

            # Recuperamos claves ingresadas por el usuario
            clave_ultima = params.get("clave_ultima")
            clave = params.get("clave")

            clave_ultima_hash = hashlib.sha256(clave_ultima.encode("utf-8")).hexdigest()
            clave_hash = hashlib.sha256(clave.encode("utf-8")).hexdigest()

            if clave_ultima_hash != currentPass :
                return {
                    "flag": "FAIL",
                    "message": "La clave ingresada como 'clave actual' no coincide con su contraseña actual, por favor, verifique la información",
                    "rows": []
                }
            
            if clave_hash == lastPass :
                return {
                    "flag": "FAIL",
                    "message": "La clave indicada se ha usado recientemente, intente con una nueva contraseña",
                    "rows": []
                }

            params["clave"] = clave_hash
            params["clave_ultima"] = clave_ultima_hash
            
            result = self.repo.updatePasswordUser(params)

            if not result:
                return {
                    "flag": "FAIL",
                    "message": "No fue posible actualizar la contraseña",
                    "rows": []
                }
            
            return {
                "flag": "OK",
                "message": "Se actualizó correctamente la contraseña",
                "rows": []
            }
        except Exception as e:
            print("[UserActions][updatePasswordUser] -> Error en proceso ", e)
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

            # se verifica credenciales
            result = self.repo.verifyCredentials(params)
            if len(result)==0:
                return {
                    "flag": "FAIL",
                    "message": "Las credenciales no son correctas o su usuario",
                    "rows": []
                }
                
            
            userState = result[0]["estado"]
            tokenActivate = params.get("process")

            # verifica si el usario esta inactivo y si esta intentando entrar SIN el link de activación de correo
            if int(userState) == 0 and tokenActivate == '' :
                return {
                    "flag": "FAIL",
                    "message": "Las credenciales no son correctas o su usuario",
                    "rows": [{"tokenActivate": tokenActivate}]
                }
            
            # verifica si el usario esta inactivo y si esta intentando entrar CON el link de activación de correo
            if int(userState) == 0 and tokenActivate != '' :
                resultToken = self.repo.checkTokenActivate({"token_activate": tokenActivate})
                if len(resultToken)==0:
                    return {
                        "flag": "FAIL",
                        "message": "Las credenciales no son correctas o su usuario",
                        "rows": []
                    }
                
                resultActivate = self.repo.activateUser({"idususario": resultToken[0]["idusuario"]})


            # Si las credenciales son correctas, generamos JWT
            user_data = result[0]
            token_data = {"sub": user_data["idusuario"]}  # payload del token
            token = create_access_token(token_data)
            
            return {
                "flag": "OK",
                "message": "Inicio de sesión correcto",
                "rows": [{**result[0], "token": token}]
            }
        except Exception as e:
            print("[UserActions][verifyCredentials] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
        
    def loginWithGoogle(self, params):
        try:
            # Validar el token de Google
            idinfo = id_token.verify_oauth2_token(
                params["id_token"],
                grequests.Request(),
                "82223109385-aip7svi9hpi9oiro18hj4duv9amsu76j.apps.googleusercontent.com"
            )

            correo = idinfo.get("email")
            nombre = idinfo.get("name")
            google_sub = idinfo.get("sub")

            # Buscar usuario por correo
            result = self.repo.fetchUserByEmail({"correo": correo})
            print('result :::::::::::::::::::::: ', result)
            if len(result) == 0:
                # Crear usuario automáticamente si no existe
                new_user = {
                    "nombre": nombre,
                    "correo": correo,
                    "usuario": correo.split("@")[0],  # puedes ajustar el usuario
                    "clave": google_sub,  # opcional: almacenar hash de google_sub
                    "usuario_creo": "GOOGLE_OAUTH"
                }
                resultSave = self.repo.saveUser(new_user)
                
                user_id = resultSave["lastInsertId"]
            else:
                user_id = result[0]["idusuario"]

            print('user_id :::::::::::::::::::::: ', user_id)
            # Generar JWT interno
            token = create_access_token({"sub": user_id})
            print('token :::::::::::::::::::::: ', token)

            return {
                "flag": "OK",
                "message": "Inicio de sesión correcto",
                "rows": [{
                    "idusuario": user_id,
                    "nombre": nombre,
                    "correo": correo,
                    "token": token
                }]
            }

        except Exception as e:
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }