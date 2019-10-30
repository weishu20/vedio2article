# @Time    : 9/27/18 11:07 AM
# @Author  : weishu
# @File    : util.py
# @Software: PyCharm
import numpy as np
import base64
import cv2
import math
import time
from datetime import datetime

def cvimage_to_base64(img):
    img_b = np.array(cv2.imencode(".jpg", img)[1]).tostring()
    img_b = base64.b64encode(img_b)
    img_b = img_b.decode("utf-8")
    return img_b

def base64_to_cvimage(image_string):
    img_bytes = bytearray(base64.b64decode(image_string))
    image_array = np.asarray(img_bytes, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return img

def distance(embeddings1, embeddings2, distance_metric=0):
    if distance_metric == 0:
        # Euclidian distance
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sum(np.square(diff), 1)
        # dist = np.sqrt(dist)
        # dist = np.linalg.norm(embeddings1 - embeddings2, ord=2)
    elif distance_metric == 1:
        # Distance based on cosine similarity
        dot = np.sum(np.multiply(embeddings1, embeddings2), axis=1)
        norm = np.linalg.norm(embeddings1, axis=1) * np.linalg.norm(embeddings2, axis=1)
        dist = dot / norm
        dist = np.arccos(dist) / math.pi
    else:
        raise 'Undefined distance metric %d' % distance_metric

    return dist

def getDistance_metric_insightface():
    return 0

def get_LAOGAO_text_box():
    return [935, 1020, 130, 1800]


def save_img(out_path, image):
    tic = time.time()
    IMG_ID = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S%f')
    cv2.imwrite(out_path + "{}.png".format(IMG_ID), image)