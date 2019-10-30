# @Time    : 4/17/19 3:43 PM
# @Author  : weishu
# @Company : 3-Reality
# @File    : convert2pb.py
# @Software: PyCharm
import tensorflow as tf
import os
from tensorflow.python.tools.freeze_graph import freeze_graph
from utils.align.detect_face import PNet, ONet, RNet


# init_op = tf.initialize_all_variables()
# sess = tf.Session()
# sess.run(init_op)
# init_g = tf.global_variables_initializer()
# init_l = tf.local_variables_initializer()
# with tf.Session() as sess:
#     data = tf.placeholder(tf.float32, (None, None, None, 3), 'input')
#     pnet = PNet({'data': data})
#     output_graph = sess._graph
#     pnet.load('det1.npy', sess)
#     sess.run(init_g)
#     sess.run(init_l)
#     f = tf.gfile.FastGFile('det1.pb', "w")
#     f.write(output_graph.as_graph_def().SerializeToString())
#     f.close()

# data = tf.placeholder(tf.float32, (None,24,24,3), 'input')
# rnet = RNet({'data':data})
# output_graph = sess._graph
# rnet.load('det2.npy', sess)
# f = tf.gfile.FastGFile('det2.pb', "w")
# f.write(output_graph.as_graph_def().SerializeToString())
# f.close()

# data = tf.placeholder(tf.float32, (None,48,48,3), 'input')
# onet = ONet({'data':data})
# output_graph = sess._graph
# onet.load('det3.npy', sess)
# f = tf.gfile.FastGFile('det3.pb', "w")
# f.write(output_graph.as_graph_def().SerializeToString())
# f.close()



data = tf.placeholder(tf.float32, (None, None, None, 3), 'input')
pnet = PNet({'data': data})
sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())
pnet.load('det1.npy', sess)
saver = tf.train.Saver()
saver.save(sess, 'chkpt', global_step=0, latest_filename='chkpt_state')
tf.train.write_graph(sess.graph.as_graph_def(), './det1', 'det1_init.pb', False)

input_saver_def_path = ''
input_binary=True
input_checkpoint_path = 'chkpt-0'
input_graph_path = './det1/det1_init.pb'
output_graph_path = './det1/det1.pb'
output_node_names = 'prob1, conv4-2/BiasAdd'
restore_op_name = "save/restore_all"
filename_tensor_name = "save/Const:0"
clear_devices = True

freeze_graph(input_graph_path, input_saver_def_path,
                              input_binary, input_checkpoint_path,
                              output_node_names, restore_op_name,
                              filename_tensor_name, output_graph_path,
                              clear_devices, "")



