# -!- coding: utf-8 -!-
import os
from multiprocessing import Pool
import jieba
import json
import jieba.analyse

"导入停用词文件"
stop = open('../data/stopwords.txt', encoding='utf-8')
stop_words = [line.strip() for line in stop]
stop.close()
"创建文件"
if not os.path.exists('../data/spilt'):
    os.mkdir('../data/spilt')


def spilt_word(filename):
    """
    分词
    :param filename: 文件名
    :return: 
    """""
    fr = open('./html\\' + filename, 'r')
    a = fr.read()
    temp = []
    a = json.loads(a)
    article = ''
    for _ in a.values():
        article = _
    d = jieba.analyse.extract_tags(article, topK=20)
    "去除停用词"
    for j in d:
        if j not in stop_words:
            if j:
                temp.append(j)
    temp = [x.strip() for x in temp if x.strip() != '']
    fx = open('./spilt\\' + '分词' + filename, mode='w', encoding='utf-8')
    temp = filename.split(".")[0] + ' ' + ' '.join(temp)
    fx.write(temp)
    fx.close()


def main():
    pool = Pool(30)
    pool.map(spilt_word, [filename for filename in os.listdir('../data/html')])
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
