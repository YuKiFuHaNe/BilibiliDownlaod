import jieba
from wordcloud import WordCloud
from lxml import etree
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from src.Utils import PIL_MASK_PATH,CACHE_PATH,FONTS_PATH
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import os


N = 20  # 柱状图绘制前N名
from src.Utils import logout
def read_xml_dm(path="/cache/data.xml"):
    '''
    读取xml文件返回jieba处理的词频数据
    Args:
        path:

    Returns:jieba

    '''
    all_dm = []
    tree = ET.parse(path)
    root = tree.getroot()
    for dm in root.findall('d'):
        all_dm.append(dm.text)
    words = jieba.lcut(str(all_dm))
    return words
def generate_word(words:list):
    # 中文分词
    text = ' '.join(words)
    # 生成对象
    img = Image.open(PIL_MASK_PATH)  # 打开遮罩图片
    mask = np.array(img)  # 将图片转换为数组

    stopwords = [] # 去掉不需要显示的词
    wc = WordCloud(font_path="msyh.ttc",
                   mask=mask,
                   width=2978,
                   height=843,
                   background_color='white',
                   max_words=900,
                   stopwords=stopwords).generate(text)

    # 显示词云
    plt.imshow(wc, interpolation='bilinear')  # 用plt显示图片
    plt.axis("off")  # 不显示坐标轴
    plt.show()  # 显示图片

    # 保存到文件
    wc.to_file(os.path.join(CACHE_PATH ,"wordcloud.png"))
    img1 = cv2.imread(os.path.join(CACHE_PATH ,"wordcloud.png"))
    img2 = cv2.imread(PIL_MASK_PATH)
    cv2.imwrite(os.path.join(CACHE_PATH,"wordcloud.png"),cv2.addWeighted(img1,0.7,img2,0.3,1))
def generate_histogram(words:list):
    global N
    counts = {}  # 通过键值对的形式存储词语及其出现的次数

    for word in words:
        if len(word) == 1:  # 单个词语不计算在内
            continue
        else:
            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

    items = list(counts.items())  # 将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
    if len(items) == 0:
        logout("无法绘制统计图，词汇长度大于1的词频为0",'error')
        exit()
    elif len(items) >= N:
        pass
    else:
        N = len(items)

    N_word = []
    N_count = []

    for i in range(N):
        word, count = items[i]
        N_word.append(word)
        N_count.append(count)
        # print("{0:<5}{1:>5}".format(word, count))

    fig, ax = plt.subplots()
    myfont = FontProperties(fname=os.path.join(FONTS_PATH,"simhei.ttf"), size=12)
    colors = ['#FA8072']
    # 绘制前十条数据（N=10）
    rects = ax.barh(N_word, N_count, align='center', color=colors)
    ax.set_yticklabels(N_word, fontproperties=myfont)
    ax.invert_yaxis()
    ax.set_title('高频词汇', fontproperties=myfont, fontsize=17)
    ax.set_xlabel(u"出现次数", fontproperties=myfont)
    plt.savefig(os.path.join(CACHE_PATH, "wordFrequency.png"))
    plt.show()


if __name__ == '__main__':
    words = read_xml_dm()
    generate_histogram(words)
    # generate_word(words)