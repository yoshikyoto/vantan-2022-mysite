from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User

 
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
