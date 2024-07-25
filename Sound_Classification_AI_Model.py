# -*- coding: utf-8 -*-
"""[공모전] 선도전문대학 ICT솔루션_코딩결과물_음향분류모델.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-Vt9sBgUTuhru63aZQKnR6levxsGCArC

첫 번째 셀
"""

## 모듈을 불러오기 위해 필요한 librosa, resampy를 패키지를 설치
!pip install librosa
!pip install resampy

"""두 번째 셀"""

## 필요한 라이브러리와 모듈을 불러옵니다.
import re
import os
import glob
import pickle

import librosa
import librosa.display

import numpy as np
import pandas as pd

from scipy.io import wavfile as wav
from tqdm import tqdm
import matplotlib.pyplot as plt

import tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import soundfile as sf

import random
import itertools
import IPython.display as ipd
from keras.models import load_model

"""세 번째 셀"""

## 코랩에 오디오 데이터를 불러오기 위해 구글 드라이브와 연동합니다.
from google.colab import drive
drive.mount('/content/drive')

"""네 번째 셀"""

name = [] # 파일 이름 저장
fold_name = [] # 폴더 이름 저장
class_na = [] # 클래스 이름 저장

# 디렉토리 내 파일 검색 함수
def search(dirname):
  i = 0
  try:
    filenames = os.listdir(dirname)
    for filename in filenames:
      full_filename = os.path.join(dirname, filename)
      if os.path.isdir(full_filename):
        search(full_filename) ##  재귀 호출을 통해 서브 디렉토리 검색
      else:
      else:
        ext = os.path.splitext(full_filename)[-1]
        if ext == ".wav":  # WAV 확장자인 경우에만 처리
          print(full_filename)
          nfile = re.sub(r"_(\d+)_", "", filename)  # 파일 이름에서 숫자 및 밑줄 제거
          nfile = re.sub(r"label.wav", "", nfile) # 파일 이름에서 "label.wav" 부분 제거
          nfile = nfile
          print(nfile)
          name.append(filename) # 파일 이름 추가
          fold_name.append('음향') # 폴더 이름 추가
          class_na.append('환경소음') # 클래스 이름 추가
  except PermissionError:
    pass

# WAV 파일 검색을 시작할 디렉토리 지정
search("/content/drive/MyDrive/창의융합/창의융합공모전/DATASET/audiofile/음향")

print(name)
print(fold_name)
print(class_na)

# 파일 정보를 데이터프레임으로 저장
test_data = pd.DataFrame()
test_data['fold'] = fold_name
test_data['slice_file_name'] = name
test_data['class_name'] = class_na

# 인덱스를 1부터 시작하도록 조정
test_data.index = range(1, len(test_data)+1)
print(test_data)

# CSV 파일로 저장 (인코딩은 utf-8-sig로 지정하여 한국어 문자 처리)
test_data.to_csv("/content/drive/MyDrive/창의융합/창의융합공모전/csv파일/음향.csv", encoding='utf-8-sig', index=False)

"""다섯 번째 셀"""

## 합칠 csv 파일경로와 파일명 지정
input_path = r'/content/drive/MyDrive/창의융합/창의융합공모전/csv파일/최종통합/' #합칠 파일들이 들어있는 디렉토리 경로
output_path = r'/content/drive/MyDrive/창의융합/창의융합공모전/csv파일/최종통합/통합_확장.csv' #최종 파일명
file_list=glob.glob(input_path+'*.csv')
print(file_list)

"""여섯 번째 셀"""

## csv 파일 합치기
with open(output_path,'w') as f:
  for i, file in enumerate (file_list): #첫 번째 파일은 그대로 불러오기
    if i==0: #첫 번째 파일은 그대로 불러오기
      with open(file,'r') as f2:
        while True:
          line=f2.readline()
          if not line:
            break
          f.write(line)
      print(file.split('\\')[-1])

    else:
      with open(file,'r') as f2:
        n=0
        while True:
          line=f2.readline()
          if n!=0: #2번째 파일부터는 첫번째 줄(헤더)제외
            f.write(line)
          if not line:
            break
          n+=1
      print(file.split('\\')[-1])

"""일곱 번째 셀"""

import librosa
from scipy.io import wavfile as wav

import numpy as np

# 오디오 파일 경로 지정
filename = '/content/drive/MyDrive/창의융합/창의융합공모전/DATASET/audiofile/음향/음향_147.wav'

# Librosa를 사용하여 오디오 데이터 및 샘플레이트 불러오기
librosa_audio, librosa_sample_rate = librosa.load(filename)
# SciPy를 사용하여 오디오 데이터 및 샘플레이트 불러오기
scipy_sample_rate, scipy_audio = wav.read(filename)

# 원본 샘플 레이트 및 Librosa로 불러온 샘플 레이트 출력
print('Original sample rate:', scipy_sample_rate)
print('Librosa sample rate:', librosa_sample_rate)

# MFCC 특징 추출
mfccs = librosa.feature.mfcc(y = librosa_audio, sr = librosa_sample_rate, n_mfcc = 40)
# MFCC 배열의 크기 출력
print(mfccs.shape)

"""여덟 번째 셀"""

## 증강 코드 (데이터의 수를 증가시키기 위해 사용하는 코드)

def reverse_and_save_from_csv(input_csv, output_folder, base_path, folder_column, filename_column):
    # CSV 파일을 읽어와 폴더명과 파일명을 가져옵니다.
    df = pd.read_csv(input_csv)
    folder_names = df[folder_column].tolist()
    filenames = df[filename_column].tolist()

    for i, (folder_name, filename) in enumerate(zip(folder_names, filenames)):
        # 폴더 경로를 생성합니다.
        folder_path = os.path.join(base_path, folder_name)

        # 파일을 로드하고 샘플링 레이트(sr)를 설정합니다.
        file_path = os.path.join(folder_path, filename)
        data, sr = librosa.load(file_path, sr=None)

        # 거꾸로 재생
        reversed_data = np.array([data[len(data) - 1 - i] for i in range(len(data))])

        # 저장할 파일 경로를 생성합니다.
        output_filename = f'리버스_음향_{i+1}.wav'
        output_path = os.path.join(output_folder, output_filename)

        # 리버스된 오디오 데이터를 파일로 저장
        sf.write(output_path, reversed_data, sr)
        print(f'{output_path} 저장 성공')

"""아홉 번째 셀"""

import numpy as np
import librosa

# 최대 패딩 길이 설정
max_pad_len = 136
test_num = 0

def extract_features(file_name):
  # 오디오 파일 불러오기 및 샘플 레이트 설정
      audio, sample_rate = librosa.load(file_name, res_type = 'kaiser_fast')
      # MFCC(Mel-Frequency Cepstral Coefficients) 특징 추출
      mfccs = librosa.feature.mfcc(y=audio, sr = sample_rate, n_mfcc = 13)

      # 패딩 폭 계산
      pad_width = max_pad_len - mfccs.shape[1]
      if pad_width > 0:  # 패딩이 필요한 경우에만 수행
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
      else:  # pad_width가 음수인 경우에도 패딩 수행(길이 더 짧은 경우)
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, abs(pad_width))), mode='constant')

      # 최대 MFCC 배열 길이 업데이트
      global max
      if mfccs.shape[1] > max:
        max = mfccs.shape[1]


      return mfccs


# 최대 패딩 길이 및 MFCC 배열 길이 출력
print(max_pad_len)
print(mfccs.shape[1])

"""열 번째 셀"""

import pandas as pd
import os
import librosa
import resampy
import sys

print(sys.path)

# 최대 MFCC 배열 길이를 저장할 변수 초기화
max = 0
fulldatasetpath = '/content/drive/MyDrive/창의융합/창의융합공모전/DATASET/audiofile'
metadata = pd.read_csv("/content/drive/MyDrive/창의융합/창의융합공모전/csv파일/통합_확장.csv")    ## csv 파일 모두 합쳐진 csv 파일로 불러오기
features = []

# pandas 데이터 프레임 인덱스 재설정
metadata.reset_index(drop=True, inplace=True)
metadata.index = metadata.index + 1

max_length=0

for index, row in metadata.iterrows():
  # 오디오 파일 경로 생성
    file_name = os.path.join(os.path.abspath(fulldatasetpath),str(row["fold"])+'/',str(row["slice_file_name"]))
    class_label = row['class_name']
    data = extract_features(file_name)
    features.append([data, class_label])

    #현재 MFCC 배열의 길이 확인
    current_length = data.shape[1]
    #최대 길이보다 길다면 최대 길이 값을 업데이트
    if current_length > max_length:
      max_length = current_length


# 추출된 특징을 데이터프레임으로 저장
featuresdf = pd.DataFrame(features, columns = ['feature', 'class_label'], index=range(1, len(features) + 1))

# 특징 추출 완료 및 결과 출력
print("Finished feature extraction from ", len(featuresdf), ' files')
print('Max :',max)
print("가장 긴 MFCC 배열의 길이:", max_length)

"""열 한 번째 셀"""

# 피클로 데이터 저장
featuresdf.to_pickle("/content/drive/MyDrive/데이터셋/피클로/음향MFCC특징추출.pkl")

"""열 두 번째 셀"""

# 피클 데이터 로드
featuresdf = pd.read_pickle("/content/drive/MyDrive/데이터셋/피클로/음향MFCC특징추출.pkl")

"""열 세 번째 셀"""

featuresdf #

"""열 네 번째 셀"""

# 필요한 라이브러리를 불러옵니다
from sklearn.preprocessing import LabelEncoder  # 라벨 인코딩을 위한 라이브러리
from tensorflow.keras.utils import to_categorical  # 원-핫 인코딩을 위한 라이브러리

# 오디오 특징 데이터(featuresdf)에서 'feature' 열을 추출하여 NumPy 배열 x로 변환합니다
x = np.array(featuresdf.feature.tolist())

# 오디오 특징 데이터(featuresdf)에서 'class_label' 열을 추출하여 NumPy 배열 y로 변환합니다
y = np.array(featuresdf.class_label.tolist())

# LabelEncoder 객체를 생성하여 클래스 레이블(y)을 숫자로 인코딩합니다
le = LabelEncoder()
yy = to_categorical(le.fit_transform(y))

"""열 다섯 번째 셀"""

from sklearn.model_selection import train_test_split

# 머신 러닝 모델을 훈련하기 위해 데이터를 훈련 세트와 테스트 세트로 나눕니다.

# x는 오디오 특징 데이터, yy는 클래스 레이블 데이터입니다.

# train_test_split 함수를 사용하여 데이터를 무작위로 섞고, 지정한 비율(여기서는 0.2, 즉 20%)로 테스트 세트로 분할합니다.
# shuffle=True로 설정하면 데이터를 섞습니다.
x_train, x_test, y_train, y_test = train_test_split(x, yy, test_size = 0.2, shuffle=True)

"""열 여섯 번쨰 셀"""

# 오디오 데이터의 형태를 모델에 입력하기 위해 데이터를 재구성합니다.

# num_rows는 MFCC 특징의 행(높이) 수입니다.
# num_columns는 MFCC 특징의 열(너비) 수입니다.
# num_channels는 오디오 데이터의 채널 수입니다. 여기서는 흑백 오디오 데이터이므로 1로 설정됩니다.

# x_train과 x_test 데이터를 reshape 메서드를 사용하여 모델이 이해할 수 있는 형태로 변환합니다.
# 이렇게 해서 데이터의 모양은 (샘플 수, num_rows, num_columns, num_channels)가 됩니다.
num_rows = 13
num_columns = 136
num_channels = 1

print("train data shape")
print(x_train.shape)
print(x_test.shape)

x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)

print("\ntrain data reshape 결과")
print(x_train.shape)
print(x_test.shape)

"""열 일곱번째 셀"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from sklearn import metrics

# 모델의 레이블 수와 필터 크기를 설정합니다.
num_labels = yy.shape[1]
filter_size = 2

# Sequential 모델을 생성하여 CNN 모델을 구현합니다.
model = Sequential()
# 첫 번째 컨볼루션 레이어를 추가합니다.
model.add(Conv2D(filters = 16, kernel_size = 2, input_shape = (num_rows, num_columns, num_channels), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (1,2)))
model.add(Dropout(0.2))

# 두 번째 컨볼루션 레이어를 추가합니다.
model.add(Conv2D(filters = 32, kernel_size = 2, activation = 'relu'))
model.add(MaxPooling2D(pool_size = 2))
model.add(Dropout(0.2))

# 세 번째 컨볼루션 레이어를 추가합니다.
model.add(Conv2D(filters = 64, kernel_size = 2, activation = 'relu'))
model.add(MaxPooling2D(pool_size = 2))
model.add(Dropout(0.2))

# 네 번째 컨볼루션 레이어를 추가합니다.
model.add(Conv2D(filters = 128, kernel_size = 2, activation = 'relu'))
max_pool_layer = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='SAME')
model.add(Dropout(0.2))
# Global Average Pooling 레이어를 추가합니다.
model.add(GlobalAveragePooling2D())

# 출력 레이어를 추가합니다. 여기서는 다중 클래스 분류를 위해 softmax 활성화 함수를 사용합니다.
model.add(Dense(num_labels, activation = 'softmax'))


# 모델 컴파일 단계입니다. 손실 함수, 메트릭, 및 옵티마이저를 설정합니다.
model.compile(loss = 'categorical_crossentropy'
    , metrics = ['accuracy']
    , optimizer = 'adam')

# 모델의 구조를 요약하여 표시합니다.
model.summary()

"""열 여덟 번째 셀"""

# 모델을 훈련합니다.
hist = model.fit(x_train,
                    y_train,
                    epochs=100,
                    batch_size=500,
                    verbose=1,
                    validation_split=0.25)

"""열 아홉 번째 셀"""

# 모델 평가
loss_and_metrics = model.evaluate(x_test, y_test)
# 모델의 평가 결과인 손실(loss)과 정확도(accuracy)를 출력합니다.
print('loss_and_metrics : ' + str(loss_and_metrics))

"""스무 번째 셀"""

model.save('/content/drive/MyDrive/데이터셋/모델/기록/model.h5') # 모델 저장

"""스무 한 번째 셀"""

# 모델 훈련 중에 발생한 손실(train loss) 및 검증 손실(validation loss)을 에포크(epoch)별로 시각화하는 역할
fig, loss_ax = plt.subplots()

loss_ax.plot(hist.history['loss'], 'b', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label= 'test loss')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')

loss_ax.legend(loc = 'upper right')
plt.show()

"""스물 두 번째 셀"""

# 모델 훈련 중에 발생한 정확도(train accuracy) 및 검증 정확도(validation accuracy)를 에포크(epoch)별로 시각화
fig, loss_ax = plt.subplots()

loss_ax.plot(hist.history['accuracy'], 'b', label = 'train accuracy')
loss_ax.plot(hist.history['val_accuracy'], 'r', label = 'test accuracy')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('accuracy')

loss_ax.legend(loc='lower right')

plt.show()