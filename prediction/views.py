# 1 最初の部分：使う道具を import する

import os  #os モジュールを使うために import する
import numpy as np  #写真を、モデルに入れる形にする
from django.conf import settings  #プロジェクトの場所（BASE_DIR）を使う
from django.core.files.storage import FileSystemStorage  #アップロードされた写真を保存する
from django.shortcuts import render  #結果を home.html に渡して表示する


import tensorflow as tf #モデルを読み込む
from tensorflow.keras import layers, models  #層の部品と、層を積み重ねる箱（build_model で使う）
from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16  #VGG16用の前処理と、VGG16の形
from tensorflow.keras.preprocessing import image  #写真を読み込んで、256×256にする
from .forms import ImageUploadForm 


# 2 モデルの読み込み：サーバーが起動したときに、1回だけモデルを読み込む

# モデルのファイルの場所を組み立てる
# 学習済みモデル（model_256.h5）の場所
MODEL_PATH = os.path.join(
    settings.BASE_DIR, "prediction", "models", "model_256.h5"
)

def build_model():
    # Colabで学習したモデルと同じ形を組み立てる（VGG16 ＋ 独自の層）
    vgg16 = VGG16(
        weights=None,   #重み（学習した数字）は空っぽのまま。あとでファイルから読み込むので、ダウンロードしない
        include_top=False,  #1000種類を見分ける最後の部分は外す（Colabと同じ）
        input_shape=(256, 256, 3)) #入力は256×256ピクセル、カラー（赤・緑・青の3つ）
    
    
    # 層を積み重ねる空の箱を作り、VGG16の層を入れる
    model = models.Sequential()
    for layer in vgg16.layers:
        model.add(layer)

    # 新しいトップ層を追加
    model.add(layers.GlobalAveragePooling2D()) #VGG16が見つけた特徴を、平均してまとめる
    model.add(layers.Dense(256, activation="relu")) #256個の部品で考える層
    model.add(layers.Dropout(0.5)) #学習中に半分を休ませる層
    model.add(layers.Dense(2, activation="softmax"))  # 2クラス分類（レモンとオレンジ）

    return model #組み立てたモデルを、関数の外に返す

# まず普通に読み込み、ダメなら形を組み立てて重みだけ読み込む
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)  # モデルの読み込み
except Exception as e:
    # 読み込めないときは、同じ形のモデルを組み立てて、重みだけ読み込む
    model = build_model()  # モデルの形を組み立てる
    model.load_weights(MODEL_PATH)  #学習済みの重みを読み込む 



# 3 predict 関数：写真を受け取って、判定して、結果を画面に渡す

def predict(request):

    #(1)フォーム送信（POST）の受け取りと画像の保存
    if request.method == "POST": #画面の判定ボタンが押されてデータが送信されたときの処理
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():  #正しい形式かチェック
            uploaded_file = request.FILES["image"] #送信された画像ファイルを取り出す

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file) #受け取った画像をサーバーの media フォルダに保存
            file_url = fs.url(filename) #アップロードされた画像の URL を作る

            #(2)AIモデル（VGG16）が読める形に画像を加工（前処理）
            img_path = os.path.join(settings.MEDIA_ROOT, filename) #保存した画像の場所を組み立てる
            img = image.load_img(img_path, target_size=(256, 256)) #256×256にリサイズして読み込む
            x = image.img_to_array(img) # 配列に変換
            x = np.expand_dims(x, axis=0) #バッチ次元を追加
            x = preprocess_input(x)  # VGG16用の前処理

            #(3)AIモデルによる予測と結果の変換
            preds = model.predict(x) #加工した画像データをAIモデルに渡し、予測結果を受け取る
            class_index = np.argmax(preds[0])  # 最も確率の高いクラスのインデックスを取得
            # クラス名（学習時の順番：0 = lemon、1 = orange）
            class_names = ["lemon", "orange"]
            predicted_class = class_names[class_index] #数字の0や1を、"orange" や "lemon" に変換


            #(4)結果を home.html に渡して表示
            return render(
                request,
                "home.html",
                {
                    "form": form,
                    "file_url": file_url,
                    "predicted_class": predicted_class,
                },
            )
    else:
        form = ImageUploadForm()
    return render(request, "home.html", {"form": form})

