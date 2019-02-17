from __future__ import absolute_import, division, print_function

import matplotlib.pylab as plt

import tensorflow as tf
from tensorflow.keras import layers
import tensorflow_hub as hub


image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(str("../DataSet/Images"))

for image_batch, label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Labe batch shape: ", label_batch.shape)
  break
