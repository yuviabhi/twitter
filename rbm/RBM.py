import numpy as np
import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
from sklearn.metrics import mean_squared_error
from math import sqrt

class RBM():
	def __init__(self, nv, nh, nt, ne = 10, bt = 5):
		self.num_timesteps = nt 
		self.n_visible = nv 
		self.n_hidden = nh 

		self.num_epochs = ne 
		self.batch_size = bt 
		self.lr = tf.constant(0.1, tf.float32) 
		
		### Variables:
		self.x  = tf.placeholder(tf.float32, [None, self.n_visible], name="x") #The placeholder variable that holds our data
		self.W  = tf.Variable(tf.random_normal([self.n_visible, self.n_hidden], 0.01), name="W") #The weight matrix that stores the edge weights
		self.bh = tf.Variable(tf.zeros([1, self.n_hidden], tf.float32, name="bh")) #The bias vector for the hidden layer
		self.bv = tf.Variable(tf.zeros([1, self.n_visible], tf.float32, name="bv")) #The bias vector for the visible layer
		
		### Training Update Code
		x_sample = self.gibbs_sample(1) 
	
		h = tf.sigmoid(tf.matmul(self.x, self.W) + self.bh) 		
		h_sample = tf.sigmoid(tf.matmul(x_sample, self.W) + self.bh) 
		
		self.final_prob = tf.sigmoid(tf.matmul(self.x, self.W) + self.bh)
		self.recons = tf.sigmoid(tf.matmul(self.final_prob, tf.transpose(self.W)) + self.bv)
				
		size_bt = tf.cast(tf.shape(self.x)[0], tf.float32)
		
		W_adder = tf.multiply(self.lr/size_bt, tf.subtract(tf.matmul(tf.transpose(self.x), h), tf.matmul(tf.transpose(x_sample), h_sample)))
		
		#Parameter Change
		#exp_1 = tf.multiply(self.lr/size_bt, tf.subtract(tf.matmul(tf.transpose(self.x), h), tf.matmul(tf.transpose(x_sample), h_sample))) 
		#exp_2 = tf.matmul( tf.subtract(tf.matmul(tf.matmul(tf.transpose(self.x),h),(tf.subtract(tf.eye(1,None,dtype=tf.float32),h))) , tf.matmul(tf.matmul(tf.transpose(x_sample),h_sample),(tf.subtract(tf.eye(1,None,dtype=tf.float32),h_sample)))) , self.W)		
		#W_adder = tf.add(exp_1 + exp_2)
		
		#Differentiation
		
		
		
		
		
		
		bv_adder = tf.multiply(self.lr/size_bt, tf.reduce_sum(tf.subtract(self.x, x_sample), 0, True))
		bh_adder = tf.multiply(self.lr/size_bt, tf.reduce_sum(tf.subtract(h, h_sample), 0, True))

		self.updt = [self.W.assign_add(W_adder), self.bv.assign_add(bv_adder), self.bh.assign_add(bh_adder)]
		
		self.sess = tf.Session()
		init = tf.global_variables_initializer()
		self.sess.run(init)
		#print self.sess.run(self.W)
		#print(self.x.get_shape()[0]*self.x.get_shape()[1])
		#print(self.x.get_shape())
		#print(tf.transpose(h).get_shape())
		
	#### Helper functions. 
	def sample(self,probs):    
		return tf.floor(probs + tf.random_uniform(tf.shape(probs), 0, 1))
		
	def gibbs_sample(self,k):
		def gibbs_step(count, k, xk):
			hk = tf.sigmoid(tf.matmul(xk, self.W) + self.bh)
			xk = tf.sigmoid(tf.matmul(hk, tf.transpose(self.W)) + self.bv)
			return count+1, k, xk
		ct = tf.constant(0)
		[_, _, x_sample] = control_flow_ops.while_loop(lambda count, num_iter, *args: count < num_iter,gibbs_step, [ct, tf.constant(k), self.x])
		x_sample = tf.stop_gradient(x_sample) 
		return x_sample

	def fit(self,trX):
		shp = trX.shape
		for epoch in range(self.num_epochs):			
			for i in range(1, shp[0],self.batch_size): 
				tr_x = trX[i:i+self.batch_size]
				self.sess.run(self.updt, feed_dict={self.x: tr_x})
			
			''' print 'Reconstruction error' '''
			tr_recons = self.reconstruct(trX) 
			print 'Epoch',epoch+1,'\t', 'RMSE: ',sqrt(mean_squared_error(trX, tr_recons)) 
			
			#Printing the weight matrix
			#print self.sess.run(self.W)

		#print self.sess.run(self.final_prob, feed_dict = {self.x:trX})
			
		return
	
	def predict(self,teX):
		return self.sess.run(self.final_prob, feed_dict = {self.x:teX})
	
	def reconstruct(self, tX):
		return self.sess.run(self.recons, feed_dict={self.x:tX})
		
if __name__=='__main__':
	#trX = np.array([[0.5,0.5],[0.3,0.3],[0.2,0.4],[0.2,0.45],[0.25,0.4],[0.1,0.2],[0.2,0.5],[0.622,0.41],[0.3,0.345],[0.88,0.43]])
	#trX = np.array([[0.1,0.1],[0.2,0.2],[0.3,0.3]])
	trX = np.array([[5.802174700791793089e-05, 6.556695615630705944e-05, 9.998764112968357987e-01],
				[6.320011630211281543e-05, 9.419148454066482727e-05, 9.998426083991571733e-01],
				[1.220023119219692533e-04, 1.499742009431645712e-04, 9.997280234871349647e-01]])	
	
	model = RBM(3, 1, 0.001, ne=10)
	model.fit(trX)
	
	#pred = model.predict(np.array([[5.802174700791793089e-05, 6.556695615630705944e-05, 9.998764112968357987e-01]]))
	tr_recons = model.reconstruct(trX) 
	#print trX
	#print tr_recons
	
	#print 'RMSE : ', sqrt(mean_squared_error(trX, tr_recons))
	#print pred

 
