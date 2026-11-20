from django.urls import path
#Djangoの道具箱から、path という道具を取り出す。path は、URL と処理する関数を結びつける道具。

from . import views #同じ prediction フォルダの中にある views.py という道具箱

urlpatterns = [
    path("", views.predict, name="predict"),  #http://127.0.0.1:8000/
]
#ブラウザからURLが来たら、このリストを上から順に見て、合うものを探す。[URLの形, 動かす関数, URLの名前]をセットで登録