
import cv2
path = "/home/weishu/disk/Pic/vedio2article/"
width = 3264
height = 2448
videocap = cv2.VideoCapture(path+"1麥田圈.mkv")
# videocap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# videocap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
success, image = videocap.read()
if success:
    width = image.shape[1]
    height = image.shape[0]
    print(width, height)
# cv2.namedWindow("test_vedio", flags=cv2.WINDOW_NORMAL)
count = 0
i = 0
while success:
    success, image = videocap.read()
    count += 1
    i += 1
    if count == 10:
        count = 0
        cv2.imwrite(path+"1_{}.jpg".format(i), image)



