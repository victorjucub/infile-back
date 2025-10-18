from config.connection import DBConnection
import psycopg

class UserRepository:

    def __init__(self, db: DBConnection):
        self.db = db

    def fetchAllUsers(self):
        try:
            print("[UserRepository][fetchAllUsers] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        USR.idusuario,
                        USR.nombre,
                        USR.correo,
                        USR.usuario,
                        USR.clave,
                        USR.clave_vence,
                        USR.clave_ultima,
                        USR.estado,
                        USR.usuario_creo,
                        TO_CHAR(USR.fecha_creo, 'DD-MM-YYYY HH24:MI:SS') AS fecha_creo,
                        USR.usuario_modifico,
                        TO_CHAR(USR.fecha_modifico, 'DD-MM-YYYY HH24:MI:SS') AS fecha_modifico
                    FROM usuario USR
                """)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchAllUsers] -> Error al ejecutar query:", e)
            return []
    
    def fetchSpecificUser(self, params):
        try:
            print("[UserRepository][fetchSpecificUser] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        USR.idusuario,
                        USR.nombre,
                        USR.correo,
                        USR.usuario,
                        USR.clave,
                        USR.clave_vence,
                        USR.clave_ultima,
                        USR.estado,
                        USR.usuario_creo,
                        TO_CHAR(USR.fecha_creo, 'DD-MM-YYYY HH24:MI:SS') AS fecha_creo,
                        USR.usuario_modifico,
                        TO_CHAR(USR.fecha_modifico, 'DD-MM-YYYY HH24:MI:SS') AS fecha_modifico
                    FROM usuario USR
                    WHERE USR.idusuario = %(idusuario)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchSpecificUser] -> Error al ejecutar query:", e)
            return []

    def saveUser(self, params):
        try:
            print("[UserRepository][saveUser] -> Ejecutando query ")
            with self.db.get_cursor() as cur:
                cur.execute("""
                    INSERT INTO usuario(
                        nombre, correo, usuario, clave, clave_vence,
                        estado, usuario_creo, fecha_creo
                    ) VALUES (
                        UPPER(%(nombre)s), %(correo)s, %(usuario)s, %(clave)s, '2024-01-01',
                        1, %(usuario_creo)s, NOW()
                    )
                    RETURNING idusuario
                """, params)
                lastInsertId = cur.fetchone()[0]
            self.db.commit()
            return {"lastInsertId":lastInsertId}
        except Exception as e:
            print("[UserRepository][saveUser] -> Error al ejecutar query:", e)
            self.db.rollback()
            return False
    
    def updateInfoUser(self, params):
        try:
            print("[UserRepository][updateInfoUser] -> Ejecutando query ")
            with self.db.get_cursor() as cur:
                cur.execute("""
                    UPDATE usuario SET
                        nombre = %(nombre)s,
                        correo = %(correo)s,
                        usuario = %(usuario)s,
                        usuario_modifico = %(usuario_modifico)s,
                        fecha_modifico = NOW()
                    WHERE idusuario = %(idusuario)s
                """, params)
            self.db.commit()
            return True
        except Exception as e:
            print("[UserRepository][updateInfoUser] -> Error al ejecutar query:", e)
            self.db.rollback()
            return False
    
    def updatePasswordUser(self, params):
        try:
            print("[UserRepository][updatePasswordUser] -> Ejecutando query ")
            with self.db.get_cursor() as cur:
                cur.execute("""
                    UPDATE usuario SET
                        nombre = %(nombre)s,
                        correo = %(correo)s,
                        usuario = %(usuario)s,
                        clave = %(clave)s,
                        clave_vence = CURRENT_DATE + INTERVAL '6 months',
                        clave_ultima = %(clave_ultima)s
                    WHERE idusuario = %(idusuario)s
                """, params)
            self.db.commit()
            return True
        except Exception as e:
            print("[UserRepository][updatePasswordUser] -> Error al ejecutar query:", e)
            self.db.rollback()
            return False
    
    def deleteUser(self, params):
        try:
            print("[UserRepository][deleteUser] -> Ejecutando query ")
            with self.db.get_cursor() as cur:
                cur.execute("""
                    DELETE FROM usuario WHERE idusuario = %(idusuario)s
                """, params)
            self.db.commit()
            return True
        except Exception as e:
            print("[UserRepository][deleteUser] -> Error al ejecutar query:", e)
            self.db.rollback()
            return False
    
    def verifyCredentials(self, params):
        try:
            print("[UserRepository][verifyCredentials] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        USR.idusuario,
                        USR.nombre,
                        USR.correo,
                        USR.usuario,
                        USR.clave_vence
                    FROM usuario USR
                    WHERE USR.correo = %(correo)s
                    AND USR.clave = %(clave)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][verifyCredentials] -> Error al ejecutar query:", e)
            return []
        
    def existeUsuario(self, params):
        try:
            print("[UserRepository][existeUsuario] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        USR.idusuario,
                        USR.usuario
                    FROM usuario USR
                    WHERE USR.usuario = %(usuario)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][existeUsuario] -> Error al ejecutar query:", e)
            return []
    
    def existeCorreo(self, params):
        try:
            print("[UserRepository][existeCorreo] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        USR.idusuario,
                        USR.correo
                    FROM usuario USR
                    WHERE USR.correo = %(correo)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][existeCorreo] -> Error al ejecutar query:", e)
            return []