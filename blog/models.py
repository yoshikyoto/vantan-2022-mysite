from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    # 記事のタイトル
    title = models.CharField(max_length=200)
    # 記事の本文
    body = models.TextField()
    # 記事を書いた人
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    """記事に対するコメントの Database Model"""

    # コメント本文
    body = models.TextField()

    # コメントを付けた記事
    # 記事が消えたらコメントも消える（CASCADE）
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    # コメントを書いた人
    # ユーザーが消えたらコメントも消える（CASCADE）
    user = models.ForeignKey(User, on_delete=models.CASCADE)