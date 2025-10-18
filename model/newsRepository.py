from config.connection import DBConnection
import psycopg

class NewsRepository:

    def __init__(self, db: DBConnection):
        self.db = db

    def fetchCategories(self):
        try:
            print("[UserRepository][fetchCategories] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        categoria,
                        COUNT(*) AS quantity
                    FROM noticias
                    GROUP BY categoria
                """)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchCategories] -> Error al ejecutar query:", e)
            return []
        
    def fetchAllNews(self, params):
        try:
            print("[UserRepository][fetchAllNews] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        NT.idnoticia,
                        NT.idnoticiaref,
                        NT.titulo,
                        NT.texto,
                        NT.resumen,
                        NT.urlNoticia,
                        NT.imagen,
                        NT.fecha_publicacion,
                        NT.autor,
                        NT.categoria,
                        NT.estado,
                        NT.usuario_creo,
                        TO_CHAR(NT.fecha_creo, 'DD-MM-YYYY HH24:MI:SS') AS fecha_creo,
                        NT.usuario_modifico,
                        TO_CHAR(NT.fecha_modifico, 'DD-MM-YYYY HH24:MI:SS') AS fecha_modifico
                    FROM noticias NT
                    WHERE NT.categoria = %(categoria)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchAllNews] -> Error al ejecutar query:", e)
            return []
    
    def fetchSpecificNew(self, params):
        try:
            print("[UserRepository][fetchSpecificNew] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        NT.idnoticia,
                        NT.idnoticiaref,
                        NT.titulo,
                        NT.texto,
                        NT.resumen,
                        NT.urlNoticia,
                        NT.imagen,
                        NT.fecha_publicacion,
                        NT.autor,
                        NT.categoria,
                        NT.estado,
                        NT.usuario_creo,
                        TO_CHAR(NT.fecha_creo, 'DD-MM-YYYY HH24:MI:SS') AS fecha_creo,
                        NT.usuario_modifico,
                        TO_CHAR(NT.fecha_modifico, 'DD-MM-YYYY HH24:MI:SS') AS fecha_modifico
                    FROM noticias NT
                    WHERE NT.idnoticiaref = %(idnoticia)s
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchSpecificNew] -> Error al ejecutar query:", e)
            return []
        
    def fetchRecomendedNews(self, params):
        try:
            print("[UserRepository][fetchRecomendedNews] -> Ejecutando query ")
            with self.db.get_cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT
                        NT.idnoticia,
                        NT.idnoticiaref,
                        NT.titulo,
                        NT.texto,
                        NT.resumen,
                        NT.urlNoticia,
                        NT.imagen,
                        NT.fecha_publicacion,
                        NT.autor,
                        NT.categoria,
                        NT.estado,
                        NT.usuario_creo,
                        TO_CHAR(NT.fecha_creo, 'DD-MM-YYYY HH24:MI:SS') AS fecha_creo,
                        NT.usuario_modifico,
                        TO_CHAR(NT.fecha_modifico, 'DD-MM-YYYY HH24:MI:SS') AS fecha_modifico
                    FROM noticias NT
                    WHERE NT.categoria = %(categoria)s
                    AND NT.idnoticiaref != %(idnoticia)s
                    LIMIT 3
                """, params)
                return cur.fetchall()
        except Exception as e:
            print("[UserRepository][fetchRecomendedNews] -> Error al ejecutar query:", e)
            return []

    def saveNews(self, params):
        try:
            print("[NewsRepository][saveUser] -> Ejecutando query ")
            with self.db.get_cursor() as cur:
                cur.execute("""
                    INSERT INTO noticias(
                        idnoticiaref, titulo, texto, resumen, urlNoticia, imagen,
                        fecha_publicacion, autor, categoria,
                        estado, usuario_creo, fecha_creo
                    ) VALUES (
                        %(idnoticia)s, %(titulo)s, %(texto)s, %(resumen)s, %(urlNoticia)s, %(imagen)s,
                        %(fecha_publicacion)s, %(autor)s, %(categoria)s,
                        1, %(usuario_creo)s, NOW()
                    )
                    RETURNING idnoticia
                """, params)
                lastInsertId = cur.fetchone()[0]
            self.db.commit()
            return {"lastInsertId":lastInsertId}
        except Exception as e:
            print("[NewsRepository][saveUser] -> Error al ejecutar query:", e)
            self.db.rollback()
            return False