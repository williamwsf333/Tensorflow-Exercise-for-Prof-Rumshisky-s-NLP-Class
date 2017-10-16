from __future__ import print_function

import os
import time 

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

N_CLASSES = 10

# Step 1: Read in data
# using TF Learn's built in function to load MNIST data to the folder data/mnist

################## Your Code Starts Here #########################

mnist = input_data.read_data_sets("data/mnist", one_hot=True)

################## Your Code ends Here ##########################


# Step 2: Define parameters for the model
# Play with these parameters yourself!
LEARNING_RATE = 0.001
BATCH_SIZE = 128
SKIP_STEP = 10
DROPOUT = 0.75
N_EPOCHS = 10

# Step 3: create placeholders for features and labels
# each image in the MNIST data is of shape 28*28 = 784
# therefore, each image is represented with a 1x784 tensor
# We'll be doing dropout for hidden layer so we'll need a placeholder
# for the dropout probability too
# Use None for shape so we can change the batch_size once we've built the graph

################## Your Code Starts Here #########################

with tf.name_scope('data'):
    X = tf.placeholder(tf.float32, [None, 784], name="X_placeholder")
    Y = tf.placeholder(tf.float32, [None, 10], name="Y_placeholder")

dropout = tf.placeholder(tf.float32, name='dropout')

################## Your Code ends Here ##########################


# Step 4 + 5: create weights + do inference
# the model is conv -> relu -> pool -> conv -> relu -> pool -> fully connected -> softmax

global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name='global_step')

with tf.variable_scope('conv1') as scope:
    # first, reshape the image to [BATCH_SIZE, 28, 28, 1] to make it work with tf.nn.conv2d
    # use the dynamic dimension -1

    ################## Your Code Starts Here #########################

    X_reshaped= tf.reshape(X, shape=[-1, 28, 28, 1], name="data_reshaped")

    ################## Your Code ends Here ##########################

    # create weights for kernel variable of dimension [5, 5, 1, 32]
    # use tf.truncated_normal_initializer()

    ################## Your Code Starts Here ##########################

    conv1_weight = tf.Variable(tf.truncated_normal([5, 5, 1, 32],
                                                               stddev=1.0/(32**0.5)),
                               name="conv1_weight")

    ################## Your Code ends Here ##########################

    # create biases variable of dimension [32]
    # use tf.random_normal_initializer()

    ################## Your Code Starts Here #########################

    conv1_bias = tf.Variable(tf.random_normal([32]), name="conv1_weight")

    ################## Your Code ends Here ##########################


    # apply tf.nn.conv2d. strides [1, 1, 1, 1], padding is 'SAME'
    ################## Your Code Starts Here #########################

    conv1 = tf.nn.conv2d(X_reshaped, conv1_weight, strides=[1,1,1,1], padding='SAME')

    ################## Your Code ends Here ##########################


    # apply relu on the sum of convolution output and biases
    ################## Your Code Starts Here #########################

    relu1 = tf.nn.relu(conv1+conv1_bias, name=scope.name)
    
    ################## Your Code ends Here ##########################

    # output is of dimension BATCH_SIZE x 28 x 28 x 32

with tf.variable_scope('pool1') as scope:
    # apply max pool with ksize [1, 2, 2, 1], and strides [1, 2, 2, 1], padding 'SAME'
    ################## Your Code Starts Here #########################

    pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                            padding='SAME')
    ################## Your Code ends Here ##########################


    # output is of dimension BATCH_SIZE x 14 x 14 x 32

with tf.variable_scope('conv2') as scope:
    # similar to conv1, except kernel now is of the size 5 x 5 x 32 x 64

    ################## Your Code Starts Here #########################

    conv2_weights = tf.get_variable('kernels', [5, 5, 32, 64], 
                        initializer=tf.truncated_normal_initializer())
    biases = tf.get_variable('biases', [64],
                        initializer=tf.random_normal_initializer())
    conv = tf.nn.conv2d(pool1, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
    conv2 = tf.nn.relu(conv + biases, name=scope.name)

    ################## Your Code ends Here #########################


    # output is of dimension BATCH_SIZE x 14 x 14 x 64

with tf.variable_scope('pool2') as scope:
    # similar to pool1
    ################## Your Code Starts Here #########################

    pool2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                            padding='SAME')

    ################## Your Code ends Here #########################

    # output is of dimension BATCH_SIZE x 7 x 7 x 64

with tf.variable_scope('fc') as scope:
    # use weight of dimension 7 * 7 * 64 x 1024
    input_features = 7 * 7 * 64
    
    # create weights and biases
    ################## Your Code Starts Here #########################

    fc_weights = tf.Variable(tf.random_normal([input_features, 1024]), name='fc_weights')
    fc_bias = tf.Variable(tf.random_normal([1024]), name='fc_weights')

    ################## Your Code ends Here #########################

    # reshape pool2 to 2 dimensional
    pool2 = tf.reshape(pool2, [-1, input_features])

    # apply relu on matmul of pool2 and w + b
    ################## Your Code Starts Here #########################
    fc = tf.nn.relu(tf.matmul(pool2, fc_weights) + fc_bias)
    ################## Your Code ends Here #########################


    # apply dropout
    fc = tf.nn.dropout(fc, dropout, name='relu_dropout')

with tf.variable_scope('softmax_linear') as scope:
    # this you should know. get logits without softmax
    # you need to create weights and biases
    ################## Your Code Starts Here #########################
    final_weights = tf.Variable(tf.random_normal([1024, N_CLASSES]), name='final_weights')
    final_bias = tf.Variable(tf.random_normal([N_CLASSES]), name='final_bias')
    logits = tf.matmul(fc, final_weights) + final_bias
    ################## Your Code ends Here #########################

# Step 6: define loss function
# use softmax cross entropy with logits as the loss function
# compute mean cross entropy, softmax is applied internally
with tf.name_scope('loss'):
    ################## Your Code Starts Here #########################
    entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y)
    loss = tf.reduce_mean(entropy)
    ################## Your Code ends Here #########################


# Step 7: define training op
# using gradient descent with learning rate of LEARNING_RATE to minimize cost
# don't forgot to pass in global_step
################## Your Code Starts Here #########################

global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name='global_step')
optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE ).minimize(loss=loss, global_step=global_step)

################## Your Code ends Here #########################

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    # to visualize using TensorBoard
    writer = tf.summary.FileWriter('./conv_graph/mnist', sess.graph)
    ##### You have to create folders to store checkpoints
    ckpt = tf.train.get_checkpoint_state(os.path.dirname('./conv_graph/checkpoints'))
    # if that checkpoint exists, restore from checkpoint
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    
    initial_step = global_step.eval()

    start_time = time.time()
    n_batches = int(mnist.train.num_examples / BATCH_SIZE)

    total_loss = 0.0
    for index in range(initial_step, n_batches * N_EPOCHS): # train the model n_epochs times
        X_batch, Y_batch = mnist.train.next_batch(BATCH_SIZE)
        _, loss_batch = sess.run([optimizer, loss], 
                                feed_dict={X: X_batch, Y:Y_batch, dropout: DROPOUT}) 
        total_loss += loss_batch
        if (index + 1) % SKIP_STEP == 0:
            print('Average loss at step {}: {:5.1f}'.format(index + 1, total_loss / SKIP_STEP))
            total_loss = 0.0
            saver.save(sess, './conv_graph/checkpoints', index)
    
    print("Optimization Finished!") # should be around 0.35 after 25 epochs
    print("Total time: {0} seconds".format(time.time() - start_time))


    # test the model
    n_batches = int(mnist.test.num_examples/BATCH_SIZE)
    total_correct_preds = 0
    for i in range(n_batches):
        X_batch, Y_batch = mnist.test.next_batch(BATCH_SIZE)
        #_, loss_batch, logits_batch = sess.run([optimizer, loss, logits],
        #                                feed_dict={X: X_batch, Y:Y_batch, dropout: DROPOUT})
        loss_batch, logits_batch = sess.run([loss, logits],
                                        feed_dict={X: X_batch, Y:Y_batch, dropout: DROPOUT})
        preds = tf.nn.softmax(logits_batch)
        correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(Y_batch, 1))
        accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32))
        total_correct_preds += sess.run(accuracy)   
    
    print("Accuracy {0}".format(total_correct_preds/mnist.test.num_examples))