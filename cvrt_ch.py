from utils.ch_cvrt.langconv import *
def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

if __name__=="__main__":
    dir = "/media/weishu/Elements/vedio2article/1麥田圈_10/"
    with open(dir + "/text.txt", 'r') as f:
        lines = ''.join(f.readlines())
        simplified_sentence = Traditional2Simplified(lines)
    print(simplified_sentence)
    with open(dir + "text_simple.txt", "w") as f:
        f.write(simplified_sentence)