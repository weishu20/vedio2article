# @Time    : 2/18/19 2:42 PM
# @Author  : weishu
# @Company : 3-Reality
# @File    : insightFace.py
# @Software: PyCharm

import cv2
import os
import numpy as np
import mxnet as mx
import sklearn.preprocessing

class Insightface_API(object):
    def __init__(self, model_str, img_size = 112):
        ctx = mx.cpu()
        # ctx = mx.gpu(0)
        image_size = [img_size, img_size]
        _vec = model_str.split(',')
        layer = 'fc1'
        assert len(_vec) == 2
        prefix = _vec[0]
        epoch = int(_vec[1])
        print('loading', prefix, epoch)
        sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
        all_layers = sym.get_internals()
        sym = all_layers[layer + '_output']
        model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
        # model.bind(data_shapes=[('data', (args.batch_size, 3, image_size[0], image_size[1]))], label_shapes=[('softmax_label', (args.batch_size,))])
        model.bind(for_training=False, data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
        model.set_params(arg_params, aux_params)
        self.model = model

    def extract(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.transpose(img, (2, 0, 1))
        input_blob = np.expand_dims(img, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data,))
        self.model.forward(db, is_train=False)
        embedding = self.model.get_outputs()[0].asnumpy()
        embedding = sklearn.preprocessing.normalize(embedding).flatten()
        return embedding


if __name__ == '__main__':
    from utils.util import distance
    # extract_model_path = os.environ['HOME'] + "/models/insightface/model-r50-am-lfw/model, 0"
    # insightface_API = Insightface_API(extract_model_path)
    # img1 = cv2.imread(os.environ['HOME'] + "/A311D/insightface/test_112_cz_1.jpg")
    # imbeddings1 = insightface_API.extract(img1)
    # print(imbeddings1)
    #
    # img2 = cv2.imread(os.environ['HOME'] + "/A311D/insightface/test_112_cz_5.jpg")
    # imbeddings2 = insightface_API.extract(img2)
    # print(imbeddings2)
    #
    # print(distance([imbeddings1], [imbeddings2], 0))

    with open('/home/weishu/A311D/insightface/bin_r/output0_512_1_cz_1.txt', 'r') as f:
        imbeddings1_ = f.readlines()
        for i in range(0, len(imbeddings1_)):
            imbeddings1_[i] = float(imbeddings1_[i].rstrip('\n'))
        print(imbeddings1_)

    with open('/home/weishu/A311D/insightface/bin_r/output0_512_1_cz_5.txt', 'r') as f:
        imbeddings2_ = f.readlines()
        for i in range(0, len(imbeddings2_)):
            imbeddings2_[i] = float(imbeddings2_[i].rstrip('\n'))
        print(imbeddings2_)

    print(distance([imbeddings1_], [imbeddings2_], 0))

