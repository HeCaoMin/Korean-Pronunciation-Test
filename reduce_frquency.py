import os


def reduce_frequency(source_wav, dst_wav):
    '''
    降低直接从视频得到的音频的采样率，以适合paddlespeech进行识别
    :param source_wav:源语音文件，
    :param dst_wav:降低采样率为16khz且为单声道的目标音频地址
    :return:无返回
    '''
    os.system("sox {} -r 16000 -b 16 -c 1 {}".format(source_wav, dst_wav))

if __name__=="__main__":
    for i in os.listdir("单词/"):
        print(i)
        reduce_frequency("单词/"+i, "korea_words/"+i)