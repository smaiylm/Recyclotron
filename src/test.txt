#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import ReadMyOwnData
import mobilenet
import tnet
import os
import pre

classnum = 4

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

net = "mobilenet"

# size = 200
classes = {'cans':0, 'kz':1, 'plastic':2, 'carton':3}
classesname = { 0:'cans' , 1:'kz' , 2:'plastic' ,3:'carton'}
#classes = collections.OrderedDict()

def one_hot(labels,Label_class):
    one_hot_label = np.array([[int(i == int(labels[j])) for i in range(Label_class)] for j in range(1)])
    return one_hot_label

def classify():
    x = tf.placeholder(tf.float32, [ None,224, 224, 3])
    y_ = tf.placeholder(tf.float32,[ None,classnum])

    if net == "mobilenet":
        y_conv = mobilenet.mobilenet(x,classnum)
        path = "mobilenet/model/best/model.ckpt"

    else:
        y_conv = tnet.mobilenet(x,classnum)
        path = "model/best/model.ckpt"

    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    batch_idxs = pre.make_data()

    img, label = ReadMyOwnData.read_and_decode("bottle_test_temp.tfrecords")
    img_test, label_test = tf.train.batch( [img,label],
                                           batch_size=batch_idxs,
                                           num_threads=1,
                                           capacity=batch_idxs)

    #tf.initialize_local_variables()

    saver = tf.train.Saver()

    with tf.Session() as sess:

        saver.restore(sess,path)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        num = 0.0
        for j in range(1):

            val, l = sess.run([img_test, label_test])
           # print(val)
            tmp = l
            l = one_hot(l, classnum)
            l_ = tf.argmax(y_conv, 1)

            nn, result  = sess.run([l_, y_conv], feed_dict={x: val, y_: l})
            return result
            #print(result)

            for jj in range(batch_idxs):
                if nn[jj] == tmp[jj]:
                    num += 1
                print(" %s is predicted as %s " % (classesname[tmp[jj]], classesname[nn[jj]]))

        print("total accuracy: %.3f " % ( num/ float(batch_idxs) ))

        coord.request_stop()
        coord.join(threads)


