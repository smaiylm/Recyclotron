# -*- coding: utf-8 -*-
import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

#cwd = './data/train/'
cwd='./data/preprocess/'
classes = {'cans':0, 'kz':1, 'plastic':2,'carton':3}
#writer = tf.python_io.TFRecordWriter("bottle_train_refined.tfrecords")
writer= tf.python_io.TFRecordWriter("bottle_train_data.tfrecords")

count = 0
#for index, name in enumerate(classes):
for name in classes:
    class_path = cwd + name + '/'
    for img_name in os.listdir(class_path):
        img_path = class_path + img_name

        img = Image.open(img_path)
        img = img.resize((224, 224))
        size = (224,224,3)
        if np.shape(img) == size:
            count += 1
            print(np.shape(img))
            img_raw = img.tobytes()
            example = tf.train.Example(features=tf.train.Features(feature={
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[classes[name]])),
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }))
            writer.write(example.SerializeToString())

print(count)

writer.close()