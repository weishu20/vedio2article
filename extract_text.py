from utils.util import get_LAOGAO_text_box
from api.ocr import ocr_youdao
from api.align import Align_API
import cv2
import numpy as np
import imageio
import os
from utils.util import distance, getDistance_metric_insightface, save_img
from api.insightFace import Insightface_API
distance_metric = getDistance_metric_insightface()
data_dir = "images/face/"
extract_model_path = '/home/weishu/disk' + "/models/insightface/model-r50-am-lfw/model, 0"
insightface_API = Insightface_API(extract_model_path)
threshold_extract = 1.3

def cal_vector(path):
    dirs = os.listdir(path)
    vectors = []
    names = []
    for dir in dirs:
        files = os.listdir(path+dir)
        for file in files:
            img = cv2.imread(path + dir + "/" + file)
            img = cv2.resize(img, (112, 112))
            temp = insightface_API.extract(img)
            vectors.append(np.asarray([temp]))
            names.append(dir)
    return vectors, names

def match(face):
    # tic = time.time()
    dis_map = {}
    face = cv2.resize(face, (112, 112))
    vector = insightface_API.extract(face)
    i = 0
    for v in vectors:
        if names[i] in dis_map.keys():
            dis_map[names[i]].append(distance(v, vector, distance_metric)[0])
        else:
            dis_map[names[i]] = [distance(v, vector, distance_metric)[0]]
        i += 1
    for key in dis_map.keys():
        dis_map[key] = np.mean(sorted(dis_map[key])[:3])
    top3 = sorted(dis_map.items(), key=lambda item: item[1])[:3]
    result = {"top3": top3, "prob":top3[0][1]}
    result["name"] = "陌生人"
    if top3[0][1] < threshold_extract:
        result["name"] = top3[0][0]
    print("match result:", result)
    # toc = time.time()
    # print("match time:{}".format(toc - tic))
    return result

vectors, names = cal_vector(data_dir)

# ffmpeg -i 1麥田圈.mkv -r 10 1麥田圈_10.mkv
path = "/media/weishu/Elements/vedio2article/"
vedio = "2南極和北極地球上最不可思議的兩個地方_10"
out_path = path+"{}/".format(vedio)
out_temp_path = path+"{}/temp/".format(vedio)
os.system("mkdir -p {}".format(out_path))
os.system("mkdir -p {}".format(out_temp_path))
f2 = open(out_path + 'text.txt', 'wb')
f2.close()
videocap = cv2.VideoCapture(path+"{}.mkv".format(vedio))
text_box = get_LAOGAO_text_box()
success, image = videocap.read()
if success:
    width = image.shape[1]
    height = image.shape[0]
    print(width, height)
cv2.namedWindow("test", flags=cv2.WINDOW_NORMAL)
count = 0
before_text = ""
align_API = Align_API()
i = 1
os.system("mkdir {}".format(out_temp_path+str(i)+"/"))
while success:
    success, image = videocap.read()
    count += 1
    if count == 5:
        count = 0
        text_image = image[text_box[0]-13:text_box[1]-10, text_box[2]:text_box[3]]
        cv2.imshow("test", text_image)
        text, regions = ocr_youdao(text_image)
        text = text.strip()
        if text != before_text:
            before_text = text
            print(text)
            file_object = open(out_path + 'text.txt', 'a+')
            file_object.write(str(text) + "\n")
            file_object.close()
    faces, bounding_boxes, points = align_API.detect(image, minsize=60, multiple_faces=True,
                                                     if_add_margin=True)
    if cv2.waitKey(10) == 27:  # exit if Escape is hit
        break

    result_name_list = []
    if len(faces) != 0:
        for face in faces:
            result_m = match(face)
            result_name_list.append(result_m["name"])
    if result_name_list.__contains__("1") or result_name_list.__contains__("2"):
        images = []
        if len(os.listdir(out_temp_path + str(i) + "/")) > 0:
            if len(os.listdir(out_temp_path + str(i) + "/")) > 4:
                for file_path in sorted(os.listdir(out_temp_path + str(i) + "/"))[
                                 2:len(os.listdir(out_temp_path + str(i) + "/")) - 2]:
                    images.append(imageio.imread(out_temp_path + str(i) + "/" + file_path))
                imageio.mimsave(out_path + "{}.gif".format(str(i) + "_" + before_text[:5]), images, 'GIF', duration=0.1)
            i += 1
            os.system("mkdir {}".format(out_temp_path + str(i) + "/"))
        continue

    print("save!!!")

    # cut = (height-text_box[0])/2/height*width
    # cut_img = image[0:text_box[0], cut, width-cut]
    # cv2.imshow("test1", cut_img)
    save_img(out_temp_path+str(i)+"/", image[0:text_box[0]-13])






