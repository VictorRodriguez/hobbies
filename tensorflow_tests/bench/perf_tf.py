

import tensorflow as tf

from tensorflow.keras.applications.resnet50 import ResNet50

from tensorflow.keras.preprocessing import image

from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

import numpy as np

import time



t_total = time.time()

#print("CREATE MODEL - BEGIN")

t_create_model = time.time()

model = ResNet50(weights='imagenet')

t_create_model = time.time()-t_create_model

#print("CREATE MODEL - END")

img_path = 'elephant.jpg'

t_load_img = time.time()

img = image.load_img(img_path, target_size=(224, 224))

t_load_img = time.time()-t_load_img

t_img_to_array = time.time()

x = image.img_to_array(img)

t_img_to_array = time.time()-t_img_to_array

t_expand_dims = time.time()

x = np.expand_dims(x, axis=0)

t_expand_dims = time.time()-t_expand_dims

t_preprocess = time.time()

x = preprocess_input(x)

t_preprocess = time.time()-t_preprocess

#print("PREDICTION - BEGIN")

t_predict = time.time()

preds = model.predict(x)

t_predict = time.time()-t_predict

#print("PREDICTION - END")

t_total = time.time()-t_total

print('Predicted:', decode_predictions(preds, top=3)[0])



print("result - t_create_model: " + str(round(t_create_model, 2)))

print("result - t_load_img: " + str(round(t_load_img, 2)))

print("result - t_img_to_array: " + str(round(t_img_to_array, 2)))

print("result - t_expand_dims: " + str(round(t_expand_dims, 2)))

print("result - t_preprocess: " + str(round(t_preprocess, 2)))

print("result - t_predict: " + str(round(t_predict, 2)))

print("result - t_total: " + str(round(t_total, 2)))
