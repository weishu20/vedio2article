# @Time    : 7/19/18 2:48 PM
# @Author  : weishu
# @Company : 3-Reality
# @File    : align.py
# @Software: PyCharm
import tensorflow as tf
from utils.align.detect_face import create_mtcnn, API_3R_detect

class Align_API(object):
    def __init__(self):
        # Root directory of the project
        self.graph = tf.Graph()
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
        self.sess = tf.Session(graph=self.graph, config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with self.sess.as_default():
            with self.graph.as_default():
                self.pnet, self.rnet, self.onet = create_mtcnn(self.sess, None)

    def detect(self, img, minsize=20, multiple_faces=True, if_align=True, if_add_margin=False):
        faces, bounding_boxes, points = API_3R_detect(img, self.pnet, self.rnet, self.onet, minsize=minsize,
                                                      multiple_faces=multiple_faces, if_align=if_align,
                                                      if_add_margin=if_add_margin)
        return faces, bounding_boxes, points