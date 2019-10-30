# @Time    : 4/10/19 3:39 PM
# @Author  : weishu
# @Company : 3-Reality
# @File    : convert2onnx.py
# @Software: PyCharm

def mxnet2onnx():
    import numpy as np
    import onnx
    import mxnet as mx
    import os
    from mxnet.contrib import onnx as onnx_mxnet
    insightface_model_path = os.environ['HOME'] + "/models/insightface/"
    converted_onnx_filename = insightface_model_path + 'onnx/insightface.onnx'
    # Export MXNet model to ONNX format via MXNet's export_model API
    converted_onnx_filename = onnx_mxnet.export_model(insightface_model_path+'model-r50-am-lfw/model-symbol.json',
                                                    insightface_model_path+'model-r50-am-lfw/model-0000.params',
                                                    [(1, 3, 112, 112)], np.float32, converted_onnx_filename)

    # Check that the newly created model is valid and meets ONNX specification.

    model_proto = onnx.load(converted_onnx_filename)
    onnx.checker.check_model(model_proto)
