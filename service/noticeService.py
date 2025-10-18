import requests
from fastapi import HTTPException

class NoticeService:
    def __init__(self):
        # self.API_KEY = "dd85d88a368e4c8bb17f31ad8795e3a0"
        self.API_KEY = "0ae5dd5463864bb48015d971e9a37651"
        self.BASE_URL = "https://api.worldnewsapi.com"

    def fetchAllNews(self, querySearch):

        if(querySearch == 'internacional'):
            url = f"{self.BASE_URL}/search-news?text=internacional&language=es&source-country=es&categories=health&earliest-publish-date=2025-10-01"
        else:
            url = f"{self.BASE_URL}/search-news?text=guatemala&language=es&source-country=gt&categories={querySearch}&earliest-publish-date=2025-10-01"

        headers = {
            "x-api-key": self.API_KEY
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al consultar la API externa: {response.text}"
            )