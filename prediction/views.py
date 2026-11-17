# 1 最初の部分：使う道具を import する

import os  #os モジュールを使うために import する
import numpy as np  #写真を、モデルに入れる形にする
from django.conf import settings  #プロジェクトの場所（BASE_DIR）を使う
from django.core.files.storage import FileSystemStorage  #アップロードされた写真を保存する
from django.shortcuts import render  #結果を home.html に渡して表示する
import tensorflow as tf #モデルを読み込む
from tensorflow.keras.applications.vgg16 import preprocess_input  #VGG16用の前処理
from tensorflow.keras.preprocessing import image  #写真を読み込んで、100×100にする
from .forms import ImageUploadForm 


# 2 モデルの読み込み：サーバーが起動したときに、1回だけモデルを読み込む

# モデルのファイルの場所を組み立てる
# 学習済みモデル（model_100.h5）の場所
MODEL_PATH = os.path.join(
    settings.BASE_DIR, "prediction", "models", "model_100.h5"
)

#学習用の設定は読み込まない
model = tf.keras.models.load_model(MODEL_PATH, compile=False)  # モデルの読み込み


# 3 predict 関数：写真を受け取って、判定して、結果を画面に渡す



