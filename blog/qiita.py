import requests

class QiitaApiClient:
    """Qiita の API を叩く役割を持つクラス"""

    def get_django_articles(self):
        # get リクエストを送る
        response = requests.get(
            "https://qiita.com/api/v2/tags/django/items",
        )
        
        # とりあえず print してみる
        # response.json() で json 形式のレスポンスの中身が見られる
        json = response.json()
        qiita_article = json[0]
        print(qiita_article["title"])
