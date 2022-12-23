from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article, Comment
from blog.qiita import QiitaApiClient
import json
import subprocess


def index(request):
    # blog_article テーブルの中身を全部取得
    # articles は Article クラスのオブジェクトが入った配列
    articles = Article.objects.all()

    qiita_api = QiitaApiClient()

    # qiita の API がエラーになったかどうか表すフラグ
    is_qiita_error = False

    # 記事一覧を初期化しておく
    qiita_articles = []
    try:
        qiita_articles = qiita_api.get_django_articles()
    except RuntimeError:
        is_qiita_error = True
 

    return render(request, "blog/index.html", {
        "articles": articles,
        "qiita_articles": qiita_articles,
        "is_qiita_error": is_qiita_error,
    })

def detail(request):
    return HttpResponse("detail page")

def open_article_file(request):
    article_filename = request.GET["filename"]

    child_process = subprocess.Popen(
        "cat " + article_filename,  # 実行されるコマンド cat <filename>
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = child_process.communicate()

    return render(request, "blog/article_file.html", {
        "title": article_filename,
        "body": stdout,
    })


# アカウントの作成を行うクラスベースビュー
class AccountCreateView(View):

    def get(self, request):
        return render(request, "blog/register.html")

    def post(self, request):
        # ユーザー情報を保存する
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        # 登録完了ページを表示
        return render(request, "blog/register_success.html")


# LoginView を継承したうえで、一部設定を変更
class AccountLoginView(LoginView):
    """ログインページのテンプレート"""
    template_name = 'blog/login.html'

    def get_default_redirect_url(self):
        """ログインに成功した時に飛ばされるURL"""
        return "/blog"


# マイページのクラスベースビュー
class MypageView(LoginRequiredMixin, View):
    login_url = '/blog/login'

    def get(self, request):
        articles = Article.objects.filter(user=request.user)
        return render(request, "blog/mypage.html", {
            "articles": articles,
        })


class AccountLogoutView(LogoutView):
    template_name = 'blog/logout.html'


class ArticleCreateView(LoginRequiredMixin, View):
    login_url = '/blog/login'

    def get(self, request):
        """記事を書く画面を表示するリクエスト"""
        return render(request, "blog/article_new.html")


class MypageArticleView(LoginRequiredMixin, View):
    login_url = '/blog/login'
    
    def post(self, request):
        """記事を保存する"""
        # リクエストで受け取った情報をDBに保存する
        article = Article(
            title=request.POST["title"],
            body=request.POST["body"],
            # user には、現在ログイン中のユーザーをセットする
            user=request.user,
        )
        article.save()
        return render(request, "blog/article_created.html")

# 記事についての View
class ArticleView(View):
    # urls.py の <id> が、 id に入る
    def get(self, request, id):
        # get は条件に合致した記事を一つ取得する
        article = Article.objects.get(id=id)

        return render(request, "blog/article.html", {
            "article": article,
        })

class ArticleApiView(View):
    
    def get(self, request):
        # DB から Article を取得
        # articles は blog.models.Article のリスト
        articles = Article.objects.all()

        # Article オブジェクトのリストを、dict の list に変換
        dict_articles = []
        for article in articles:
            # Article のオブジェクトを dict に変換
            dict_article = {
                "id": article.id,
                "title": article.title,
                "body": article.body,
            }
            # 変換後の dict を list に追加
            dict_articles.append(dict_article)

        json = {
            "articles": dict_articles,
        }
        return JsonResponse(json)


    # post を追加
    def post(self, request):
        # リクエストボディに入っている JSON 形式の文字列を
        # list や dict に変換してくれる
        json_dict = json.loads(request.body)

        # 保存は今まで通り
        article = Article(
            title=json_dict["title"],
            body=json_dict["body"],
            # user には、現在ログイン中のユーザーをセットする
            user=request.user,
        )
        article.save()

        return JsonResponse({
            "message": "記事の投稿に成功しました"
        })


class CommentApiView(View):
    def post(self, request, article_id):
        json_dict = json.loads(request.body)

        # 渡された article_id から article を取得
        article = Article.objects.get(id=article_id)

        # article からコメントを作成して保存
        comment = Comment(
            body=json_dict["body"],
            article=article,
            user=request.user
        )
        comment.save()

        return JsonResponse({
            "message": "コメントの投稿に成功しました"
        })


class ArticleDetailView(View):

    def get(self, request, article_id):
        # article_id から記事の情報を取得する
        article = Article.objects.get(id=article_id)

        # dict 形式に変換したコメントが複数入っているリスト
        dict_comments = []

        # Comment クラスの方の related_name をつけると、その名前を使って、
        # Article クラスからコメント一覧が取得できるようになります
        # （ややこしいので気をつけてください）
        # コメント一覧を取得して、dict 形式に変換していきます
        for comment in article.comments.all():
            # dict 形式に変換
            dict_comment = {
                "id": comment.id,
                "body": comment.body,
                "user": {
                    "id": comment.user.id,
                    "username": comment.user.username,
                }
            }
            dict_comments.append(dict_comment)

        return JsonResponse({
            "article": {
                "id": article.id,
                "title": article.title,
                "user": {
                    "id": article.user.id,
                    "username": article.user.username,
                },
                # comments の部分にはさっき作成した dict のリストを入れます
                "comments": dict_comments,
            }
        })
