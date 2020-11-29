#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import tensorflow as tf 
import numpy as np
import ReadMyOwnData
import tnet
import mobilenet
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

epoch = 100
batch_size = 100

classnum = 4

def one_hot(labels,Label_class):
    one_hot_label = np.array([[int(i == int(labels[j])) for i in range(Label_class)] for j in range(len(labels))])
    return one_hot_label

x = tf.placeholder(tf.float32, [None,224,224,3],name='x') # / 255.0
y_ = tf.placeholder(tf.float32, [None,classnum],name='y_')

y_conv  = tnet.mobilenet(x,classnum) #tnet.mobilenet(x)

tf.add_to_collection('./model/network-output', y_conv)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)), reduction_indices=[1]))
#cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)))
#train_step = tf.train.AdamOptimizer(0.00005).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


img_test, label_test = ReadMyOwnData.read_and_decode("bottle_test_data.tfrecords")
img, label = ReadMyOwnData.read_and_decode("bottle_train_data.tfrecords")

img_test, label_test = tf.train.batch( [img_test,label_test],
                                       batch_size=batch_size,
                                       num_threads=1,
                                       capacity=32)

# img_test, label_test = tf.train.input_producer( [img_test,label_test],
#                                                 num_epochs=1,
#                                                 shuffle=False,
#                                                 capacity=32)


img_batch, label_batch = tf.train.shuffle_batch( [img, label],
                                                batch_size=batch_size, capacity=2*batch_size+20,
                                                min_after_dequeue=20,
                                                num_threads=1)

global_ = tf.Variable(0, name='global_', trainable=False)
lr = tf.train.exponential_decay(0.0008, global_step=global_, decay_steps=1, decay_rate=0.9)
train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

init = tf.initialize_all_variables()

t_vars = tf.trainable_variables()
#print(t_vars)

saver = tf.train.Saver(max_to_keep=1000+2)

recorder = 0
best_epoch_index = 0

with tf.Session() as sess:

    sess.run(init)
    coord = tf.train.Coordinator() 
    threads=tf.train.start_queue_runners(sess=sess,coord=coord) 
    batch_idxs = int(910/batch_size)

    for i in range(epoch):

        acc_all = 0
        cro_all = 0

        for j in range(batch_idxs):
            val, l = sess.run([img_batch, label_batch])

            l = one_hot(l,classnum)
            _, cro, acc,step = sess.run([train_step, cross_entropy , accuracy ,global_], feed_dict={x: val, y_: l})

            #if j % 1 == 0:
            #   print("Epoch:[%4d/%4d] [%4d/%4d], cross_entropy:[%.6f], accuracy:[%.3f]" % (i+1,epoch, j+1, batch_idxs, cro,acc) )
            acc_all += acc
            cro_all += cro

        print("train:  Epoch:[%4d/%4d] , cross_entropy:[%.6f], accuracy:[%.3f]" % (i + 1, epoch, cro_all/batch_idxs, acc_all/batch_idxs))
    
        val, l = sess.run([img_test, label_test])
        tmp = l
        l = one_hot(l, classnum)
        l_ = tf.argmax(y_conv,1)
        nn, y, acc = sess.run([l_, y_conv, accuracy], feed_dict={x: val, y_: l})

        #print(y)

        #print(nn,'\n',tmp)
        
        num = 0.0
        for iy in range(nn.size):
            if nn[iy] == tmp[iy]:
                num += 1
                
        ac = num / float(nn.size)

        # if i == 1:
        #     with tf.variable_scope("", reuse=True):
        #         v5 = tf.get_variable("MobileNet/conv_ds_2/depthwise_conv/depthwise_weights")
        #         print(sess.run(v5))
        
        
        if ac > recorder:
            saver.save(sess, "model/best/model.ckpt")#, global_step=5)
            recorder = ac
            best_epoch_index = i

        saver.save(sess, "model/latest/model.ckpt")

        saver.save(sess, "model/every/"+str(i)+"/model.ckpt")

        print("test accuracy: %.4f, best accuracy: [%.4f] with epoch index is %3d" % (ac, recorder, best_epoch_index))
        print('\n')


    coord.request_stop()
    coord.join(threads)
