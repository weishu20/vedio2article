from utils.util import get_LAOGAO_text_box
import cv2
path = "/media/weishu/Elements/vedio2article/"
videocap = cv2.VideoCapture(path+"1麥田圈_10.mkv")
text_box = get_LAOGAO_text_box()
success, image = videocap.read()
if success:
    width = image.shape[1]
    height = image.shape[0]
    print(width, height)
cv2.namedWindow("test_", flags=cv2.WINDOW_NORMAL)
count = 0
while success:
    success, image = videocap.read()
    count += 1
    if count == 10:
        count = 0
        text_image = image[text_box[0]-4:text_box[1], text_box[2]:text_box[3]]
        cv2.imshow("test_", text_image)
    if cv2.waitKey(10) == 27:  # exit if Escape is hit
        break





