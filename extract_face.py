import os
import cv2
import time
from datetime import datetime
from api.align import Align_API

align_API = Align_API()

path = "/home/weishu/disk/Pic/vedio2article/"
for img_file in os.listdir(path):
    if img_file.endswith(".jpg"):
        image = cv2.imread(path+img_file)

        faces, bounding_boxes, points = align_API.detect(image, minsize=60, multiple_faces=True,
                                                             if_add_margin=True)
        for face in faces:
            tic = time.time()
            IMG_ID = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S%f')
            cv2.imwrite("images/face/{}.jpg".format(IMG_ID), face)