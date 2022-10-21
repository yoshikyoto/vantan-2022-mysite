from django.urls import path
# blog ディレクトリの中の views.py を import
from blog import views

urlpatterns = [
    # views.py の index() 関数を呼び出す
    path('', views.index, name='index'),
    path('detail', views.detail, name='detail'),
    path("register", views.AccountCreateView.as_view(), name="register"),
]
