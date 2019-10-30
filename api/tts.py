# @Time    : 3/15/19 10:41 AM
# @Author  : weishu
# @Company : 3-Reality
# @File    : tts.py
# @Software: PyCharm

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import json
import re
import playsound

class TTS_API(object):
    def __init__(self):
        API_KEY = 'cx48llpjQ1LpRh4BG6va8RFs'
        SECRET_KEY = '7685986dfe3f3e2c685828c329a214c6'

        # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        self.PER = 1
        # 语速，取值0-15，默认为5中语速
        self.SPD = 5
        # 音调，取值0-15，默认为5中语调
        self.PIT = 5
        # 音量，取值0-9，默认为5中音量
        self.VOL = 5
        # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        self.AUE = 3

        self.FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
        self.FORMAT = self.FORMATS[self.AUE]

        self.CUID = "123456PYTHON"

        self.TTS_URL = 'http://tsn.baidu.com/text2audio'
        self.TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
        self.SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选
        # print("fetch token begin")
        self.params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        post_data = urlencode(self.params)
        self.post_data = post_data.encode('utf-8')
        req = Request(self.TOKEN_URL, self.post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            # print('token http response http code : ' + str(err.code))
            result_str = err.read()
        result_str = result_str.decode()

        # print(result_str)
        result = json.loads(result_str)
        # print(result)
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not self.SCOPE in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
            self.token = result['access_token']
        else:
            raise DemoError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    def play_one_voice(self, text):
        tex = quote_plus(text)  # 此处TEXT需要两次urlencode
        params = {'tok': self.token, 'tex': tex, 'per': self.PER, 'spd': self.SPD, 'pit': self.PIT, 'vol': self.VOL, 'aue': self.AUE, 'cuid': self.CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)
        # print('test on Web Browser' + self.TTS_URL + '?' + data)

        req = Request(self.TTS_URL, data.encode('utf-8'))

        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            has_error = ('Content-Type' not in f.headers.keys() or f.headers['Content-Type'].find('audio/') < 0)
        except URLError as err:
            print('asr http response http code : ' + str(err.errno))
            result_str = err.strerror
            has_error = True

        save_file = "error.txt" if has_error else 'result.' + self.FORMAT
        with open(save_file, 'wb') as of:
            of.write(result_str)

        if has_error:
            result_str = str(result_str, 'utf-8')
            print("tts api  error:" + result_str)

        print("result saved as :" + save_file)
        playsound.playsound(save_file, True)
        print("read done")

    def play_voice(self, text):
        print(text)
        if len(text) <= 2048:
            self.play_one_voice(text)
        else:
            per_send_num = 2048
            per_word_min = 10
            end = per_send_num
            start = 0
            flag = True
            while flag:
                if end == len(text):
                    send_text = text[start:end]
                    flag = False
                else:
                    if re.search(r'\s', text[end]):
                        send_text = text[start:end]
                        start = end + 1
                    else:
                        find_text = str(text[end - 1 - per_word_min:end])
                        # print(find_text)
                        pattern = re.compile(r'\s', re.I)
                        result = pattern.search(find_text)
                        index = result.end(0) - 1
                        send_text = text[start:end - 1 - per_word_min + index]
                        start = end - per_word_min + index
                self.play_one_voice(send_text)
                # print(len(send_text), send_text)
                if len(text) - start > per_send_num:
                    end = start + per_send_num
                else:
                    end = len(text)

class DemoError(Exception):
    pass

if __name__=="__main__":
    tts_API = TTS_API()
    tts_API.play_voice("欢迎使用百度语音合成。")