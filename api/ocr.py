# @Time    : 10/8/18 1:21 PM
# @Author  : weishu
# @Company : 3-Reality
# @File    : ocr.py
# @Software: PyCharm
import pytesseract
import random
import json
import hashlib
import urllib
import urllib.request
import urllib.parse
import cv2
from utils.util import cvimage_to_base64

def ocr(image):
    if image is not None:
        # config = ('-l eng --oem 1 --psm 3')
        config = ('-l chi_sim --oem 1 --psm 3')
        text = pytesseract.image_to_string(image, config=config)
        return text
    return ""

def ocr_youdao(image, langType="zh-en"):
    url = "https://openapi.youdao.com/ocrapi"
    appKey = "322c030a1a727104"
    secretKey = "TYtutFDMKfNayNt8jSVsiHUMQtBLTuum"
    salt = random.randint(1, 65536)
    detectType = '10012' #10011
    imageType = '1'
    if image is not None:
        image_base64 = cvimage_to_base64(image)
        sign = appKey + image_base64 + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode("utf-8"))
        sign = m1.hexdigest()
        data = {'appKey': appKey, 'img': image_base64, 'detectType': detectType,
                'imageType': imageType, 'langType': langType, 'salt': str(salt), 'sign': sign}
        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(url, data)
        response = urllib.request.urlopen(request)

        req_json = json.loads(response.read().decode())
        if req_json['errorCode']=='0':
            regions = req_json["Result"]["regions"]
            text = ''
            for region in regions:
                lines = region["lines"]
                for line in lines:
                    text += line["text"]
                    text += "\n"
            return text, regions
    return "", ""

if __name__ == '__main__':
    img = cv2.imread("/home/reality/Pic/show/output/document_20181115104749931656.jpg")
    # print(ocr(img))
    text, regions = ocr_youdao(img)
    print(text)
    print(regions)