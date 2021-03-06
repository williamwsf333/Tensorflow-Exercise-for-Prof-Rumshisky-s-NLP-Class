import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import time

# Define paramaters for the model
learning_rate = 0.01
batch_size = 128
n_epochs = 10

# Step 1: Read in data
# using TF Learn's built in function to load MNIST data to the folder data/mnist


#################### Your Code Starts Here ##########################



#################### Your Code Ends Here ##########################


# Step 2: create placeholders for features and labels
# each image in the MNIST data is of shape 28*28 = 784
# therefore, each image is represented with a 1x784 tensor
# there are 10 classes for each image, corresponding to digits 0 - 9. 

#################### Your Code Starts Here ##########################



#################### Your Code Ends Here ##########################

# Step 3: create weights and bias
# weights are initialized to be centred around zero 
# biases are initialized to 0
# shape of w depends on the dimension of X and Y so that Y = X * w + b
# shape of b depends on Y

#################### Your Code Starts Here ##########################



#################### Your Code Ends Here ##########################


# Step 4: build model
# the model that returns the logits.
# this logits will be later passed through softmax layer
# to get the probability distribution of possible label of the image
# DO NOT DO SOFTMAX HERE

#################### Your Code Starts Here ##########################



#################### Your Code Ends Here ##########################

# Step 5: define loss function
# use cross entropy loss of the real labels with the softmax of logits
# use the method:
# tf.nn.softmax_cross_entropy_with_logits(logits, Y)
# then use tf.reduce_mean to get the mean loss of the batch


#################### Your Code Starts Here ##########################



#################### Your Code Ends Here ##########################


# Step 6-a: define training op
# using gradient descent to minimize loss

#################### Your Code Starts Here ##########################


#################### Your Code Ends Here ##########################

with tf.Session() as sess:
	start_time = time.time()
	writer = tf.summary.FileWriter('./my_graph/logistic_regression', sess.graph)
	sess.run(tf.global_variables_initializer())	
	n_batches = int(mnist.train.num_examples/batch_size)
	for i in range(n_epochs): # train the model n_epochs times
		total_loss = 0

		for _ in range(n_batches):
			X_batch, Y_batch = mnist.train.next_batch(batch_size)

			# Step 6-b: run optimizer + fetch loss_batch
			#################### Your Code Starts Here ##########################

			
			#################### Your Code Ends Here ##########################

			total_loss += loss_batch
		print 'Average loss epoch {0}: {1}'.format(i, total_loss/n_batches)

	print 'Total time: {0} seconds'.format(time.time() - start_time)

	print('Optimization Finished!') # should be around 0.35 after 25 epochs
	w_values, b_values = sess.run([w, b])

	# test the model
	n_batches = int(mnist.test.num_examples/batch_size)
	total_correct_preds = 0
	for i in range(n_batches):
		X_batch, Y_batch = mnist.test.next_batch(batch_size)
		loss_batch, logits = sess.run([loss, logits_batch], feed_dict={input_per_batch: X_batch,
																						   label_per_batch:Y_batch})
		preds = tf.nn.softmax(logits)
		correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(Y_batch, 1))
		accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32)) 
		total_correct_preds += sess.run(accuracy)	
	
	print 'Accuracy {0}'.format(total_correct_preds/mnist.test.num_examples)
writer.close()