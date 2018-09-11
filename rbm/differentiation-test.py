import tensorflow as tf
import numpy as np
from math import pi
import matplotlib.pyplot as mp
import seaborn
seaborn.set()

x_ = np.linspace(0,10,100)

x = tf.placeholder(tf.float32)
y = tf.sigmoid(x)

with tf.Session() as session:
    feed_dict = {x:x_}
    y_  = session.run(y,feed_dict=feed_dict)
    out = session.run(tf.gradients(y,x),feed_dict=feed_dict)
    gradient = out[0]
    
mp.plot(x_,y_)
#mp.plot(x_,gradient)

mp.show()
