# -*- coding: utf-8 -*-
"""FaceMaskdetection

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JYthNzt2ti_yl60QzA-4l6HZG5kzkRHH
"""

#installing the kaggle library 
!pip install kaggle

#configuring the path of kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d omkargurav/face-mask-dataset

#unzipping the zip file
from zipfile import ZipFile

dataset = "/content/face-mask-dataset.zip"

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print("the ds is extracted")

!ls

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from google.colab.patches import cv2_imshow
from PIL import Image 
from sklearn.model_selection import train_test_split

with_mask_files = os.listdir('/content/data/with_mask')
without_mask_files = os.listdir('/content/data/without_mask')

print(with_mask_files[0:5])

print(without_mask_files[-5:])

print("Number of mask images: ", len(with_mask_files))

print("Number of non mask images: ", len(without_mask_files))

#with mask --> label 1
#without mask --> label 2

with_mask_labels = [1]*len(with_mask_files)
without_mask_labels = [0]*len(without_mask_files)

print(with_mask_labels[0:5])
print(without_mask_labels[0:5])

print(len(with_mask_labels))
print(len(without_mask_labels))

labels = with_mask_labels + without_mask_labels
print(len(labels))

#displaying with mask image
img= mpimg.imread('/content/data/with_mask/with_mask_279.jpg')
imgplot = plt.imshow(img)
plt.show()

#displaying with mask image
img= mpimg.imread('/content/data/without_mask/without_mask_3516.jpg')
imgplot = plt.imshow(img)
plt.show()

#image preprocessing 
#1. Resizing the image
#2. converting in numpy arrays

#for mask photos
with_mask_path = "/content/data/with_mask/"
data = []

for img_file in with_mask_files :

  image = Image.open(with_mask_path + img_file) #opening the image
  image = image.resize((128,128)) #resizing 
  image = image.convert('RGB') #converting to rgb
  image = np.array(image) #converting to np array
  data.append(image)

#for non mark photos

without_mask_path = '/content/data/without_mask/'


for img_file in without_mask_files:

  image = Image.open(without_mask_path + img_file)
  image = image.resize((128,128))
  image = image.convert('RGB')
  image = np.array(image)
  data.append(image)

len(data)

len(labels)

type(data[0])

data[0].shape #hieght, width, colorchannel

type(data)

# converting label list and image list to numpy arrays

x = np.array(data)
y = np.array(labels)

type(x)

print(x.shape)
print(y.shape)

#Train Test Split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=3)

print(x.shape, x_train.shape, x_test.shape)

#scaling the data : reducing the data range from 0-255 to 0-1

x_train_scaled = x_train/255
x_test_scaled = x_test/255

#Building a convolution neural networks

import tensorflow as tf   # developed by google, pytorch by youtube
from tensorflow import keras  #keras is a library, whose backend is tensorflow or pytorch

num_of_classes = 2

model = keras.Sequential()

model.add(keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(128,128,3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))


model.add(keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dropout(0.5))


model.add(keras.layers.Dense(num_of_classes, activation='sigmoid'))

# compile the neural network
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['acc'])

# training the neural network
history = model.fit(x_train_scaled, y_train, validation_split=0.1, epochs=5)

#model evaluation

loss, accuracy = model.evaluate(x_test_scaled, y_test)
print(accuracy)

h = history

# plot the loss value
plt.plot(h.history['loss'], label='train loss')
plt.plot(h.history['val_loss'], label='validation loss')
plt.legend()
plt.show()

# plot the accuracy value
plt.plot(h.history['acc'], label='train accuracy')
plt.plot(h.history['val_acc'], label='validation accuracy')
plt.legend()
plt.show()

# predictive system

input_image_path = input("enter path of input image")

input_image= cv2.imread(input_image_path)
cv_imshow(input_image)

input_image_resize = cv2.resize(input_image, (128,128))
input_image_scales = input_image_resize/255

input_image_reshaped = np.reshape(input_image_scales, [1,128,128,3])

input_prediction = model.predict(input_image_reshaped)

print(input_prediction)
input_pred_label = np.argmax(input_prediction)

print(input_pred_label)
if input_pred_label == 1:
  print('The person is wearing a mask, GOOD!')
else:
  print('The person is not wearing a mask, COVIDDDDD!')

# predictive system

input_image_path = input("enter path of input image")

input_image= cv2.imread(input_image_path)
cv_imshow(input_image)

input_image_resize = cv2.resize(input_image, (128,128))
input_image_scales = input_image_resize/255

input_image_reshaped = np.reshape(input_image_scales, [1,128,128,3])

input_prediction = model.predict(input_image_reshaped)

print(input_prediction)
input_pred_label = np.argmax(input_prediction)

print(input_pred_label)
if input_pred_label == 1:
  print('The person is wearing a mask, GOOD!')
else:
  print('The person is not wearing a mask, COVIDDDDD!')

