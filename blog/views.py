from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

 
def index(request):
    return render(request, "blog/index.html")

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
