# -!- coding: utf-8 -!-
import json

import jieba
import numpy as np
import pandas as pd
from goose3 import Goose
from goose3.text import StopWordsChinese
from 检索.abstract import Abstract
from 检索.tfidf import Tfidf

g = Goose({'stopwords_class': StopWordsChinese})
"输入查询词"
# sentence = '乘客'


class Find:
    def __init__(self, sentence):
        self.sentence = sentence


    def spilt_key_word(self):
        """
        对查找词进行分词去除停用词
        :return:查找词的列表 
        """""
        key_words = []
        "去除停用词"
        "加载停用词"
        stop = open('data/stopwords.txt', encoding='utf-8')
        stop_words = [line.strip() for line in stop]
        stop.close()
        for j in jieba.cut(self.sentence):
            if j not in stop_words:
                key_words.append(j)
        key_words = [x.strip() for x in key_words if x.strip() != '']
        key_words = list(set(key_words))
        return key_words

    def intersection_doc(self):
        """
        文档求交
        :return:  文档列表，查找词
        """""
        data = pd.read_csv('data/测试倒序.csv')
        key_words = self.spilt_key_word()
        doc_list = []
        counts = {}
        # 文档求交
        for i in key_words:
            a = data[data['WorldId'].isin([i])]
            doc_hits = eval(a.iloc[0, 3])
            for key in doc_hits.keys():
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1
        for key_x, values_x in counts.items():
            if values_x == len(key_words):
                doc_list.append(key_x)
        return doc_list, key_words

    def count_tfidf(self):
        """
        计算tfidf
        :return: tfidf值，文档列表，查找词
        """""
        doc_list, key_words = self.intersection_doc()
        """texts记录所查事物和有关文档的内容"""
        texts = list()
        texts.append(self.sentence)
        temp = doc_list.copy()
        """遍历所有的文档"""
        for j in temp:
            a = open('data/html\\' + str(j) + '.txt', 'r').read()
            a = json.loads(a)
            article = ''
            for _ in a.values():
                article = _
            if article != '':
                texts.append(article)
            else:
                doc_list.remove(j)
        tf_idf = Tfidf(texts)
        tf_idf = tf_idf.count_tfidf()
        doc_list.insert(0, 0)
        tf_idf.index = doc_list
        return tf_idf, doc_list, key_words

    def get_cos_similar_multi(self, v1: list, v2: list):
        """
        计算一个文档和其余文档的相似度
        :param v1: 第一个文档
        :param v2: 其余文档
        :return: 结果
        """""
        num = np.dot([v1], np.array(v2).T)  # 向量点乘
        "v1行方向求模，v2列方向求模，结果点乘"
        deo = np.linalg.norm(v1) * np.linalg.norm(v2, axis=1)  # 求模长的乘积
        res = num / deo
        res[np.isneginf(res)] = 0
        return res

    def count_cos_sim(self, tf_idf, doc_list):
        """
        计算第一个文档和其余文档的相似度
        :param tf_idf: 
        :param doc_list: 所有的文档
        :return: 
        """""
        res = self.get_cos_similar_multi(np.array(tf_idf)[0], np.array(tf_idf)[1:])
        sim = []
        for i in res.tolist():
            sim = i
        "按相似度给文章排序"
        del doc_list[0]
        sort_zipped = sorted(zip(sim, doc_list), key=lambda z: (z[0]), reverse=True)
        sim1, doc_list = [list(z) for z in zip(*sort_zipped)]
        return doc_list

    def find(self):
        tfidf, docs, keywords = self.count_tfidf()
        docs = self.count_cos_sim(tfidf, docs)
        # urls = []
        # titles = []
        url = ''
        title = ''
        results = []
        for doc in docs:
            fr = open('data/html\\' + str(doc) + '.txt', 'r')
            b = fr.read()
            b = json.loads(b)
            for m in b.keys():
                m = m.split(' ')
                url = m[1]
                title = m[2]
                # urls.append(url)
                # titles.append(title)
                # print(url)
                # print(title)
            text = ''
            for _ in b.values():
                text = _
            target = ' '.join(keywords)
            abstract = Abstract("".join(text), target, size=40)
            result = abstract.get_abstract()
            results.append((url, title, result))
        return results
            # print("摘要结果为： {}".format(result))

# if __name__ == '__main__':
#     tfidf, docs, keywords = count_tfidf()
#     docs = count_cos_sim(tfidf, docs)
#     for doc in docs:
#         fr = open('./html\\' + str(doc) + '.txt', 'r')
#         b = fr.read()
#         b = json.loads(b)
#         for m in b.keys():
#             m = m.split(' ')
#             url = m[1]
#             title = m[2]
#             print(url)
#             print(title)
#         text = ''
#         for _ in b.values():
#             text = _
#         target = ' '.join(keywords)
#         abstract = Abstract("".join(text), target, size=40)
#         result = abstract.get_abstract()
#         print("摘要结果为： {}".format(result))
