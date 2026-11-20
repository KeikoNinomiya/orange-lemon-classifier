"""
URL configuration for orangeorlemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#settings.py に書いた設定を、このファイルで使えるようにする
from django.conf import settings 
#アップロードした写真などのファイルを、ブラウザで見られるようにする道具
from django.conf.urls.static import static 

from django.contrib import admin #Djangoの管理画面（最初から入っている）
from django.urls import include, path #path はURLと関数をつなぐ道具。include は「この先はアプリの urls.pyにまかせる」道具


urlpatterns = [   #このサイトのURLの一覧表を作り始める
    
    path("admin/", admin.site.urls),  # 管理画面（最初からある）
    path("", include("prediction.urls")),  #サイトの入り口は、prediction アプリにまかせる
]

if settings.DEBUG:   #開発中（DEBUG = True）のときだけ、この設定を使う
    urlpatterns += static(   #URLの一覧表に、写真用のつなぎ方を足す
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT #/media/ で始まるURLに来たら、media フォルダの中を探す
        )