from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article

 
def index(request):
    # blog_article テーブルの中身を全部取得
    # articles は Article クラスのオブジェクトが入った配列
    articles = Article.objects.all()
    return render(request, "blog/index.html", {
        "articles": articles,
    })

def detail(request):
    return HttpResponse("detail page")


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
# まだログイン制限などは入れていない
class MypageView(LoginRequiredMixin, View):
    login_url = '/blog/login'

    def get(self, request):
        return render(request, "blog/mypage.html")


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