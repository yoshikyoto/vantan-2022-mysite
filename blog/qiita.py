import requests

class QiitaApiClient:
    """Qiita の API を叩く役割を持つクラス"""

    def get_django_articles(self):
        # get リクエストを送る
        # e09e6d53707a4825b41b20bf96c891deeb95fb9f
        response = requests.get(
            "https://qiita.com/api/v2/tags/django/items",
            headers={"Authorization": "Bearer asdfg"}
        )

        if response.status_code != 200:
            raise RuntimeError("Qiitaの記事が取得できませんでした")
        
        # 配列の初期化
        qiita_articles = []

        # json は list 型（qiitaの投稿のリスト）
        json = response.json()

        # json_article は dict 型
        for json_article in json:
            # dict からタイトルとurlを取り出して
            # QiitaArticle クラスのオブジェクトを作成
            qiita_article = QiitaArticle(
                json_article["title"],
                json_article["url"],
            )
            qiita_articles.append(qiita_article)
        return qiita_articles


class QiitaArticle:

    def __init__(self, title, url):
        self.title = title
        self.url = url