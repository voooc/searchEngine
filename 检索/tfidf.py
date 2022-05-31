# -!- coding: utf-8 -!-
import jieba
import math
import pandas as pd
from collections import Counter
pd.set_option('display.max_columns', None)


class Tfidf(object):

    def __init__(self, texts):
        self.stop_words = []
        self.docs = []
        self.words = []
        self.tf = []
        self.df = {}
        self.tfidf = [[]]
        self.texts = texts

    def load_stop(self):
        stop = open('data/stopwords.txt', encoding='utf-8')
        self.stop_words = [line.strip() for line in stop]
        stop.close()

    def open_file(self):
        self.load_stop()
        for text in self.texts:
            temp = []
            text = text.strip()
            word = jieba.cut(text)
            "去除停用词"
            for j in word:
                if j not in self.stop_words:
                    temp.append(j)
            temp = [x.strip() for x in temp if x.strip() != '']
            self.docs.append(temp)
            self.words = temp + self.words
        self.words = list(set(self.words))

    def count_tf(self):
        for i, doc in enumerate(self.docs):
            tf_word = dict(Counter(doc))
            "归一化"
            for j in tf_word:
                tf_word[j] = tf_word[j] / len(doc)
                "顺便记录包含各个单词的文档数"
                if j in self.df:
                    self.df[j] += 1
                else:
                    self.df[j] = 1
            self.tf.append(tf_word)

    def count_df(self):
        for i in self.df:
            self.df[i] = math.log(len(self.docs) / (self.df[i] + 1))

    def count_tfidf(self):
        self.open_file()
        self.count_tf()
        self.count_df()
        x = 0
        "dataframe来形成每个文档每个单词的tfidf值"
        self.tfidf = [[0 for _ in range(len(self.words))] for _ in range(len(self.tf))]
        self.tfidf = pd.DataFrame(self.tfidf, columns=self.words, dtype=float)
        for i in self.tf:
            temp = {}
            for j in i:
                temp[j] = 1 * i[j] * self.df[j]
                self.tfidf.at[self.tfidf.index[x], j] = temp[j]
            x += 1
        return self.tfidf
