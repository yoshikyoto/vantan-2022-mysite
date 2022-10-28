from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    # 記事のタイトル
    title = models.CharField(max_length=200)
    # 記事の本文
    body = models.TextField()
    # 記事を書いた人
    user = models.ForeignKey(User, on_delete=models.CASCADE)
