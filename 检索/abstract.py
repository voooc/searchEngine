# -!- coding: utf-8 -!-
from 检索.tfidf import Tfidf
import numpy as np


class Abstract(object):
    def __init__(self, text, key_word, size):
        self.text = text
        self.pos = []
        self.key_word = key_word
        self.size = size

    def bf(self, word):
        i = 0
        j = 0
        while i < len(self.text) and j < len(word):
            if self.text[i] == word[j]:
                i += 1
                j += 1
                if j == len(word):
                    self.pos.append(i - j)
                    j = 0
            else:
                i = i - j + 1
                j = 0

    def spilt_text(self):
        self.key_word = self.key_word.split(' ')
        for word in self.key_word:
            self.bf(word)
        sentences = []
        for i in self.pos:
            sentences.append(self.text[i:i + self.size].replace('\n', ''))
        return sentences

    def get_abstract(self):
        sentences = self.spilt_text()
        tf_idf = Tfidf(sentences)
        tf_idf = tf_idf.count_tfidf()
        scores = []
        for i in range(len(sentences)):
            score = 0
            for word in self.key_word:
                score += tf_idf.at[tf_idf.index[i], word]
            scores.append(score)
        sort_zipped = sorted(zip(scores, sentences), key=lambda z: (z[0]), reverse=True)
        scores, sentences = [list(z) for z in zip(*sort_zipped)]
        index = np.argmax(np.array(scores))
        res = str(sentences[index])
        # for i in self.key_word:
        #     res = res.replace(i, "\033[31m" + i + "\033[0m")
        # print(res)
        return res