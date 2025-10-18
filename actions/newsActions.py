from config.connection import DBConnection
from model.newsRepository import NewsRepository
from service.noticeService import NoticeService

noticeService = NoticeService()

class NewsActions:
    def __init__(self, db: DBConnection):
        self.repo = NewsRepository(db)

    def fetchCategories(self):
        try:
            print("[NewsActions][fetchCategories] -> Ejecutando proceso ")
            result = self.repo.fetchCategories()
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[NewsActions][fetchCategories] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
        
    def fetchAllNews(self):
        try:
            print("[NewsActions][fetchAllNews] -> Ejecutando proceso ")
            # result = noticeService.fetchAllNews(params["category"])
            result = self.repo.fetchAllNews()
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[NewsActions][fetchAllNews] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def fetchNewsByCategory(self, params):
        try:
            print("[NewsActions][fetchNewsByCategory] -> Ejecutando proceso ")
            result = self.repo.fetchNewsByCategory(params)
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[NewsActions][fetchNewsByCategory] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def fetchSpecificNew(self, params):
        try:
            print("[UserActions][fetchSpecificNew] -> Ejecutando proceso ")
            result = self.repo.fetchSpecificNew(params)
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
            print("[UserActions][fetchSpecificNew] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
        
    def fetchRecomendedNews(self, params):
        try:
            print("[NewsActions][fetchRecomendedNews] -> Ejecutando proceso ")
            # result = noticeService.fetchRecomendedNews(params["category"])
            result = self.repo.fetchRecomendedNews(params)
            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": result
            }
        except Exception as e:
            print("[NewsActions][fetchRecomendedNews] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }
    
    def migrateNews(self, params):
        try:
            print("[NewsActions][fetchAllNews] -> Ejecutando proceso ")
            resultNews = noticeService.fetchAllNews(params["category"])

            noticias = resultNews["news"]
            for item in noticias:
                resultMigrate = self.repo.saveNews({
                    "idnoticia": item["id"],
                    "titulo": item["title"],
                    "texto": item["text"],
                    "resumen": item["summary"],
                    "urlNoticia": item["url"],
                    "imagen": item["image"],
                    "fecha_publicacion": item["publish_date"],
                    "autor": item["author"],
                    "categoria": item["category"],
                    "usuario_creo": "vjucub"
                })

            return {
                "flag": "OK",
                "message": "Información encontrada",
                "rows": resultNews
            }
        except Exception as e:
            print("[NewsActions][fetchAllNews] -> Error en proceso ", e)
            return {
                "flag": "FAIL",
                "message": e,
                "rows": []
            }